# CW Rounding Receipt v0.1 — proposed accounting standard

STATUS: DRAFT / CI-FIRST / NO PRODUCTION AUTHORITY

**Unit:** 1 CW micro-unit = USD 1/100000 = $0.00001 (one thousandth of one cent). All monetary calculations use signed integers, never IEEE-754 floating-point.

**Three different zeroes**
1. Exact zero: raw signed micro-unit sum = 0.
2. Display zero: nonzero sum is rendered as $0.00 at two-decimal precision.
3. Settlement/legal zero: nothing presently payable under the stated contract, threshold, rounding, or write-off rule. No legal obligation is inferred from an internal ledger entry.

**Required receipt fields**
- receipt_version, receipt_id, as_of_utc, currency (USD), unit_scale (100000 per USD)
- source_manifest_sha256, source_count, evidence_refs (including provenance and permissions)
- raw_units (signed integer), rounding_stage ("aggregate_then_settle"), settlement_rule_id, settlement_rule_version
- settlement_increment_units (1000 per cent), settled_units (signed integer), remainder_units (signed integer)
- remainder_disposition ("carry_forward" | "contractual_write_off" | "settlement_adjustment"), disposition_authority_ref
- operator_signature_ref (optional; absent is **UNSIGNED**, not invalid), workflow_commit_sha, workflow_run_id (optional pending CI)
- accounting_status (SIMULATED | VERIFIED_RECORD | SETTLED). A hash, signature or CI pass **never** implies a payment was made.

**Invariants**
- raw_units = settled_units + remainder_units (signed; never discard remainder)
- sum raw integer micro-units before applying settlement rounding once
- settlement is recorded only on independent transaction/bank evidence
- each change appends a new receipt linking prior receipt hash; do not overwrite history
- positive and negative amounts, refunds, non-cent settlements, and all rounding tie conventions must be covered by an explicit policy
- reject missing source evidence, double settlement, integer overflow, unsigned authorization, unverifiable signature, or contradictory policy

**Illustrative synthetic replay**
- 1,000 entries x 1 micro-unit = 1,000 micro-units = $0.01000
- premature per-entry truncation to cents: $0.00; aggregate before truncation: $0.01
- aggregate settlement: 1,000 units; carry remainder: 0; conservation PASS
- 1,234 units = $0.01234; truncation-to-cent settles 1,000 units ($0.01), carries 234 units ($0.00234)
- no bank obligation, earnings, actual settlement, tax treatment, or income established by either sample

**Cloudflare design (not deployed):** Workers serves public verification; a controlled single-writer Durable Object/transactional DB serializes authorized receipts; R2 stores public manifests; GitHub Actions replays checks. Never treat KV as the authoritative concurrent write ledger. Gate private records and signatures; never expose private financial data. No wallet connection required for read-only verification.

**Operator boundary:** human signs exact, typed approval packet only after source/hashes/policy verification. Approval, acknowledgment, spending, publication and settlement are distinct permissions. GLOBAL HOLD on production changes, wallet signatures, transfers, and merges.
