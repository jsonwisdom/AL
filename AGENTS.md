# ALMS Agent Rules

Copilot and agents may do implementation labor only.

Allowed:
- Create scripts
- Improve docs
- Add tests
- Build audit reports
- Open PRs

Forbidden:
- Claim verification succeeded unless scripts prove it
- Treat status.json as canonical unless scope is declared
- Rewrite receipt history
- Delete tombstones
- Create UIDs or final receipts from pending logs
- Touch wallet/private-key/signing flows

Required PR block:

ALMS_CHANGE_SUMMARY:
_truth_changed:
merkle_changed:
status_surface_changed:
commands_run:
reproduction_result:
risk:
