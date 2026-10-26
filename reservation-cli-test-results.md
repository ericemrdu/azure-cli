# Reservation CLI test results

Date: 2026-10-21 (UTC)

Results: **25 CLI checks passed, 2 CLI checks blocked**.

Scope: Azure CLI reservation integration, including argument validation,
resource output, updates, asynchronous operations, and error reporting.
RP behaviour is outside scope; service failures are recorded as blockers.

Environment: local worktree CLI (`azlocal`) against Dogfood. Commands ran
sequentially using one R1 test reservation, with I1 temporarily enabled.
No `az rest`, direct HTTP workarounds, or load tests were used.

Command examples use `-n`, `-g`, and `--subscription`. Some were converted from
`--ids` and have not been rerun; their recorded outputs retain the original
ignored-subscription warnings.

Output contract update: reservation results now expose tier fields without
`reservedRequestRate`, `reservedEgressGbps`, or `reservedIngressGbps`. The
recorded outputs below predate this change and remain unchanged.

Each check includes its command, recorded output, exit code, and result.
Where both streams contain output, stderr precedes stdout. `(no output)`
denotes empty streams. Expected rejections count as passed validation checks,
not successful operations.

Started: `2026-10-21T07:52:24.154041+00:00`.

## 1. Confirm the Dogfood cloud endpoint

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

Result: **PASS**.

## 2. List reservations in a resource group

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

Result: **PASS**.

## 3. Show reservation as JSON

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

Result: **PASS**. Internal stamp properties are absent from the public output.

## 4. Reject reservation creation without a specified tier

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

Result: **PASS**.

## 5. Historical rejection of a two-character reservation name

The CLI now accepts reservation names of 1-63 characters. This recorded
rejection predates that change and does not validate the current length limit.

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

Result: **PASS**.

## 6. Reject an unsupported request-rate tier

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

Result: **PASS**.

## 7. Reject reservation creation without a stamp ID

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

Result: **PASS**.

## 8. Reject a zero operation timeout

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

Result: **PASS**.

## 9. Reject a reservation update without changes

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

Result: **PASS**.

## 10. Reject removal of the last positive capacity tier

The reservation has `R1` and no ingress/egress capacity.

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

Result: **PASS**.

## 11. Reject an unsupported numeric capacity argument

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

Result: **PASS**.

## 12. Reject generic property updates through --set

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

Result: **PASS**.

## 13. Reject --reservation on registry update

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

Result: **PASS**.

## 14. Report a reservation-not-found error

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

Result: **PASS**.

## 15. Reject registry creation with a missing reservation

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

Result: **PASS**. Rejected during preflight, before registry creation.

## 16. Reject registry creation with a reservation in another region

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

Result: **PASS**. Rejected during preflight, before registry creation.

## 17. Update reservation tags without changing capacity

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

Result: **PASS**. CLI returns the requested tags, with request rate still 1 RU
and ingress/egress capacity still zero.

## 18. Add ingress capacity using a lowercase tier

Tags had been cleared before this update; the empty `tags` object is not a
side effect of the tier change.

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

## 19. Remove ingress capacity with no-wait

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

Result: **PASS**. Submission only; completion is checked below.

## 20. Wait for the ingress update to complete

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

Result: **PASS**.

## 21. Associate an existing registry with an R1 reservation

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

Result: **BLOCKED**. CLI surfaces HTTP 409 and exits with code 1 because the
deployed RP requires `RequestRate-L`, while the CLI accepts `R1`-`R64`.
Successful association is not validated.

Disassociation of an established association and successful registry creation with `--reservation` remain **BLOCKED** by the tier mismatch. An unassociated-registry disassociate call is not counted as a substitute.

## 22. List registries associated with a reservation

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

Result: **PASS**. Empty-list path only; output for an established association
is not validated.

## 23. List reservations across a subscription

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

Result: **BLOCKED**. CLI surfaces the service/ARM HTTP 502 collection error and
exits with code 1. Successful subscription-wide listing is not validated.

## 24. Create reservation with no-wait

The original test reservation was deleted before this command.

Input:

```powershell
azlocal acr reservation create -n eric-cli-validation-1021 -g eric-reservations-dfaue --subscription 06f5e253-d825-4052-87ec-c4f12bc8f343 -l australiaeast --stamp-id dfaue-1 --request-rate-tier R1 --tags cliTest=name-reuse --no-wait -o json
```

Actual Output:

```text
WARNING: Command group 'acr reservation' is in preview and under development. Reference and support levels: https://aka.ms/CLI_refstatus
```

Exit code: **0**

Result: **PASS**. Submission only; completion is checked below.

## 25. Wait for creation

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

Result: **PASS**.

## 26. Delete reservation with no-wait

The reservation had no registry associations. Deletion ran after
`earliestDeletableAt` plus a 10-second clock margin.

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

Result: **PASS**. Submission only; completion is checked below.

## 27. Wait for deletion

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

Result: **PASS**.

## Run summary

- Passed CLI command checks: **25**.
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
