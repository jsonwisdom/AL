# Reproduce Constitutional Agent v0.1.0

Run from this directory:

python scripts/demo.py

Expected cases:
- happy_path -> PASS, $0.42
- refusal_write_denied -> PASS_WITH_REFUSAL, R-001_WRITE_DENIED
- missing_anchor_rejected -> REJECT, NO_ANCHOR_NO_COVERAGE

Expected final line:
CONSTITUTIONAL EXECUTION CELL: PASS
