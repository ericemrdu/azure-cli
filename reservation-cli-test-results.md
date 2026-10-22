# Reservation CLI test results

Date: 2026-10-21 (UTC)

Included results: **56 CLI checks passed, 2 CLI checks blocked**.
Test reservations were cleaned up; `ericreservationdfaue` remains provisioned and
unassociated. The numbered sections below show the documented command syntax,
recorded output, and exit code.

This report focuses on reservation behaviour, using JSON for resource-state
evidence. Repeated initial reads, alternate output formats, help-output checks,
and redundant waits are omitted. Reads after updates and during cleanup are
retained to verify persisted changes and safe deletion. The original run had
80 passed CLI checks and 2 blocked checks; 24 passed checks are omitted here.

Reservation command inputs use `-n`, `-g`, and `--subscription` rather than
`--ids`. These inputs have been rewritten for readability and have not been
rerun. Outputs and results remain from the original run, which used `--ids`
for some commands; the corresponding ignored-subscription warnings are retained
as historical evidence.

The following checks use the local worktree CLI (`azlocal`) against Dogfood. Commands run
sequentially. No `az rest` or direct HTTP
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
azlocal acr reservation show -n eric-cli-validation-1021 -g eric-reservations-dfaue --subscription 06f5e253-d825-4052-87ec-c4f12bc8f343 -o json
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

## 5. Read empty association list

Input:

```powershell
azlocal acr reservation list-registries -n eric-cli-validation-1021 -g eric-reservations-dfaue --subscription 06f5e253-d825-4052-87ec-c4f12bc8f343 -o json
```

Actual Output:

```text
WARNING: option '--subscription' will be ignored due to use of '--ids'.
WARNING: Command group 'acr reservation' is in preview and under development. Reference and support levels: https://aka.ms/CLI_refstatus
[]
```

Exit code: **0**

Result: **PASS**. Command completed successfully.

## 6. Create without a positive tier

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

## 7. Create with invalid short name

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

## 8. Create with invalid tier

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

## 9. Create with missing stamp

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

## 10. Create with blank stamp

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

## 11. Create with zero timeout

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

## 12. Create with negative timeout

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

## 13. Create with None tier

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

## 14. Legacy label rejected by CLI

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

## 15. Update without changes

Input:

```powershell
azlocal acr reservation update -n eric-cli-validation-1021 -g eric-reservations-dfaue --subscription 06f5e253-d825-4052-87ec-c4f12bc8f343
```

Actual Output:

```text
WARNING: option '--subscription' will be ignored due to use of '--ids'.
WARNING: Command group 'acr reservation' is in preview and under development. Reference and support levels: https://aka.ms/CLI_refstatus
ERROR: Specify a tier or --tags to update.
```

Exit code: **1**

Result: **PASS**. Expected rejection; no valid capacity increase requested.

## 16. Reject removing last positive dimension

Input:

```powershell
azlocal acr reservation update -n eric-cli-validation-1021 -g eric-reservations-dfaue --subscription 06f5e253-d825-4052-87ec-c4f12bc8f343 --request-rate-tier None
```

Actual Output:

```text
WARNING: option '--subscription' will be ignored due to use of '--ids'.
WARNING: Command group 'acr reservation' is in preview and under development. Reference and support levels: https://aka.ms/CLI_refstatus
ERROR: At least one reserved dimension must have a positive tier.
```

Exit code: **1**

Result: **PASS**. Expected rejection; no valid capacity increase requested.

## 17. Reject raw numeric capacity

Input:

```powershell
azlocal acr reservation update -n eric-cli-validation-1021 -g eric-reservations-dfaue --subscription 06f5e253-d825-4052-87ec-c4f12bc8f343 --request-rate-rus 100
```

Actual Output:

```text
ERROR: unrecognized arguments: --request-rate-rus 100

https://aka.ms/cli_ref
Read more about the command in reference docs
```

Exit code: **2**

Result: **PASS**. Expected rejection; no valid capacity increase requested.

## 18. Reject generic set bypass

Input:

```powershell
azlocal acr reservation update -n eric-cli-validation-1021 -g eric-reservations-dfaue --subscription 06f5e253-d825-4052-87ec-c4f12bc8f343 --set properties.requestRateRus=100
```

Actual Output:

```text
ERROR: unrecognized arguments: --set properties.requestRateRus=100

https://aka.ms/cli_ref
Read more about the command in reference docs
```

Exit code: **2**

Result: **PASS**. Expected rejection; no valid capacity increase requested.

## 19. Reject reservation on registry update

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

## 20. Show nonexistent reservation

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

## 21. Update nonexistent reservation

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

## 22. Capacity unchanged after negative tests

Input:

```powershell
azlocal acr reservation show -n eric-cli-validation-1021 -g eric-reservations-dfaue --subscription 06f5e253-d825-4052-87ec-c4f12bc8f343 -o json
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

## 23. Wait deleted for nonexistent reservation

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

## 24. Registry create preflight: missing reservation

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

## 25. Registry create preflight: region mismatch

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

## 26. Registry preflight did not create a registry

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

## 27. Tags-only update

Input:

```powershell
azlocal acr reservation update -n eric-cli-validation-1021 -g eric-reservations-dfaue --subscription 06f5e253-d825-4052-87ec-c4f12bc8f343 --tags cliTest=full-validation phase=tags --timeout 120 -o json
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

## 28. Tags update retained numeric dimensions

Input:

```powershell
azlocal acr reservation show -n eric-cli-validation-1021 -g eric-reservations-dfaue --subscription 06f5e253-d825-4052-87ec-c4f12bc8f343 -o json
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

## 29. Clear tags

Input:

```powershell
azlocal acr reservation update -n eric-cli-validation-1021 -g eric-reservations-dfaue --subscription 06f5e253-d825-4052-87ec-c4f12bc8f343 --tags '' --timeout 120 -o json
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

## 30. Case-insensitive R1 update without increasing capacity

Input:

```powershell
azlocal acr reservation update -n eric-cli-validation-1021 -g eric-reservations-dfaue --subscription 06f5e253-d825-4052-87ec-c4f12bc8f343 --request-rate-tier r1 --timeout 120 -o json
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

## 31. Add I1 using case-insensitive tier

Input:

```powershell
azlocal acr reservation update -n eric-cli-validation-1021 -g eric-reservations-dfaue --subscription 06f5e253-d825-4052-87ec-c4f12bc8f343 --ingress-tier i1 --timeout 120 -o json
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

## 32. Verify ingress update persisted

Input:

```powershell
azlocal acr reservation show -n eric-cli-validation-1021 -g eric-reservations-dfaue --subscription 06f5e253-d825-4052-87ec-c4f12bc8f343 -o json
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

## 33. Remove ingress with no-wait

Input:

```powershell
azlocal acr reservation update -n eric-cli-validation-1021 -g eric-reservations-dfaue --subscription 06f5e253-d825-4052-87ec-c4f12bc8f343 --ingress-tier None --no-wait -o json
```

Actual Output:

```text
WARNING: option '--subscription' will be ignored due to use of '--ids'.
WARNING: Command group 'acr reservation' is in preview and under development. Reference and support levels: https://aka.ms/CLI_refstatus
```

Exit code: **0**

Result: **PASS**. No-wait return validated; completion checked separately.

## 34. Wait updated after no-wait

Input:

```powershell
azlocal acr reservation wait -n eric-cli-validation-1021 -g eric-reservations-dfaue --subscription 06f5e253-d825-4052-87ec-c4f12bc8f343 --updated --interval 5 --timeout 120
```

Actual Output:

```text
WARNING: option '--subscription' will be ignored due to use of '--ids'.
WARNING: Command group 'acr reservation' is in preview and under development. Reference and support levels: https://aka.ms/CLI_refstatus
```

Exit code: **0**

Result: **PASS**. Command completed successfully.

## 35. Verify None removal persisted

Input:

```powershell
azlocal acr reservation show -n eric-cli-validation-1021 -g eric-reservations-dfaue --subscription 06f5e253-d825-4052-87ec-c4f12bc8f343 -o json
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

## 36. Explicitly remove already-zero egress

Input:

```powershell
azlocal acr reservation update -n eric-cli-validation-1021 -g eric-reservations-dfaue --subscription 06f5e253-d825-4052-87ec-c4f12bc8f343 --egress-tier None --timeout 120 -o json
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

## 37. Associate existing test registry using R1

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

## 38. Association list after compatibility check

Input:

```powershell
azlocal acr reservation list-registries -n eric-cli-validation-1021 -g eric-reservations-dfaue --subscription 06f5e253-d825-4052-87ec-c4f12bc8f343 -o json
```

Actual Output:

```text
WARNING: option '--subscription' will be ignored due to use of '--ids'.
WARNING: Command group 'acr reservation' is in preview and under development. Reference and support levels: https://aka.ms/CLI_refstatus
[]
```

Exit code: **0**

Result: **PASS**. Command completed successfully.

## 39. Registry remains unassociated

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

## 40. Subscription-scoped list

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

## 41. First lifecycle: read before cleanup

Input:

```powershell
azlocal acr reservation show -n eric-cli-validation-1021 -g eric-reservations-dfaue --subscription 06f5e253-d825-4052-87ec-c4f12bc8f343 -o json
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

## 42. First lifecycle: require no registry associations

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

## 43. First lifecycle: delete reservation

Input:

```powershell
azlocal acr reservation delete -n eric-cli-validation-1021 -g eric-reservations-dfaue --subscription 06f5e253-d825-4052-87ec-c4f12bc8f343 --yes --no-wait
```

Actual Output:

```text
WARNING: option '--subscription' will be ignored due to use of '--ids'.
WARNING: Command group 'acr reservation' is in preview and under development. Reference and support levels: https://aka.ms/CLI_refstatus
```

Exit code: **0**

Result: **PASS**. Deletion accepted; --no-wait does not itself confirm completion.

## 44. First lifecycle: wait for deletion

Input:

```powershell
azlocal acr reservation wait -n eric-cli-validation-1021 -g eric-reservations-dfaue --subscription 06f5e253-d825-4052-87ec-c4f12bc8f343 --deleted --interval 5 --timeout 120
```

Actual Output:

```text
WARNING: option '--subscription' will be ignored due to use of '--ids'.
WARNING: Command group 'acr reservation' is in preview and under development. Reference and support levels: https://aka.ms/CLI_refstatus
```

Exit code: **0**

Result: **PASS**. Deletion condition reached.

## 45. First lifecycle: show deleted reservation

Input:

```powershell
azlocal acr reservation show -n eric-cli-validation-1021 -g eric-reservations-dfaue --subscription 06f5e253-d825-4052-87ec-c4f12bc8f343 -o json
```

Actual Output:

```text
WARNING: option '--subscription' will be ignored due to use of '--ids'.
WARNING: Command group 'acr reservation' is in preview and under development. Reference and support levels: https://aka.ms/CLI_refstatus
ERROR: Capacity reservation request failed (HTTP 404): The Resource 'Microsoft.ContainerRegistry/capacityReservations/eric-cli-validation-1021' under resource group 'eric-reservations-dfaue' was not found. For more details please go to https://aka.ms/ARMResourceNotFoundFix
```

Exit code: **3**

Result: **PASS**. Expected not-found exit code 3.

## 46. First lifecycle: final resource-group list

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

## 47. Recreate same name with no-wait

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

## 48. Wait created after name reuse

Input:

```powershell
azlocal acr reservation wait -n eric-cli-validation-1021 -g eric-reservations-dfaue --subscription 06f5e253-d825-4052-87ec-c4f12bc8f343 --created --interval 5 --timeout 120
```

Actual Output:

```text
WARNING: option '--subscription' will be ignored due to use of '--ids'.
WARNING: Command group 'acr reservation' is in preview and under development. Reference and support levels: https://aka.ms/CLI_refstatus
```

Exit code: **0**

Result: **PASS**. Command completed successfully.

## 49. Same-name reservation read

Input:

```powershell
azlocal acr reservation show -n eric-cli-validation-1021 -g eric-reservations-dfaue --subscription 06f5e253-d825-4052-87ec-c4f12bc8f343 -o json
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

## 50. Idempotent create does not request extra capacity

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

## 51. Minimum commitment blocks immediate delete

Input:

```powershell
azlocal acr reservation delete -n eric-cli-validation-1021 -g eric-reservations-dfaue --subscription 06f5e253-d825-4052-87ec-c4f12bc8f343 --yes --timeout 30
```

Actual Output:

```text
WARNING: option '--subscription' will be ignored due to use of '--ids'.
WARNING: Command group 'acr reservation' is in preview and under development. Reference and support levels: https://aka.ms/CLI_refstatus
ERROR: Capacity reservation request failed (HTTP 409): The reservation's minimum-commitment window has not elapsed.
```

Exit code: **1**

Result: **PASS**. Expected service-side 409; the resource remains until the commitment expires.

## 52. Recreated lifecycle: read before cleanup

Input:

```powershell
azlocal acr reservation show -n eric-cli-validation-1021 -g eric-reservations-dfaue --subscription 06f5e253-d825-4052-87ec-c4f12bc8f343 -o json
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

## 53. Recreated lifecycle: require no registry associations

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

## 54. Recreated lifecycle: delete reservation

Input:

```powershell
azlocal acr reservation delete -n eric-cli-validation-1021 -g eric-reservations-dfaue --subscription 06f5e253-d825-4052-87ec-c4f12bc8f343 --yes --no-wait
```

Actual Output:

```text
WARNING: option '--subscription' will be ignored due to use of '--ids'.
WARNING: Command group 'acr reservation' is in preview and under development. Reference and support levels: https://aka.ms/CLI_refstatus
```

Exit code: **0**

Result: **PASS**. Deletion accepted; --no-wait does not itself confirm completion.

## 55. Recreated lifecycle: wait for deletion

Input:

```powershell
azlocal acr reservation wait -n eric-cli-validation-1021 -g eric-reservations-dfaue --subscription 06f5e253-d825-4052-87ec-c4f12bc8f343 --deleted --interval 5 --timeout 120
```

Actual Output:

```text
WARNING: option '--subscription' will be ignored due to use of '--ids'.
WARNING: Command group 'acr reservation' is in preview and under development. Reference and support levels: https://aka.ms/CLI_refstatus
```

Exit code: **0**

Result: **PASS**. Deletion condition reached.

## 56. Recreated lifecycle: show deleted reservation

Input:

```powershell
azlocal acr reservation show -n eric-cli-validation-1021 -g eric-reservations-dfaue --subscription 06f5e253-d825-4052-87ec-c4f12bc8f343 -o json
```

Actual Output:

```text
WARNING: option '--subscription' will be ignored due to use of '--ids'.
WARNING: Command group 'acr reservation' is in preview and under development. Reference and support levels: https://aka.ms/CLI_refstatus
ERROR: Capacity reservation request failed (HTTP 404): The Resource 'Microsoft.ContainerRegistry/capacityReservations/eric-cli-validation-1021' under resource group 'eric-reservations-dfaue' was not found. For more details please go to https://aka.ms/ARMResourceNotFoundFix
```

Exit code: **3**

Result: **PASS**. Expected not-found exit code 3.

## 57. Recreated lifecycle: final resource-group list

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

## 58. Final retained registry state

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

- Passed CLI command checks included in this report: **56**.
- Blocked CLI command checks: **2**.
- Failed command checks: **0**.
- Test reservation cleanup: **completed**, confirmed by `wait --deleted`, show
  returning exit code 3, and an empty resource-group reservation list.
- Existing registry `ericreservationdfaue`: **Succeeded and unassociated**, preserved.
- Blockers: R1 association returns HTTP 409 because the RP requires
  `RequestRate-L`; subscription-scoped reservation listing returns HTTP 502.
- No higher-capacity tiers, traffic generation, forced scale-out, RBAC changes, or ledger mutations were run.
- Live asynchronous scale-out, real timeout/failure injection, and other-cloud behavior are not covered.
- Finished: `2026-10-21T08:01:04.556897+00:00`.
