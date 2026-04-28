# ALMS Operator Guide

**ALMS — A Deterministic Truth Machine**

Proof > Narrative ⚙️

---

## 1. What This Is

ALMS = Receipts Machine

Purpose: convert public claims into verifiable, replayable truth.

Core rule: if it cannot be independently verified, it does not count.

---

## 2. System Architecture

```txt
INPUT → RECEIPT → HASH → MERKLE ROOT → ANCHOR → VERIFY
```

Layers:

```txt
_truth/   = source of truth: receipts, ledger, Merkle state
scripts/  = deterministic builders and audit tools
studio/   = human-facing modules: visuals, dashboards, learning, publishing
docs/     = schemas, protocol definitions, operator guidance
```

---

## 3. Core Commands

```bash
./scripts/build_merkle_root.sh
./scripts/export_live_dashboard.sh
./scripts/preflight_repo_audit.sh
```

`preflight_repo_audit.sh` is mandatory before commits that affect verification state.

---

## 4. Verification Flow

```txt
ENS → ROOT → MANIFEST → RECEIPT → ARTIFACT
```

Operator checklist:

1. Resolve root.
2. Fetch manifest.
3. Locate receipt.
4. Recompute hash.
5. Match artifact.

If any step fails, the claim is not verified.

---

## 5. Non-Negotiable Rules

1. No `UNKNOWN_HASH` in production.
2. No homepage changes without audit.
3. No manual mutation of receipt state without rebuilding Merkle root.
4. All outputs must be reproducible.
5. One source of truth per claim.

---

## 6. Module Boundaries

```txt
_truth/            = verification data layer
scripts/           = execution layer
studio/live-intel/ = experimental visual command surface
docs/              = doctrine and operator instructions
```

Do not use live visual modules as source truth.

---

## 7. Adding a New Claim

```bash
# 1. Add receipt
_truth/receipts/CLAIM.json

# 2. Build optional visual card
./scripts/build_mn_card.sh CLAIM

# 3. Rebuild Merkle root
./scripts/build_merkle_root.sh

# 4. Audit
./scripts/preflight_repo_audit.sh

# 5. Commit
git add .
git commit -m "Add CLAIM"
git push
```

---

## 8. Operator Mindset

You are not publishing content.

You are maintaining a verification machine.

Every output must survive:

- recomputation
- adversarial inspection
- time
