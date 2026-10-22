# Reservation CLI test results

Date: 2026-10-21 (UTC)

Expanded run: **80 CLI checks passed, 2 CLI checks blocked, 86 mocked tests passed**.
Test reservations were cleaned up; `ericreservationdfaue` remains provisioned and
unassociated. The numbered sections below retain each command, its output, and
its exit code.

## Reservation list

Executed through the local worktree CLI (`azlocal`) against Dogfood.
Output refreshed after the table-formatting change to display unset tiers as `None`.

Input:

```powershell
azlocal acr reservation list -g eric-reservations-dfaue --subscription 06f5e253-d825-4052-87ec-c4f12bc8f343 -o table
```

Actual Output:

```text
WARNING: Command group 'acr reservation' is in preview and under development. Reference and support levels: https://aka.ms/CLI_refstatus
NAME                      LOCATION       REQUEST RATE TIER    EGRESS TIER    INGRESS TIER    STATE
------------------------  -------------  -------------------  -------------  --------------  ---------
eric-cli-validation-1021  australiaeast  R1                   None           None            Succeeded
```

Exit code: **0**

Result: **PASS**. The resource-group-scoped list returns the test reservation
in Australia East with request-rate tier R1 and provisioning state Succeeded.

## Expanded validation run

The following checks use the same worktree CLI as `azlocal`. Commands run
sequentially unless identified as offline tests. No `az rest` or direct HTTP
workarounds are used. Live capacity is limited to one test reservation with R1
and, temporarily, I1; there are no traffic generators or high-capacity tests.

Warnings are retained. Where both streams contain output, stderr is shown
before stdout; `(no output)` denotes empty streams. Exit codes expected for
negative tests are recorded as successful rejections, not successful operations.

Cleanup is authorized for test reservations only. The existing registry
`ericreservationdfaue` is to remain provisioned and unassociated.

Started: `2026-10-21T07:52:24.154041+00:00`.

## 1. Dogfood context

Input:

```powershell
azlocal cloud show --query '{cloud:name,arm:endpoints.resourceManager}' -o json
```

Actual Output:

```text
{
  "arm": "https://api-dogfood.resources.windows-int.net/",
  "cloud": "Dogfood"
}
```

Exit code: **0**

Result: **PASS**. Command completed successfully.

## 2. Starting reservation inventory

Input:

```powershell
azlocal acr reservation list -g eric-reservations-dfaue --subscription 06f5e253-d825-4052-87ec-c4f12bc8f343 -o json
```

Actual Output:

```text
WARNING: Command group 'acr reservation' is in preview and under development. Reference and support levels: https://aka.ms/CLI_refstatus
[
  {
    "id": "/subscriptions/06f5e253-d825-4052-87ec-c4f12bc8f343/resourceGroups/eric-reservations-dfaue/providers/Microsoft.ContainerRegistry/capacityReservations/eric-cli-validation-1021",
    "location": "australiaeast",
    "name": "eric-cli-validation-1021",
    "properties": {
      "createdAt": "2026-10-21T07:38:12.4074335+00:00",
      "earliestDeletableAt": "2026-10-21T07:43:12.4074335+00:00",
      "ingressTier": "None",
      "lastModifiedAt": "2026-10-21T07:39:51.037022+00:00",
      "provisioningState": "Succeeded",
      "requestRateTier": "R1",
      "reservedEgressGbps": 0.0,
      "reservedIngressGbps": 0.0,
      "reservedRequestRate": 1.0
    },
    "resourceGroup": "eric-reservations-dfaue",
    "tags": {
      "cliTest": "validation",
      "phase": "updated"
    },
    "type": "Microsoft.ContainerRegistry/capacityReservations"
  }
]
```

Exit code: **0**

Result: **PASS**. Command completed successfully.

## 3. Starting reservation state

Input:

```powershell
azlocal acr reservation show --ids /subscriptions/06f5e253-d825-4052-87ec-c4f12bc8f343/resourceGroups/eric-reservations-dfaue/providers/Microsoft.ContainerRegistry/capacityReservations/eric-cli-validation-1021 --subscription 06f5e253-d825-4052-87ec-c4f12bc8f343 -o json
```

Actual Output:

```text
WARNING: option '--subscription' will be ignored due to use of '--ids'.
WARNING: Command group 'acr reservation' is in preview and under development. Reference and support levels: https://aka.ms/CLI_refstatus
{
  "id": "/subscriptions/06f5e253-d825-4052-87ec-c4f12bc8f343/resourceGroups/eric-reservations-dfaue/providers/Microsoft.ContainerRegistry/capacityReservations/eric-cli-validation-1021",
  "location": "australiaeast",
  "name": "eric-cli-validation-1021",
  "properties": {
    "createdAt": "2026-10-21T07:38:12.4074335+00:00",
    "earliestDeletableAt": "2026-10-21T07:43:12.4074335+00:00",
    "ingressTier": "None",
    "lastModifiedAt": "2026-10-21T07:39:51.037022+00:00",
    "provisioningState": "Succeeded",
    "requestRateTier": "R1",
    "reservedEgressGbps": 0.0,
    "reservedIngressGbps": 0.0,
    "reservedRequestRate": 1.0
  },
  "resourceGroup": "eric-reservations-dfaue",
  "tags": {
    "cliTest": "validation",
    "phase": "updated"
  },
  "type": "Microsoft.ContainerRegistry/capacityReservations"
}
```

Exit code: **0**

Result: **PASS**. R1 and zero ingress/egress retained; no internal stamp properties in JSON.

## 4. Existing registry is unassociated

Input:

```powershell
azlocal acr show -n ericreservationdfaue -g eric-reservations-dfaue --subscription 06f5e253-d825-4052-87ec-c4f12bc8f343 -o json
```

Actual Output:

```text
{
  "adminUserEnabled": false,
  "anonymousPullEnabled": false,
  "autoGeneratedDomainNameLabelScope": "Unsecure",
  "creationDate": "2026-10-21T06:56:40.717943+00:00",
  "dataEndpointEnabled": false,
  "dataEndpointHostNames": [],
  "encryption": {
    "keyVaultProperties": null,
    "status": "disabled"
  },
  "endpointProtocol": "IPv4",
  "id": "/subscriptions/06f5e253-d825-4052-87ec-c4f12bc8f343/resourceGroups/eric-reservations-dfaue/providers/Microsoft.ContainerRegistry/registries/ericreservationdfaue",
  "identity": null,
  "location": "australiaeast",
  "loginServer": "ericreservationdfaue.azurecr-test.io",
  "metadataSearch": "Disabled",
  "name": "ericreservationdfaue",
  "networkRuleBypassAllowedForTasks": false,
  "networkRuleBypassOptions": "AzureServices",
  "networkRuleSet": {
    "defaultAction": "Allow",
    "ipRules": [],
    "virtualNetworkRules": []
  },
  "policies": {
    "azureAdAuthenticationAsArmPolicy": {
      "status": "enabled"
    },
    "exportPolicy": {
      "status": "enabled"
    },
    "quarantinePolicy": {
      "status": "disabled"
    },
    "retentionPolicy": {
      "days": 7,
      "lastUpdatedTime": "2026-10-21T06:56:49.523095+00:00",
      "status": "disabled"
    },
    "softDeletePolicy": {
      "lastUpdatedTime": "2026-10-21T06:56:49.523376+00:00",
      "retentionDays": 7,
      "status": "disabled"
    },
    "trustPolicy": {
      "status": "disabled",
      "type": "Notary"
    }
  },
  "privateEndpointConnections": [],
  "provisioningState": "Succeeded",
  "publicNetworkAccess": "Enabled",
  "regionalEndpointHostNames": [],
  "regionalEndpoints": "Disabled",
  "reservation": null,
  "resourceGroup": "eric-reservations-dfaue",
  "roleAssignmentMode": "LegacyRegistryPermissions",
  "sku": {
    "name": "Premium",
    "tier": "Premium"
  },
  "status": null,
  "systemData": {
    "createdAt": "2026-10-21T06:56:40.717943+00:00",
    "createdBy": "ericdu@acrbami202608.ccsctp.net",
    "createdByType": "User",
    "lastModifiedAt": "2026-10-21T06:56:40.717943+00:00",
    "lastModifiedBy": "ericdu@acrbami202608.ccsctp.net",
    "lastModifiedByType": "User"
  },
  "tags": {
    "cliTest": "reservation-lifecycle"
  },
  "type": "Microsoft.ContainerRegistry/registries",
  "writableCacheRepos": "Disabled",
  "zoneRedundancy": "Disabled"
}
```

Exit code: **0**

Result: **PASS**. Command completed successfully.

## 5. Help: az acr reservation

Input:

```powershell
azlocal acr reservation --help
```

Actual Output:

```text

Group
    az acr reservation : Manage preview capacity reservations through the POC ARM API.
        Uses API version 2026-09-01-preview at the selected cloud's ARM endpoint. The POC is
        deployed in Dogfood.
        Capacity reservations support named request-rate, egress and ingress tiers. Creation
        requires --stamp-id
        and at least one tier. Stamp details are excluded from results. Ledger seeding is an
        operator prerequisite
        and is not supported by these commands. The POC does not support migration of private-
        endpoint registries or replicas.
        WARNING: This command group is in preview and under development. Reference and support
        levels: https://aka.ms/CLI_refstatus

Commands:
    associate       : Associate an existing registry with a capacity reservation.
    create          : Reserve request-rate, egress or ingress capacity on an onboarded POC stamp.
    delete          : Delete a reservation after its associations and minimum commitment have
                      cleared.
    disassociate    : Remove a registry from a capacity reservation.
    list            : List capacity reservations in a resource group or subscription.
    list-registries : List registry associations with customer-facing states.
    show            : Show a capacity reservation without stamp internals.
    update          : Resize a capacity reservation using named tiers.
    wait            : Wait for a capacity reservation to reach a provisioning state.
```

Exit code: **0**

Result: **PASS**. Command completed successfully.

## 6. Help: az acr reservation create

Input:

```powershell
azlocal acr reservation create --help
```

Actual Output:

```text

Command
    az acr reservation create : Reserve request-rate, egress or ingress capacity on an onboarded POC
    stamp.
        Specify at least one tier; omitted dimensions reserve zero. The POC minimum commitment
        defaults to five minutes.
        Operations wait for completion unless --no-wait is supplied. Tier capacity mappings are
        fixed POC values.
        WARNING: Command group 'acr reservation' is in preview and under development. Reference and
        support levels: https://aka.ms/CLI_refstatus

Arguments
    --name -n           [Required] : Name of the capacity reservation.
    --resource-group -g [Required] : Name of resource group. You can configure the default group
                                     using `az configure --defaults group=<name>`.
    --stamp-id          [Required] : Identifier of the onboarded Dogfood stamp supplying capacity.
                                     Required for the POC; excluded from command output.
    --egress-tier                  : Egress tier. E1 reserves 16 Gbps; each tier doubles the
                                     capacity.  Allowed values: E1, E16, E2, E32, E4, E8.
    --ingress-tier                 : Ingress tier. I1 reserves 0.5 Gbps; each tier doubles the
                                     capacity.  Allowed values: I1, I16, I2, I4, I8.
    --location -l                  : Location. Values from: `az account list-locations`. You can
                                     configure the default location using `az configure --defaults
                                     location=<location>`.
    --no-wait                      : Do not wait for the operation to complete.
    --request-rate-tier            : Request-rate tier. R1 reserves 1 RU; each tier doubles the
                                     capacity.  Allowed values: R1, R16, R2, R32, R4, R64, R8.
    --tags                         : Space-separated tags: key[=value] [key[=value] ...]. Use "" to
                                     clear existing tags.
    --timeout                      : The timeout in seconds.  Default: 1800.

Global Policy Arguments
    --acquire-policy-token         : Acquiring an Azure Policy token automatically for this resource
                                     operation.
    --change-reference             : The related change reference ID for this resource operation.

Global Arguments
    --debug                        : Increase logging verbosity to show all debug logs.
    --help -h                      : Show this help message and exit.
    --only-show-errors             : Only show errors, suppressing warnings.
    --output -o                    : Output format.  Allowed values: json, jsonc, none, table, tsv,
                                     yaml, yamlc.  Default: json.
    --query                        : JMESPath query string. See http://jmespath.org/ for more
                                     information and examples.
    --subscription                 : Name or ID of subscription. You can configure the default
                                     subscription using `az account set -s NAME_OR_ID`.
    --verbose                      : Increase logging verbosity. Use --debug for full debug logs.

Examples
    Reserve request-rate and egress capacity.
        az acr reservation create -n MyReservation -g MyResourceGroup -l australiaeast --stamp-id
        dfaue-1 --request-rate-tier R4 --egress-tier E4

    Reserve ingress capacity without waiting.
        az acr reservation create -n MyIngressReservation -g MyResourceGroup -l australiaeast
        --stamp-id dfaue-1 --ingress-tier I2 --no-wait
```

Exit code: **0**

Result: **PASS**. Command completed successfully.

## 7. Help: az acr reservation show

Input:

```powershell
azlocal acr reservation show --help
```

Actual Output:

```text

Command
    az acr reservation show : Show a capacity reservation without stamp internals.
        WARNING: Command group 'acr reservation' is in preview and under development. Reference and
        support levels: https://aka.ms/CLI_refstatus
Arguments

Resource Id Arguments
    --ids               : One or more resource IDs (space-delimited). It should be a complete
                          resource ID containing all information of 'Resource Id' arguments. You
                          should provide either --ids or other 'Resource Id' arguments.
    --name -n           : Name of the capacity reservation.
    --resource-group -g : Name of resource group. You can configure the default group using `az
                          configure --defaults group=<name>`.
    --subscription      : Name or ID of subscription. You can configure the default subscription
                          using `az account set -s NAME_OR_ID`.

Global Arguments
    --debug             : Increase logging verbosity to show all debug logs.
    --help -h           : Show this help message and exit.
    --only-show-errors  : Only show errors, suppressing warnings.
    --output -o         : Output format.  Allowed values: json, jsonc, none, table, tsv, yaml,
                          yamlc.  Default: json.
    --query             : JMESPath query string. See http://jmespath.org/ for more information and
                          examples.
    --verbose           : Increase logging verbosity. Use --debug for full debug logs.

Examples
    Show a reservation.
        az acr reservation show -n MyReservation -g MyResourceGroup

    Show its provisioning state.
        az acr reservation show -n MyReservation -g MyResourceGroup --query
        properties.provisioningState
```

Exit code: **0**

Result: **PASS**. Command completed successfully.

## 8. Help: az acr reservation list

Input:

```powershell
azlocal acr reservation list --help
```

Actual Output:

```text

Command
    az acr reservation list : List capacity reservations in a resource group or subscription.
        WARNING: Command group 'acr reservation' is in preview and under development. Reference and
        support levels: https://aka.ms/CLI_refstatus
Arguments
    --resource-group -g : Name of resource group. You can configure the default group using `az
                          configure --defaults group=<name>`.

Global Arguments
    --debug             : Increase logging verbosity to show all debug logs.
    --help -h           : Show this help message and exit.
    --only-show-errors  : Only show errors, suppressing warnings.
    --output -o         : Output format.  Allowed values: json, jsonc, none, table, tsv, yaml,
                          yamlc.  Default: json.
    --query             : JMESPath query string. See http://jmespath.org/ for more information and
                          examples.
    --subscription      : Name or ID of subscription. You can configure the default subscription
                          using `az account set -s NAME_OR_ID`.
    --verbose           : Increase logging verbosity. Use --debug for full debug logs.

Examples
    List reservations in a resource group.
        az acr reservation list -g MyResourceGroup

    List reservations in the current subscription.
        az acr reservation list
```

Exit code: **0**

Result: **PASS**. Command completed successfully.

## 9. Help: az acr reservation update

Input:

```powershell
azlocal acr reservation update --help
```

Actual Output:

```text

Command
    az acr reservation update : Resize a capacity reservation using named tiers.
        Omitted dimensions retain their current capacity. Use None to remove a dimension; at least
        one dimension
        must remain positive. Updates read current capacity before submitting all three amounts, so
        avoid concurrent
        updates to the same reservation. The POC's provisioning state is trusted, including after a
        service-side rollback.
        WARNING: Command group 'acr reservation' is in preview and under development. Reference and
        support levels: https://aka.ms/CLI_refstatus

Arguments
    --egress-tier          : Egress tier. E1 reserves 16 Gbps; each tier doubles the capacity.
                             Allowed values: E1, E16, E2, E32, E4, E8, None.
    --ingress-tier         : Ingress tier. I1 reserves 0.5 Gbps; each tier doubles the capacity.
                             Allowed values: I1, I16, I2, I4, I8, None.
    --no-wait              : Do not wait for the operation to complete.
    --request-rate-tier    : Request-rate tier. R1 reserves 1 RU; each tier doubles the capacity.
                             Allowed values: None, R1, R16, R2, R32, R4, R64, R8.
    --tags                 : Space-separated tags: key[=value] [key[=value] ...]. Use "" to clear
                             existing tags.
    --timeout              : The timeout in seconds.  Default: 1800.

Global Policy Arguments
    --acquire-policy-token : Acquiring an Azure Policy token automatically for this resource
                             operation.
    --change-reference     : The related change reference ID for this resource operation.

Resource Id Arguments
    --ids                  : One or more resource IDs (space-delimited). It should be a complete
                             resource ID containing all information of 'Resource Id' arguments. You
                             should provide either --ids or other 'Resource Id' arguments.
    --name -n              : Name of the capacity reservation.
    --resource-group -g    : Name of resource group. You can configure the default group using `az
                             configure --defaults group=<name>`.
    --subscription         : Name or ID of subscription. You can configure the default subscription
                             using `az account set -s NAME_OR_ID`.

Global Arguments
    --debug                : Increase logging verbosity to show all debug logs.
    --help -h              : Show this help message and exit.
    --only-show-errors     : Only show errors, suppressing warnings.
    --output -o            : Output format.  Allowed values: json, jsonc, none, table, tsv, yaml,
                             yamlc.  Default: json.
    --query                : JMESPath query string. See http://jmespath.org/ for more information
                             and examples.
    --verbose              : Increase logging verbosity. Use --debug for full debug logs.

Examples
    Increase egress while keeping other dimensions unchanged.
        az acr reservation update -n MyReservation -g MyResourceGroup --egress-tier E8

    Remove ingress while retaining a request-rate reservation.
        az acr reservation update -n MyReservation -g MyResourceGroup --request-rate-tier R4
        --ingress-tier None
```

Exit code: **0**

Result: **PASS**. Command completed successfully.

## 10. Help: az acr reservation delete

Input:

```powershell
azlocal acr reservation delete --help
```

Actual Output:

```text

Command
    az acr reservation delete : Delete a reservation after its associations and minimum commitment
    have cleared.
        WARNING: Command group 'acr reservation' is in preview and under development. Reference and
        support levels: https://aka.ms/CLI_refstatus
Arguments
    --no-wait              : Do not wait for the operation to complete.
    --timeout              : The timeout in seconds.  Default: 1800.
    --yes -y               : Do not prompt for confirmation.

Global Policy Arguments
    --acquire-policy-token : Acquiring an Azure Policy token automatically for this resource
                             operation.
    --change-reference     : The related change reference ID for this resource operation.

Resource Id Arguments
    --ids                  : One or more resource IDs (space-delimited). It should be a complete
                             resource ID containing all information of 'Resource Id' arguments. You
                             should provide either --ids or other 'Resource Id' arguments.
    --name -n              : Name of the capacity reservation.
    --resource-group -g    : Name of resource group. You can configure the default group using `az
                             configure --defaults group=<name>`.
    --subscription         : Name or ID of subscription. You can configure the default subscription
                             using `az account set -s NAME_OR_ID`.

Global Arguments
    --debug                : Increase logging verbosity to show all debug logs.
    --help -h              : Show this help message and exit.
    --only-show-errors     : Only show errors, suppressing warnings.
    --output -o            : Output format.  Allowed values: json, jsonc, none, table, tsv, yaml,
                             yamlc.  Default: json.
    --query                : JMESPath query string. See http://jmespath.org/ for more information
                             and examples.
    --verbose              : Increase logging verbosity. Use --debug for full debug logs.

Examples
    Delete a reservation with confirmation.
        az acr reservation delete -n MyReservation -g MyResourceGroup

    Delete without prompting.
        az acr reservation delete -n MyReservation -g MyResourceGroup --yes
```

Exit code: **0**

Result: **PASS**. Command completed successfully.

## 11. Help: az acr reservation associate

Input:

```powershell
azlocal acr reservation associate --help
```

Actual Output:

```text

Command
    az acr reservation associate : Associate an existing registry with a capacity reservation.
        The registry must be in the reservation's subscription and resource group. Waits until the
        association is Active,
        displayed as Succeeded, unless --no-wait is supplied. Pending changes are displayed as
        Updating.
        A timeout does not cancel the operation. The POC does not expose background migration
        failure details.
        WARNING: Command group 'acr reservation' is in preview and under development. Reference and
        support levels: https://aka.ms/CLI_refstatus

Arguments
    --registry-name [Required] : Name of an existing registry in the reservation subscription and
                                 resource group.
    --no-wait                  : Do not wait for the operation to complete.
    --timeout                  : The timeout in seconds.  Default: 1800.

Global Policy Arguments
    --acquire-policy-token     : Acquiring an Azure Policy token automatically for this resource
                                 operation.
    --change-reference         : The related change reference ID for this resource operation.

Resource Id Arguments
    --ids                      : One or more resource IDs (space-delimited). It should be a complete
                                 resource ID containing all information of 'Resource Id' arguments.
                                 You should provide either --ids or other 'Resource Id' arguments.
    --name -n                  : Name of the capacity reservation.
    --resource-group -g        : Name of resource group. You can configure the default group using
                                 `az configure --defaults group=<name>`.
    --subscription             : Name or ID of subscription. You can configure the default
                                 subscription using `az account set -s NAME_OR_ID`.

Global Arguments
    --debug                    : Increase logging verbosity to show all debug logs.
    --help -h                  : Show this help message and exit.
    --only-show-errors         : Only show errors, suppressing warnings.
    --output -o                : Output format.  Allowed values: json, jsonc, none, table, tsv,
                                 yaml, yamlc.  Default: json.
    --query                    : JMESPath query string. See http://jmespath.org/ for more
                                 information and examples.
    --verbose                  : Increase logging verbosity. Use --debug for full debug logs.

Examples
    Associate and wait for completion.
        az acr reservation associate -n MyReservation -g MyResourceGroup --registry-name myregistry

    Start association without waiting.
        az acr reservation associate -n MyReservation -g MyResourceGroup --registry-name myregistry
        --no-wait
```

Exit code: **0**

Result: **PASS**. Command completed successfully.

## 12. Help: az acr reservation disassociate

Input:

```powershell
azlocal acr reservation disassociate --help
```

Actual Output:

```text

Command
    az acr reservation disassociate : Remove a registry from a capacity reservation.
        Waits until this registry's association disappears unless --no-wait is supplied.
        A timeout does not cancel the operation or delete the registry.
        WARNING: Command group 'acr reservation' is in preview and under development. Reference and
        support levels: https://aka.ms/CLI_refstatus

Arguments
    --registry-name [Required] : Name of an existing registry in the reservation subscription and
                                 resource group.
    --no-wait                  : Do not wait for the operation to complete.
    --timeout                  : The timeout in seconds.  Default: 1800.

Global Policy Arguments
    --acquire-policy-token     : Acquiring an Azure Policy token automatically for this resource
                                 operation.
    --change-reference         : The related change reference ID for this resource operation.

Resource Id Arguments
    --ids                      : One or more resource IDs (space-delimited). It should be a complete
                                 resource ID containing all information of 'Resource Id' arguments.
                                 You should provide either --ids or other 'Resource Id' arguments.
    --name -n                  : Name of the capacity reservation.
    --resource-group -g        : Name of resource group. You can configure the default group using
                                 `az configure --defaults group=<name>`.
    --subscription             : Name or ID of subscription. You can configure the default
                                 subscription using `az account set -s NAME_OR_ID`.

Global Arguments
    --debug                    : Increase logging verbosity to show all debug logs.
    --help -h                  : Show this help message and exit.
    --only-show-errors         : Only show errors, suppressing warnings.
    --output -o                : Output format.  Allowed values: json, jsonc, none, table, tsv,
                                 yaml, yamlc.  Default: json.
    --query                    : JMESPath query string. See http://jmespath.org/ for more
                                 information and examples.
    --verbose                  : Increase logging verbosity. Use --debug for full debug logs.

Examples
    Disassociate and wait for completion.
        az acr reservation disassociate -n MyReservation -g MyResourceGroup --registry-name
        myregistry

    Start disassociation without waiting.
        az acr reservation disassociate -n MyReservation -g MyResourceGroup --registry-name
        myregistry --no-wait
```

Exit code: **0**

Result: **PASS**. Command completed successfully.

## 13. Help: az acr reservation list-registries

Input:

```powershell
azlocal acr reservation list-registries --help
```

Actual Output:

```text

Command
    az acr reservation list-registries : List registry associations with customer-facing states.
        WARNING: Command group 'acr reservation' is in preview and under development. Reference and
        support levels: https://aka.ms/CLI_refstatus
Arguments

Global Policy Arguments
    --acquire-policy-token : Acquiring an Azure Policy token automatically for this resource
                             operation.
    --change-reference     : The related change reference ID for this resource operation.

Resource Id Arguments
    --ids                  : One or more resource IDs (space-delimited). It should be a complete
                             resource ID containing all information of 'Resource Id' arguments. You
                             should provide either --ids or other 'Resource Id' arguments.
    --name -n              : Name of the capacity reservation.
    --resource-group -g    : Name of resource group. You can configure the default group using `az
                             configure --defaults group=<name>`.
    --subscription         : Name or ID of subscription. You can configure the default subscription
                             using `az account set -s NAME_OR_ID`.

Global Arguments
    --debug                : Increase logging verbosity to show all debug logs.
    --help -h              : Show this help message and exit.
    --only-show-errors     : Only show errors, suppressing warnings.
    --output -o            : Output format.  Allowed values: json, jsonc, none, table, tsv, yaml,
                             yamlc.  Default: json.
    --query                : JMESPath query string. See http://jmespath.org/ for more information
                             and examples.
    --verbose              : Increase logging verbosity. Use --debug for full debug logs.

Examples
    List associated registries.
        az acr reservation list-registries -n MyReservation -g MyResourceGroup

    List registry names only.
        az acr reservation list-registries -n MyReservation -g MyResourceGroup --query
        "[].registryId" -o tsv
```

Exit code: **0**

Result: **PASS**. Command completed successfully.

## 14. Help: az acr reservation wait

Input:

```powershell
azlocal acr reservation wait --help
```

Actual Output:

```text

Command
    az acr reservation wait : Wait for a capacity reservation to reach a provisioning state.
        This waits for the reservation resource, not its registry associations.
        WARNING: Command group 'acr reservation' is in preview and under development. Reference and
        support levels: https://aka.ms/CLI_refstatus

Arguments

Global Policy Arguments
    --acquire-policy-token : Acquiring an Azure Policy token automatically for this resource
                             operation.
    --change-reference     : The related change reference ID for this resource operation.

Resource Id Arguments
    --ids                  : One or more resource IDs (space-delimited). It should be a complete
                             resource ID containing all information of 'Resource Id' arguments. You
                             should provide either --ids or other 'Resource Id' arguments.
    --name -n              : Name of the capacity reservation.
    --resource-group -g    : Name of resource group. You can configure the default group using `az
                             configure --defaults group=<name>`.
    --subscription         : Name or ID of subscription. You can configure the default subscription
                             using `az account set -s NAME_OR_ID`.

Wait Condition Arguments
    --created              : Wait until created with 'provisioningState' at 'Succeeded'.
    --custom               : Wait until the condition satisfies a custom JMESPath query. E.g.
                             provisioningState!='InProgress',
                             instanceView.statuses[?code=='PowerState/running'].
    --deleted              : Wait until deleted.
    --exists               : Wait until the resource exists.
    --interval             : Polling interval in seconds.  Default: 30.
    --timeout              : The timeout in seconds.  Default: 3600.
    --updated              : Wait until updated with provisioningState at 'Succeeded'.

Global Arguments
    --debug                : Increase logging verbosity to show all debug logs.
    --help -h              : Show this help message and exit.
    --only-show-errors     : Only show errors, suppressing warnings.
    --output -o            : Output format.  Allowed values: json, jsonc, none, table, tsv, yaml,
                             yamlc.  Default: json.
    --query                : JMESPath query string. See http://jmespath.org/ for more information
                             and examples.
    --verbose              : Increase logging verbosity. Use --debug for full debug logs.

Examples
    Wait for successful provisioning.
        az acr reservation wait -n MyReservation -g MyResourceGroup --created

    Wait for deletion.
        az acr reservation wait -n MyReservation -g MyResourceGroup --deleted
```

Exit code: **0**

Result: **PASS**. Command completed successfully.

## 15. Registry integration help: create

Input:

```powershell
azlocal acr create --help
```

Actual Output:

```text

Command
    az acr create : Create an Azure Container Registry.
        With --reservation, create the registry first, then associate it with an existing capacity
        reservation.
        The reservation must be ready and in the same subscription, resource group and region.
        If association fails or times out, the registry is preserved and the command reports the
        partial failure.

Arguments
    --name -n              [Required] : The name of the container registry. It should be specified
                                        in lower case. You can configure the default registry name
                                        using `az configure --defaults acr=<registry name>`.
    --resource-group -g    [Required] : Name of resource group. You can configure the default group
                                        using `az configure --defaults group=<name>`.
    --sku                  [Required] : The SKU of the container registry.  Allowed values: Basic,
                                        Premium, Standard.
    --admin-enabled                   : Indicates whether the admin user is enabled.  Allowed
                                        values: false, true.
    --allow-exports         [Preview] : Configure exportPolicy to allow/disallow artifacts from
                                        being exported from this registry. Artifacts can be exported
                                        via import or transfer operations. For more information,
                                        please visit https://aka.ms/acr/export-policy.  Allowed
                                        values: false, true.
        WARNING: Argument '--allow-exports' is in preview and under development. Reference and
        support levels: https://aka.ms/CLI_refstatus
    --allow-metadata-search [Preview] : Enable or disable the metadata-search feature for the
                                        registry. If not specified, this is set to disabled by
                                        default.  Allowed values: false, true.
        WARNING: Argument '--allow-metadata-search' is in preview and under development. Reference
        and support levels: https://aka.ms/CLI_refstatus
    --dnl-scope             [Preview] : Domain name label scope will add a hash to the resource
                                        name. The resulting login server name will be in the format
                                        `registryname`-`hash`.azurecr-io. Default is Unsecure.
                                        Allowed values: NoReuse, ResourceGroupReuse,
                                        SubscriptionReuse, TenantReuse, Unsecure.
        WARNING: Argument '--dnl-scope' is in preview and under development. Reference and support
        levels: https://aka.ms/CLI_refstatus
    --location -l                     : Location. Values from: `az account list-locations`. You can
                                        configure the default location using `az configure
                                        --defaults location=<location>`.
    --reservation           [Preview] : Name of a capacity reservation in the same subscription,
                                        resource group and region. Create the registry, then
                                        associate it and wait. The registry is preserved if
                                        association fails.
        WARNING: Argument '--reservation' is in preview and under development. Reference and support
        levels: https://aka.ms/CLI_refstatus
    --reservation-timeout             : Maximum time in seconds to wait for the reservation
                                        association after registry creation. Only used with
                                        --reservation.  Default: 1800.
    --tags                            : Space-separated tags: key[=value] [key[=value] ...]. Use ""
                                        to clear existing tags.
    --workspace             [Preview] : Name or ID of the Log Analytics workspace to send registry
                                        diagnostic logs to. All events will be enabled. You can use
                                        "az monitor log-analytics workspace create" to create one.
                                        Extra billing may apply.
        WARNING: Argument '--workspace' is in preview and under development. Reference and support
        levels: https://aka.ms/CLI_refstatus
    --writable-cache-repos  [Preview] : 'Enable or disable writing to repositories backed by cache
                                        rules. If not specified, this is set to Disabled by
                                        default'.  Allowed values: Disabled, Enabled.
        WARNING: Argument '--writable-cache-repos' is in preview and under development. Reference
        and support levels: https://aka.ms/CLI_refstatus
    --zone-redundancy       [Preview] : Indicates whether or not zone redundancy should be enabled
                                        for this registry or replication. For more information, such
                                        as supported locations, please visit https://aka.ms/acr/az.
                                        Zone-redundancy cannot be updated. Defaults to 'Disabled'.
                                        Allowed values: Disabled, Enabled.
        WARNING: Argument '--zone-redundancy' is in preview and under development. Reference and
        support levels: https://aka.ms/CLI_refstatus

Customer managed key Arguments
    --identity                        : Use assigned managed identity resource id or name if in the
                                        same resource group.
    --key-encryption-key              : Azure Key Vault or Managed HSM key URI. To enable automated
                                        rotation, provide a versionless key URI. For manual
                                        rotation, provide a versioned key URI.

Global Policy Arguments
    --acquire-policy-token            : Acquiring an Azure Policy token automatically for this
                                        resource operation.
    --change-reference                : The related change reference ID for this resource operation.

Network Rule Arguments
    --allow-trusted-services          : Allow trusted Azure Services to access network restricted
                                        registries. For more information, please visit
                                        https://aka.ms/acr/trusted-services. The Default is to
                                        allow.  Allowed values: false, true.
    --data-endpoint-enabled           : Enable dedicated data endpoint for client firewall
                                        configuration.  Allowed values: false, true.
    --default-action                  : Default action to apply when no rule matches. Only
                                        applicable to Premium SKU.  Allowed values: Allow, Deny.
    --endpoint-protocol     [Preview] : The endpoint protocol for the registry. Allowed values:
                                        IPv4, IPv4AndIPv6.  Allowed values: IPv4, IPv4AndIPv6.
        WARNING: Argument '--endpoint-protocol' is in preview and under development. Reference and
        support levels: https://aka.ms/CLI_refstatus
    --public-network-enabled          : Allow public network access for the container registry. The
                                        Default is to allow.  Allowed values: false, true.
    --regional-endpoints    [Preview] : Indicates whether or not regional endpoints should be
                                        enabled for the registry.  Allowed values: Disabled,
                                        Enabled.
        WARNING: Argument '--regional-endpoints' is in preview and under development. Reference and
        support levels: https://aka.ms/CLI_refstatus

Permissions and Role Assignment Arguments
    --role-assignment-mode            : Role assignment mode of the registry. For more information
                                        on this feature, see https://aka.ms/acr/auth/abac. The
                                        Default is rbac.  Allowed values: rbac, rbac-abac.

Global Arguments
    --debug                           : Increase logging verbosity to show all debug logs.
    --help -h                         : Show this help message and exit.
    --only-show-errors                : Only show errors, suppressing warnings.
    --output -o                       : Output format.  Allowed values: json, jsonc, none, table,
                                        tsv, yaml, yamlc.  Default: json.
    --query                           : JMESPath query string. See http://jmespath.org/ for more
                                        information and examples.
    --subscription                    : Name or ID of subscription. You can configure the default
                                        subscription using `az account set -s NAME_OR_ID`.
    --verbose                         : Increase logging verbosity. Use --debug for full debug logs.

Examples
    Create a registry and associate it with a ready Dogfood capacity reservation.
        az acr create -n myregistry -g MyResourceGroup --sku Premium -l australiaeast --reservation
        MyReservation

    Create a managed container registry with the Standard SKU.
        az acr create -n myregistry -g MyResourceGroup --sku Standard


    Create a registry with ABAC-based Repository Permission enabled.
        az acr create -n myregistry -g MyResourceGroup --sku Standard --role-assignment-mode rbac-
        abac


    Create a managed container registry with the Premium SKU and regional endpoints enabled.
        az acr create -n myregistry -g MyResourceGroup --sku Premium --regional-endpoints enabled


    Create a managed container registry with the Premium SKU and dual-stack (IPv4 and IPv6) endpoint
    protocol.
        az acr create -n myregistry -g MyResourceGroup --sku Premium --data-endpoint-enabled true
        --endpoint-protocol IPv4AndIPv6


    Create a managed container registry with writable cache repositories enabled.
        az acr create -n myregistry -g MyResourceGroup --sku Premium --writable-cache-repos enabled


    Create a Premium registry encrypted with a customer-managed key in Managed HSM.
        az acr create --name myregistry --resource-group MyResourceGroup --sku Premium --identity
        myidentity --key-encryption-key https://myhsm.managedhsm.azure.net/keys/mykey
```

Exit code: **0**

Result: **PASS**. Command completed successfully.

## 16. Registry integration help: show

Input:

```powershell
azlocal acr show --help
```

Actual Output:

```text

Command
    az acr show : Get the details of an Azure Container Registry.
        In clouds named Dogfood or AzureDogfood, also look up the registry's capacity reservation
        within its resource group.
        This requires permission to list reservations and their registry associations. If lookup
        fails, a warning is emitted
        and the reservation field is omitted. A null reservation means the lookup succeeded and
        found no association.

Arguments
    --name -n [Required] : The name of the container registry. It should be specified in lower case.
                           You can configure the default registry name using `az configure
                           --defaults acr=<registry name>`.
    --resource-group -g  : Name of resource group. You can configure the default group using `az
                           configure --defaults group=<name>`.

Global Arguments
    --debug              : Increase logging verbosity to show all debug logs.
    --help -h            : Show this help message and exit.
    --only-show-errors   : Only show errors, suppressing warnings.
    --output -o          : Output format.  Allowed values: json, jsonc, none, table, tsv, yaml,
                           yamlc.  Default: json.
    --query              : JMESPath query string. See http://jmespath.org/ for more information and
                           examples.
    --subscription       : Name or ID of subscription. You can configure the default subscription
                           using `az account set -s NAME_OR_ID`.
    --verbose            : Increase logging verbosity. Use --debug for full debug logs.

Examples
    Get the login server for an Azure Container Registry.
        az acr show -n myregistry --query loginServer


    Get the details of an Azure Container Registry
        az acr show --name myregistry --resource-group MyResourceGroup

    Check status of ABAC-based Repository Permission on a registry.
        az acr show --name myregistry --resource-group MyResourceGroup --query roleAssignmentMode
```

Exit code: **0**

Result: **PASS**. Command completed successfully.

## 17. Registry integration help: update

Input:

```powershell
azlocal acr update --help
```

Actual Output:

```text

Command
    az acr update : Update an Azure Container Registry.

Arguments
    --name -n              [Required] : The name of the container registry. It should be specified
                                        in lower case. You can configure the default registry name
                                        using `az configure --defaults acr=<registry name>`.
    --admin-enabled                   : Indicates whether the admin user is enabled.  Allowed
                                        values: false, true.
    --allow-exports         [Preview] : Configure exportPolicy to allow/disallow artifacts from
                                        being exported from this registry. Artifacts can be exported
                                        via import or transfer operations. For more information,
                                        please visit https://aka.ms/acr/export-policy.  Allowed
                                        values: false, true.
        WARNING: Argument '--allow-exports' is in preview and under development. Reference and
        support levels: https://aka.ms/CLI_refstatus
    --allow-metadata-search [Preview] : Enable or disable the metadata-search feature for the
                                        registry.  Allowed values: false, true.
        WARNING: Argument '--allow-metadata-search' is in preview and under development. Reference
        and support levels: https://aka.ms/CLI_refstatus
    --anonymous-pull-enabled          : Enable registry-wide pull from unauthenticated clients.
                                        Allowed values: false, true.
    --resource-group -g               : Name of resource group. You can configure the default group
                                        using `az configure --defaults group=<name>`.
    --sku                             : The SKU of the container registry.  Allowed values: Basic,
                                        Premium, Standard.
    --tags                            : Space-separated tags: key[=value] [key[=value] ...]. Use ""
                                        to clear existing tags.
    --writable-cache-repos  [Preview] : 'Enable or disable writing to repositories backed by cache
                                        rules. If not specified, this is set to Disabled by
                                        default'.  Allowed values: Disabled, Enabled.
        WARNING: Argument '--writable-cache-repos' is in preview and under development. Reference
        and support levels: https://aka.ms/CLI_refstatus

Generic Update Arguments
    --add                             : Add an object to a list of objects by specifying a path and
                                        key value pairs.  Example: `--add property.listProperty
                                        <key=value, string or JSON string>`.
    --force-string                    : When using 'set' or 'add', preserve string literals instead
                                        of attempting to convert to JSON.
    --remove                          : Remove a property or an element from a list.  Example:
                                        `--remove property.list <indexToRemove>` OR `--remove
                                        propertyToRemove`.
    --set                             : Update an object by specifying a property path and value to
                                        set.  Example: `--set property1.property2=<value>`.

Global Policy Arguments
    --acquire-policy-token            : Acquiring an Azure Policy token automatically for this
                                        resource operation.
    --change-reference                : The related change reference ID for this resource operation.

Network Rule Arguments
    --allow-trusted-services          : Allow trusted Azure Services to access network restricted
                                        registries. For more information, please visit
                                        https://aka.ms/acr/trusted-services.  Allowed values: false,
                                        true.
    --data-endpoint-enabled           : Enable dedicated data endpoint for client firewall
                                        configuration.  Allowed values: false, true.
    --default-action                  : Default action to apply when no rule matches. Only
                                        applicable to Premium SKU.  Allowed values: Allow, Deny.
    --endpoint-protocol     [Preview] : The endpoint protocol for the registry. Allowed values:
                                        IPv4, IPv4AndIPv6.  Allowed values: IPv4, IPv4AndIPv6.
        WARNING: Argument '--endpoint-protocol' is in preview and under development. Reference and
        support levels: https://aka.ms/CLI_refstatus
    --public-network-enabled          : Allow public network access for the container registry.
                                        Allowed values: false, true.
    --regional-endpoints    [Preview] : Indicates whether or not regional endpoints should be
                                        enabled for the registry.  Allowed values: Disabled,
                                        Enabled.
        WARNING: Argument '--regional-endpoints' is in preview and under development. Reference and
        support levels: https://aka.ms/CLI_refstatus

Permissions and Role Assignment Arguments
    --role-assignment-mode            : Role assignment mode of the registry. For more information
                                        on this feature, see https://aka.ms/acr/auth/abac. The
                                        Default is rbac.  Allowed values: rbac, rbac-abac.

Global Arguments
    --debug                           : Increase logging verbosity to show all debug logs.
    --help -h                         : Show this help message and exit.
    --only-show-errors                : Only show errors, suppressing warnings.
    --output -o                       : Output format.  Allowed values: json, jsonc, none, table,
                                        tsv, yaml, yamlc.  Default: json.
    --query                           : JMESPath query string. See http://jmespath.org/ for more
                                        information and examples.
    --subscription                    : Name or ID of subscription. You can configure the default
                                        subscription using `az account set -s NAME_OR_ID`.
    --verbose                         : Increase logging verbosity. Use --debug for full debug logs.

Examples
    Update tags for an Azure Container Registry.
        az acr update -n myregistry --tags key1=value1 key2=value2


    Enable the administrator user account for an Azure Container Registry.
        az acr update -n myregistry --admin-enabled true


    Turn on ABAC-based Repository Permission on an existing registry.
        az acr update -n myregistry --role-assignment-mode rbac-abac


    Enable regional endpoints on an existing registry.
        az acr update -n myregistry --regional-endpoints enabled


    Update the endpoint protocol for an Azure Container Registry.
        az acr update -n myregistry --endpoint-protocol IPv4AndIPv6


    Enable writable cache repositories on an existing registry.
        az acr update -n myregistry --writable-cache-repos enabled
```

Exit code: **0**

Result: **PASS**. Command completed successfully.

## 18. List reservations as JSON

Input:

```powershell
azlocal acr reservation list -g eric-reservations-dfaue --subscription 06f5e253-d825-4052-87ec-c4f12bc8f343 -o json
```

Actual Output:

```text
WARNING: Command group 'acr reservation' is in preview and under development. Reference and support levels: https://aka.ms/CLI_refstatus
[
  {
    "id": "/subscriptions/06f5e253-d825-4052-87ec-c4f12bc8f343/resourceGroups/eric-reservations-dfaue/providers/Microsoft.ContainerRegistry/capacityReservations/eric-cli-validation-1021",
    "location": "australiaeast",
    "name": "eric-cli-validation-1021",
    "properties": {
      "createdAt": "2026-10-21T07:38:12.4074335+00:00",
      "earliestDeletableAt": "2026-10-21T07:43:12.4074335+00:00",
      "ingressTier": "None",
      "lastModifiedAt": "2026-10-21T07:39:51.037022+00:00",
      "provisioningState": "Succeeded",
      "requestRateTier": "R1",
      "reservedEgressGbps": 0.0,
      "reservedIngressGbps": 0.0,
      "reservedRequestRate": 1.0
    },
    "resourceGroup": "eric-reservations-dfaue",
    "tags": {
      "cliTest": "validation",
      "phase": "updated"
    },
    "type": "Microsoft.ContainerRegistry/capacityReservations"
  }
]
```

Exit code: **0**

Result: **PASS**. Command completed successfully.

## 19. List reservations as table

Input:

```powershell
azlocal acr reservation list -g eric-reservations-dfaue --subscription 06f5e253-d825-4052-87ec-c4f12bc8f343 -o table
```

Actual Output:

```text
WARNING: Command group 'acr reservation' is in preview and under development. Reference and support levels: https://aka.ms/CLI_refstatus
NAME                      LOCATION       REQUEST RATE TIER    EGRESS TIER    INGRESS TIER    STATE
------------------------  -------------  -------------------  -------------  --------------  ---------
eric-cli-validation-1021  australiaeast  R1                   None           None            Succeeded
```

Exit code: **0**

Result: **PASS**. Command completed successfully.

## 20. List names as TSV

Input:

```powershell
azlocal acr reservation list -g eric-reservations-dfaue --subscription 06f5e253-d825-4052-87ec-c4f12bc8f343 --query '[].name' -o tsv
```

Actual Output:

```text
WARNING: Command group 'acr reservation' is in preview and under development. Reference and support levels: https://aka.ms/CLI_refstatus
eric-cli-validation-1021
```

Exit code: **0**

Result: **PASS**. Command completed successfully.

## 21. Show by name

Input:

```powershell
azlocal acr reservation show -n eric-cli-validation-1021 -g eric-reservations-dfaue --subscription 06f5e253-d825-4052-87ec-c4f12bc8f343 -o json
```

Actual Output:

```text
WARNING: Command group 'acr reservation' is in preview and under development. Reference and support levels: https://aka.ms/CLI_refstatus
{
  "id": "/subscriptions/06f5e253-d825-4052-87ec-c4f12bc8f343/resourceGroups/eric-reservations-dfaue/providers/Microsoft.ContainerRegistry/capacityReservations/eric-cli-validation-1021",
  "location": "australiaeast",
  "name": "eric-cli-validation-1021",
  "properties": {
    "createdAt": "2026-10-21T07:38:12.4074335+00:00",
    "earliestDeletableAt": "2026-10-21T07:43:12.4074335+00:00",
    "ingressTier": "None",
    "lastModifiedAt": "2026-10-21T07:39:51.037022+00:00",
    "provisioningState": "Succeeded",
    "requestRateTier": "R1",
    "reservedEgressGbps": 0.0,
    "reservedIngressGbps": 0.0,
    "reservedRequestRate": 1.0
  },
  "resourceGroup": "eric-reservations-dfaue",
  "tags": {
    "cliTest": "validation",
    "phase": "updated"
  },
  "type": "Microsoft.ContainerRegistry/capacityReservations"
}
```

Exit code: **0**

Result: **PASS**. Command completed successfully.

## 22. Show by resource ID

Input:

```powershell
azlocal acr reservation show --ids /subscriptions/06f5e253-d825-4052-87ec-c4f12bc8f343/resourceGroups/eric-reservations-dfaue/providers/Microsoft.ContainerRegistry/capacityReservations/eric-cli-validation-1021 --subscription 06f5e253-d825-4052-87ec-c4f12bc8f343 -o json
```

Actual Output:

```text
WARNING: option '--subscription' will be ignored due to use of '--ids'.
WARNING: Command group 'acr reservation' is in preview and under development. Reference and support levels: https://aka.ms/CLI_refstatus
{
  "id": "/subscriptions/06f5e253-d825-4052-87ec-c4f12bc8f343/resourceGroups/eric-reservations-dfaue/providers/Microsoft.ContainerRegistry/capacityReservations/eric-cli-validation-1021",
  "location": "australiaeast",
  "name": "eric-cli-validation-1021",
  "properties": {
    "createdAt": "2026-10-21T07:38:12.4074335+00:00",
    "earliestDeletableAt": "2026-10-21T07:43:12.4074335+00:00",
    "ingressTier": "None",
    "lastModifiedAt": "2026-10-21T07:39:51.037022+00:00",
    "provisioningState": "Succeeded",
    "requestRateTier": "R1",
    "reservedEgressGbps": 0.0,
    "reservedIngressGbps": 0.0,
    "reservedRequestRate": 1.0
  },
  "resourceGroup": "eric-reservations-dfaue",
  "tags": {
    "cliTest": "validation",
    "phase": "updated"
  },
  "type": "Microsoft.ContainerRegistry/capacityReservations"
}
```

Exit code: **0**

Result: **PASS**. R1 and zero ingress/egress retained; no internal stamp properties in JSON.

## 23. Show table

Input:

```powershell
azlocal acr reservation show --ids /subscriptions/06f5e253-d825-4052-87ec-c4f12bc8f343/resourceGroups/eric-reservations-dfaue/providers/Microsoft.ContainerRegistry/capacityReservations/eric-cli-validation-1021 --subscription 06f5e253-d825-4052-87ec-c4f12bc8f343 -o table
```

Actual Output:

```text
WARNING: option '--subscription' will be ignored due to use of '--ids'.
WARNING: Command group 'acr reservation' is in preview and under development. Reference and support levels: https://aka.ms/CLI_refstatus
NAME                      LOCATION       REQUEST RATE TIER    EGRESS TIER    INGRESS TIER    STATE
------------------------  -------------  -------------------  -------------  --------------  ---------
eric-cli-validation-1021  australiaeast  R1                   None           None            Succeeded
```

Exit code: **0**

Result: **PASS**. Command completed successfully.

## 24. Show YAML

Input:

```powershell
azlocal acr reservation show --ids /subscriptions/06f5e253-d825-4052-87ec-c4f12bc8f343/resourceGroups/eric-reservations-dfaue/providers/Microsoft.ContainerRegistry/capacityReservations/eric-cli-validation-1021 --subscription 06f5e253-d825-4052-87ec-c4f12bc8f343 -o yaml
```

Actual Output:

```text
WARNING: option '--subscription' will be ignored due to use of '--ids'.
WARNING: Command group 'acr reservation' is in preview and under development. Reference and support levels: https://aka.ms/CLI_refstatus
id: /subscriptions/06f5e253-d825-4052-87ec-c4f12bc8f343/resourceGroups/eric-reservations-dfaue/providers/Microsoft.ContainerRegistry/capacityReservations/eric-cli-validation-1021
location: australiaeast
name: eric-cli-validation-1021
properties:
  createdAt: '2026-10-21T07:38:12.4074335+00:00'
  earliestDeletableAt: '2026-10-21T07:43:12.4074335+00:00'
  ingressTier: None
  lastModifiedAt: '2026-10-21T07:39:51.037022+00:00'
  provisioningState: Succeeded
  requestRateTier: R1
  reservedEgressGbps: 0.0
  reservedIngressGbps: 0.0
  reservedRequestRate: 1.0
resourceGroup: eric-reservations-dfaue
tags:
  cliTest: validation
  phase: updated
type: Microsoft.ContainerRegistry/capacityReservations
```

Exit code: **0**

Result: **PASS**. Command completed successfully.

## 25. Query request-rate capacity

Input:

```powershell
azlocal acr reservation show --ids /subscriptions/06f5e253-d825-4052-87ec-c4f12bc8f343/resourceGroups/eric-reservations-dfaue/providers/Microsoft.ContainerRegistry/capacityReservations/eric-cli-validation-1021 --subscription 06f5e253-d825-4052-87ec-c4f12bc8f343 --query properties.reservedRequestRate -o tsv
```

Actual Output:

```text
WARNING: option '--subscription' will be ignored due to use of '--ids'.
WARNING: Command group 'acr reservation' is in preview and under development. Reference and support levels: https://aka.ms/CLI_refstatus
1.0
```

Exit code: **0**

Result: **PASS**. Command completed successfully.

## 26. Output none

Input:

```powershell
azlocal acr reservation show --ids /subscriptions/06f5e253-d825-4052-87ec-c4f12bc8f343/resourceGroups/eric-reservations-dfaue/providers/Microsoft.ContainerRegistry/capacityReservations/eric-cli-validation-1021 --subscription 06f5e253-d825-4052-87ec-c4f12bc8f343 -o none
```

Actual Output:

```text
WARNING: option '--subscription' will be ignored due to use of '--ids'.
WARNING: Command group 'acr reservation' is in preview and under development. Reference and support levels: https://aka.ms/CLI_refstatus
```

Exit code: **0**

Result: **PASS**. Stdout is empty; preview warnings remain visible on stderr.

## 27. Wait created by ID

Input:

```powershell
azlocal acr reservation wait --ids /subscriptions/06f5e253-d825-4052-87ec-c4f12bc8f343/resourceGroups/eric-reservations-dfaue/providers/Microsoft.ContainerRegistry/capacityReservations/eric-cli-validation-1021 --subscription 06f5e253-d825-4052-87ec-c4f12bc8f343 --created --interval 5 --timeout 30
```

Actual Output:

```text
WARNING: option '--subscription' will be ignored due to use of '--ids'.
WARNING: Command group 'acr reservation' is in preview and under development. Reference and support levels: https://aka.ms/CLI_refstatus
```

Exit code: **0**

Result: **PASS**. Command completed successfully.

## 28. Wait custom condition

Input:

```powershell
azlocal acr reservation wait --ids /subscriptions/06f5e253-d825-4052-87ec-c4f12bc8f343/resourceGroups/eric-reservations-dfaue/providers/Microsoft.ContainerRegistry/capacityReservations/eric-cli-validation-1021 --subscription 06f5e253-d825-4052-87ec-c4f12bc8f343 --custom 'properties.reservedRequestRate == `1`' --interval 5 --timeout 30
```

Actual Output:

```text
WARNING: option '--subscription' will be ignored due to use of '--ids'.
WARNING: Command group 'acr reservation' is in preview and under development. Reference and support levels: https://aka.ms/CLI_refstatus
```

Exit code: **0**

Result: **PASS**. Command completed successfully.

## 29. Read empty association list

Input:

```powershell
azlocal acr reservation list-registries --ids /subscriptions/06f5e253-d825-4052-87ec-c4f12bc8f343/resourceGroups/eric-reservations-dfaue/providers/Microsoft.ContainerRegistry/capacityReservations/eric-cli-validation-1021 --subscription 06f5e253-d825-4052-87ec-c4f12bc8f343 -o json
```

Actual Output:

```text
WARNING: option '--subscription' will be ignored due to use of '--ids'.
WARNING: Command group 'acr reservation' is in preview and under development. Reference and support levels: https://aka.ms/CLI_refstatus
[]
```

Exit code: **0**

Result: **PASS**. Command completed successfully.

## 30. Create without a positive tier

Input:

```powershell
azlocal acr reservation create -n eric-cli-invalid-1021 -g eric-reservations-dfaue --subscription 06f5e253-d825-4052-87ec-c4f12bc8f343 -l australiaeast --stamp-id dfaue-1
```

Actual Output:

```text
WARNING: Command group 'acr reservation' is in preview and under development. Reference and support levels: https://aka.ms/CLI_refstatus
ERROR: At least one reserved dimension must have a positive tier.
```

Exit code: **1**

Result: **PASS**. Expected rejection; no valid capacity increase requested.

## 31. Create with invalid short name

Input:

```powershell
azlocal acr reservation create -n ab -g eric-reservations-dfaue --subscription 06f5e253-d825-4052-87ec-c4f12bc8f343 -l australiaeast --stamp-id dfaue-1 --request-rate-tier R1
```

Actual Output:

```text
WARNING: Command group 'acr reservation' is in preview and under development. Reference and support levels: https://aka.ms/CLI_refstatus
ERROR: Reservation names must contain 3-63 letters, digits or hyphens and start with a letter or digit.
```

Exit code: **1**

Result: **PASS**. Expected rejection; no valid capacity increase requested.

## 32. Create with invalid tier

Input:

```powershell
azlocal acr reservation create -n eric-cli-invalid-1021 -g eric-reservations-dfaue --subscription 06f5e253-d825-4052-87ec-c4f12bc8f343 -l australiaeast --stamp-id dfaue-1 --request-rate-tier R3
```

Actual Output:

```text
ERROR: az acr reservation create: 'R3' is not a valid value for '--request-rate-tier'. Allowed values: R1, R2, R4, R8, R16, R32, R64.
Did you mean 'R32' ?

Examples from command's help:
az acr reservation create -n MyReservation -g MyResourceGroup -l australiaeast --stamp-id dfaue-1 --request-rate-tier R4 --egress-tier E4
Reserve request-rate and egress capacity.

az acr reservation create -n MyIngressReservation -g MyResourceGroup -l australiaeast --stamp-id dfaue-1 --ingress-tier I2 --no-wait
Reserve ingress capacity without waiting.

https://aka.ms/cli_ref
Read more about the command in reference docs
```

Exit code: **2**

Result: **PASS**. Expected rejection; no valid capacity increase requested.

## 33. Create with missing stamp

Input:

```powershell
azlocal acr reservation create -n eric-cli-invalid-1021 -g eric-reservations-dfaue --subscription 06f5e253-d825-4052-87ec-c4f12bc8f343 -l australiaeast --request-rate-tier R1
```

Actual Output:

```text
ERROR: the following arguments are required: --stamp-id

Examples from command's help:
az acr reservation create -n MyReservation -g MyResourceGroup -l australiaeast --stamp-id dfaue-1 --request-rate-tier R4 --egress-tier E4
Reserve request-rate and egress capacity.

az acr reservation create -n MyIngressReservation -g MyResourceGroup -l australiaeast --stamp-id dfaue-1 --ingress-tier I2 --no-wait
Reserve ingress capacity without waiting.

https://aka.ms/cli_ref
Read more about the command in reference docs
```

Exit code: **2**

Result: **PASS**. Expected rejection; no valid capacity increase requested.

## 34. Create with blank stamp

Input:

```powershell
azlocal acr reservation create -n eric-cli-invalid-1021 -g eric-reservations-dfaue --subscription 06f5e253-d825-4052-87ec-c4f12bc8f343 -l australiaeast --stamp-id ' ' --request-rate-tier R1
```

Actual Output:

```text
WARNING: Command group 'acr reservation' is in preview and under development. Reference and support levels: https://aka.ms/CLI_refstatus
ERROR: --stamp-id must not be empty.
```

Exit code: **1**

Result: **PASS**. Expected rejection; no valid capacity increase requested.

## 35. Create with zero timeout

Input:

```powershell
azlocal acr reservation create -n eric-cli-invalid-1021 -g eric-reservations-dfaue --subscription 06f5e253-d825-4052-87ec-c4f12bc8f343 -l australiaeast --stamp-id dfaue-1 --request-rate-tier R1 --timeout 0
```

Actual Output:

```text
WARNING: Command group 'acr reservation' is in preview and under development. Reference and support levels: https://aka.ms/CLI_refstatus
ERROR: --timeout must be greater than zero.
```

Exit code: **1**

Result: **PASS**. Expected rejection; no valid capacity increase requested.

## 36. Create with negative timeout

Input:

```powershell
azlocal acr reservation create -n eric-cli-invalid-1021 -g eric-reservations-dfaue --subscription 06f5e253-d825-4052-87ec-c4f12bc8f343 -l australiaeast --stamp-id dfaue-1 --request-rate-tier R1 --timeout -1
```

Actual Output:

```text
WARNING: Command group 'acr reservation' is in preview and under development. Reference and support levels: https://aka.ms/CLI_refstatus
ERROR: --timeout must be greater than zero.
```

Exit code: **1**

Result: **PASS**. Expected rejection; no valid capacity increase requested.

## 37. Create with None tier

Input:

```powershell
azlocal acr reservation create -n eric-cli-invalid-1021 -g eric-reservations-dfaue --subscription 06f5e253-d825-4052-87ec-c4f12bc8f343 -l australiaeast --stamp-id dfaue-1 --request-rate-tier None
```

Actual Output:

```text
ERROR: az acr reservation create: 'None' is not a valid value for '--request-rate-tier'. Allowed values: R1, R2, R4, R8, R16, R32, R64.

Examples from command's help:
az acr reservation create -n MyReservation -g MyResourceGroup -l australiaeast --stamp-id dfaue-1 --request-rate-tier R4 --egress-tier E4
Reserve request-rate and egress capacity.

az acr reservation create -n MyIngressReservation -g MyResourceGroup -l australiaeast --stamp-id dfaue-1 --ingress-tier I2 --no-wait
Reserve ingress capacity without waiting.

https://aka.ms/cli_ref
Read more about the command in reference docs
```

Exit code: **2**

Result: **PASS**. Expected rejection; no valid capacity increase requested.

## 38. Legacy label rejected by CLI

Input:

```powershell
azlocal acr reservation create -n eric-cli-invalid-1021 -g eric-reservations-dfaue --subscription 06f5e253-d825-4052-87ec-c4f12bc8f343 -l australiaeast --stamp-id dfaue-1 --request-rate-tier RequestRate-L
```

Actual Output:

```text
ERROR: az acr reservation create: 'RequestRate-L' is not a valid value for '--request-rate-tier'. Allowed values: R1, R2, R4, R8, R16, R32, R64.

Examples from command's help:
az acr reservation create -n MyReservation -g MyResourceGroup -l australiaeast --stamp-id dfaue-1 --request-rate-tier R4 --egress-tier E4
Reserve request-rate and egress capacity.

az acr reservation create -n MyIngressReservation -g MyResourceGroup -l australiaeast --stamp-id dfaue-1 --ingress-tier I2 --no-wait
Reserve ingress capacity without waiting.

https://aka.ms/cli_ref
Read more about the command in reference docs
```

Exit code: **2**

Result: **PASS**. Expected rejection; no valid capacity increase requested.

## 39. Update without changes

Input:

```powershell
azlocal acr reservation update --ids /subscriptions/06f5e253-d825-4052-87ec-c4f12bc8f343/resourceGroups/eric-reservations-dfaue/providers/Microsoft.ContainerRegistry/capacityReservations/eric-cli-validation-1021 --subscription 06f5e253-d825-4052-87ec-c4f12bc8f343
```

Actual Output:

```text
WARNING: option '--subscription' will be ignored due to use of '--ids'.
WARNING: Command group 'acr reservation' is in preview and under development. Reference and support levels: https://aka.ms/CLI_refstatus
ERROR: Specify a tier or --tags to update.
```

Exit code: **1**

Result: **PASS**. Expected rejection; no valid capacity increase requested.

## 40. Reject removing last positive dimension

Input:

```powershell
azlocal acr reservation update --ids /subscriptions/06f5e253-d825-4052-87ec-c4f12bc8f343/resourceGroups/eric-reservations-dfaue/providers/Microsoft.ContainerRegistry/capacityReservations/eric-cli-validation-1021 --subscription 06f5e253-d825-4052-87ec-c4f12bc8f343 --request-rate-tier None
```

Actual Output:

```text
WARNING: option '--subscription' will be ignored due to use of '--ids'.
WARNING: Command group 'acr reservation' is in preview and under development. Reference and support levels: https://aka.ms/CLI_refstatus
ERROR: At least one reserved dimension must have a positive tier.
```

Exit code: **1**

Result: **PASS**. Expected rejection; no valid capacity increase requested.

## 41. Reject raw numeric capacity

Input:

```powershell
azlocal acr reservation update --ids /subscriptions/06f5e253-d825-4052-87ec-c4f12bc8f343/resourceGroups/eric-reservations-dfaue/providers/Microsoft.ContainerRegistry/capacityReservations/eric-cli-validation-1021 --subscription 06f5e253-d825-4052-87ec-c4f12bc8f343 --request-rate-rus 100
```

Actual Output:

```text
ERROR: unrecognized arguments: --request-rate-rus 100

https://aka.ms/cli_ref
Read more about the command in reference docs
```

Exit code: **2**

Result: **PASS**. Expected rejection; no valid capacity increase requested.

## 42. Reject generic set bypass

Input:

```powershell
azlocal acr reservation update --ids /subscriptions/06f5e253-d825-4052-87ec-c4f12bc8f343/resourceGroups/eric-reservations-dfaue/providers/Microsoft.ContainerRegistry/capacityReservations/eric-cli-validation-1021 --subscription 06f5e253-d825-4052-87ec-c4f12bc8f343 --set properties.requestRateRus=100
```

Actual Output:

```text
ERROR: unrecognized arguments: --set properties.requestRateRus=100

https://aka.ms/cli_ref
Read more about the command in reference docs
```

Exit code: **2**

Result: **PASS**. Expected rejection; no valid capacity increase requested.

## 43. Reject reservation on registry update

Input:

```powershell
azlocal acr update -n ericreservationdfaue -g eric-reservations-dfaue --subscription 06f5e253-d825-4052-87ec-c4f12bc8f343 --reservation eric-cli-validation-1021
```

Actual Output:

```text
ERROR: unrecognized arguments: --reservation eric-cli-validation-1021

https://aka.ms/cli_ref
Read more about the command in reference docs
```

Exit code: **2**

Result: **PASS**. Expected rejection; no valid capacity increase requested.

## 44. Show nonexistent reservation

Input:

```powershell
azlocal acr reservation show -n eric-cli-missing-1021 -g eric-reservations-dfaue --subscription 06f5e253-d825-4052-87ec-c4f12bc8f343 -o json
```

Actual Output:

```text
WARNING: Command group 'acr reservation' is in preview and under development. Reference and support levels: https://aka.ms/CLI_refstatus
ERROR: Capacity reservation request failed (HTTP 404): The Resource 'Microsoft.ContainerRegistry/capacityReservations/eric-cli-missing-1021' under resource group 'eric-reservations-dfaue' was not found. For more details please go to https://aka.ms/ARMResourceNotFoundFix
```

Exit code: **3**

Result: **PASS**. Expected rejection; no valid capacity increase requested.

## 45. Update nonexistent reservation

Input:

```powershell
azlocal acr reservation update -n eric-cli-missing-1021 -g eric-reservations-dfaue --subscription 06f5e253-d825-4052-87ec-c4f12bc8f343 --tags cliTest=missing
```

Actual Output:

```text
WARNING: Command group 'acr reservation' is in preview and under development. Reference and support levels: https://aka.ms/CLI_refstatus
ERROR: Capacity reservation request failed (HTTP 404): The Resource 'Microsoft.ContainerRegistry/capacityReservations/eric-cli-missing-1021' under resource group 'eric-reservations-dfaue' was not found. For more details please go to https://aka.ms/ARMResourceNotFoundFix
```

Exit code: **3**

Result: **PASS**. Expected rejection; no valid capacity increase requested.

## 46. Capacity unchanged after negative tests

Input:

```powershell
azlocal acr reservation show --ids /subscriptions/06f5e253-d825-4052-87ec-c4f12bc8f343/resourceGroups/eric-reservations-dfaue/providers/Microsoft.ContainerRegistry/capacityReservations/eric-cli-validation-1021 --subscription 06f5e253-d825-4052-87ec-c4f12bc8f343 -o json
```

Actual Output:

```text
WARNING: option '--subscription' will be ignored due to use of '--ids'.
WARNING: Command group 'acr reservation' is in preview and under development. Reference and support levels: https://aka.ms/CLI_refstatus
{
  "id": "/subscriptions/06f5e253-d825-4052-87ec-c4f12bc8f343/resourceGroups/eric-reservations-dfaue/providers/Microsoft.ContainerRegistry/capacityReservations/eric-cli-validation-1021",
  "location": "australiaeast",
  "name": "eric-cli-validation-1021",
  "properties": {
    "createdAt": "2026-10-21T07:38:12.4074335+00:00",
    "earliestDeletableAt": "2026-10-21T07:43:12.4074335+00:00",
    "ingressTier": "None",
    "lastModifiedAt": "2026-10-21T07:39:51.037022+00:00",
    "provisioningState": "Succeeded",
    "requestRateTier": "R1",
    "reservedEgressGbps": 0.0,
    "reservedIngressGbps": 0.0,
    "reservedRequestRate": 1.0
  },
  "resourceGroup": "eric-reservations-dfaue",
  "tags": {
    "cliTest": "validation",
    "phase": "updated"
  },
  "type": "Microsoft.ContainerRegistry/capacityReservations"
}
```

Exit code: **0**

Result: **PASS**. R1 and zero ingress/egress retained; no internal stamp properties in JSON.

## 47. Wait deleted for nonexistent reservation

Input:

```powershell
azlocal acr reservation wait -n eric-cli-missing-1021 -g eric-reservations-dfaue --subscription 06f5e253-d825-4052-87ec-c4f12bc8f343 --deleted --interval 5 --timeout 30
```

Actual Output:

```text
WARNING: Command group 'acr reservation' is in preview and under development. Reference and support levels: https://aka.ms/CLI_refstatus
```

Exit code: **0**

Result: **PASS**. Command completed successfully.

## 48. Registry create preflight: missing reservation

Input:

```powershell
azlocal acr create -n ericclipreflight1021 -g eric-reservations-dfaue --subscription 06f5e253-d825-4052-87ec-c4f12bc8f343 -l australiaeast --sku Premium --reservation eric-cli-missing-1021
```

Actual Output:

```text
WARNING: Argument '--reservation' is in preview and under development. Reference and support levels: https://aka.ms/CLI_refstatus
ERROR: Capacity reservation request failed (HTTP 404): The Resource 'Microsoft.ContainerRegistry/capacityReservations/eric-cli-missing-1021' under resource group 'eric-reservations-dfaue' was not found. For more details please go to https://aka.ms/ARMResourceNotFoundFix
```

Exit code: **3**

Result: **PASS**. Rejected before registry creation.

## 49. Registry create preflight: region mismatch

Input:

```powershell
azlocal acr create -n ericclipreflight1021 -g eric-reservations-dfaue --subscription 06f5e253-d825-4052-87ec-c4f12bc8f343 -l eastus --sku Premium --reservation eric-cli-validation-1021
```

Actual Output:

```text
WARNING: Argument '--reservation' is in preview and under development. Reference and support levels: https://aka.ms/CLI_refstatus
ERROR: The registry and capacity reservation must be in the same region.
```

Exit code: **1**

Result: **PASS**. Rejected before registry creation.

## 50. Registry preflight did not create a registry

Input:

```powershell
azlocal acr list -g eric-reservations-dfaue --subscription 06f5e253-d825-4052-87ec-c4f12bc8f343 --query '[].name' -o json
```

Actual Output:

```text
[
  "ericreservationdfaue"
]
```

Exit code: **0**

Result: **PASS**. Command completed successfully.

## 51. Tags-only update by ID

Input:

```powershell
azlocal acr reservation update --ids /subscriptions/06f5e253-d825-4052-87ec-c4f12bc8f343/resourceGroups/eric-reservations-dfaue/providers/Microsoft.ContainerRegistry/capacityReservations/eric-cli-validation-1021 --subscription 06f5e253-d825-4052-87ec-c4f12bc8f343 --tags cliTest=full-validation phase=tags --timeout 120 -o json
```

Actual Output:

```text
WARNING: option '--subscription' will be ignored due to use of '--ids'.
WARNING: Command group 'acr reservation' is in preview and under development. Reference and support levels: https://aka.ms/CLI_refstatus
{
  "id": "/subscriptions/06f5e253-d825-4052-87ec-c4f12bc8f343/resourceGroups/eric-reservations-dfaue/providers/Microsoft.ContainerRegistry/capacityReservations/eric-cli-validation-1021",
  "location": "australiaeast",
  "name": "eric-cli-validation-1021",
  "properties": {
    "createdAt": "2026-10-21T07:38:12.4074335+00:00",
    "earliestDeletableAt": "2026-10-21T07:43:12.4074335+00:00",
    "ingressTier": "None",
    "lastModifiedAt": "2026-10-21T07:54:22.0334708+00:00",
    "provisioningState": "Succeeded",
    "requestRateTier": "R1",
    "reservedEgressGbps": 0.0,
    "reservedIngressGbps": 0.0,
    "reservedRequestRate": 1.0
  },
  "resourceGroup": "eric-reservations-dfaue",
  "tags": {
    "cliTest": "full-validation",
    "phase": "tags"
  },
  "type": "Microsoft.ContainerRegistry/capacityReservations"
}
```

Exit code: **0**

Result: **PASS**. Command completed successfully.

## 52. Tags update retained numeric dimensions

Input:

```powershell
azlocal acr reservation show --ids /subscriptions/06f5e253-d825-4052-87ec-c4f12bc8f343/resourceGroups/eric-reservations-dfaue/providers/Microsoft.ContainerRegistry/capacityReservations/eric-cli-validation-1021 --subscription 06f5e253-d825-4052-87ec-c4f12bc8f343 -o json
```

Actual Output:

```text
WARNING: option '--subscription' will be ignored due to use of '--ids'.
WARNING: Command group 'acr reservation' is in preview and under development. Reference and support levels: https://aka.ms/CLI_refstatus
{
  "id": "/subscriptions/06f5e253-d825-4052-87ec-c4f12bc8f343/resourceGroups/eric-reservations-dfaue/providers/Microsoft.ContainerRegistry/capacityReservations/eric-cli-validation-1021",
  "location": "australiaeast",
  "name": "eric-cli-validation-1021",
  "properties": {
    "createdAt": "2026-10-21T07:38:12.4074335+00:00",
    "earliestDeletableAt": "2026-10-21T07:43:12.4074335+00:00",
    "ingressTier": "None",
    "lastModifiedAt": "2026-10-21T07:54:22.0334708+00:00",
    "provisioningState": "Succeeded",
    "requestRateTier": "R1",
    "reservedEgressGbps": 0.0,
    "reservedIngressGbps": 0.0,
    "reservedRequestRate": 1.0
  },
  "resourceGroup": "eric-reservations-dfaue",
  "tags": {
    "cliTest": "full-validation",
    "phase": "tags"
  },
  "type": "Microsoft.ContainerRegistry/capacityReservations"
}
```

Exit code: **0**

Result: **PASS**. R1 and zero ingress/egress retained; no internal stamp properties in JSON.

## 53. Clear tags

Input:

```powershell
azlocal acr reservation update --ids /subscriptions/06f5e253-d825-4052-87ec-c4f12bc8f343/resourceGroups/eric-reservations-dfaue/providers/Microsoft.ContainerRegistry/capacityReservations/eric-cli-validation-1021 --subscription 06f5e253-d825-4052-87ec-c4f12bc8f343 --tags '' --timeout 120 -o json
```

Actual Output:

```text
WARNING: option '--subscription' will be ignored due to use of '--ids'.
WARNING: Command group 'acr reservation' is in preview and under development. Reference and support levels: https://aka.ms/CLI_refstatus
{
  "id": "/subscriptions/06f5e253-d825-4052-87ec-c4f12bc8f343/resourceGroups/eric-reservations-dfaue/providers/Microsoft.ContainerRegistry/capacityReservations/eric-cli-validation-1021",
  "location": "australiaeast",
  "name": "eric-cli-validation-1021",
  "properties": {
    "createdAt": "2026-10-21T07:38:12.4074335+00:00",
    "earliestDeletableAt": "2026-10-21T07:43:12.4074335+00:00",
    "ingressTier": "None",
    "lastModifiedAt": "2026-10-21T07:54:30.5952809+00:00",
    "provisioningState": "Succeeded",
    "requestRateTier": "R1",
    "reservedEgressGbps": 0.0,
    "reservedIngressGbps": 0.0,
    "reservedRequestRate": 1.0
  },
  "resourceGroup": "eric-reservations-dfaue",
  "tags": {},
  "type": "Microsoft.ContainerRegistry/capacityReservations"
}
```

Exit code: **0**

Result: **PASS**. Command completed successfully.

## 54. Case-insensitive R1 update without increasing capacity

Input:

```powershell
azlocal acr reservation update --ids /subscriptions/06f5e253-d825-4052-87ec-c4f12bc8f343/resourceGroups/eric-reservations-dfaue/providers/Microsoft.ContainerRegistry/capacityReservations/eric-cli-validation-1021 --subscription 06f5e253-d825-4052-87ec-c4f12bc8f343 --request-rate-tier r1 --timeout 120 -o json
```

Actual Output:

```text
WARNING: option '--subscription' will be ignored due to use of '--ids'.
WARNING: Command group 'acr reservation' is in preview and under development. Reference and support levels: https://aka.ms/CLI_refstatus
{
  "id": "/subscriptions/06f5e253-d825-4052-87ec-c4f12bc8f343/resourceGroups/eric-reservations-dfaue/providers/Microsoft.ContainerRegistry/capacityReservations/eric-cli-validation-1021",
  "location": "australiaeast",
  "name": "eric-cli-validation-1021",
  "properties": {
    "createdAt": "2026-10-21T07:38:12.4074335+00:00",
    "earliestDeletableAt": "2026-10-21T07:43:12.4074335+00:00",
    "ingressTier": "None",
    "lastModifiedAt": "2026-10-21T07:54:30.5952809+00:00",
    "provisioningState": "Succeeded",
    "requestRateTier": "R1",
    "reservedEgressGbps": 0.0,
    "reservedIngressGbps": 0.0,
    "reservedRequestRate": 1.0
  },
  "resourceGroup": "eric-reservations-dfaue",
  "tags": {},
  "type": "Microsoft.ContainerRegistry/capacityReservations"
}
```

Exit code: **0**

Result: **PASS**. Command completed successfully.

## 55. Add I1 using case-insensitive tier

Input:

```powershell
azlocal acr reservation update --ids /subscriptions/06f5e253-d825-4052-87ec-c4f12bc8f343/resourceGroups/eric-reservations-dfaue/providers/Microsoft.ContainerRegistry/capacityReservations/eric-cli-validation-1021 --subscription 06f5e253-d825-4052-87ec-c4f12bc8f343 --ingress-tier i1 --timeout 120 -o json
```

Actual Output:

```text
WARNING: option '--subscription' will be ignored due to use of '--ids'.
WARNING: Command group 'acr reservation' is in preview and under development. Reference and support levels: https://aka.ms/CLI_refstatus
{
  "id": "/subscriptions/06f5e253-d825-4052-87ec-c4f12bc8f343/resourceGroups/eric-reservations-dfaue/providers/Microsoft.ContainerRegistry/capacityReservations/eric-cli-validation-1021",
  "location": "australiaeast",
  "name": "eric-cli-validation-1021",
  "properties": {
    "createdAt": "2026-10-21T07:38:12.4074335+00:00",
    "earliestDeletableAt": "2026-10-21T07:43:12.4074335+00:00",
    "ingressTier": "I1",
    "lastModifiedAt": "2026-10-21T07:54:39.6555728+00:00",
    "provisioningState": "Succeeded",
    "requestRateTier": "R1",
    "reservedEgressGbps": 0.0,
    "reservedIngressGbps": 0.5,
    "reservedRequestRate": 1.0
  },
  "resourceGroup": "eric-reservations-dfaue",
  "tags": {},
  "type": "Microsoft.ContainerRegistry/capacityReservations"
}
```

Exit code: **0**

Result: **PASS**. Adds 0.5 Gbps ingress within the existing registry pool; request rate remains 1 RU.

## 56. Verify ingress update persisted

Input:

```powershell
azlocal acr reservation show --ids /subscriptions/06f5e253-d825-4052-87ec-c4f12bc8f343/resourceGroups/eric-reservations-dfaue/providers/Microsoft.ContainerRegistry/capacityReservations/eric-cli-validation-1021 --subscription 06f5e253-d825-4052-87ec-c4f12bc8f343 -o json
```

Actual Output:

```text
WARNING: option '--subscription' will be ignored due to use of '--ids'.
WARNING: Command group 'acr reservation' is in preview and under development. Reference and support levels: https://aka.ms/CLI_refstatus
{
  "id": "/subscriptions/06f5e253-d825-4052-87ec-c4f12bc8f343/resourceGroups/eric-reservations-dfaue/providers/Microsoft.ContainerRegistry/capacityReservations/eric-cli-validation-1021",
  "location": "australiaeast",
  "name": "eric-cli-validation-1021",
  "properties": {
    "createdAt": "2026-10-21T07:38:12.4074335+00:00",
    "earliestDeletableAt": "2026-10-21T07:43:12.4074335+00:00",
    "ingressTier": "I1",
    "lastModifiedAt": "2026-10-21T07:54:39.6555728+00:00",
    "provisioningState": "Succeeded",
    "requestRateTier": "R1",
    "reservedEgressGbps": 0.0,
    "reservedIngressGbps": 0.5,
    "reservedRequestRate": 1.0
  },
  "resourceGroup": "eric-reservations-dfaue",
  "tags": {},
  "type": "Microsoft.ContainerRegistry/capacityReservations"
}
```

Exit code: **0**

Result: **PASS**. Command completed successfully.

## 57. Remove ingress with no-wait

Input:

```powershell
azlocal acr reservation update --ids /subscriptions/06f5e253-d825-4052-87ec-c4f12bc8f343/resourceGroups/eric-reservations-dfaue/providers/Microsoft.ContainerRegistry/capacityReservations/eric-cli-validation-1021 --subscription 06f5e253-d825-4052-87ec-c4f12bc8f343 --ingress-tier None --no-wait -o json
```

Actual Output:

```text
WARNING: option '--subscription' will be ignored due to use of '--ids'.
WARNING: Command group 'acr reservation' is in preview and under development. Reference and support levels: https://aka.ms/CLI_refstatus
```

Exit code: **0**

Result: **PASS**. No-wait return validated; completion checked separately.

## 58. Wait updated after no-wait

Input:

```powershell
azlocal acr reservation wait --ids /subscriptions/06f5e253-d825-4052-87ec-c4f12bc8f343/resourceGroups/eric-reservations-dfaue/providers/Microsoft.ContainerRegistry/capacityReservations/eric-cli-validation-1021 --subscription 06f5e253-d825-4052-87ec-c4f12bc8f343 --updated --interval 5 --timeout 120
```

Actual Output:

```text
WARNING: option '--subscription' will be ignored due to use of '--ids'.
WARNING: Command group 'acr reservation' is in preview and under development. Reference and support levels: https://aka.ms/CLI_refstatus
```

Exit code: **0**

Result: **PASS**. Command completed successfully.

## 59. Verify None removal persisted

Input:

```powershell
azlocal acr reservation show --ids /subscriptions/06f5e253-d825-4052-87ec-c4f12bc8f343/resourceGroups/eric-reservations-dfaue/providers/Microsoft.ContainerRegistry/capacityReservations/eric-cli-validation-1021 --subscription 06f5e253-d825-4052-87ec-c4f12bc8f343 -o json
```

Actual Output:

```text
WARNING: option '--subscription' will be ignored due to use of '--ids'.
WARNING: Command group 'acr reservation' is in preview and under development. Reference and support levels: https://aka.ms/CLI_refstatus
{
  "id": "/subscriptions/06f5e253-d825-4052-87ec-c4f12bc8f343/resourceGroups/eric-reservations-dfaue/providers/Microsoft.ContainerRegistry/capacityReservations/eric-cli-validation-1021",
  "location": "australiaeast",
  "name": "eric-cli-validation-1021",
  "properties": {
    "createdAt": "2026-10-21T07:38:12.4074335+00:00",
    "earliestDeletableAt": "2026-10-21T07:43:12.4074335+00:00",
    "ingressTier": "None",
    "lastModifiedAt": "2026-10-21T07:54:47.1952604+00:00",
    "provisioningState": "Succeeded",
    "requestRateTier": "R1",
    "reservedEgressGbps": 0.0,
    "reservedIngressGbps": 0.0,
    "reservedRequestRate": 1.0
  },
  "resourceGroup": "eric-reservations-dfaue",
  "tags": {},
  "type": "Microsoft.ContainerRegistry/capacityReservations"
}
```

Exit code: **0**

Result: **PASS**. R1 and zero ingress/egress retained; no internal stamp properties in JSON.

## 60. Explicitly remove already-zero egress

Input:

```powershell
azlocal acr reservation update --ids /subscriptions/06f5e253-d825-4052-87ec-c4f12bc8f343/resourceGroups/eric-reservations-dfaue/providers/Microsoft.ContainerRegistry/capacityReservations/eric-cli-validation-1021 --subscription 06f5e253-d825-4052-87ec-c4f12bc8f343 --egress-tier None --timeout 120 -o json
```

Actual Output:

```text
WARNING: option '--subscription' will be ignored due to use of '--ids'.
WARNING: Command group 'acr reservation' is in preview and under development. Reference and support levels: https://aka.ms/CLI_refstatus
{
  "id": "/subscriptions/06f5e253-d825-4052-87ec-c4f12bc8f343/resourceGroups/eric-reservations-dfaue/providers/Microsoft.ContainerRegistry/capacityReservations/eric-cli-validation-1021",
  "location": "australiaeast",
  "name": "eric-cli-validation-1021",
  "properties": {
    "createdAt": "2026-10-21T07:38:12.4074335+00:00",
    "earliestDeletableAt": "2026-10-21T07:43:12.4074335+00:00",
    "ingressTier": "None",
    "lastModifiedAt": "2026-10-21T07:54:47.1952604+00:00",
    "provisioningState": "Succeeded",
    "requestRateTier": "R1",
    "reservedEgressGbps": 0.0,
    "reservedIngressGbps": 0.0,
    "reservedRequestRate": 1.0
  },
  "resourceGroup": "eric-reservations-dfaue",
  "tags": {},
  "type": "Microsoft.ContainerRegistry/capacityReservations"
}
```

Exit code: **0**

Result: **PASS**. Command completed successfully.

## 61. Associate existing test registry using R1

Input:

```powershell
azlocal acr reservation associate -n eric-cli-validation-1021 -g eric-reservations-dfaue --subscription 06f5e253-d825-4052-87ec-c4f12bc8f343 --registry-name ericreservationdfaue --timeout 120 -o json
```

Actual Output:

```text
WARNING: Command group 'acr reservation' is in preview and under development. Reference and support levels: https://aka.ms/CLI_refstatus
ERROR: Capacity reservation request failed (HTTP 409): Assignment requires reservation properties.requestRateTier 'RequestRate-L'. Create or update the reservation with the supported POC tier, then retry assignment.
```

Exit code: **1**

Result: **BLOCKED**. The deployed RP requires RequestRate-L, while the CLI accepts R1-R64. No REST bypass used.

Disassociation of an established association and successful registry creation with `--reservation` remain **BLOCKED** by the tier mismatch. An unassociated-registry disassociate call is not counted as a substitute.

## 62. Association list after compatibility check

Input:

```powershell
azlocal acr reservation list-registries --ids /subscriptions/06f5e253-d825-4052-87ec-c4f12bc8f343/resourceGroups/eric-reservations-dfaue/providers/Microsoft.ContainerRegistry/capacityReservations/eric-cli-validation-1021 --subscription 06f5e253-d825-4052-87ec-c4f12bc8f343 -o json
```

Actual Output:

```text
WARNING: option '--subscription' will be ignored due to use of '--ids'.
WARNING: Command group 'acr reservation' is in preview and under development. Reference and support levels: https://aka.ms/CLI_refstatus
[]
```

Exit code: **0**

Result: **PASS**. Command completed successfully.

## 63. Registry remains unassociated

Input:

```powershell
azlocal acr show -n ericreservationdfaue -g eric-reservations-dfaue --subscription 06f5e253-d825-4052-87ec-c4f12bc8f343 -o json
```

Actual Output:

```text
{
  "adminUserEnabled": false,
  "anonymousPullEnabled": false,
  "autoGeneratedDomainNameLabelScope": "Unsecure",
  "creationDate": "2026-10-21T06:56:40.717943+00:00",
  "dataEndpointEnabled": false,
  "dataEndpointHostNames": [],
  "encryption": {
    "keyVaultProperties": null,
    "status": "disabled"
  },
  "endpointProtocol": "IPv4",
  "id": "/subscriptions/06f5e253-d825-4052-87ec-c4f12bc8f343/resourceGroups/eric-reservations-dfaue/providers/Microsoft.ContainerRegistry/registries/ericreservationdfaue",
  "identity": null,
  "location": "australiaeast",
  "loginServer": "ericreservationdfaue.azurecr-test.io",
  "metadataSearch": "Disabled",
  "name": "ericreservationdfaue",
  "networkRuleBypassAllowedForTasks": false,
  "networkRuleBypassOptions": "AzureServices",
  "networkRuleSet": {
    "defaultAction": "Allow",
    "ipRules": [],
    "virtualNetworkRules": []
  },
  "policies": {
    "azureAdAuthenticationAsArmPolicy": {
      "status": "enabled"
    },
    "exportPolicy": {
      "status": "enabled"
    },
    "quarantinePolicy": {
      "status": "disabled"
    },
    "retentionPolicy": {
      "days": 7,
      "lastUpdatedTime": "2026-10-21T06:56:49.523095+00:00",
      "status": "disabled"
    },
    "softDeletePolicy": {
      "lastUpdatedTime": "2026-10-21T06:56:49.523376+00:00",
      "retentionDays": 7,
      "status": "disabled"
    },
    "trustPolicy": {
      "status": "disabled",
      "type": "Notary"
    }
  },
  "privateEndpointConnections": [],
  "provisioningState": "Succeeded",
  "publicNetworkAccess": "Enabled",
  "regionalEndpointHostNames": [],
  "regionalEndpoints": "Disabled",
  "reservation": null,
  "resourceGroup": "eric-reservations-dfaue",
  "roleAssignmentMode": "LegacyRegistryPermissions",
  "sku": {
    "name": "Premium",
    "tier": "Premium"
  },
  "status": null,
  "systemData": {
    "createdAt": "2026-10-21T06:56:40.717943+00:00",
    "createdBy": "ericdu@acrbami202608.ccsctp.net",
    "createdByType": "User",
    "lastModifiedAt": "2026-10-21T06:56:40.717943+00:00",
    "lastModifiedBy": "ericdu@acrbami202608.ccsctp.net",
    "lastModifiedByType": "User"
  },
  "tags": {
    "cliTest": "reservation-lifecycle"
  },
  "type": "Microsoft.ContainerRegistry/registries",
  "writableCacheRepos": "Disabled",
  "zoneRedundancy": "Disabled"
}
```

Exit code: **0**

Result: **PASS**. Command completed successfully.

## 64. Subscription-scoped list

Input:

```powershell
azlocal acr reservation list --subscription 06f5e253-d825-4052-87ec-c4f12bc8f343 -o json
```

Actual Output:

```text
WARNING: Command group 'acr reservation' is in preview and under development. Reference and support levels: https://aka.ms/CLI_refstatus
ERROR: Capacity reservation request failed (HTTP 502): Resource provider 'Microsoft.ContainerRegistry' failed to return collection response for type 'capacityReservations'.
```

Exit code: **1**

Result: **BLOCKED**. Service/ARM collection failure; CLI reports error instead of partial success.

## 65. First lifecycle: read before cleanup

Input:

```powershell
azlocal acr reservation show --ids /subscriptions/06f5e253-d825-4052-87ec-c4f12bc8f343/resourceGroups/eric-reservations-dfaue/providers/Microsoft.ContainerRegistry/capacityReservations/eric-cli-validation-1021 --subscription 06f5e253-d825-4052-87ec-c4f12bc8f343 -o json
```

Actual Output:

```text
WARNING: option '--subscription' will be ignored due to use of '--ids'.
WARNING: Command group 'acr reservation' is in preview and under development. Reference and support levels: https://aka.ms/CLI_refstatus
{
  "id": "/subscriptions/06f5e253-d825-4052-87ec-c4f12bc8f343/resourceGroups/eric-reservations-dfaue/providers/Microsoft.ContainerRegistry/capacityReservations/eric-cli-validation-1021",
  "location": "australiaeast",
  "name": "eric-cli-validation-1021",
  "properties": {
    "createdAt": "2026-10-21T07:38:12.4074335+00:00",
    "earliestDeletableAt": "2026-10-21T07:43:12.4074335+00:00",
    "ingressTier": "None",
    "lastModifiedAt": "2026-10-21T07:54:47.1952604+00:00",
    "provisioningState": "Succeeded",
    "requestRateTier": "R1",
    "reservedEgressGbps": 0.0,
    "reservedIngressGbps": 0.0,
    "reservedRequestRate": 1.0
  },
  "resourceGroup": "eric-reservations-dfaue",
  "tags": {},
  "type": "Microsoft.ContainerRegistry/capacityReservations"
}
```

Exit code: **0**

Result: **PASS**. R1 and zero ingress/egress retained; no internal stamp properties in JSON.

## 66. First lifecycle: require no registry associations

Input:

```powershell
azlocal acr reservation list-registries -n eric-cli-validation-1021 -g eric-reservations-dfaue --subscription 06f5e253-d825-4052-87ec-c4f12bc8f343 -o json
```

Actual Output:

```text
WARNING: Command group 'acr reservation' is in preview and under development. Reference and support levels: https://aka.ms/CLI_refstatus
[]
```

Exit code: **0**

Result: **PASS**. Command completed successfully.

## 67. First lifecycle: delete by resource ID

Input:

```powershell
azlocal acr reservation delete --ids /subscriptions/06f5e253-d825-4052-87ec-c4f12bc8f343/resourceGroups/eric-reservations-dfaue/providers/Microsoft.ContainerRegistry/capacityReservations/eric-cli-validation-1021 --subscription 06f5e253-d825-4052-87ec-c4f12bc8f343 --yes --no-wait
```

Actual Output:

```text
WARNING: option '--subscription' will be ignored due to use of '--ids'.
WARNING: Command group 'acr reservation' is in preview and under development. Reference and support levels: https://aka.ms/CLI_refstatus
```

Exit code: **0**

Result: **PASS**. Deletion accepted; --no-wait does not itself confirm completion.

## 68. First lifecycle: wait for deletion

Input:

```powershell
azlocal acr reservation wait --ids /subscriptions/06f5e253-d825-4052-87ec-c4f12bc8f343/resourceGroups/eric-reservations-dfaue/providers/Microsoft.ContainerRegistry/capacityReservations/eric-cli-validation-1021 --subscription 06f5e253-d825-4052-87ec-c4f12bc8f343 --deleted --interval 5 --timeout 120
```

Actual Output:

```text
WARNING: option '--subscription' will be ignored due to use of '--ids'.
WARNING: Command group 'acr reservation' is in preview and under development. Reference and support levels: https://aka.ms/CLI_refstatus
```

Exit code: **0**

Result: **PASS**. Deletion condition reached.

## 69. First lifecycle: show deleted reservation

Input:

```powershell
azlocal acr reservation show --ids /subscriptions/06f5e253-d825-4052-87ec-c4f12bc8f343/resourceGroups/eric-reservations-dfaue/providers/Microsoft.ContainerRegistry/capacityReservations/eric-cli-validation-1021 --subscription 06f5e253-d825-4052-87ec-c4f12bc8f343 -o json
```

Actual Output:

```text
WARNING: option '--subscription' will be ignored due to use of '--ids'.
WARNING: Command group 'acr reservation' is in preview and under development. Reference and support levels: https://aka.ms/CLI_refstatus
ERROR: Capacity reservation request failed (HTTP 404): The Resource 'Microsoft.ContainerRegistry/capacityReservations/eric-cli-validation-1021' under resource group 'eric-reservations-dfaue' was not found. For more details please go to https://aka.ms/ARMResourceNotFoundFix
```

Exit code: **3**

Result: **PASS**. Expected not-found exit code 3.

## 70. First lifecycle: final resource-group list

Input:

```powershell
azlocal acr reservation list -g eric-reservations-dfaue --subscription 06f5e253-d825-4052-87ec-c4f12bc8f343 -o json
```

Actual Output:

```text
WARNING: Command group 'acr reservation' is in preview and under development. Reference and support levels: https://aka.ms/CLI_refstatus
[]
```

Exit code: **0**

Result: **PASS**. Test resource group has no reservations.

## 71. Recreate same name with no-wait

Input:

```powershell
azlocal acr reservation create -n eric-cli-validation-1021 -g eric-reservations-dfaue --subscription 06f5e253-d825-4052-87ec-c4f12bc8f343 -l australiaeast --stamp-id dfaue-1 --request-rate-tier R1 --tags cliTest=name-reuse --no-wait -o json
```

Actual Output:

```text
WARNING: Command group 'acr reservation' is in preview and under development. Reference and support levels: https://aka.ms/CLI_refstatus
```

Exit code: **0**

Result: **PASS**. Same-name create accepted; completion checked separately.

## 72. Wait created after name reuse

Input:

```powershell
azlocal acr reservation wait --ids /subscriptions/06f5e253-d825-4052-87ec-c4f12bc8f343/resourceGroups/eric-reservations-dfaue/providers/Microsoft.ContainerRegistry/capacityReservations/eric-cli-validation-1021 --subscription 06f5e253-d825-4052-87ec-c4f12bc8f343 --created --interval 5 --timeout 120
```

Actual Output:

```text
WARNING: option '--subscription' will be ignored due to use of '--ids'.
WARNING: Command group 'acr reservation' is in preview and under development. Reference and support levels: https://aka.ms/CLI_refstatus
```

Exit code: **0**

Result: **PASS**. Command completed successfully.

## 73. Same-name reservation read

Input:

```powershell
azlocal acr reservation show --ids /subscriptions/06f5e253-d825-4052-87ec-c4f12bc8f343/resourceGroups/eric-reservations-dfaue/providers/Microsoft.ContainerRegistry/capacityReservations/eric-cli-validation-1021 --subscription 06f5e253-d825-4052-87ec-c4f12bc8f343 -o json
```

Actual Output:

```text
WARNING: option '--subscription' will be ignored due to use of '--ids'.
WARNING: Command group 'acr reservation' is in preview and under development. Reference and support levels: https://aka.ms/CLI_refstatus
{
  "id": "/subscriptions/06f5e253-d825-4052-87ec-c4f12bc8f343/resourceGroups/eric-reservations-dfaue/providers/Microsoft.ContainerRegistry/capacityReservations/eric-cli-validation-1021",
  "location": "australiaeast",
  "name": "eric-cli-validation-1021",
  "properties": {
    "createdAt": "2026-10-21T07:55:36.9249712+00:00",
    "earliestDeletableAt": "2026-10-21T08:00:36.9249712+00:00",
    "lastModifiedAt": "2026-10-21T07:55:36.9480829+00:00",
    "provisioningState": "Succeeded",
    "requestRateTier": "R1",
    "reservedEgressGbps": 0.0,
    "reservedIngressGbps": 0.0,
    "reservedRequestRate": 1.0
  },
  "resourceGroup": "eric-reservations-dfaue",
  "tags": {
    "cliTest": "name-reuse"
  },
  "type": "Microsoft.ContainerRegistry/capacityReservations"
}
```

Exit code: **0**

Result: **PASS**. R1 and zero ingress/egress retained; no internal stamp properties in JSON.

## 74. Idempotent create does not request extra capacity

Input:

```powershell
azlocal acr reservation create -n eric-cli-validation-1021 -g eric-reservations-dfaue --subscription 06f5e253-d825-4052-87ec-c4f12bc8f343 -l australiaeast --stamp-id dfaue-1 --request-rate-tier R1 --tags cliTest=name-reuse --timeout 120 -o json
```

Actual Output:

```text
WARNING: Command group 'acr reservation' is in preview and under development. Reference and support levels: https://aka.ms/CLI_refstatus
{
  "id": "/subscriptions/06f5e253-d825-4052-87ec-c4f12bc8f343/resourceGroups/eric-reservations-dfaue/providers/Microsoft.ContainerRegistry/capacityReservations/eric-cli-validation-1021",
  "location": "australiaeast",
  "name": "eric-cli-validation-1021",
  "properties": {
    "createdAt": "2026-10-21T07:55:36.9249712+00:00",
    "earliestDeletableAt": "2026-10-21T08:00:36.9249712+00:00",
    "lastModifiedAt": "2026-10-21T07:55:36.9480829+00:00",
    "provisioningState": "Succeeded",
    "requestRateTier": "R1",
    "reservedEgressGbps": 0.0,
    "reservedIngressGbps": 0.0,
    "reservedRequestRate": 1.0
  },
  "resourceGroup": "eric-reservations-dfaue",
  "tags": {
    "cliTest": "name-reuse"
  },
  "type": "Microsoft.ContainerRegistry/capacityReservations"
}
```

Exit code: **0**

Result: **PASS**. Command completed successfully.

## 75. Minimum commitment blocks immediate delete

Input:

```powershell
azlocal acr reservation delete --ids /subscriptions/06f5e253-d825-4052-87ec-c4f12bc8f343/resourceGroups/eric-reservations-dfaue/providers/Microsoft.ContainerRegistry/capacityReservations/eric-cli-validation-1021 --subscription 06f5e253-d825-4052-87ec-c4f12bc8f343 --yes --timeout 30
```

Actual Output:

```text
WARNING: option '--subscription' will be ignored due to use of '--ids'.
WARNING: Command group 'acr reservation' is in preview and under development. Reference and support levels: https://aka.ms/CLI_refstatus
ERROR: Capacity reservation request failed (HTTP 409): The reservation's minimum-commitment window has not elapsed.
```

Exit code: **1**

Result: **PASS**. Expected service-side 409; the resource remains until the commitment expires.

## 76. Offline handler and parser regression suite

Input:

```powershell
& 'Q:\dev\repos\copilot-worktrees\azure-cli\ericdu-literate-happiness\.venv\Scripts\python.exe' -m unittest azure.cli.command_modules.acr.tests.latest.test_acr_reservation azure.cli.command_modules.acr.tests.latest.test_acr_commands_mock azure.cli.command_modules.acr.tests.latest.test_acr_validators -v
```

Actual Output:

```text
test_acr_create_invalid_reservation_does_not_create (azure.cli.command_modules.acr.tests.latest.test_acr_reservation.RegistryIntegrationTests.test_acr_create_invalid_reservation_does_not_create) ... ok
test_acr_create_waits_before_associating (azure.cli.command_modules.acr.tests.latest.test_acr_reservation.RegistryIntegrationTests.test_acr_create_waits_before_associating) ... ok
test_acr_create_without_reservation_preserves_poller (azure.cli.command_modules.acr.tests.latest.test_acr_reservation.RegistryIntegrationTests.test_acr_create_without_reservation_preserves_poller) ... ok
test_acr_show_wires_lookup (azure.cli.command_modules.acr.tests.latest.test_acr_reservation.RegistryIntegrationTests.test_acr_show_wires_lookup) ... ok
test_acr_registry_cli_reservation_help_scope (azure.cli.command_modules.acr.tests.latest.test_acr_reservation.ReservationCommandTests.test_acr_registry_cli_reservation_help_scope) ... ok
test_acr_registry_cli_update_rejects_reservation (azure.cli.command_modules.acr.tests.latest.test_acr_reservation.ReservationCommandTests.test_acr_registry_cli_update_rejects_reservation) ... ERROR: unrecognized arguments: --reservation test-reservation

https://aka.ms/cli_ref
Read more about the command in reference docs
ok
test_acr_reservation_cli_associations (azure.cli.command_modules.acr.tests.latest.test_acr_reservation.ReservationCommandTests.test_acr_reservation_cli_associations) ... WARNING: Command group 'acr reservation' is in preview and under development. Reference and support levels: https://aka.ms/CLI_refstatus
WARNING: Command group 'acr reservation' is in preview and under development. Reference and support levels: https://aka.ms/CLI_refstatus
WARNING: Command group 'acr reservation' is in preview and under development. Reference and support levels: https://aka.ms/CLI_refstatus
ok
test_acr_reservation_cli_create_and_update_tiers (azure.cli.command_modules.acr.tests.latest.test_acr_reservation.ReservationCommandTests.test_acr_reservation_cli_create_and_update_tiers) ... WARNING: Command group 'acr reservation' is in preview and under development. Reference and support levels: https://aka.ms/CLI_refstatus
WARNING: Command group 'acr reservation' is in preview and under development. Reference and support levels: https://aka.ms/CLI_refstatus
ok
test_acr_reservation_cli_help_loads_without_service_calls (azure.cli.command_modules.acr.tests.latest.test_acr_reservation.ReservationCommandTests.test_acr_reservation_cli_help_loads_without_service_calls) ... ok
test_acr_reservation_cli_read_delete_and_wait (azure.cli.command_modules.acr.tests.latest.test_acr_reservation.ReservationCommandTests.test_acr_reservation_cli_read_delete_and_wait) ... WARNING: Command group 'acr reservation' is in preview and under development. Reference and support levels: https://aka.ms/CLI_refstatus
WARNING: Command group 'acr reservation' is in preview and under development. Reference and support levels: https://aka.ms/CLI_refstatus
WARNING: Command group 'acr reservation' is in preview and under development. Reference and support levels: https://aka.ms/CLI_refstatus
WARNING: Command group 'acr reservation' is in preview and under development. Reference and support levels: https://aka.ms/CLI_refstatus
WARNING: Command group 'acr reservation' is in preview and under development. Reference and support levels: https://aka.ms/CLI_refstatus
WARNING: Command group 'acr reservation' is in preview and under development. Reference and support levels: https://aka.ms/CLI_refstatus
WARNING: Command group 'acr reservation' is in preview and under development. Reference and support levels: https://aka.ms/CLI_refstatus
ok
test_acr_reservation_cli_requires_stamp_and_rejects_raw_capacity (azure.cli.command_modules.acr.tests.latest.test_acr_reservation.ReservationCommandTests.test_acr_reservation_cli_requires_stamp_and_rejects_raw_capacity) ... ERROR: the following arguments are required: --stamp-id

Examples from command's help:
az acr reservation create -n MyReservation -g MyResourceGroup -l australiaeast --stamp-id dfaue-1 --request-rate-tier R4 --egress-tier E4
Reserve request-rate and egress capacity.

az acr reservation create -n MyIngressReservation -g MyResourceGroup -l australiaeast --stamp-id dfaue-1 --ingress-tier I2 --no-wait
Reserve ingress capacity without waiting.

https://aka.ms/cli_ref
Read more about the command in reference docs
ERROR: az acr reservation create: '100' is not a valid value for '--request-rate-tier'. Allowed values: R1, R2, R4, R8, R16, R32, R64.

Examples from command's help:
az acr reservation create -n MyReservation -g MyResourceGroup -l australiaeast --stamp-id dfaue-1 --request-rate-tier R4 --egress-tier E4
Reserve request-rate and egress capacity.

az acr reservation create -n MyIngressReservation -g MyResourceGroup -l australiaeast --stamp-id dfaue-1 --ingress-tier I2 --no-wait
Reserve ingress capacity without waiting.

https://aka.ms/cli_ref
Read more about the command in reference docs
ERROR: unrecognized arguments: --request-rate-rus 100

https://aka.ms/cli_ref
Read more about the command in reference docs
ERROR: unrecognized arguments: --set properties.requestRateRus=100

https://aka.ms/cli_ref
Read more about the command in reference docs
ok
test_acr_reservation_cli_show_not_found_exits_three (azure.cli.command_modules.acr.tests.latest.test_acr_reservation.ReservationCommandTests.test_acr_reservation_cli_show_not_found_exits_three) ... WARNING: Command group 'acr reservation' is in preview and under development. Reference and support levels: https://aka.ms/CLI_refstatus
ERROR: Capacity reservation request failed (HTTP 404): Reservation not found.
ok
test_acr_reservation_cli_unset_tiers_only_normalized_in_table (azure.cli.command_modules.acr.tests.latest.test_acr_reservation.ReservationCommandTests.test_acr_reservation_cli_unset_tiers_only_normalized_in_table) ... WARNING: Command group 'acr reservation' is in preview and under development. Reference and support levels: https://aka.ms/CLI_refstatus
WARNING: Command group 'acr reservation' is in preview and under development. Reference and support levels: https://aka.ms/CLI_refstatus
WARNING: Command group 'acr reservation' is in preview and under development. Reference and support levels: https://aka.ms/CLI_refstatus
WARNING: Command group 'acr reservation' is in preview and under development. Reference and support levels: https://aka.ms/CLI_refstatus
ok
test_acr_registry_create_association_partial_failure_keeps_registry (azure.cli.command_modules.acr.tests.latest.test_acr_reservation.ReservationTests.test_acr_registry_create_association_partial_failure_keeps_registry) ... ok
test_acr_registry_create_association_returns_enriched_registry (azure.cli.command_modules.acr.tests.latest.test_acr_reservation.ReservationTests.test_acr_registry_create_association_returns_enriched_registry) ... ok
test_acr_registry_create_validates_reservation_before_side_effects (azure.cli.command_modules.acr.tests.latest.test_acr_reservation.ReservationTests.test_acr_registry_create_validates_reservation_before_side_effects) ... ok
test_acr_registry_reservation_lookup_distinguishes_none_from_failure (azure.cli.command_modules.acr.tests.latest.test_acr_reservation.ReservationTests.test_acr_registry_reservation_lookup_distinguishes_none_from_failure) ... ok
test_acr_registry_reservation_lookup_is_rg_scoped (azure.cli.command_modules.acr.tests.latest.test_acr_reservation.ReservationTests.test_acr_registry_reservation_lookup_is_rg_scoped) ... ok
test_acr_registry_show_public_cloud_is_unchanged (azure.cli.command_modules.acr.tests.latest.test_acr_reservation.ReservationTests.test_acr_registry_show_public_cloud_is_unchanged) ... ok
test_acr_reservation_associate_waits_for_active (azure.cli.command_modules.acr.tests.latest.test_acr_reservation.ReservationTests.test_acr_reservation_associate_waits_for_active) ... ok
test_acr_reservation_association_no_wait (azure.cli.command_modules.acr.tests.latest.test_acr_reservation.ReservationTests.test_acr_reservation_association_no_wait) ... ok
test_acr_reservation_association_state_mapping (azure.cli.command_modules.acr.tests.latest.test_acr_reservation.ReservationTests.test_acr_reservation_association_state_mapping) ... ok
test_acr_reservation_association_timeout_does_not_report_success (azure.cli.command_modules.acr.tests.latest.test_acr_reservation.ReservationTests.test_acr_reservation_association_timeout_does_not_report_success) ... ok
test_acr_reservation_connection_error_is_actionable (azure.cli.command_modules.acr.tests.latest.test_acr_reservation.ReservationTests.test_acr_reservation_connection_error_is_actionable) ... ok
test_acr_reservation_create_all_tier_mappings (azure.cli.command_modules.acr.tests.latest.test_acr_reservation.ReservationTests.test_acr_reservation_create_all_tier_mappings) ... ok
test_acr_reservation_create_polls_202_and_honours_retry_after (azure.cli.command_modules.acr.tests.latest.test_acr_reservation.ReservationTests.test_acr_reservation_create_polls_202_and_honours_retry_after) ... ok
test_acr_reservation_create_requires_positive_tier (azure.cli.command_modules.acr.tests.latest.test_acr_reservation.ReservationTests.test_acr_reservation_create_requires_positive_tier) ... ok
test_acr_reservation_create_validates_name_stamp_and_timeout (azure.cli.command_modules.acr.tests.latest.test_acr_reservation.ReservationTests.test_acr_reservation_create_validates_name_stamp_and_timeout) ... ok
test_acr_reservation_delete_no_wait (azure.cli.command_modules.acr.tests.latest.test_acr_reservation.ReservationTests.test_acr_reservation_delete_no_wait) ... ok
test_acr_reservation_delete_polls_202_until_not_found (azure.cli.command_modules.acr.tests.latest.test_acr_reservation.ReservationTests.test_acr_reservation_delete_polls_202_until_not_found) ... ok
test_acr_reservation_delete_returns_no_output (azure.cli.command_modules.acr.tests.latest.test_acr_reservation.ReservationTests.test_acr_reservation_delete_returns_no_output) ... ok
test_acr_reservation_disassociate_waits_for_target_only (azure.cli.command_modules.acr.tests.latest.test_acr_reservation.ReservationTests.test_acr_reservation_disassociate_waits_for_target_only) ... ok
test_acr_reservation_duplicate_associations_do_not_report_success (azure.cli.command_modules.acr.tests.latest.test_acr_reservation.ReservationTests.test_acr_reservation_duplicate_associations_do_not_report_success) ... ok
test_acr_reservation_empty_202_response (azure.cli.command_modules.acr.tests.latest.test_acr_reservation.ReservationTests.test_acr_reservation_empty_202_response) ... ok
test_acr_reservation_failed_lro_reports_error (azure.cli.command_modules.acr.tests.latest.test_acr_reservation.ReservationTests.test_acr_reservation_failed_lro_reports_error) ... ok
test_acr_reservation_http_errors_include_plain_text_poc_errors (azure.cli.command_modules.acr.tests.latest.test_acr_reservation.ReservationTests.test_acr_reservation_http_errors_include_plain_text_poc_errors) ... ok
test_acr_reservation_invalid_association_cannot_mean_unassociated (azure.cli.command_modules.acr.tests.latest.test_acr_reservation.ReservationTests.test_acr_reservation_invalid_association_cannot_mean_unassociated) ... ok
test_acr_reservation_invalid_identity_is_reported (azure.cli.command_modules.acr.tests.latest.test_acr_reservation.ReservationTests.test_acr_reservation_invalid_identity_is_reported) ... ok
test_acr_reservation_list_rejects_malformed_response (azure.cli.command_modules.acr.tests.latest.test_acr_reservation.ReservationTests.test_acr_reservation_list_rejects_malformed_response) ... ok
test_acr_reservation_list_scopes_and_pagination (azure.cli.command_modules.acr.tests.latest.test_acr_reservation.ReservationTests.test_acr_reservation_list_scopes_and_pagination) ... ok
test_acr_reservation_no_wait_returns_without_polling (azure.cli.command_modules.acr.tests.latest.test_acr_reservation.ReservationTests.test_acr_reservation_no_wait_returns_without_polling) ... ok
test_acr_reservation_poll_timeout (azure.cli.command_modules.acr.tests.latest.test_acr_reservation.ReservationTests.test_acr_reservation_poll_timeout) ... ok
test_acr_reservation_polls_resource_without_monitor (azure.cli.command_modules.acr.tests.latest.test_acr_reservation.ReservationTests.test_acr_reservation_polls_resource_without_monitor) ... ok
test_acr_reservation_rejects_external_monitor (azure.cli.command_modules.acr.tests.latest.test_acr_reservation.ReservationTests.test_acr_reservation_rejects_external_monitor) ... ok
test_acr_reservation_rejects_external_next_link (azure.cli.command_modules.acr.tests.latest.test_acr_reservation.ReservationTests.test_acr_reservation_rejects_external_next_link) ... ok
test_acr_reservation_rejects_repeated_page (azure.cli.command_modules.acr.tests.latest.test_acr_reservation.ReservationTests.test_acr_reservation_rejects_repeated_page) ... ok
test_acr_reservation_show_filters_internals (azure.cli.command_modules.acr.tests.latest.test_acr_reservation.ReservationTests.test_acr_reservation_show_filters_internals) ... ok
test_acr_reservation_table_output_has_no_internals (azure.cli.command_modules.acr.tests.latest.test_acr_reservation.ReservationTests.test_acr_reservation_table_output_has_no_internals) ... ok
test_acr_reservation_table_unset_tiers_display_none (azure.cli.command_modules.acr.tests.latest.test_acr_reservation.ReservationTests.test_acr_reservation_table_unset_tiers_display_none) ... ok
test_acr_reservation_terminal_resource_failure_after_successful_monitor (azure.cli.command_modules.acr.tests.latest.test_acr_reservation.ReservationTests.test_acr_reservation_terminal_resource_failure_after_successful_monitor) ... ok
test_acr_reservation_update_none_removes_dimension_and_label (azure.cli.command_modules.acr.tests.latest.test_acr_reservation.ReservationTests.test_acr_reservation_update_none_removes_dimension_and_label) ... ok
test_acr_reservation_update_preserves_omitted_amounts (azure.cli.command_modules.acr.tests.latest.test_acr_reservation.ReservationTests.test_acr_reservation_update_preserves_omitted_amounts) ... ok
test_acr_reservation_update_rejects_all_zero (azure.cli.command_modules.acr.tests.latest.test_acr_reservation.ReservationTests.test_acr_reservation_update_rejects_all_zero) ... ok
test_acr_reservation_update_rejects_missing_current_amounts (azure.cli.command_modules.acr.tests.latest.test_acr_reservation.ReservationTests.test_acr_reservation_update_rejects_missing_current_amounts) ... ok
test_acr_reservation_update_requires_change (azure.cli.command_modules.acr.tests.latest.test_acr_reservation.ReservationTests.test_acr_reservation_update_requires_change) ... ok
test_acr_reservation_update_tags_only_preserves_all_dimensions (azure.cli.command_modules.acr.tests.latest.test_acr_reservation.ReservationTests.test_acr_reservation_update_tags_only_preserves_all_dimensions) ... ok
test_acr_reservation_update_trusts_succeeded_after_rollback (azure.cli.command_modules.acr.tests.latest.test_acr_reservation.ReservationTests.test_acr_reservation_update_trusts_succeeded_after_rollback) ... ok
test_get_docker_credentials (azure.cli.command_modules.acr.tests.latest.test_acr_commands_mock.AcrMockCommandsTests.test_get_docker_credentials) ... Q:\dev\repos\copilot-worktrees\azure-cli\ericdu-literate-happiness\src\azure-cli\azure\cli\command_modules\acr\_format.py:547: DeprecationWarning: datetime.datetime.utcnow() is deprecated and scheduled for removal in a future version. Use timezone-aware objects to represent datetimes in UTC: datetime.datetime.now(datetime.UTC).
  return "{} {}".format(datetime.utcnow(), message)
ok
test_helm_delete (azure.cli.command_modules.acr.tests.latest.test_acr_commands_mock.AcrMockCommandsTests.test_helm_delete) ... ok
test_helm_list (azure.cli.command_modules.acr.tests.latest.test_acr_commands_mock.AcrMockCommandsTests.test_helm_list) ... ok
test_helm_push (azure.cli.command_modules.acr.tests.latest.test_acr_commands_mock.AcrMockCommandsTests.test_helm_push) ... ok
test_helm_show (azure.cli.command_modules.acr.tests.latest.test_acr_commands_mock.AcrMockCommandsTests.test_helm_show) ... ok
test_manifest_delete (azure.cli.command_modules.acr.tests.latest.test_acr_commands_mock.AcrMockCommandsTests.test_manifest_delete) ... ok
test_manifest_deleted_list (azure.cli.command_modules.acr.tests.latest.test_acr_commands_mock.AcrMockCommandsTests.test_manifest_deleted_list) ... ok
test_manifest_deleted_restore (azure.cli.command_modules.acr.tests.latest.test_acr_commands_mock.AcrMockCommandsTests.test_manifest_deleted_restore) ... ok
test_manifest_deleted_tags_list (azure.cli.command_modules.acr.tests.latest.test_acr_commands_mock.AcrMockCommandsTests.test_manifest_deleted_tags_list) ... ok
test_manifest_list (azure.cli.command_modules.acr.tests.latest.test_acr_commands_mock.AcrMockCommandsTests.test_manifest_list) ... ok
test_manifest_list_referrers (azure.cli.command_modules.acr.tests.latest.test_acr_commands_mock.AcrMockCommandsTests.test_manifest_list_referrers) ... ok
test_manifest_metadata_list (azure.cli.command_modules.acr.tests.latest.test_acr_commands_mock.AcrMockCommandsTests.test_manifest_metadata_list) ... ok
test_manifest_metadata_show (azure.cli.command_modules.acr.tests.latest.test_acr_commands_mock.AcrMockCommandsTests.test_manifest_metadata_show) ... ok
test_manifest_metadata_update (azure.cli.command_modules.acr.tests.latest.test_acr_commands_mock.AcrMockCommandsTests.test_manifest_metadata_update) ... ok
test_manifest_show (azure.cli.command_modules.acr.tests.latest.test_acr_commands_mock.AcrMockCommandsTests.test_manifest_show) ... ok
test_repository_delete (azure.cli.command_modules.acr.tests.latest.test_acr_commands_mock.AcrMockCommandsTests.test_repository_delete) ... ok
test_repository_list (azure.cli.command_modules.acr.tests.latest.test_acr_commands_mock.AcrMockCommandsTests.test_repository_list) ... ok
test_repository_list_deleted (azure.cli.command_modules.acr.tests.latest.test_acr_commands_mock.AcrMockCommandsTests.test_repository_list_deleted) ... ok
test_repository_show (azure.cli.command_modules.acr.tests.latest.test_acr_commands_mock.AcrMockCommandsTests.test_repository_show) ... ok
test_repository_show_manifests (azure.cli.command_modules.acr.tests.latest.test_acr_commands_mock.AcrMockCommandsTests.test_repository_show_manifests) ... ok
test_repository_show_tags (azure.cli.command_modules.acr.tests.latest.test_acr_commands_mock.AcrMockCommandsTests.test_repository_show_tags) ... ok
test_repository_update (azure.cli.command_modules.acr.tests.latest.test_acr_commands_mock.AcrMockCommandsTests.test_repository_update) ... ok
test_config_exception_falls_back_to_default (azure.cli.command_modules.acr.tests.latest.test_acr_commands_mock.ResolveAcrScopeTests.test_config_exception_falls_back_to_default) ... ok
test_default_when_unset (azure.cli.command_modules.acr.tests.latest.test_acr_commands_mock.ResolveAcrScopeTests.test_default_when_unset) ... ok
test_full_url_is_used_verbatim (azure.cli.command_modules.acr.tests.latest.test_acr_commands_mock.ResolveAcrScopeTests.test_full_url_is_used_verbatim) ... ok
test_short_name_is_expanded (azure.cli.command_modules.acr.tests.latest.test_acr_commands_mock.ResolveAcrScopeTests.test_short_name_is_expanded) ... ok
test_registry_name_invalid_inputs_should_raise_error (azure.cli.command_modules.acr.tests.latest.test_acr_validators.AcrValidatorsTests.test_registry_name_invalid_inputs_should_raise_error)
Test invalid registry names that should raise InvalidArgumentValueError. ... ok
test_registry_name_valid_inputs (azure.cli.command_modules.acr.tests.latest.test_acr_validators.AcrValidatorsTests.test_registry_name_valid_inputs)
Test valid registry names that should pass validation. ... ok
test_registry_name_with_dnl_suffix_loginserver (azure.cli.command_modules.acr.tests.latest.test_acr_validators.AcrValidatorsTests.test_registry_name_with_dnl_suffix_loginserver) ... ok

----------------------------------------------------------------------
Ran 86 tests in 1.601s

OK
```

Exit code: **0**

Result: **PASS**. Mocked suite covers tier mappings, HTTP 202/LRO failures, timeouts, pagination, partial registry-creation failures, and association state mapping. Not live load testing.

## 77. Recreated lifecycle: read before cleanup

Input:

```powershell
azlocal acr reservation show --ids /subscriptions/06f5e253-d825-4052-87ec-c4f12bc8f343/resourceGroups/eric-reservations-dfaue/providers/Microsoft.ContainerRegistry/capacityReservations/eric-cli-validation-1021 --subscription 06f5e253-d825-4052-87ec-c4f12bc8f343 -o json
```

Actual Output:

```text
WARNING: option '--subscription' will be ignored due to use of '--ids'.
WARNING: Command group 'acr reservation' is in preview and under development. Reference and support levels: https://aka.ms/CLI_refstatus
{
  "id": "/subscriptions/06f5e253-d825-4052-87ec-c4f12bc8f343/resourceGroups/eric-reservations-dfaue/providers/Microsoft.ContainerRegistry/capacityReservations/eric-cli-validation-1021",
  "location": "australiaeast",
  "name": "eric-cli-validation-1021",
  "properties": {
    "createdAt": "2026-10-21T07:55:36.9249712+00:00",
    "earliestDeletableAt": "2026-10-21T08:00:36.9249712+00:00",
    "lastModifiedAt": "2026-10-21T07:55:36.9480829+00:00",
    "provisioningState": "Succeeded",
    "requestRateTier": "R1",
    "reservedEgressGbps": 0.0,
    "reservedIngressGbps": 0.0,
    "reservedRequestRate": 1.0
  },
  "resourceGroup": "eric-reservations-dfaue",
  "tags": {
    "cliTest": "name-reuse"
  },
  "type": "Microsoft.ContainerRegistry/capacityReservations"
}
```

Exit code: **0**

Result: **PASS**. R1 and zero ingress/egress retained; no internal stamp properties in JSON.

## 78. Recreated lifecycle: require no registry associations

Input:

```powershell
azlocal acr reservation list-registries -n eric-cli-validation-1021 -g eric-reservations-dfaue --subscription 06f5e253-d825-4052-87ec-c4f12bc8f343 -o json
```

Actual Output:

```text
WARNING: Command group 'acr reservation' is in preview and under development. Reference and support levels: https://aka.ms/CLI_refstatus
[]
```

Exit code: **0**

Result: **PASS**. Command completed successfully.

Cleanup waited for the service's minimum commitment until `2026-10-21T08:00:36.924971+00:00` (plus a 10-second clock margin).

## 79. Recreated lifecycle: delete by resource ID

Input:

```powershell
azlocal acr reservation delete --ids /subscriptions/06f5e253-d825-4052-87ec-c4f12bc8f343/resourceGroups/eric-reservations-dfaue/providers/Microsoft.ContainerRegistry/capacityReservations/eric-cli-validation-1021 --subscription 06f5e253-d825-4052-87ec-c4f12bc8f343 --yes --no-wait
```

Actual Output:

```text
WARNING: option '--subscription' will be ignored due to use of '--ids'.
WARNING: Command group 'acr reservation' is in preview and under development. Reference and support levels: https://aka.ms/CLI_refstatus
```

Exit code: **0**

Result: **PASS**. Deletion accepted; --no-wait does not itself confirm completion.

## 80. Recreated lifecycle: wait for deletion

Input:

```powershell
azlocal acr reservation wait --ids /subscriptions/06f5e253-d825-4052-87ec-c4f12bc8f343/resourceGroups/eric-reservations-dfaue/providers/Microsoft.ContainerRegistry/capacityReservations/eric-cli-validation-1021 --subscription 06f5e253-d825-4052-87ec-c4f12bc8f343 --deleted --interval 5 --timeout 120
```

Actual Output:

```text
WARNING: option '--subscription' will be ignored due to use of '--ids'.
WARNING: Command group 'acr reservation' is in preview and under development. Reference and support levels: https://aka.ms/CLI_refstatus
```

Exit code: **0**

Result: **PASS**. Deletion condition reached.

## 81. Recreated lifecycle: show deleted reservation

Input:

```powershell
azlocal acr reservation show --ids /subscriptions/06f5e253-d825-4052-87ec-c4f12bc8f343/resourceGroups/eric-reservations-dfaue/providers/Microsoft.ContainerRegistry/capacityReservations/eric-cli-validation-1021 --subscription 06f5e253-d825-4052-87ec-c4f12bc8f343 -o json
```

Actual Output:

```text
WARNING: option '--subscription' will be ignored due to use of '--ids'.
WARNING: Command group 'acr reservation' is in preview and under development. Reference and support levels: https://aka.ms/CLI_refstatus
ERROR: Capacity reservation request failed (HTTP 404): The Resource 'Microsoft.ContainerRegistry/capacityReservations/eric-cli-validation-1021' under resource group 'eric-reservations-dfaue' was not found. For more details please go to https://aka.ms/ARMResourceNotFoundFix
```

Exit code: **3**

Result: **PASS**. Expected not-found exit code 3.

## 82. Recreated lifecycle: final resource-group list

Input:

```powershell
azlocal acr reservation list -g eric-reservations-dfaue --subscription 06f5e253-d825-4052-87ec-c4f12bc8f343 -o json
```

Actual Output:

```text
WARNING: Command group 'acr reservation' is in preview and under development. Reference and support levels: https://aka.ms/CLI_refstatus
[]
```

Exit code: **0**

Result: **PASS**. Test resource group has no reservations.

## 83. Final retained registry state

Input:

```powershell
azlocal acr show -n ericreservationdfaue -g eric-reservations-dfaue --subscription 06f5e253-d825-4052-87ec-c4f12bc8f343 -o json
```

Actual Output:

```text
{
  "adminUserEnabled": false,
  "anonymousPullEnabled": false,
  "autoGeneratedDomainNameLabelScope": "Unsecure",
  "creationDate": "2026-10-21T06:56:40.717943+00:00",
  "dataEndpointEnabled": false,
  "dataEndpointHostNames": [],
  "encryption": {
    "keyVaultProperties": null,
    "status": "disabled"
  },
  "endpointProtocol": "IPv4",
  "id": "/subscriptions/06f5e253-d825-4052-87ec-c4f12bc8f343/resourceGroups/eric-reservations-dfaue/providers/Microsoft.ContainerRegistry/registries/ericreservationdfaue",
  "identity": null,
  "location": "australiaeast",
  "loginServer": "ericreservationdfaue.azurecr-test.io",
  "metadataSearch": "Disabled",
  "name": "ericreservationdfaue",
  "networkRuleBypassAllowedForTasks": false,
  "networkRuleBypassOptions": "AzureServices",
  "networkRuleSet": {
    "defaultAction": "Allow",
    "ipRules": [],
    "virtualNetworkRules": []
  },
  "policies": {
    "azureAdAuthenticationAsArmPolicy": {
      "status": "enabled"
    },
    "exportPolicy": {
      "status": "enabled"
    },
    "quarantinePolicy": {
      "status": "disabled"
    },
    "retentionPolicy": {
      "days": 7,
      "lastUpdatedTime": "2026-10-21T06:56:49.523095+00:00",
      "status": "disabled"
    },
    "softDeletePolicy": {
      "lastUpdatedTime": "2026-10-21T06:56:49.523376+00:00",
      "retentionDays": 7,
      "status": "disabled"
    },
    "trustPolicy": {
      "status": "disabled",
      "type": "Notary"
    }
  },
  "privateEndpointConnections": [],
  "provisioningState": "Succeeded",
  "publicNetworkAccess": "Enabled",
  "regionalEndpointHostNames": [],
  "regionalEndpoints": "Disabled",
  "reservation": null,
  "resourceGroup": "eric-reservations-dfaue",
  "roleAssignmentMode": "LegacyRegistryPermissions",
  "sku": {
    "name": "Premium",
    "tier": "Premium"
  },
  "status": null,
  "systemData": {
    "createdAt": "2026-10-21T06:56:40.717943+00:00",
    "createdBy": "ericdu@acrbami202608.ccsctp.net",
    "createdByType": "User",
    "lastModifiedAt": "2026-10-21T06:56:40.717943+00:00",
    "lastModifiedBy": "ericdu@acrbami202608.ccsctp.net",
    "lastModifiedByType": "User"
  },
  "tags": {
    "cliTest": "reservation-lifecycle"
  },
  "type": "Microsoft.ContainerRegistry/registries",
  "writableCacheRepos": "Disabled",
  "zoneRedundancy": "Disabled"
}
```

Exit code: **0**

Result: **PASS**. Command completed successfully.

## Run summary

- Passed CLI command checks: **80**.
- Blocked CLI command checks: **2**.
- Offline regression suite: **86 tests passed** (one additional recorded command).
- Failed command checks: **0**.
- Test reservation cleanup: **completed**, confirmed by `wait --deleted`, show
  returning exit code 3, and an empty resource-group reservation list.
- Existing registry `ericreservationdfaue`: **Succeeded and unassociated**, preserved.
- Blockers: R1 association returns HTTP 409 because the RP requires
  `RequestRate-L`; subscription-scoped reservation listing returns HTTP 502.
- No higher-capacity tiers, traffic generation, forced scale-out, RBAC changes, or ledger mutations were run.
- Live asynchronous scale-out, real timeout/failure injection, and other-cloud behavior are not covered; mocked coverage is separate.
- Finished: `2026-10-21T08:01:04.556897+00:00`.
