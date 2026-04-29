# ALMS Verification — 2026 Q2

Single-command, offline verification of ALMS batch integrity and ENS calldata.

## 1. Run

```bash
chmod +x verify_alms_2026_Q2.sh
./verify_alms_2026_Q2.sh
```

Optional adversarial audit:

```bash
RUN_AUDIT=1 ./verify_alms_2026_Q2.sh
```

## 2. What This Never Does

- No RPC calls — zero network
- No signing — terminal never touches keys
- No mutation — read-only execution
- No config — hardcoded paths
- No trust — every value recomputed

## 3. Expected Output

Success:

```
ALMS_VERIFY_OK epoch=2026-Q2 root=0x...
```

Exit code: 0

Failure:

```
VERIFY_FAIL <reason>
```

Exit code: 1

## 4. Dependencies

- jq
- sha256sum
- xxd
- Foundry (cast)

Install Foundry:

```bash
curl -L https://foundry.paradigm.xyz | bash && foundryup
```

Verify keccak:

```bash
cast keccak hello
```

## 5. How to Falsify This

1. Edit `_truth/attest/witness/*.json` → must FAIL
2. Add extra witness file → STRICT_MODE=1 must FAIL
3. Edit batch manifest → must FAIL
4. Tamper calldata → must FAIL

Any mutation that passes = system failure.

## 6. Boundary Statement

Terminal: generates + verifies only
Browser: signs ENS setText
GitHub: stores receipts
ENS: anchors identity

Any path where terminal signs or calls RPC is a critical vulnerability.
