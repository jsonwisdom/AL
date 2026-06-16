# Jay's Root — Tiered Layering Schema

## Status

`ROOT_LAYERING_OPENED`

## Purpose

Define Jay's public website/root as a tiered verification surface for Computer Wisdom, ALMS, Meta/Facebook distribution, federal/state fixtures, and public proof.

This is not wallet-first and not platform-owned.

## Core Rule

```text
Root identity -> deterministic fixtures -> state/federal receipts -> public verifier -> optional chain witness
```

## Tier Model

### Tier 0 — Identity Root

```json
{
  "operator": "jaywisdom.eth",
  "alias": "jaywisdom.base",
  "github": "jsonwisdom/AL",
  "status": "IDENTITY_GITHUB_PROVEN"
}
```

Role: public operator identity and namespace root.

### Tier 1 — Canonical Bytes

```json
{
  "source": "GitHub",
  "repo": "jsonwisdom/AL",
  "role": "canonical_byte_surface"
}
```

Role: exact files, commits, schemas, receipts, fixtures.

### Tier 2 — ALMS Proof Layer

```json
{
  "system": "ALMS",
  "role": "hash_receipt_verification",
  "methods": ["jq -cS", "sha256", "browser_recompute"]
}
```

Role: convert claims and task sets into verifiable receipts.

### Tier 3 — Fixture Layer

```json
{
  "fixtures": [
    "federal",
    "state",
    "county",
    "platform",
    "market_observer"
  ],
  "role": "structured_evidence_inputs"
}
```

Role: fed/state/county/platform data objects that can be independently replayed.

### Tier 4 — State Layer

```json
{
  "state": "machine_readable_latest",
  "path": "_truth/meta/public_exports/latest.json",
  "role": "current_public_proof_pointer"
}
```

Role: one JSON pointer that updates site, verifier, posts, and future chain witness.

### Tier 5 — Public Website Layer

```json
{
  "site": "https://jsonwisdom.github.io/AL/",
  "role": "human_public_entrypoint",
  "pages": [
    "computer-wisdom-public-proof.html",
    "verify.html"
  ]
}
```

Role: simple public explanation and one-click verification.

### Tier 6 — Distribution Layer

```json
{
  "platforms": ["Meta", "Facebook", "X", "Zora", "Base app"],
  "role": "distribution_only",
  "authority": "none"
}
```

Role: carry links/posts. They do not authenticate truth.

### Tier 7 — Optional Witness Layer

```json
{
  "chain": "Base",
  "tools": ["EAS", "ENS", "transaction pointer"],
  "role": "optional_public_timestamp_witness",
  "required_for_verification": false
}
```

Role: external witness after bytes are already verifiable.

## UID Definition for Jay's Root

`UID` here means a public, stable identifier for a proof object.

It may be one of:

```text
GitHub commit SHA
ALMS receipt hash
Team Kernel Merkle root
EAS attestation UID
ENS text/contenthash pointer
```

The website must never treat platform IDs as authoritative UIDs.

## Federal / State Fixture Plan

```text
_truth/fixtures/
  federal/
  state/
  county/
  platform/
_truth/state/
  latest.json
  mn.json
  us.json
  meta.json
schemas/
  fixture.federal.v1.schema.json
  fixture.state.v1.schema.json
  root.state.v1.schema.json
```

## Public Site Requirement

The public site should show three layers clearly:

```text
1. Identity: jaywisdom.eth / jaywisdom.base
2. Proof: GitHub commit + ALMS hash + browser verifier
3. Witness: optional Base/EAS/ENS pointer
```

## Final Rule

Meta/Facebook can distribute Jay's proof. They cannot define, block, or authenticate it.

**Jay's Root = identity + bytes + receipts + verifier + optional witness.**
