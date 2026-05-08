# Agent SDK

Status: LOCAL_MEMBRANE_HARNESS

The Agent SDK lets contributors test whether an agent is constitutionally bounded before opening a PR.

It enforces:

- `agents/<agent_id>/manifest.yaml` exists
- manifest conforms to `schemas/agent_manifest_v0.1.schema.json`
- lifecycle is runnable
- target URLs stay inside `allowed_domains`
- URL schemes match `allowed_url_schemes`
- emitted verdicts stay inside `allowed_verdicts`
- receipts do not include forbidden fields

## Usage

```bash
python agent-sdk/harness.py agents/four04_crawler/manifest.yaml
```

## Boundary

The SDK does not prove an agent is correct.

It proves only that the agent's declared constitutional boundary is machine-checkable.

## Non-Claims

The SDK does not provide:

- adjudication
- risk scoring
- trust scoring
- interpretation
- RAP unlock access
- mainnet authority

## State

```json
{
  "agent_sdk": "LOCAL_MEMBRANE_HARNESS",
  "purpose": "pre-PR boundedness check",
  "authority": "NONE",
  "no_ghost_anchor": true
}
```
