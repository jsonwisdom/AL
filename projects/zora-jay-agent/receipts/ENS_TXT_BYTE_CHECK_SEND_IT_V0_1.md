# ENS TXT Byte Check — SEND IT V0.1

STATUS: MANUAL_WORKFLOW_DISPATCH_REQUESTED
TRUTH_STATE: YELLOW_PENDING_RUN
NO_FAKE_GREEN: ACTIVE

## Target

repo: jsonwisdom/AL
workflow: .github/workflows/daily-ens-txt-byte-check.yml
workflow_name: Daily ENS TXT Byte Checker

## Names Under Test

- jaywisdom.eth = SEAL_L1
- jaywisdom.base.eth = ENGINE_L2

## Required Action

Trigger the GitHub Actions workflow manually using `workflow_dispatch`.

UI path:

1. Open `jsonwisdom/AL` on GitHub.
2. Open `Actions`.
3. Select `Daily ENS TXT Byte Checker`.
4. Click `Run workflow`.
5. Use branch `master`.
6. Click `Run workflow` again.

## Required Promotion Evidence

The system MAY NOT promote to GREEN unless all of the following exist:

- Workflow run completed.
- Resolver read-back executed for `jaywisdom.eth`.
- Resolver read-back executed for `jaywisdom.base.eth`.
- Every required TXT record matched exact UTF-8 bytes.
- Runtime report artifact exists.
- Baseline artifact exists beside the runtime report.

## If Failure Occurs

Failure is useful. Preserve the artifact. The artifact should expose:

- missing key
- attempted resolver key candidates
- expected UTF-8
- expected byte length
- expected SHA-256
- expected bytes hex
- actual value fields when available

## Ruling

SEND_IT_REQUESTED: TRUE
CONNECTOR_DISPATCH_AVAILABLE: FALSE
MANUAL_DISPATCH_REQUIRED: TRUE
GREEN_BLOCKED_UNTIL_ARTIFACT_READBACK: TRUE
