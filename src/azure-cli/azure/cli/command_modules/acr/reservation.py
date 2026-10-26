# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

import json
import math
import re
import time
from urllib.parse import quote, urljoin

from knack.log import get_logger
from knack.util import CLIError
from requests.exceptions import RequestException

from azure.cli.core.azclierror import (
    AzureConnectionError, AzureResponseError, BadRequestError, ForbiddenError, HTTPError,
    InvalidArgumentValueError, RequiredArgumentMissingError, ResourceNotFoundError, UnauthorizedError,
)
from azure.cli.core.commands.client_factory import get_subscription_id
from azure.cli.core.util import is_same_origin, send_raw_request, todict

logger = get_logger(__name__)

API_VERSION = '2026-09-01-preview'
DEFAULT_TIMEOUT = 1800
POLL_INTERVAL = 15
REQUEST_RATE_TIERS = {f'R{n}': n for n in (1, 2, 4, 8, 16, 32, 64)}
EGRESS_TIERS = {f'E{n}': 16 * n for n in (1, 2, 4, 8, 16, 32)}
INGRESS_TIERS = {f'I{n}': 0.5 * n for n in (1, 2, 4, 8, 16)}
_DIMENSIONS = (
    ('requestRateTier', 'requestRateRus', 'reservedRequestRate', REQUEST_RATE_TIERS),
    ('egressTier', 'egressGbps', 'reservedEgressGbps', EGRESS_TIERS),
    ('ingressTier', 'ingressGbps', 'reservedIngressGbps', INGRESS_TIERS),
)
_ASSOCIATION_STATES = {'Migrating': 'Updating', 'Removing': 'Updating', 'Active': 'Succeeded'}
_PUBLIC_PROPERTIES = (
    'requestRateTier', 'egressTier', 'ingressTier',
    'provisioningState', 'statusReason', 'earliestDeletableAt', 'createdAt', 'lastModifiedAt',
)


def _public_message(message):
    # Infrastructure diagnostics remain available to operators, not in customer-facing output.
    if re.search(r'\bstamp\w*\b|\bvmss\b|\bcosmos\b|\bledger\b', message, re.IGNORECASE):
        return 'The requested capacity operation could not be completed. Check capacity availability and retry.'
    return message


def _json_object(response):
    try:
        result = response.json()
    except ValueError as ex:
        raise AzureResponseError('The capacity reservation API returned invalid JSON.') from ex
    if not isinstance(result, dict):
        raise AzureResponseError('The capacity reservation API did not return a JSON object.')
    return result


def _request(cmd, method, path, body=None):
    endpoint = cmd.cli_ctx.cloud.endpoints.resource_manager.rstrip('/') + '/'
    url = urljoin(endpoint, path)
    if not is_same_origin(url, endpoint):
        raise AzureResponseError('The capacity reservation API returned a link outside the selected ARM endpoint.')
    try:
        response = send_raw_request(cmd.cli_ctx, method, url,
                                    body=json.dumps(body) if body is not None else None)
    except HTTPError as ex:
        response = ex.response
        try:
            detail = response.json()
        except ValueError:
            detail = response.text
        if isinstance(detail, dict):
            detail = detail.get('error', detail)
            detail = detail.get('message') if isinstance(detail, dict) else detail
        message = _public_message(detail) if isinstance(detail, str) else 'The service rejected the request.'
        message = f'Capacity reservation request failed (HTTP {response.status_code}): {message}'
        error_type = {
            400: BadRequestError, 401: UnauthorizedError, 403: ForbiddenError, 404: ResourceNotFoundError,
        }.get(response.status_code, AzureResponseError)
        raise error_type(message) from None
    except RequestException as ex:
        raise AzureConnectionError(
            'Unable to reach the capacity reservation API. Check connectivity and retry.') from ex
    if response.status_code not in (200, 201, 202, 204):
        raise AzureResponseError(f'Unexpected capacity reservation HTTP response: {response.status_code}.')
    return response


def _collection_path(cmd, resource_group_name=None):
    path = '/subscriptions/' + quote(get_subscription_id(cmd.cli_ctx), safe='')
    if resource_group_name is not None:
        path += '/resourceGroups/' + quote(resource_group_name, safe='')
    return path + '/providers/Microsoft.ContainerRegistry/capacityReservations'


def _resource_path(cmd, reservation_name, resource_group_name):
    if not re.fullmatch(r'[a-zA-Z0-9][a-zA-Z0-9-]{0,62}', reservation_name):
        raise InvalidArgumentValueError(
            'Reservation names must contain 1-63 letters, digits or hyphens and start with a letter or digit.')
    return _collection_path(cmd, resource_group_name) + '/' + reservation_name


def _api_url(path):
    return path + '?api-version=' + API_VERSION


def _get(cmd, path):
    return _json_object(_request(cmd, 'GET', _api_url(path)))


def _properties(resource):
    properties = resource.get('properties')
    if not isinstance(properties, dict):
        raise AzureResponseError('The capacity reservation response is missing its properties.')
    return properties


def _public_reservation(resource):
    properties = _properties(resource)
    if any(not isinstance(resource.get(key), str) or not resource[key] for key in ('id', 'name', 'location')):
        raise AzureResponseError('The capacity reservation response is missing its identity or location.')
    result = {key: resource[key] for key in ('id', 'name', 'type', 'location', 'tags') if key in resource}
    result['properties'] = {key: properties[key] for key in _PUBLIC_PROPERTIES if key in properties}
    reason = result['properties'].get('statusReason')
    if isinstance(reason, str):
        result['properties']['statusReason'] = _public_message(reason)
    return result


def _list(cmd, path, method='GET'):
    items = []
    url = _api_url(path)
    visited = set()
    while url:
        if url in visited:
            raise AzureResponseError('The capacity reservation API returned a repeated pagination link.')
        visited.add(url)
        result = _json_object(_request(cmd, method, url))
        page = result.get('value')
        if not isinstance(page, list) or any(not isinstance(item, dict) for item in page):
            raise AzureResponseError('The capacity reservation API returned an invalid list.')
        items.extend(page)
        url = result.get('nextLink')
        if url is not None and not isinstance(url, str):
            raise AzureResponseError('The capacity reservation API returned an invalid pagination link.')
        method = 'GET'
    return items


def _validate_timeout(timeout):
    if timeout <= 0:
        raise InvalidArgumentValueError('--timeout must be greater than zero.')


def _pause(deadline, response=None):
    remaining = deadline - time.monotonic()
    if remaining <= 0:
        raise AzureResponseError(
            'Timed out waiting for the capacity reservation operation. Completion could not be confirmed; '
            'the operation may still be running. Check its status before retrying.')
    delay = POLL_INTERVAL
    if response is not None and response.headers.get('Retry-After') is not None:
        try:
            delay = max(1, int(response.headers['Retry-After']))
        except ValueError:
            logger.warning('Invalid Retry-After header; polling again after %s seconds.', POLL_INTERVAL)
    time.sleep(min(delay, remaining))
    if time.monotonic() >= deadline:
        raise AzureResponseError(
            'Timed out waiting for the capacity reservation operation. It may still be running; check its status.')


def _check_failure(state, detail):
    if state in ('Failed', 'Canceled', 'Cancelled'):
        message = _public_message(detail) if isinstance(detail, str) else 'Check the reservation and retry.'
        raise AzureResponseError(f'Capacity reservation operation {state.lower()}. {message}')


def _finish(cmd, path, response, no_wait, timeout):
    resource = _json_object(response) if response.content else None
    if no_wait:
        return _public_reservation(resource) if resource is not None else None
    monitor = response.headers.get('Azure-AsyncOperation')
    deadline = time.monotonic() + timeout
    while True:
        if resource is not None:
            properties = _properties(resource)
            state = properties.get('provisioningState')
            _check_failure(state, properties.get('statusReason'))
            if state == 'Succeeded' and response.status_code != 202:
                # TODO: POC resize rollback also reports Succeeded. Verify requested floors once the contract improves.
                return _public_reservation(resource)
        _pause(deadline, response)
        if monitor:
            response = _request(cmd, 'GET', monitor)
            operation = _json_object(response)
            state = operation.get('status')
            error = operation.get('error') or {}
            _check_failure(state, error.get('message') if isinstance(error, dict) else None)
            if state == 'Succeeded':
                resource = _get(cmd, path)
                properties = _properties(resource)
                _check_failure(properties.get('provisioningState'), properties.get('statusReason'))
                if properties.get('provisioningState') == 'Succeeded':
                    return _public_reservation(resource)
            else:
                resource = None
        else:
            response = _request(cmd, 'GET', _api_url(path))
            resource = _json_object(response)


def _tier_properties(request_rate_tier, egress_tier, ingress_tier, current=None):
    properties = {}
    for (label, amount, reserved, tiers), selected in zip(
            _DIMENSIONS, (request_rate_tier, egress_tier, ingress_tier)):
        if selected is None:
            if current is None:
                properties[amount] = 0
                continue
            value = current.get(reserved)
            if isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(value) or value < 0:
                raise AzureResponseError(f'The capacity reservation response has an invalid {reserved} value.')
            properties[amount] = value
            if current.get(label) is not None:
                properties[label] = current[label]
            continue
        if selected == 'None':
            if current is None:
                raise InvalidArgumentValueError('None is only supported when updating a reservation.')
            properties[amount] = 0
        elif selected in tiers:
            properties[amount] = tiers[selected]
        else:
            raise InvalidArgumentValueError(f'Invalid tier {selected!r}. Choose one of: {", ".join(tiers)}.')
        properties[label] = selected
    if not any(properties[amount] > 0 for _, amount, _, _ in _DIMENSIONS):
        raise InvalidArgumentValueError('At least one reserved dimension must have a specified tier.')
    return properties


def acr_reservation_create(cmd, reservation_name, resource_group_name, stamp_id, location,
                           request_rate_tier=None, egress_tier=None, ingress_tier=None, tags=None,
                           no_wait=False, timeout=DEFAULT_TIMEOUT):
    _validate_timeout(timeout)
    if not stamp_id.strip():
        raise InvalidArgumentValueError('--stamp-id must not be empty.')
    properties = _tier_properties(request_rate_tier, egress_tier, ingress_tier)
    properties['stampId'] = stamp_id
    body = {'location': location, 'properties': properties}
    if tags is not None:
        body['tags'] = tags
    path = _resource_path(cmd, reservation_name, resource_group_name)
    return _finish(cmd, path, _request(cmd, 'PUT', _api_url(path), body), no_wait, timeout)


def acr_reservation_show(cmd, reservation_name, resource_group_name):
    return _public_reservation(_get(cmd, _resource_path(cmd, reservation_name, resource_group_name)))


def acr_reservation_wait_get(cmd, reservation_name, resource_group_name):
    try:
        return acr_reservation_show(cmd, reservation_name, resource_group_name)
    except ResourceNotFoundError as ex:
        # The generic wait handler recognises SDK HTTP 404 errors for --deleted.
        from azure.core.exceptions import ResourceNotFoundError as HttpResourceNotFoundError
        error = HttpResourceNotFoundError(message=str(ex))
        error.status_code = 404
        raise error from ex


def acr_reservation_list(cmd, resource_group_name=None):
    return [_public_reservation(item) for item in _list(cmd, _collection_path(cmd, resource_group_name))]


def acr_reservation_update(cmd, reservation_name, resource_group_name,
                           request_rate_tier=None, egress_tier=None, ingress_tier=None, tags=None,
                           no_wait=False, timeout=DEFAULT_TIMEOUT):
    _validate_timeout(timeout)
    if all(value is None for value in (request_rate_tier, egress_tier, ingress_tier, tags)):
        raise RequiredArgumentMissingError('Specify a tier or --tags to update.')
    path = _resource_path(cmd, reservation_name, resource_group_name)
    current = _properties(_get(cmd, path))
    # TODO: Remove read/merge when the POC PATCH preserves omitted dimensions instead of resetting them to zero.
    body = {'properties': _tier_properties(request_rate_tier, egress_tier, ingress_tier, current)}
    if tags is not None:
        body['tags'] = tags
    return _finish(cmd, path, _request(cmd, 'PATCH', _api_url(path), body), no_wait, timeout)


def acr_reservation_delete(cmd, reservation_name, resource_group_name, no_wait=False, timeout=DEFAULT_TIMEOUT):
    _validate_timeout(timeout)
    path = _resource_path(cmd, reservation_name, resource_group_name)
    response = _request(cmd, 'DELETE', _api_url(path))
    if response.status_code == 204 or no_wait:
        return
    deadline = time.monotonic() + timeout
    while True:
        _pause(deadline, response)
        try:
            response = _request(cmd, 'GET', _api_url(path))
        except ResourceNotFoundError:
            return
        properties = _properties(_json_object(response))
        _check_failure(properties.get('provisioningState'), properties.get('statusReason'))


def _associations(cmd, path):
    associations = _list(cmd, path + '/listRegistries', method='POST')
    for item in associations:
        if any(not isinstance(item.get(key), str) or not item[key] for key in ('registryId', 'associationState')):
            raise AzureResponseError('The capacity reservation API returned an invalid registry association.')
    return associations


def _public_association(association):
    result = {key: association[key] for key in ('registryId', 'associationState', 'associatedAt') if key in association}
    state = result.get('associationState')
    result['associationState'] = _ASSOCIATION_STATES.get(state, state)
    return result


def acr_reservation_list_registries(cmd, reservation_name, resource_group_name):
    path = _resource_path(cmd, reservation_name, resource_group_name)
    return [_public_association(item) for item in _associations(cmd, path)]


def _change_association(cmd, reservation_name, resource_group_name, registry_name, remove, no_wait, timeout):
    _validate_timeout(timeout)
    path = _resource_path(cmd, reservation_name, resource_group_name)
    action = 'disassociate' if remove else 'associate'
    _request(cmd, 'POST', _api_url(path + '/' + action), {'registryName': registry_name})
    if no_wait:
        return None
    deadline = time.monotonic() + timeout
    while True:
        matches = [item for item in _associations(cmd, path)
                   if str(item.get('registryId', '')).lower() == registry_name.lower()]
        if len(matches) > 1:
            raise AzureResponseError('The API returned multiple associations for the same registry.')
        if remove and not matches:
            return None
        if matches:
            state = matches[0].get('associationState')
            _check_failure(state, None)
            if not remove and state == 'Active':
                return _public_association(matches[0])
        # TODO: Surface migration failures when the POC exposes a failure state/reason instead of pending forever.
        _pause(deadline)


def acr_reservation_associate(cmd, reservation_name, resource_group_name, registry_name,
                              no_wait=False, timeout=DEFAULT_TIMEOUT):
    return _change_association(cmd, reservation_name, resource_group_name, registry_name, False, no_wait, timeout)


def acr_reservation_disassociate(cmd, reservation_name, resource_group_name, registry_name,
                                 no_wait=False, timeout=DEFAULT_TIMEOUT):
    return _change_association(cmd, reservation_name, resource_group_name, registry_name, True, no_wait, timeout)


def prepare_registry_reservation(cmd, reservation_name, resource_group_name, location, timeout):
    _validate_timeout(timeout)
    reservation = acr_reservation_show(cmd, reservation_name, resource_group_name)
    if _properties(reservation).get('provisioningState') != 'Succeeded':
        raise InvalidArgumentValueError('The capacity reservation must be provisioned before creating the registry.')
    if str(reservation.get('location', '')).replace(' ', '').lower() != str(location).replace(' ', '').lower():
        raise InvalidArgumentValueError('The registry and capacity reservation must be in the same region.')
    return reservation


def associate_created_registry(cmd, registry, reservation, resource_group_name, registry_name, timeout):
    name = reservation['name']
    try:
        association = acr_reservation_associate(cmd, name, resource_group_name, registry_name, timeout=timeout)
    except CLIError as ex:
        raise AzureResponseError(
            f"Registry '{registry_name}' was created, but reservation association did not complete. "
            f"The registry has not been deleted. {ex}",
            recommendation=f'Check the association and retry with: az acr reservation associate --name "{name}" '
            f'--resource-group "{resource_group_name}" --registry-name "{registry_name}"') from ex
    result = todict(registry)
    result['reservation'] = {
        'id': reservation['id'], 'name': name, 'associationState': association['associationState'],
    }
    return result


def enrich_registry_reservation(cmd, registry, resource_group_name, registry_name):
    # The POC API is deployed in Dogfood only; preserve existing show behaviour in other clouds.
    if cmd.cli_ctx.cloud.name.lower() not in ('dogfood', 'azuredogfood'):
        return registry
    try:
        matches = []
        for reservation in acr_reservation_list(cmd, resource_group_name):
            for association in acr_reservation_list_registries(cmd, reservation['name'], resource_group_name):
                if str(association.get('registryId', '')).lower() == registry_name.lower():
                    matches.append({
                        'id': reservation['id'], 'name': reservation['name'],
                        'associationState': association['associationState'],
                    })
        if len(matches) > 1:
            raise AzureResponseError('The registry appears in more than one capacity reservation.')
    except CLIError as ex:
        logger.warning(
            'Could not determine the registry capacity reservation; the reservation field is omitted. %s', ex)
        return registry
    result = todict(registry)
    result['reservation'] = matches[0] if matches else None
    return result
