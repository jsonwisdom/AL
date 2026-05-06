# MINNESOTA_FIXTURE_001 — Intake Pending

## Status

`INTAKE_PENDING_SOURCE_URI`

---

## Constitutional State

```text
KERNEL_STATUS: SEALED
REPLAY_COURT_STATUS: SEATED_V1
REPLAY_AUTHORITY: ACTIVE
ADMISSIBILITY_GATE: OPEN_FOR_LAWFUL_FIXTURES
NEXT_LAWFUL_CASE: MINNESOTA_FIXTURE_001
```

---

## Required Fields Before Fixture Admission

The fixture MUST NOT be added to the replay harness until these fields are filled with real public-record evidence:

```json
{
  "case_id": "MINNESOTA_FIXTURE_001",
  "source_title": "<official Minnesota public record title>",
  "source_uri": "<exact public source URL>",
  "publisher": "<official publisher>",
  "retrieved_at": "<ISO-8601 retrieval timestamp>",
  "source_type": "json",
  "canonical_inline_json": {},
  "transform_policy": "ALMS_JSON_INLINE_CANONICAL_V1",
  "expected_verdict": "PASS"
}
```

---

## Admission Rule

No source URI, no fixture.

No retrieval timestamp, no fixture.

No canonical bytes, no replay.

No declared transform policy, no admissibility.

---

## Initial Target

The first civic case SHOULD use a small JSON object derived from a Minnesota public record, not a PDF transform.

PDF parsing and source-document transforms are future cases.

The first civic case must prove the seated court path without parser drift.

---

## Final Rule

Do not register `MINNESOTA_FIXTURE_001` in `tests/run_replay_cases.py` until the source fields are complete and the canonical digest is computed from exact bytes.

Verify > narrative.
