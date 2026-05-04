# ALMS Constitution Multi-Source Consensus Plan

Status: DESIGN LOCK — NO EXTERNAL MIRROR CLAIMED

## Purpose

Move the Article I verification surface from a single hosted source to a multi-source verification model.

Current source of truth:
- GitHub repository: `jsonwisdom/AL`
- Article I root: `09873d69046c82736187786483562306208a0d01f974673323065a0438627341`
- Rule: `ALMS_GLOBAL_MERKLE_RULE_V1`

## Current Trust Boundary

GitHub is the authoritative source for:
- clause spans
- section manifests
- Article I global manifest
- local replay script
- browser verifier
- CI enforcement workflow

## Future Mirror Targets

External mirrors must not be treated as canonical until the mirror receipt exists.

Candidate mirror layers:
1. IPFS
2. Arweave
3. GitHub release artifact
4. EAS/Base attestation
5. ENS text-record pointer

## Mirror Receipt Requirements

A mirror is admissible only if the repo contains a receipt with:

```json
{
  "artifact": "ALMS_CONSTITUTION_MIRROR_RECEIPT",
  "source_root_sha256": "09873d69046c82736187786483562306208a0d01f974673323065a0438627341",
  "source_commit_sha": "<git_commit>",
  "mirror_type": "ipfs|arweave|release|eas|ens",
  "mirror_identifier": "<cid_or_tx_or_url>",
  "created_at": "<utc_iso8601>",
  "verification_status": "PENDING|VERIFIED|REJECTED"
}
```

## Consensus Rule Draft

A verifier may show:

- GREEN: GitHub replay passes and at least one external mirror independently matches the Article I root.
- YELLOW: GitHub replay passes but no external mirror is available.
- RED: Any source returns a mismatching root.
- GRAY: Source unavailable or indeterminate.

## Non-Negotiable Rule

No CID, tx hash, release URL, ENS record, or external mirror identifier may be described as verified until it is recorded in a repo-resident receipt and independently replayed.

Proof > narrative.
