# Glass-Box Republic (AL)

> *The right to see the walls — and to challenge what’s inside them — is now protocol.*

**Status:** LIVE — Governance V1 Active  
**Registry of Record:** This repository  
**Protocol Signature:** `GLASS_BOX_REPUBLIC_GENESIS`

---

## What This Is

The Glass-Box Republic is a constitutional architecture for agentic systems. It defines machine-native due process for automated execution: tamper-evident receipts, adversarial challenge, binding remedies, and separated enforcement.

It is not a company. Not a platform. Not a product.  
It is a **protocol for contestability** — the minimum viable constitution for a world where AI agents mediate economic and social reality.

---

## Constitutional Core

| Layer | Schema | Function |
|-------|--------|----------|
| Receipt | `RECEIPT_V1` | Self-justiciable execution record |
| Challenge | `CHALLENGE_V1` | Hybrid evidentiary-remedial dispute resolution |
| Settlement | `SETTLEMENT_PROTOCOL_V1` | Finality, sanctions, escrow |
| Escalation | `ESCALATION_LOGIC_V1` | Multi-jurisdictional referral |
| Settlement Receipt | `SETTLEMENT_RECEIPT_V1` | Tamper-evident proof of finality |

**Invariant:** No execution without receipt. No receipt without challenge surface. No remedy without separated enforcement.

---

## Verifier (Executable Courthouse)

The verifier is the replay supremacy engine.

Current status:
- Constitutional schemas frozen under `GOVERNANCE_V1`
- Rust verifier crate active under `/verifier`
- Golden heartbeat test committed
- Current replay engine posture: `VERIFIER_ERROR` no-op court

### Clean Operator Bring-Up

Use a clean shallow clone of `master`:

```bash
rm -rf AL

git clone --depth 1 --branch master https://github.com/jsonwisdom/AL.git AL

cd AL/verifier
cargo test
```

### Expected Current Heartbeat

The current verifier intentionally emits:

```json
{
  "status": "VERIFIER_ERROR"
}
```

This is constitutional and expected until deterministic replay execution is implemented.

### Golden Fixtures

Fixtures live at:

```text
/tests/fixtures/receipt_valid_v1.json
/tests/fixtures/verdict_verifier_error_v1.json
```

The golden test performs exact JSON equality against the committed verdict fixture.

---

## Repo Rules

1. **Canonical Immutability:** Schemas are never altered — only versioned with full audit trails.
2. **Replay Supremacy:** Every commit must be replay-verifiable against current schema hashes.
3. **Governance Versioning:** All logic must reference a `GOVERNANCE_V1` compatible anchor.

---

## Activation

This repository was activated by `ACTIVATION_V1` manifest commit. From that point, it is the Registry of Record for the Glass-Box Republic protocol.

**The system is live.**
