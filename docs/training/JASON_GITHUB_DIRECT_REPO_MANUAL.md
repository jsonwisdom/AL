# Jason GitHub Direct Repo Manual

## Purpose

This repo is portable. Google Cloud Shell is only a temporary workbench.

The source of truth is GitHub.

## Core Rule

Receipts stay. Signing power leaves.

## Safe Surfaces

| Surface | Role |
|---|---|
| GitHub repo | Source of truth |
| GitHub Actions | Verifier and receipt printer |
| Cloud Shell | Temporary helper only |
| Browser wallet | Signing surface only |
| ENS / Base / EAS | Anchor surfaces after verification |

## Repo Lanes

| Folder | Purpose |
|---|---|
| scripts/ | Bash tools |
| .github/workflows/ | GitHub automation |
| _truth/security/ | Security scan reports |
| _truth/receipts/ | Receipt outputs |
| docs/ | Manuals and operator guides |
| contracts/ | Schemas and specs |
| studio/ | Interface and product docs |
| site/ | Public dashboard/static outputs |
| watchers/ | Observer scripts |

## Operating Rules

1. Start every session with `cd ~/AL`.
2. Check repo state with `git status`.
3. Do not paste private keys, seed phrases, or wallet files.
4. Public 0x hashes, addresses, UIDs, and contract addresses are receipts.
5. Private keys, seed phrases, service accounts, and tokens are critical secrets.
6. Run verification before anchoring.
7. Commit receipts to GitHub.
8. Sign only in browser wallet after verification.

## GitHub Direct Receipt Rule

A branch URL is a pointer, not a receipt.

Use commit-pinned raw URLs for replayable byte verification:

```bash
URL="https://raw.githubusercontent.com/<OWNER>/<REPO>/<COMMIT_SHA>/<PATH>"
curl -fsSL "$URL" | sha256sum
```

A GitHub receipt is valid only when all fields are known:

```json
{
  "surface": "github_commit_pinned_raw",
  "repo": "jsonwisdom/AL",
  "path": "<path>",
  "commit_sha": "<40-char commit sha>",
  "url": "https://raw.githubusercontent.com/jsonwisdom/AL/<commit_sha>/<path>",
  "sha256": "<64-char sha256>",
  "result": "VERIFIED"
}
```

## External Verifier Gate

A declarative assistant cannot close a governance loop by itself.

The final SHA-256 gate must be produced by at least one real execution surface:

- human local shell
- GitHub Actions verifier
- replay daemon
- hardware-anchored verifier

Required command pattern:

```bash
curl -fsSL "https://raw.githubusercontent.com/jsonwisdom/AL/<COMMIT_SHA>/<PATH>" | sha256sum
```

If no external digest is supplied, the machine must hold:

```json
{
  "status": "SINGLE_GATE_WAIT",
  "posture": "HELD_FOR_EXTERNAL_VERIFIER",
  "global_state": "NO_DRIFT"
}
```

Do not infer, invent, or pattern-fill hashes.

Reject placeholder-like hashes and halt until a real external verifier provides the digest.

## Governance Lineage Pattern

A governed object must descend from a sealed parent and remain replayable.

Current lineage pattern:

```text
GENESIS -> RULES_V1 -> EPOCH_0001 -> PROPOSAL_0001 -> ACTIVATION_0001 -> EPOCH_0002
```

Valid next objects after a sealed epoch:

- `WITNESS_PARAMETER_UPDATE_<N>_PROPOSAL.json`
- `WITNESS_CONFLICT_LEDGER_<N>.json`

No new proposal, ledger, epoch, or activation may advance while a SHA-256 gate is open.

## Session Start

```bash
cd ~/AL
git status
git pull
```
