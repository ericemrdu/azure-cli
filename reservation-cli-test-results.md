# Reservation CLI test results

Date: 2026-10-21 (UTC)

Included results: **34 CLI checks passed, 2 CLI checks blocked**.
Test reservations were cleaned up; `ericreservationdfaue` remains provisioned and
unassociated. The numbered sections below show the documented command syntax,
recorded output, and exit code.

This report validates Azure CLI integration: argument validation, request
handling, resource output, persisted updates, asynchronous operations, and
service-error reporting. JSON provides resource-state evidence. One
representative check is retained per behaviour; alternate output formats,
repeated validation variants, and duplicate lifecycle evidence are omitted.
RP allocation rules, idempotency, and minimum-commitment enforcement are not
validation targets. Service failures are recorded as integration blockers,
not successful end-to-end feature checks.

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

## 4. Create without a positive tier

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

## 5. Create with invalid short name

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

## 6. Create with invalid tier

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

## 7. Create with missing stamp

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

## 8. Create with zero timeout

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

## 9. Update without changes

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

## 10. Reject removing last positive dimension

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

## 11. Reject raw numeric capacity

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

## 12. Reject generic set bypass

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

## 13. Reject reservation on registry update

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

## 14. Show nonexistent reservation

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

Result: **PASS**. CLI surfaces the service's HTTP 404 as a resource-not-found error with exit code 3.

## 15. Capacity unchanged after negative tests

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

## 16. Registry create preflight: missing reservation

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

## 17. Registry create preflight: region mismatch

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

## 18. Registry preflight did not create a registry

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

## 19. Tags-only update

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

## 20. Tags update retained numeric dimensions

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

## 21. Clear tags

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

## 22. Add I1 using case-insensitive tier

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

Result: **PASS**. CLI accepts the case-insensitive tier `i1` and returns `I1`
with `reservedIngressGbps` 0.5; request rate remains 1 RU.

## 23. Verify ingress update persisted

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

## 24. Remove ingress with no-wait

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

## 25. Wait updated after no-wait

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

## 26. Verify None removal persisted

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

## 27. Associate existing test registry using R1

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

## 28. Association list after compatibility check

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

## 29. Subscription-scoped list

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

## 30. Recreate same name with no-wait

Run context: the original test reservation was deleted and deletion confirmed
before this command. That intermediate cleanup is summarised rather than
repeating the final deletion checks below. This check demonstrates CLI create
with `--no-wait`; it does not assert RP name-reuse semantics.

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

## 31. Wait created after name reuse

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

## 32. Same-name reservation read

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

## 33. Recreated lifecycle: delete reservation

Cleanup context: the reservation had no registry associations. Deletion was
performed after its recorded `earliestDeletableAt` time plus a 10-second clock
margin; minimum-commitment enforcement is not counted as a CLI check.

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

## 34. Recreated lifecycle: wait for deletion

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

## 35. Recreated lifecycle: final resource-group list

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

## 36. Final retained registry state

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

- Passed CLI command checks included in this report: **34**.
- Blocked CLI command checks: **2**.
- Failed command checks: **0**.
- Test reservation cleanup: **completed**, confirmed by `wait --deleted`
  and an empty resource-group reservation list.
- Existing registry `ericreservationdfaue`: **Succeeded and unassociated**, preserved.
- Blockers: R1 association returns HTTP 409 because the RP requires
  `RequestRate-L`; subscription-scoped reservation listing returns HTTP 502.
- No higher-capacity tiers, traffic generation, forced scale-out, RBAC changes, or ledger mutations were run.
- Live asynchronous scale-out, real timeout/failure injection, and other-cloud behavior are not covered.
- Finished: `2026-10-21T08:01:04.556897+00:00`.
