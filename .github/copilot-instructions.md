# ALMS Repository Instructions

Core rule:
Do not invent truth. Do not mutate verification state unless explicitly required.

ALMS purpose:
Convert claims into reproducible, receipt-backed verification artifacts.

Repository boundaries:
- `_truth/` is source-of-truth state.
- `scripts/` contains deterministic builders and audit tools.
- `docs/` contains doctrine and operator guidance.
- `studio/` contains human-facing visual and publishing surfaces.
- `contracts/` contains protocol and execution code.

Hard constraints:
- Bash-first.
- No private keys.
- No terminal signing.
- No RPC unless explicitly requested.
- No homepage edits unless explicitly requested.
- No `UNKNOWN_HASH` in production.
- Do not manually edit Merkle roots.
- Rebuild roots through scripts only.
- Run preflight audit before proposing commits.

If uncertain, stop and mark:
ALMS_REVIEW_REQUIRED
