# DRFT-002-STRANGER-COURT: Stranger-Friendly Replay Court Deployment

## Status
RESOLVED — public replay membrane deployed on `master` using only artifacts that exist in the repository.

## Detection
During remote verification, the proposed ALMS delegation paths were not present on `master`:

- `verify_alms_2026_Q2.sh` — not found
- `scripts/verify_alms_batch.sh` — not found

Referencing those scripts from the public oath would have created a phantom constitutional layer.

## Resolution
The public oath was constrained to live, auditable artifacts:

- `verify.sh` — stranger-facing Clerk
- `src/matrix_runner.py` — deterministic SHA-256 court logic
- `Dockerfile.replay` — portable replay chamber

The court now emits:

- `REPLAY_CONFIRMED`
- `ROOT`
- `MATRIX: GREEN`
- `Execution ≡ Registry holds.`

## Deployment Receipts

- Matrix runner deployed: `e80f4798c80c2d2025551406ef5dda6ff0479fcf`
- Public oath activated: `d431c04a3b1ec7b3d3f14897503e50e5d48b09e1`
- Docker replay chamber added: `c8536b37ee2c390bf306aef04a8775f170cf8ea9`
- Full verdict surface emitted: `09aed9388e52b8467cbd236d582d6576a164e72d`

## Invariant
No phantom scripts. No assumed infrastructure. No ceremonial green.

Only executable artifacts on `master` may participate in the public oath.

## Stranger Test

```bash
git clone https://github.com/jsonwisdom/AL.git
cd AL
docker build -t al-court -f Dockerfile.replay .
docker run --rm al-court
```

Expected verdict:

```text
REPLAY_CONFIRMED
MATRIX: GREEN
Execution ≡ Registry holds.
```

## Closure
The membrane is small, boring, auditable, and real.
