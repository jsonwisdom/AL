# AL User Manual — Jay's Wisdom

## Purpose

AL is a receipt machine for public claims.

It turns a claim into a verifiable chain:

```text
source bytes → extracted text → canonical claim → ledger entry → manifest → root → anchor
```

The rule is simple:

> Verification over narrative. Claims must be testable from receipts.

---

## What AL Verifies

Anchor #1 currently verifies four Minnesota budget rows from the February 2026 Minnesota Management and Budget forecast:

| # | Claim | Value |
|---|-------|-------|
| 001 | Health & Human Services | 25,808,265 |
| 002 | Public Safety & Judiciary | 3,640,627 |
| 003 | E-12 Education | 25,869,108 |
| 004 | Higher Education | 4,015,828 |

Current public root:

```text
sha256:2296352053488d28c6517523e0392080d3cef10724db0e2142779572c6179d7a
```

Public manifest:

```text
https://raw.githubusercontent.com/jsonwisdom/AL/master/docs/verified-claims.json
```

ENS anchor:

```text
jaywisdom.eth → al.verified_claims
```

---

## When To Use AL

Use AL when a public claim needs a receipt-backed proof path.

Good fits:

- budget line items
- public financial claims
- official government document excerpts
- public records where exact source text matters
- claims that should survive screenshots, reposts, edits, and narrative drift

Do not use AL for:

- rumors
- opinions
- claims without a source document
- screenshots without source bytes
- broad summaries that cannot be checked against exact text

---

## Where The System Lives

Core repository:

```text
https://github.com/jsonwisdom/AL
```

Primary files:

```text
claims/                         canonical claim JSON files
_truth/ledger.jsonl             append-only VCLP ledger
docs/verified-claims.json       generated public manifest
docs/ipfs-anchor.txt            current root anchor metadata
docs/ANCHOR_001.md              human-readable Anchor #1 record
scripts/verify_verified_claims_root.sh
scripts/check_verified_claims_manifest.sh
scripts/auto_append_mn_budget_claims.sh
```

Lowest-impact public witness:

```text
https://raw.githubusercontent.com/jsonwisdom/AL/master/docs/verified-claims.json
```

GitHub Pages is optional. ENS is used only for final sealed roots, not routine updates.

---

## Why AL Exists

Institutions often publish claims faster than citizens can verify them.

AL makes verification cheap and repeatable:

- exact source text is preserved
- claim hashes are deterministic
- ledger history is append-only
- public manifest is generated, not hand-curated
- CI rejects drift
- ENS anchors sealed states outside GitHub

The system does not ask people to believe Jay.

It asks them to recompute the root.

---

## How To Verify Anchor #1

From a terminal:

```bash
cd AL
bash scripts/verify_verified_claims_root.sh \
  https://raw.githubusercontent.com/jsonwisdom/AL/master/docs/verified-claims.json
```

Expected result:

```text
VERIFY_ROOT_OK root=sha256:2296352053488d28c6517523e0392080d3cef10724db0e2142779572c6179d7a
```

To verify the local repo:

```bash
bash verify.sh
bash scripts/check_verified_claims_manifest.sh
bash scripts/verify_verified_claims_root.sh
```

All three should pass.

---

## How To Trigger A Safe Dry Run

A dry run previews what the ingestion engine would add.

```bash
cd AL
git pull origin master
DRY_RUN=1 LIMIT=10 bash scripts/auto_append_mn_budget_claims.sh
```

A dry run does not write the ledger, canonical files, manifest, commits, or pushes.

Expected signals:

```text
AUTO_SKIP already_manifested ...
AUTO_DEDUPE_SKIP ...
AUTO_CONFIDENCE_REJECT ...
AUTO_CANDIDATE ...
AUTO_APPEND_DRY_RUN_OK ...
```

---

## How To Trigger Real Ingestion

Only run real ingestion from a clean repo.

```bash
cd AL
git status --short
```

If there is output, stop and inspect it first.

Then run:

```bash
DRY_RUN=0 \
LIMIT=2 \
AUTO_COMMIT=1 \
AUTO_PUSH=1 \
bash scripts/auto_append_mn_budget_claims.sh
```

The loop performs:

```text
clean repo → extract → schema → whitelist → dedupe → confidence → append → verify → commit → push
```

If the worktree is dirty, the script fails before mutation:

```text
AUTO_APPEND_FAIL reason=dirty_worktree
```

That protects provenance.

---

## Gate Stack

Before any ledger write, AL enforces:

| Gate | Purpose |
|------|---------|
| Schema validation | TSV row must match expected structure |
| Whitelist | Only approved labels pass |
| Dedupe | Semantic hash blocks duplicate claims |
| Confidence | Rejects low-signal or malformed values |
| Dirty worktree guard | Ensures commit equals ingestion delta |

This is the operating rule:

```text
No clean input → no ledger write.
No verified ledger → no manifest.
No matching root → no anchor.
```

---

## How To Seal A New Anchor

Use this only after the manifest is clean and verified.

1. Rebuild manifest:

```bash
bash scripts/build_verified_claims_manifest.sh
```

2. Verify manifest and ledger:

```bash
bash scripts/check_verified_claims_manifest.sh
bash scripts/verify_verified_claims_root.sh
```

3. Rebuild anchor file:

```bash
bash scripts/build_ipfs_anchor.sh
cat docs/ipfs-anchor.txt
```

4. Commit the new anchor state:

```bash
git add docs/verified-claims.json docs/ipfs-anchor.txt
git commit -m "anchor: verified claims root"
git push origin master
```

5. Update ENS through ENS Manager UI only.

Use one text record:

```text
key: al.verified_claims
value: root=<root>;commit=<commit>;manifest=https://raw.githubusercontent.com/jsonwisdom/AL/master/docs/verified-claims.json
```

Do not use unverified `cast ENS` shortcuts.

---

## Anchor #2 Rule

Anchor #1 must not be rewritten.

Future claims become Anchor #2, Anchor #3, and so on.

For Anchor #2, create:

```text
docs/ANCHOR_002.md
```

Then update the same ENS key only after the new root is clean.

---

## Failure Meanings

| Output | Meaning | Action |
|--------|---------|--------|
| `MANIFEST_DRIFT` | Generated manifest differs from committed manifest | Rebuild and commit manifest |
| `VERIFY_ROOT_FAIL` | Anchor root does not match manifest | Rebuild anchor or inspect manifest |
| `AUTO_DEDUPE_SKIP` | Claim already exists semantically | No action needed |
| `AUTO_CONFIDENCE_REJECT` | Candidate is low-signal or malformed | Inspect extractor before trusting row |
| `AUTO_SCHEMA_REJECT` | Candidate row structure is invalid | Fix extractor or source format |
| `dirty_worktree` | Local repo has uncommitted changes | Commit, restore, or inspect before running |

---

## Jay's Wisdom Operating Principle

Do not argue with the ledger.

If the root matches, the state is verified.
If the root fails, the narrative stops.

Receipts first. Claims second. Vibes never.

⚙️ Verification > Narrative
