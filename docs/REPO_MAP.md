# REPO MAP

## Top-Level

- `/README.md` — operator overview (front door)
- `/docs/` — architecture, doctrine, map
- `/receipts/` — machine-readable receipts (NY-001, NY-003, etc.)
- `/data/` — canonical outputs (CSV/JSON)
- `/scripts/` — deterministic transforms (SQL, Python)
- `/agents/` — observers and validators
- `/proof/` — public HTML surfaces

## Current Contents

### Civic Proof
- `proof/computer-wisdom-public-proof.html` — live public table
- `receipts/NY-001.json` — County FIPS 62/62
- `receipts/NY-003.json` — ACS income 62/62
- `receipts/NY-004.json` — GSOD 2024 climate 6/62
- `receipts/NY-007B.json` — GSOD trends 4/62
- `receipts/NY-010.json` — Extreme events 4/62
- `receipts/NY-011S.json` — Sparse validation 4/62
- `receipts/NY-012.json` — Methodology note

### Constitutional Machine
- `scripts/` — normalization and receipt generation
- `docs/DOCTRINE.md` — immutable principles
- `docs/ARCHITECTURE.md` — verification flow

### Agent Infrastructure
- `agents/observers/` — scheduled replay jobs
- `agents/validators/` — hash and anchor checkers
- `agents/automation/` — drift detection

## How to Navigate

1. Start at README for what you can verify today
2. Read ARCHITECTURE for the flow
3. Read DOCTRINE for the rules
4. Open a receipt in `/receipts/` to replay
5. Check `/proof/` for the human-readable surface

Future states (AL, TX, etc.) will follow the same map. No re-architecture required.
