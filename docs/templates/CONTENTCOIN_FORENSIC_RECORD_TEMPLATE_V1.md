# CONTENTCOIN_FORENSIC_RECORD_TEMPLATE_V1

**Template ID:** `CONTENTCOIN_FORENSIC_RECORD_TEMPLATE_V1`  
**Schema:** `CONTENTCOIN_FORENSIC_RECORD_SCHEMA_V1`  
**Status:** `DRAFT_LOCKED`  
**Class:** `REPLAYABLE_FORENSIC_TEMPLATE`  
**Operator:** `jaywisdom.base.eth`  

---

## Purpose

This template standardizes future ContentCoin forensic records so that every analysis remains evidence-bounded, uncertainty-aware, and replay-legitimate.

Use this template when evaluating Zora/Base ContentCoins, low-context onchain media objects, or creator-coin surfaces with uncertain provenance.

---

## Record Header

```text
Record ID: CONTENTCOIN_FORENSIC_RECORD_<CONTRACT>_V1
Contract: <0x...>
Network: Base
Zora Page: <url_or_null>
Referrer Observed: <0x... | null>
Observed Surface Label: <label_or_null>
Record Status: EVIDENCE_BOUNDED_PRELIMINARY
Schema: CONTENTCOIN_FORENSIC_RECORD_SCHEMA_V1
```

---

## 1. Constitutional Boundary

State the evidence boundary before classification.

```text
Absence of metadata does not prove malicious origin.
Sparse provenance does not prove coordinated farming.
Referrer reuse does not prove sybil attribution.
Factory-like deployment does not prove deception without supporting checks.
```

---

## 2. Deterministic Classification

```json
{
  "classification": "LOW_CONTEXT_CONTENTCOIN | ATTESTED_CREATOR_COIN | FACTORY_PATTERN_CONFIRMED | FARM_ATTRIBUTION_CONFIRMED | INSUFFICIENT_EVIDENCE",
  "narrative_binding": "NONE | WEAK | MODERATE | STRONG",
  "identity_binding": "UNVERIFIED | WEAK | PROFILE_LINKED | WALLET_ATTESTED | STRONG",
  "replay_meaningfulness": "LOW | MODERATE | HIGH",
  "metadata_density": "EMPTY | SPARSE | PARTIAL | RICH",
  "lineage_confidence": "UNKNOWN | UNCONFIRMED_FACTORY_PATTERN | BYTECODE_MATCH_CONFIRMED | DEPLOYER_CLUSTER_CONFIRMED",
  "risk_flags": [],
  "forensic_status": "INSUFFICIENT_EVIDENCE_FOR_FARM_ATTRIBUTION"
}
```

---

## 3. Evidence-Bounded Interpretation

Write one concise paragraph.

Template:

```text
This object is classified as <classification> because <supported evidence>. The current evidence supports <bounded claims>. It does not support <unsupported claims>. Additional checks are required before stronger attribution is lawful.
```

---

## 4. Supported Claims

List only claims directly supported by observable evidence.

```text
- <supported_claim_1>
- <supported_claim_2>
- <supported_claim_3>
```

---

## 5. Unsupported Claims

List claims that are tempting but not yet lawful.

```text
- Confirmed coordinated farming operation.
- Confirmed malicious intent.
- Confirmed sybil launch cluster.
- Confirmed deceptive deployment.
- Confirmed shared deployer authority.
- Confirmed economic manipulation.
```

---

## 6. Cognitive Metadata Deficiency

Assess whether the object has enough semantic surface area for lawful interpretation.

```text
The primary deficiency is <metadata/identity/narrative/lineage/attestation> insufficiency, not proven malice. The object lacks enough cognitive metadata to be socially legible without additional forensic checks.
```

---

## 7. Cognitive Metadata Density Inputs

```json
{
  "CMD": "COGNITIVE_METADATA_DENSITY",
  "inputs": {
    "identity_binding": null,
    "narrative_binding": null,
    "media_binding": null,
    "lineage_visibility": null,
    "attestation_depth": null,
    "creator_continuity": null,
    "replay_context": null
  }
}
```

---

## 8. Replay-Legitimate Next Checks

Select only the checks needed for the next classification transition.

```text
- Holder graph analysis.
- Deploy timing cluster check.
- Bytecode equivalence test.
- Funding lineage trace.
- Mint entropy analysis.
- Referrer behavior comparison.
- Creator/profile metadata refresh check.
```

---

## 9. Boundary Rule

```text
Low-attestation does not equal malicious origin.
Sparse metadata does not equal farm attribution.
A forensic system must classify what the evidence supports, not what the pattern tempts the observer to assert.
```

---

## 10. Deep Rule

```text
The future information war is not only truth versus lies.
It is high-context objects versus low-context objects.
Low-context objects produce attribution inflation unless cognitive metadata boundaries are enforced.
```

---

## Validation Checklist

```text
[ ] contract address present
[ ] network present
[ ] schema id present
[ ] classification declared
[ ] supported claims declared
[ ] unsupported claims declared
[ ] uncertainty boundary declared
[ ] next checks declared
[ ] cognitive metadata deficiency declared
[ ] no unsupported attribution made
```

---

## Usage Rule

If the analyst cannot complete the supported/unsupported claim split, the record must remain `INSUFFICIENT_EVIDENCE`.
