# Qwen Replay Adapter — Phase 0 Design

## Contract

- `MODE_OBSERVE`: behavior-preserving observability.
- `MODE_ENFORCE`: optional denial before tool execution; behavior-changing by design.
- Boundary: composition around `BaseTool.call`.
- Requested parameters are hashed but passed unchanged to the underlying tool.
- `requested_arguments_hash` and `executed_arguments_hash` are mandatory.
- If they differ, `mutation_source` is mandatory or verification fails.
- `call_index` is run-global and lock-protected.
- Thread-local state is reserved for parent context only.
- QV_005 tests deterministic nested graph semantics, not real concurrency.
- QV_006 real parallel ordering is deferred.

## Canonicalization

Phase 0 uses recursive Unicode NFC normalization plus deterministic Python JSON encoding:

`json.dumps(sort_keys=True, separators=(",", ":"), ensure_ascii=False, allow_nan=False)`

Future work: RFC 8785 JCS, dual-hash migration, then deprecation of the Python profile.

## Manifest

Generation and verification are separate operations:

```bash
python scripts/generate_manifest.py
python scripts/verify_manifest.py
```
