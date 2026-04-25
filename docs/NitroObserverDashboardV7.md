# Nitro Observer Dashboard v7 (Base)

This note defines the **v6 → v7** dashboard behavior for
`NitroEnclaveVerifier` observer feeds.

## Feed fields expected

From `_truth/base/nitro_observer_feed.json`:

- `networks.<chain>.revoker_event_state.last_revoker`
- `networks.<chain>.revoker_live`
- `networks.<chain>.revoke_call_state.total_calls`
- `status.role_visibility`
- `status.live_revoker_visibility`
- `status.action_visibility`
- `status.alerting`

## UI row: dual revoker visibility

Show event-derived and live storage side by side:

```
Revoker (Event-derived) | Revoker (Live Storage) | Drift
UNKNOWN                 | 0x0000...0000          | MATCH (SAFE)
```

Interpretation:

- `last_revoker = UNKNOWN` means **no `RevokerUpdated` event seen**.
- `revoker_live = 0x0000000000000000000000000000000000000000` is an explicit
  live-state read indicating no active revoker.

## Status logic (per chain)

- **GREEN: BASELINE CLEAN**
  - `revoker_live == 0x0000000000000000000000000000000000000000`
  - `revoke_call_state.total_calls == 0`
- **YELLOW**
  - any read-path error (for example `READ_ERROR` in a collector)
  - or mismatch requiring operator review
- **RED**
  - `revoker_live` is non-zero
  - or `revoke_call_state.total_calls > 0`

## Suggested jq snippets

### Compact per-chain panel data

```bash
jq '{
  generated_at,
  contract,
  chains: (
    .networks
    | to_entries
    | map({
        chain: .key,
        event_revoker: .value.revoker_event_state.last_revoker,
        live_revoker: .value.revoker_live,
        revoke_calls: .value.revoke_call_state.total_calls,
        state: (
          if (.value.revoker_live != "0x0000000000000000000000000000000000000000") or (.value.revoke_call_state.total_calls > 0)
          then "RED"
          elif (.value.revoker_event_state.last_revoker == "READ_ERROR") or (.value.revoker_live == "READ_ERROR")
          then "YELLOW"
          else "GREEN"
          end
        )
      })
  )
}' _truth/base/nitro_observer_feed.json
```

### Text table for terminal dashboards

```bash
jq -r '
  ["chain","event_revoker","live_revoker","revoke_calls","state"],
  (.networks|to_entries[]|[
    .key,
    .value.revoker_event_state.last_revoker,
    .value.revoker_live,
    (.value.revoke_call_state.total_calls|tostring),
    (if (.value.revoker_live != "0x0000000000000000000000000000000000000000") or (.value.revoke_call_state.total_calls > 0) then "RED"
     elif (.value.revoker_event_state.last_revoker == "READ_ERROR") or (.value.revoker_live == "READ_ERROR") then "YELLOW"
     else "GREEN" end)
  ])
  | @tsv
' _truth/base/nitro_observer_feed.json
```

## Operator note

The v7 panel removes ambiguity by treating live storage as the source of truth,
while preserving event-derived context for drift and observability.
