# Apple Blossom Awesome — CI-FIRST reverse replay (2026-11-23)

Receipt: MN-DATA-BROKER-2026-11-23
Disposition: STATEWIDE SCOPE — HOLD
Execution class: LOCAL RECONSTRUCTION / SYNTHETIC TESTING, **NOT BYTE-FOR-BYTE ORIGINAL SOURCE VERIFICATION**.

## Runtime results
- Local Python 3.13 execution of reconstructed validator and nine synthetic tests: **8 passed, 1 failed**.
- Failure: `test_original_required_hold` expected HOLD but got FAIL because the fixture had `source_documents.agency_id=None`, violating the required field rule. The validator correctly prioritized the schema FAIL.
- Local corrected fixture adds a valid synthetic agency and references it in the source-document record. **9/9 passed** in local Python runtime. This is a corrected *test fixture*, not a correction to a real-world procurement record.
- The original GitHub test remains unchanged; corrected test committed as `test_registry_validator_corrected.py`.

## SHA-256 of local reconstructed artifacts
- validate_registry.py: `09a8a0bd168bde4f99b575a48b0a3b586e295c4d9a7a5ccf4fb103802c9dce33`
- original test_registry_validator.py: `08ab8196afbda2ba3bc29c1750d89b3665fd247fc71f42527702a4d0f11b7191`
- failing test log: `a1b5593abe654ddada0ebc32e9d30653d8d09281e447bfd20201826ac1779820`
- corrected test file: `fd9771d49b53a51dabde5297dbe4f7a2bca37d4c9f286020f65f3ca9e35744a4`
- corrected test log: `07c4560351dfb86bcab74ca8aede885fd80e675d9cbdb6e36c2f69462a03c01e`

**Hash boundary:** these are hashes of local reconstructed bytes. They do not authenticate the GitHub originals. Logs are retained locally in the ChatGPT execution environment, not uploaded to GitHub.

## Four additional adversarial reverse-replay probes (local)
1. Empty `registry.agencies` array -> PASS: two expected agency identifiers are not enforced.
2. Duplicate county names with distinct IDs -> PASS: county-name uniqueness is not enforced.
3. Foreign-key specification with nonexistent target column -> PASS: referenced target-column validity is not enforced.
4. Synthetic `source_documents` row marked VERIFIED with a matching hash of synthetic bytes -> PASS: cryptographic integrity alone does not prove source authenticity or real procurement.

**Classification:** 4 validation coverage gaps; not evidence of any Minnesota purchase or surveillance.

## Required next safeguards
- Require exact agency ID set (DPS/BCA and DOC) and statuses.
- Validate 87 distinct canonical county names and ID-name pairs against authoritative source.
- Validate foreign-key target field against declared primary keys.
- Split SHA-256 byte integrity from provenance/authenticity and procurement classification; a hash match alone cannot confer VERIFIED evidence status.
- Preserve FAIL and HOLD semantics; never treat empty transaction tables as evidence of zero activity.
- Execute byte-identical GitHub checkout and hash inputs before declaring source-equivalent runtime PASS.

## Authority gates
- No agency contacts or MGDPA transmissions.
- No production merge or Cloudflare deployment.
- No verified procurement records.
- All existing agency requests remain HOLD_NOT_SENT.
