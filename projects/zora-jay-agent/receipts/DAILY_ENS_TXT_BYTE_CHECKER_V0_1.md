# DAILY_ENS_TXT_BYTE_CHECKER_V0_1

STATUS: WORKFLOW_ADDED
TRUTH_STATE: YELLOW_UNTIL_FIRST_RUN
NO_FAKE_GREEN: ACTIVE

## Problem

`jaywisdom.eth` TXT records had not been checked in months.
That is a witness-layer hygiene failure.

The L1 Seal and L2 Engine must be checked by resolver read-back, not by memory, screenshots, or narrative.

## Names

- `jaywisdom.eth` = SEAL_L1
- `jaywisdom.base.eth` = ENGINE_L2

## Added Files

- `.github/workflows/daily-ens-txt-byte-check.yml`
- `scripts/ens_txt_byte_checker.mjs`
- `projects/zora-jay-agent/config/ens_txt_byte_baseline_v0_1.json`

## Daily Workflow

The workflow runs daily and can also be triggered manually with `workflow_dispatch`.

It performs byte-for-byte ENS TXT resolver read-back against the expected UTF-8 values.

## Baseline Preserved

### Public Key

```text
did:key:jaywisdom-v1
```

### Verified Root Material

```text
root=sha256:65377be53afaa04856a5bad16a6f90481ef703e4ce1af35763647f0dbb86d460;commit=03e0e1711a6294d8a35b478a5b90ee17046b2f64;advisory=ipfs://QmbrGfzwy5DmzGhE5Txscs7BfaRknNosc3G5r1pfQEsdqF
```

## Failure Policy

The checker fails on:

- missing resolver
- missing TXT record
- empty TXT record
- byte mismatch
- unreadable `jaywisdom.base.eth` path

A failure does not mean identity failure.
A failure means the witness layer is not allowed to claim GREEN.

## Promotion Rule

GREEN requires:

1. workflow run completes,
2. resolver read-back succeeds,
3. expected bytes match actual bytes,
4. report artifact exists,
5. no strict failure remains.

Until then:

```text
TRUTH_STATE: YELLOW_UNTIL_FIRST_RUN
NO_FAKE_GREEN: ACTIVE
```
