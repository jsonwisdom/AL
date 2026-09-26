# Minnesota — Canonical Civic Memory Root

## State

```text
STATE_FIXTURE_001              = MINNESOTA
NO_FAKE_GREEN                 = TRUE
HUMAN_REVIEW_REQUIRED         = TRUE
SILENCE_IS_NOT_CONSENT        = TRUE
MINORITY_REPORT_PRESERVED     = TRUE
WOMENS_OPINIONS_PRESERVED     = TRUE
MODEL_AUTHORITY               = FALSE
```

This folder is the canonical organizational root for Minnesota material in `jsonwisdom/AL`.

It is designed to contain Minnesota source documents, receipts, fiscal replay work, governor records, county and city records, scripts, manifests, organizational frameworks, minority reports, and review queues.

## Migration principle

Minnesota material is not moved through an unreviewed bulk rename.

```text
DISCOVER
→ CLASSIFY
→ PREFLIGHT
→ HASH
→ MOVE
→ REWRITE ACTIVE REFERENCES
→ VERIFY DESTINATION HASHES
→ BUILD MANIFEST
→ ISSUE RECEIPT
→ OPEN DRAFT PR
```

Source evidence remains byte-preserved. Active scripts, workflows, and documentation may have path references updated. Ambiguous material is placed in a human-review queue instead of being guessed into or out of Minnesota.

## Repeatable action trigger

After the framework PR is merged:

1. Open the repository **Actions** tab.
2. Select **Minnesota Canonical Folder Migration**.
3. Choose **Run workflow**.
4. Run `dry-run` first.
5. Download and inspect the migration-plan artifact.
6. To apply, run again using mode `apply` and enter exactly:

```text
MOVE_MINNESOTA_WITH_RECEIPTS
```

Apply mode never commits directly to `master`. It creates an isolated migration branch and opens a **draft pull request**.

Running the action again is safe. Already-moved material converges to no changes, while newly added or newly classified Minnesota material can be captured in a later receipt.

## Governance frameworks

- [`MINNESOTA_ORGANIZATIONAL_FRAMEWORK_V1.md`](governance/MINNESOTA_ORGANIZATIONAL_FRAMEWORK_V1.md)
- [`WOMENS_OPINION_RECORD_SCHEMA_V1.json`](governance/WOMENS_OPINION_RECORD_SCHEMA_V1.json)
- [`MINORITY_REPORT_MOM_EDITION_V1.md`](governance/MINORITY_REPORT_MOM_EDITION_V1.md)
- [`CIVILIAN_RESISTANCE_GOBLINS_OF_SILENCE_V1.md`](governance/CIVILIAN_RESISTANCE_GOBLINS_OF_SILENCE_V1.md)

## Minority Report: Mom Edition

County-level Mobile Oversight and Mutual-Support Units preserve local facts, needs, women’s opinions, dissent, and unanswered questions during outages and emergencies.

```text
MOMS = Mobile Oversight and Mutual-Support Units
KAREN = Knowledge, Accountability, Resilience, and Emergency Network
```

These are civilian resilience and lawful oversight frameworks. They create no police, military, emergency-command, or vigilante authority.

## Goblins of Silence

The Goblins of Silence are process failures—not labels for people:

```text
NO RECORD
NO RESPONSE
NO VERSION HISTORY
NO NAMED AUTHORITY
NO DEADLINE TRACE
NO MINORITY REPORT
NO RECEIPT
```

Civilian Resistance answers those patterns through nonviolent documentation, verification, organization, mutual aid, and replayable receipts.

## Files controlling migration

- `MIGRATION_POLICY_V1.json` — classification, immutability, review, and governance rules
- `automation/migrate_minnesota_v1.py` — deterministic migration engine
- `automation/test_migrate_minnesota_v1.py` — disposable-repository safety tests
- `.github/workflows/minnesota-canonical-migration.yml` — manual dry-run/apply trigger
- `.github/workflows/minnesota-migration-tests.yml` — migration test gate

## Authority boundary

Moving a document does not change its meaning, authenticity, legal effect, or authority.

A receipt proves what the migration process did. It does not prove every claim contained in the migrated material.
