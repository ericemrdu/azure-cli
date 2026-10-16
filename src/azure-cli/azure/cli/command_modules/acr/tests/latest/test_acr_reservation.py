# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

import copy
import io
import json
import unittest
from types import SimpleNamespace
from unittest import mock

from requests import Response
from requests.exceptions import ConnectionError as RequestsConnectionError

from azure.cli.core.azclierror import (
    AzureConnectionError, AzureResponseError, HTTPError, InvalidArgumentValueError,
    RequiredArgumentMissingError, ResourceNotFoundError,
)
from azure.cli.command_modules.acr import reservation as api
from azure.cli.command_modules.acr import custom
from azure.cli.command_modules.acr._format import registry_output_format, reservation_output_format


SUBSCRIPTION = '00000000-0000-0000-0000-000000000001'
RESOURCE_GROUP = 'test-group'
RESERVATION = 'test-reservation'
REGISTRY = 'testregistry'
ENDPOINT = 'https://api-dogfood.example.test'
BASE_PATH = (f'/subscriptions/{SUBSCRIPTION}/resourceGroups/{RESOURCE_GROUP}/'
             f'providers/Microsoft.ContainerRegistry/capacityReservations')
RESOURCE_PATH = BASE_PATH + '/' + RESERVATION
RESOURCE_URL = ENDPOINT + RESOURCE_PATH + '?api-version=' + api.API_VERSION
MONITOR_URL = ENDPOINT + RESOURCE_PATH + '/operationStatuses/default?api-version=' + api.API_VERSION


def response(body=None, status=200, headers=None):
    result = Response()
    result.status_code = status
    result.reason = 'Test response'
    result._content = json.dumps(body).encode() if body is not None else b''
    result.headers.update(headers or {})
    return result


def resource(state='Succeeded'):
    return {
        'id': RESOURCE_PATH, 'name': RESERVATION,
        'type': 'Microsoft.ContainerRegistry/capacityReservations', 'location': 'australiaeast',
        'properties': {
            'stampId': 'internal-stamp', 'tierCatalogVersion': 'internal-catalog',
            'registryPool': {'vmssResourceId': '/internal/vmss'},
            'requestRateTier': 'R4', 'egressTier': 'E4', 'ingressTier': 'I2',
            'reservedRequestRate': 4, 'reservedEgressGbps': 64, 'reservedIngressGbps': 1,
            'provisioningState': state, 'earliestDeletableAt': '2026-10-01T00:05:00Z',
        },
    }


def association(state='Active', name=REGISTRY):
    return {'registryId': name, 'associationState': state, 'associatedAt': '2026-10-01T00:00:00Z'}


class ReservationTests(unittest.TestCase):

    def setUp(self):
        self.cmd = SimpleNamespace(cli_ctx=SimpleNamespace(cloud=SimpleNamespace(
            name='Dogfood', endpoints=SimpleNamespace(resource_manager=ENDPOINT))))
        self.http = self._patch('send_raw_request')
        self._patch('get_subscription_id', return_value=SUBSCRIPTION)
        self.sleep = self._patch('time.sleep')

    def _patch(self, name, **kwargs):
        patcher = mock.patch('azure.cli.command_modules.acr.reservation.' + name, **kwargs)
        self.addCleanup(patcher.stop)
        return patcher.start()

    def test_acr_reservation_create_all_tier_mappings(self):
        for argument, field, mapping in (
                ('request_rate_tier', 'requestRateRus', api.REQUEST_RATE_TIERS),
                ('egress_tier', 'egressGbps', api.EGRESS_TIERS),
                ('ingress_tier', 'ingressGbps', api.INGRESS_TIERS)):
            for tier, capacity in mapping.items():
                with self.subTest(tier=tier):
                    self.http.return_value = response(resource(), 201)
                    result = api.acr_reservation_create(
                        self.cmd, RESERVATION, RESOURCE_GROUP, 'internal-stamp', 'australiaeast',
                        **{argument: tier})
                    call = self.http.call_args
                    self.assertEqual(call.args, (self.cmd.cli_ctx, 'PUT', RESOURCE_URL))
                    body = json.loads(call.kwargs['body'])
                    self.assertEqual(body['properties'][field], capacity)
                    self.assertEqual(body['properties']['stampId'], 'internal-stamp')
                    self.assertEqual(sum(body['properties'][key] > 0 for key in
                                         ('requestRateRus', 'egressGbps', 'ingressGbps')), 1)
                    self.assertNotIn('internal', json.dumps(result))
        self.sleep.assert_not_called()

    def test_acr_reservation_create_requires_positive_tier(self):
        for arguments in ({}, {'request_rate_tier': 'None'}, {'egress_tier': '64'},
                          {'request_rate_tier': 'R3'}):
            with self.subTest(arguments=arguments):
                with self.assertRaises(InvalidArgumentValueError):
                    api.acr_reservation_create(
                        self.cmd, RESERVATION, RESOURCE_GROUP, 'stamp', 'australiaeast', **arguments)
        self.http.assert_not_called()

    def test_acr_reservation_create_validates_name_stamp_and_timeout(self):
        for name, stamp, timeout in (('a/b', 'stamp', 30), ('ab', 'stamp', 30),
                                     (RESERVATION, ' ', 30), (RESERVATION, 'stamp', 0)):
            with self.subTest(name=name, stamp=stamp, timeout=timeout):
                with self.assertRaises(InvalidArgumentValueError):
                    api.acr_reservation_create(
                        self.cmd, name, RESOURCE_GROUP, stamp, 'australiaeast',
                        request_rate_tier='R1', timeout=timeout)
        self.http.assert_not_called()

    def test_acr_reservation_update_preserves_omitted_amounts(self):
        self.http.side_effect = [response(resource()), response(resource())]
        api.acr_reservation_update(self.cmd, RESERVATION, RESOURCE_GROUP, egress_tier='E8')
        self.assertEqual(self.http.call_args.args[1], 'PATCH')
        body = json.loads(self.http.call_args.kwargs['body'])
        self.assertEqual(body['properties'], {
            'requestRateRus': 4, 'requestRateTier': 'R4',
            'egressGbps': 128, 'egressTier': 'E8',
            'ingressGbps': 1, 'ingressTier': 'I2',
        })

    def test_acr_reservation_update_none_removes_dimension_and_label(self):
        self.http.side_effect = [response(resource()), response(resource())]
        api.acr_reservation_update(self.cmd, RESERVATION, RESOURCE_GROUP, ingress_tier='None')
        properties = json.loads(self.http.call_args.kwargs['body'])['properties']
        self.assertEqual(properties['ingressGbps'], 0)
        self.assertEqual(properties['ingressTier'], 'None')
        self.assertEqual(properties['egressGbps'], 64)

    def test_acr_reservation_update_rejects_all_zero(self):
        self.http.return_value = response(resource())
        with self.assertRaises(InvalidArgumentValueError):
            api.acr_reservation_update(self.cmd, RESERVATION, RESOURCE_GROUP,
                                       request_rate_tier='None', egress_tier='None', ingress_tier='None')
        self.assertEqual(self.http.call_count, 1)

    def test_acr_reservation_update_requires_change(self):
        with self.assertRaises(RequiredArgumentMissingError):
            api.acr_reservation_update(self.cmd, RESERVATION, RESOURCE_GROUP)
        self.http.assert_not_called()

    def test_acr_reservation_update_rejects_missing_current_amounts(self):
        invalid = resource()
        del invalid['properties']['reservedIngressGbps']
        self.http.return_value = response(invalid)
        with self.assertRaises(AzureResponseError):
            api.acr_reservation_update(self.cmd, RESERVATION, RESOURCE_GROUP, egress_tier='E8')
        self.assertEqual(self.http.call_count, 1)

    def test_acr_reservation_update_tags_only_preserves_all_dimensions(self):
        self.http.side_effect = [response(resource()), response(resource())]
        api.acr_reservation_update(self.cmd, RESERVATION, RESOURCE_GROUP, tags={})
        body = json.loads(self.http.call_args.kwargs['body'])
        self.assertEqual(body['tags'], {})
        self.assertEqual(body['properties']['requestRateRus'], 4)
        self.assertEqual(body['properties']['egressGbps'], 64)
        self.assertEqual(body['properties']['ingressGbps'], 1)

    def test_acr_reservation_create_polls_202_and_honours_retry_after(self):
        self.http.side_effect = [
            response(resource('Provisioning'), 202, {'Azure-AsyncOperation': MONITOR_URL, 'Retry-After': '2'}),
            response({'status': 'InProgress'}, headers={'Retry-After': '3'}),
            response({'status': 'Succeeded'}),
            response(resource()),
        ]
        result = api.acr_reservation_create(
            self.cmd, RESERVATION, RESOURCE_GROUP, 'stamp', 'australiaeast', request_rate_tier='R4')
        self.assertEqual(result['properties']['provisioningState'], 'Succeeded')
        self.assertEqual([call.args[2] for call in self.http.call_args_list],
                         [RESOURCE_URL, MONITOR_URL, MONITOR_URL, RESOURCE_URL])
        self.assertEqual(self.sleep.call_args_list, [mock.call(2), mock.call(3)])

    def test_acr_reservation_no_wait_returns_without_polling(self):
        self.http.return_value = response(resource('Provisioning'), 202,
                                          {'Azure-AsyncOperation': MONITOR_URL})
        result = api.acr_reservation_create(
            self.cmd, RESERVATION, RESOURCE_GROUP, 'stamp', 'australiaeast',
            egress_tier='E1', no_wait=True)
        self.assertEqual(result['properties']['provisioningState'], 'Provisioning')
        self.assertNotIn('stampId', result['properties'])
        self.assertEqual(self.http.call_count, 1)
        self.sleep.assert_not_called()

    def test_acr_reservation_polls_resource_without_monitor(self):
        self.http.side_effect = [response(resource('Provisioning'), 202), response(resource())]
        api.acr_reservation_create(
            self.cmd, RESERVATION, RESOURCE_GROUP, 'stamp', 'australiaeast', ingress_tier='I1')
        self.assertEqual(self.http.call_count, 2)

    def test_acr_reservation_failed_lro_reports_error(self):
        self.http.side_effect = [
            response(resource('Provisioning'), 202, {'Azure-AsyncOperation': MONITOR_URL}),
            response({'status': 'Failed', 'error': {'message': 'Requested capacity is unavailable.'}}),
        ]
        with self.assertRaisesRegex(AzureResponseError, 'Requested capacity is unavailable'):
            api.acr_reservation_create(
                self.cmd, RESERVATION, RESOURCE_GROUP, 'stamp', 'australiaeast', egress_tier='E4')

    def test_acr_reservation_update_trusts_succeeded_after_rollback(self):
        rolled_back = resource()
        rolled_back['properties']['statusReason'] = 'Resize scale-out failed; reverted to the previous size.'
        self.http.side_effect = [
            response(resource()), response(resource('Updating'), 202, {'Azure-AsyncOperation': MONITOR_URL}),
            response({'status': 'Succeeded'}), response(rolled_back),
        ]
        result = api.acr_reservation_update(self.cmd, RESERVATION, RESOURCE_GROUP, egress_tier='E8')
        self.assertEqual(result['properties']['provisioningState'], 'Succeeded')
        self.assertEqual(result['properties']['reservedEgressGbps'], 64)

    def test_acr_reservation_poll_timeout(self):
        self._patch('time.monotonic', side_effect=[0, 0, 1])
        self.http.return_value = response(resource('Provisioning'), 202)
        with self.assertRaisesRegex(AzureResponseError, 'Timed out'):
            api.acr_reservation_create(
                self.cmd, RESERVATION, RESOURCE_GROUP, 'stamp', 'australiaeast',
                request_rate_tier='R1', timeout=1)
        self.assertEqual(self.http.call_count, 1)

    def test_acr_reservation_rejects_external_monitor(self):
        self.http.return_value = response(
            resource('Provisioning'), 202, {'Azure-AsyncOperation': 'https://untrusted.example.test/status'})
        with self.assertRaisesRegex(AzureResponseError, 'outside the selected ARM endpoint'):
            api.acr_reservation_create(
                self.cmd, RESERVATION, RESOURCE_GROUP, 'stamp', 'australiaeast', request_rate_tier='R1')
        self.assertEqual(self.http.call_count, 1)

    def test_acr_reservation_list_scopes_and_pagination(self):
        next_link = ENDPOINT + BASE_PATH + '?api-version=' + api.API_VERSION + '&continuation=next'
        self.http.side_effect = [
            response({'value': [resource()], 'nextLink': next_link}),
            response({'value': [resource()]}),
        ]
        result = api.acr_reservation_list(self.cmd, RESOURCE_GROUP)
        self.assertEqual(len(result), 2)
        self.assertEqual(self.http.call_args_list[0].args[2], ENDPOINT + api._api_url(BASE_PATH))
        self.assertNotIn('stampId', json.dumps(result))
        self.http.side_effect = None
        self.http.return_value = response({'value': []})
        api.acr_reservation_list(self.cmd)
        self.assertNotIn('/resourceGroups/', self.http.call_args.args[2])

    def test_acr_reservation_rejects_external_next_link(self):
        self.http.return_value = response({'value': [], 'nextLink': 'https://untrusted.example.test/list'})
        with self.assertRaises(AzureResponseError):
            api.acr_reservation_list(self.cmd)
        self.assertEqual(self.http.call_count, 1)

    def test_acr_reservation_rejects_repeated_page(self):
        self.http.return_value = response({'value': [], 'nextLink': api._api_url(BASE_PATH)})
        with self.assertRaisesRegex(AzureResponseError, 'repeated'):
            api.acr_reservation_list(self.cmd, RESOURCE_GROUP)

    def test_acr_reservation_list_rejects_malformed_response(self):
        self.http.return_value = response({'value': {}})
        with self.assertRaisesRegex(AzureResponseError, 'invalid list'):
            api.acr_reservation_list(self.cmd)

    def test_acr_reservation_show_filters_internals(self):
        item = resource()
        item['properties']['statusReason'] = "Stamp 'internal-stamp' failed to scale its VMSS."
        self.http.return_value = response(item)
        result = api.acr_reservation_show(self.cmd, RESERVATION, RESOURCE_GROUP)
        self.assertNotIn('internal', json.dumps(result))
        self.assertIn('capacity operation', result['properties']['statusReason'])

    def test_acr_reservation_delete_returns_no_output(self):
        self.http.return_value = response(status=204)
        self.assertIsNone(api.acr_reservation_delete(self.cmd, RESERVATION, RESOURCE_GROUP))
        self.assertEqual(self.http.call_args.args[1:3], ('DELETE', RESOURCE_URL))

    def test_acr_reservation_delete_polls_202_until_not_found(self):
        self.http.side_effect = [
            response(status=202, headers={'Retry-After': '1'}),
            response(resource('Deleting')),
            HTTPError('Not found', response('Reservation not found.', 404)),
        ]
        self.assertIsNone(api.acr_reservation_delete(self.cmd, RESERVATION, RESOURCE_GROUP))
        self.assertEqual(self.http.call_count, 3)
        self.assertEqual(self.sleep.call_args_list, [mock.call(1), mock.call(api.POLL_INTERVAL)])

    def test_acr_reservation_delete_no_wait(self):
        self.http.return_value = response(status=202)
        self.assertIsNone(api.acr_reservation_delete(self.cmd, RESERVATION, RESOURCE_GROUP, no_wait=True))
        self.assertEqual(self.http.call_count, 1)
        self.sleep.assert_not_called()

    def test_acr_reservation_http_errors_include_plain_text_poc_errors(self):
        for status, detail in ((404, {'error': {'message': 'Reservation not found.'}}),
                               (409, 'Minimum commitment has not elapsed.')):
            with self.subTest(status=status):
                self.http.side_effect = HTTPError('HTTP failure', response(detail, status))
                expected = ResourceNotFoundError if status == 404 else AzureResponseError
                with self.assertRaisesRegex(expected, str(status)):
                    api.acr_reservation_show(self.cmd, RESERVATION, RESOURCE_GROUP)

    def test_acr_reservation_connection_error_is_actionable(self):
        self.http.side_effect = RequestsConnectionError('internal detail')
        with self.assertRaisesRegex(AzureConnectionError, 'Check connectivity'):
            api.acr_reservation_show(self.cmd, RESERVATION, RESOURCE_GROUP)

    def test_acr_reservation_associate_waits_for_active(self):
        self.http.side_effect = [
            response(status=204), response({'value': [association('Migrating')]}),
            response({'value': [association()]}),
        ]
        result = api.acr_reservation_associate(self.cmd, RESERVATION, RESOURCE_GROUP, REGISTRY)
        self.assertEqual(result['associationState'], 'Succeeded')
        self.assertEqual(json.loads(self.http.call_args_list[0].kwargs['body']), {'registryName': REGISTRY})
        self.assertEqual(self.http.call_args_list[1].args[1], 'POST')
        self.sleep.assert_called_once_with(api.POLL_INTERVAL)

    def test_acr_reservation_disassociate_waits_for_target_only(self):
        self.http.side_effect = [
            response(status=204), response({'value': [association('Removing'), association(name='another')]}),
            response({'value': [association(name='another')]}),
        ]
        self.assertIsNone(api.acr_reservation_disassociate(self.cmd, RESERVATION, RESOURCE_GROUP, REGISTRY))
        self.sleep.assert_called_once()

    def test_acr_reservation_association_no_wait(self):
        for handler in (api.acr_reservation_associate, api.acr_reservation_disassociate):
            with self.subTest(handler=handler.__name__):
                self.http.reset_mock()
                self.http.return_value = response(status=204)
                self.assertIsNone(handler(self.cmd, RESERVATION, RESOURCE_GROUP, REGISTRY, no_wait=True))
                self.assertEqual(self.http.call_count, 1)
        self.sleep.assert_not_called()

    def test_acr_reservation_association_timeout_does_not_report_success(self):
        self._patch('time.monotonic', side_effect=[0, 0, 1])
        self.http.side_effect = [response(status=204), response({'value': [association('Migrating')]})]
        with self.assertRaisesRegex(AzureResponseError, 'may still be running'):
            api.acr_reservation_associate(self.cmd, RESERVATION, RESOURCE_GROUP, REGISTRY, timeout=1)

    def test_acr_reservation_association_state_mapping(self):
        states = ['Migrating', 'Removing', 'Active', 'Unexpected']
        self.http.return_value = response({'value': [association(state) for state in states]})
        result = api.acr_reservation_list_registries(self.cmd, RESERVATION, RESOURCE_GROUP)
        self.assertEqual([item['associationState'] for item in result],
                         ['Updating', 'Updating', 'Succeeded', 'Unexpected'])

    def test_acr_reservation_invalid_association_cannot_mean_unassociated(self):
        self.http.return_value = response({'value': [{'associationState': 'Active'}]})
        with self.assertRaisesRegex(AzureResponseError, 'invalid registry association'):
            api.acr_reservation_list_registries(self.cmd, RESERVATION, RESOURCE_GROUP)

    def test_acr_reservation_invalid_identity_is_reported(self):
        invalid = resource()
        del invalid['name']
        self.http.return_value = response(invalid)
        with self.assertRaisesRegex(AzureResponseError, 'identity or location'):
            api.acr_reservation_show(self.cmd, RESERVATION, RESOURCE_GROUP)

    def test_acr_registry_reservation_lookup_is_rg_scoped(self):
        other = resource()
        other['name'] = 'other-reservation'
        self.http.side_effect = [
            response({'value': [other, resource()]}),
            response({'value': [association(name='differentregistry')]}),
            response({'value': [association('Migrating', REGISTRY.upper())]}),
        ]
        registry = {'name': REGISTRY, 'loginServer': REGISTRY + '.azurecr.io'}
        original = copy.deepcopy(registry)
        result = api.enrich_registry_reservation(self.cmd, registry, RESOURCE_GROUP, REGISTRY)
        self.assertEqual(result['reservation']['name'], RESERVATION)
        self.assertEqual(result['reservation']['associationState'], 'Updating')
        self.assertEqual(registry, original)
        self.assertEqual(self.http.call_count, 3)
        self.assertTrue(all('/resourceGroups/' + RESOURCE_GROUP in call.args[2]
                            for call in self.http.call_args_list))

    def test_acr_registry_reservation_lookup_distinguishes_none_from_failure(self):
        registry = {'name': REGISTRY}
        self.http.return_value = response({'value': []})
        self.assertIsNone(api.enrich_registry_reservation(
            self.cmd, registry, RESOURCE_GROUP, REGISTRY)['reservation'])
        self.http.side_effect = HTTPError('Forbidden', response('Not allowed', 403))
        with mock.patch.object(api.logger, 'warning') as warning:
            result = api.enrich_registry_reservation(self.cmd, registry, RESOURCE_GROUP, REGISTRY)
        self.assertIs(result, registry)
        self.assertNotIn('reservation', result)
        warning.assert_called_once()

    def test_acr_registry_show_public_cloud_is_unchanged(self):
        self.cmd.cli_ctx.cloud.name = 'AzureCloud'
        registry = object()
        self.assertIs(api.enrich_registry_reservation(self.cmd, registry, RESOURCE_GROUP, REGISTRY), registry)
        self.http.assert_not_called()

    def test_acr_registry_create_validates_reservation_before_side_effects(self):
        for state, location in (('Updating', 'australiaeast'), ('Succeeded', 'eastus')):
            with self.subTest(state=state, location=location):
                self.http.return_value = response(resource(state))
                with self.assertRaises(InvalidArgumentValueError):
                    api.prepare_registry_reservation(self.cmd, RESERVATION, RESOURCE_GROUP, location, 30)

    def test_acr_registry_create_association_partial_failure_keeps_registry(self):
        self.http.side_effect = HTTPError('Conflict', response('Reservation is not ready.', 409))
        registry = {'name': REGISTRY}
        with self.assertRaisesRegex(AzureResponseError, 'registry has not been deleted') as error:
            api.associate_created_registry(self.cmd, registry, resource(), RESOURCE_GROUP, REGISTRY, 30)
        self.assertIn('az acr reservation associate', str(error.exception.recommendations))
        self.assertEqual(self.http.call_count, 1)
        self.assertEqual(self.http.call_args.args[1], 'POST')

    def test_acr_registry_create_association_returns_enriched_registry(self):
        self.http.side_effect = [response(status=204), response({'value': [association()]})]
        registry = {'name': REGISTRY}
        result = api.associate_created_registry(
            self.cmd, registry, resource(), RESOURCE_GROUP, REGISTRY, 30)
        self.assertEqual(result['reservation'], {
            'id': RESOURCE_PATH, 'name': RESERVATION, 'associationState': 'Succeeded',
        })

    def test_acr_reservation_table_output_has_no_internals(self):
        formatted = reservation_output_format(resource())
        self.assertNotIn('stamp', json.dumps(formatted).lower())
        self.assertIn('R4', json.dumps(formatted))
        registry = {'name': REGISTRY, 'reservation': {'name': RESERVATION}}
        self.assertIn(RESERVATION, json.dumps(registry_output_format(registry)))


class RegistryIntegrationTests(unittest.TestCase):

    def setUp(self):
        self.cmd = mock.MagicMock()
        self.client = mock.MagicMock()
        self.cmd.get_models.return_value = (mock.Mock(), mock.Mock(), mock.Mock())
        patcher = mock.patch.object(custom, 'get_managed_sku', return_value=['Premium'])
        patcher.start()
        self.addCleanup(patcher.stop)

    def test_acr_create_without_reservation_preserves_poller(self):
        result = custom.acr_create(self.cmd, self.client, REGISTRY, RESOURCE_GROUP, 'Premium')
        self.assertIs(result, self.client.begin_create.return_value)

    @mock.patch.object(api, 'prepare_registry_reservation')
    def test_acr_create_invalid_reservation_does_not_create(self, prepare):
        prepare.side_effect = InvalidArgumentValueError('Reservation is not ready.')
        with self.assertRaises(InvalidArgumentValueError):
            custom.acr_create(self.cmd, self.client, REGISTRY, RESOURCE_GROUP, 'Premium',
                              location='australiaeast', reservation=RESERVATION)
        self.client.begin_create.assert_not_called()

    @mock.patch('azure.cli.core.commands.LongRunningOperation')
    @mock.patch.object(api, 'associate_created_registry')
    @mock.patch.object(api, 'prepare_registry_reservation')
    def test_acr_create_waits_before_associating(self, prepare, associate, lro):
        prepare.return_value = resource()
        created = {'name': REGISTRY}
        lro.return_value.return_value = created
        associate.return_value = {'name': REGISTRY, 'reservation': {'name': RESERVATION}}
        result = custom.acr_create(self.cmd, self.client, REGISTRY, RESOURCE_GROUP, 'Premium',
                                   location='australiaeast', reservation=RESERVATION)
        lro.return_value.assert_called_once_with(self.client.begin_create.return_value)
        associate.assert_called_once_with(self.cmd, created, prepare.return_value, RESOURCE_GROUP, REGISTRY, 1800)
        self.assertIs(result, associate.return_value)
        self.client.begin_delete.assert_not_called()

    @mock.patch.object(custom, 'get_resource_group_name_by_registry_name', return_value=RESOURCE_GROUP)
    @mock.patch.object(api, 'enrich_registry_reservation')
    def test_acr_show_wires_lookup(self, enrich, _resolve_group):
        result = custom.acr_show(self.cmd, self.client, REGISTRY)
        enrich.assert_called_once_with(self.cmd, self.client.get.return_value, RESOURCE_GROUP, REGISTRY)
        self.assertIs(result, enrich.return_value)


class ReservationCommandTests(unittest.TestCase):

    def _invoke(self, arguments, responses, expected_exit=0):
        from azure.cli.core import get_default_cli
        output = io.StringIO()
        with mock.patch.object(api, 'get_subscription_id', return_value=SUBSCRIPTION), \
                mock.patch.object(api, 'send_raw_request', side_effect=responses) as send:
            cli = get_default_cli()
            try:
                exit_code = cli.invoke(['acr', 'reservation'] + arguments + ['--only-show-errors'], out_file=output)
            except SystemExit as ex:
                exit_code = ex.code
            self.assertEqual(exit_code, expected_exit)
            return output.getvalue(), send.call_args_list

    def test_acr_reservation_cli_create_and_update_tiers(self):
        identity = ['-n', RESERVATION, '-g', RESOURCE_GROUP]
        output, calls = self._invoke(
            ['create'] + identity + ['-l', 'australiaeast', '--stamp-id', 'internal-stamp',
                                     '--request-rate-tier', 'r4', '--egress-tier', 'e2', '--ingress-tier', 'i1'],
            [response(resource(), 201)])
        properties = json.loads(calls[0].kwargs['body'])['properties']
        self.assertEqual(properties['requestRateRus'], 4)
        self.assertEqual(properties['egressGbps'], 32)
        self.assertEqual(properties['ingressGbps'], 0.5)
        self.assertNotIn('stampId', output)
        output, calls = self._invoke(
            ['update'] + identity + ['--ingress-tier', 'None'],
            [response(resource()), response(resource())])
        properties = json.loads(calls[1].kwargs['body'])['properties']
        self.assertEqual(properties['ingressGbps'], 0)
        self.assertEqual(properties['requestRateRus'], 4)
        self.assertEqual(properties['egressGbps'], 64)

    def test_acr_reservation_cli_read_delete_and_wait(self):
        identity = ['-n', RESERVATION, '-g', RESOURCE_GROUP]
        for arguments, responses, method in (
                (['show'] + identity, [response(resource())], 'GET'),
                (['show', '--ids', RESOURCE_PATH], [response(resource())], 'GET'),
                (['list', '-g', RESOURCE_GROUP], [response({'value': [resource()]})], 'GET'),
                (['list'], [response({'value': []})], 'GET'),
                (['delete'] + identity + ['--yes'], [response(status=204)], 'DELETE'),
                (['wait'] + identity + ['--created'], [response(resource())], 'GET'),
                (['wait'] + identity + ['--deleted'],
                 [HTTPError('Not found', response('Reservation not found.', 404))], 'GET')):
            with self.subTest(command=arguments):
                output, calls = self._invoke(arguments, responses)
                self.assertEqual(calls[0].args[1], method)
                self.assertNotIn('stampId', output)

    def test_acr_reservation_cli_associations(self):
        identity = ['-n', RESERVATION, '-g', RESOURCE_GROUP]
        for verb in ('associate', 'disassociate'):
            with self.subTest(verb=verb):
                output, calls = self._invoke(
                    [verb] + identity + ['--registry-name', REGISTRY, '--no-wait'], [response(status=204)])
                self.assertEqual(json.loads(calls[0].kwargs['body']), {'registryName': REGISTRY})
                self.assertEqual(len(calls), 1)
        output, _calls = self._invoke(
            ['list-registries'] + identity, [response({'value': [association('Migrating')]})])
        self.assertEqual(json.loads(output)[0]['associationState'], 'Updating')

    def test_acr_reservation_cli_requires_stamp_and_rejects_raw_capacity(self):
        for arguments in (
                ['create', '-n', RESERVATION, '-g', RESOURCE_GROUP, '--request-rate-tier', 'R4'],
                ['create', '-n', RESERVATION, '-g', RESOURCE_GROUP, '--stamp-id', 'stamp',
                 '--request-rate-tier', '100'],
                ['update', '-n', RESERVATION, '-g', RESOURCE_GROUP, '--request-rate-rus', '100']):
            with self.subTest(arguments=arguments):
                _output, calls = self._invoke(arguments, [], expected_exit=2)
                self.assertEqual(calls, [])

    def test_acr_reservation_cli_show_not_found_exits_three(self):
        self._invoke(['show', '-n', RESERVATION, '-g', RESOURCE_GROUP],
                     [HTTPError('Not found', response('Reservation not found.', 404))], expected_exit=3)
