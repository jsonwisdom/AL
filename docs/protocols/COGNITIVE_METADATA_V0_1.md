# Cognitive Metadata v0.1

**Protocol ID:** `COGNITIVE_METADATA_V0_1`  
**Status:** `DRAFT_LOCKED`  
**Operator:** `jaywisdom.base.eth`  
**Class:** `HUMAN_NAVIGATION_LAYER`  
**Primary Function:** Make every protocol human-navigable before it becomes machine-enforced.

---

## Invariant

A protocol is not constitutionally complete unless its cognitive burden, interpretive role, compression class, and misreading risks are explicitly declared.

Metadata is not decoration.

Metadata is the handle humans use to carry the machine.

---

## Cognitive Metadata Object

```json
{
  "cognitive_metadata": {
    "metadata_id": "sha256(canonical_metadata)",
    "protocol_ref": "CONTINUITY_COLLAPSE_PROTOCOL_V0_1",
    "operator": "jaywisdom.base.eth",
    "cognitive_role": "HUMAN_NAVIGATION_LAYER",
    "reading_level": "EXPERT | OPERATOR | CIVIC | MACHINE",
    "compression_class": "LOSSLESS_SUMMARY | OPERATIONAL_SUMMARY | CIVIC_SUMMARY",
    "semantic_tags": [
      "continuity",
      "collapse",
      "regenesis",
      "lineage",
      "temporal_integrity"
    ],
    "attention_cost": "LOW | MEDIUM | HIGH | CRITICAL",
    "interpretability_risk": "LOW | MEDIUM | HIGH | CRITICAL",
    "required_context": [
      "Temporal Drift Containment",
      "Temporal Recovery",
      "Continuity Horizon",
      "Civilizational Time Invariants"
    ],
    "summary": "Defines lawful continuity collapse and renewal without false continuity claims.",
    "danger_if_misread": "Collapse may be mistaken for erasure rather than receipt-bound discontinuity.",
    "reader_instruction": "Read as controlled disintegration, not system failure.",
    "status": "DRAFT_LOCKED"
  }
}
```

---

## Required Fields

| Field | Function |
|---|---|
| `metadata_id` | Canonical hash of the metadata object. |
| `protocol_ref` | Protocol or artifact this metadata describes. |
| `cognitive_role` | Mental job the object performs for a human reader. |
| `reading_level` | Intended audience: expert, operator, civic, or machine. |
| `compression_class` | Declares how much detail has been compressed. |
| `semantic_tags` | Searchable conceptual anchors. |
| `attention_cost` | Human verification burden estimate. |
| `interpretability_risk` | Risk that the object becomes cognitively unsafe or opaque. |
| `required_context` | Prior surfaces needed to read the object safely. |
| `danger_if_misread` | Known failure mode if interpreted incorrectly. |
| `reader_instruction` | The lawful cognitive frame for reading. |
| `status` | Draft, active, deprecated, or superseded state. |

---

## Membrane Loop

```text
PROTOCOL
→ COGNITIVE_METADATA
→ INTERPRETABILITY_CHECK
→ RECEIPT
→ REPLAY_SURFACE
```

No protocol enters the organism without cognitive metadata.

---

## Cognitive Failure Modes

| Failure | Meaning |
|---|---|
| `UNLABELED_COMPLEXITY` | Protocol imposes cognitive burden without warning. |
| `MISSING_CONTEXT` | Reader lacks required prior surfaces. |
| `FALSE_SIMPLICITY` | Compression hides important causal structure. |
| `NARRATIVE_OVERLOAD` | Story layer overwhelms replay meaning. |
| `EXPERT_CAPTURE` | Only specialists can interpret the object. |
| `MACHINE_ONLY_LEGIBILITY` | Artifact becomes technically valid but human-inhabitable. |

---

## Validation Rule

A protocol passes cognitive metadata validation only if:

```text
metadata_id exists
AND protocol_ref exists
AND cognitive_role is declared
AND reading_level is declared
AND attention_cost is declared
AND interpretability_risk is declared
AND danger_if_misread is declared
AND reader_instruction is declared
```

If any field is missing, the artifact remains cognitively incomplete.

---

## Deep Rule

A replay civilization cannot merely be correct.

It must be carryable by human minds.

Cognitive metadata is the bridge between machine-valid truth and human-survivable understanding.
