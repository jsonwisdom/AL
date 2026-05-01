# Jay Wisdom Protocol v1.0

## Purpose

Jay Wisdom Protocol defines a GitHub-first verification workflow for building portable, auditable, zero-trust systems.

The protocol separates public receipts from private signing power.

## Core Rule

Receipts stay. Signing power leaves.

## Primary Principle

Verification over narrative.

A claim is accepted only when the repo, receipt, CI log, or public anchor can verify it.

## Trust Surfaces

| Surface | Role |
|---|---|
| GitHub repo | Source of truth |
| GitHub Actions | Verification and receipt printer |
| Cloud Shell | Temporary workbench only |
| Browser wallet | Signing surface only |
| ENS | Public identity and pointer layer |
| Base | Public transaction layer |
| EAS | Public attestation layer |
| IPFS / GCS | Public artifact storage layer |

## Repo Lanes

| Path | Purpose |
|---|---|
| scripts/ | Deterministic tools |
| .github/workflows/ | CI enforcement |
| _truth/security/ | Safety scan receipts |
| _truth/ci/ | CI enforcement receipts |
| _truth/receipts/ | Verification receipts |
| docs/ | Protocols and manuals |
| docs/training/ | Operator training |
| contracts/ | Schemas and verification specs |
| site/ | Public status surfaces |
| watchers/ | Observer tools |
| studio/ | Interface and product documentation |

## Verification States

| State | Meaning |
|---|---|
| DRAFT | File exists but is not verified |
| LOCAL_VERIFIED | Local scripts pass |
| CI_GREEN | GitHub Actions pass |
| ANCHOR_READY | Artifact is safe to anchor |
| ANCHORED | Public anchor exists |
| SEALED | Receipt is committed and independently verifiable |

## Public Receipts

Allowed public artifacts:

- Wallet addresses
- Contract addresses
- Transaction hashes
- EAS UIDs
- ENS names
- IPFS CIDs
- SHA-256 hashes

These are evidence, not signing power.

## Forbidden Repo Material

The repo must not contain:

- Private keys
- Seed phrases
- Wallet keystores
- Service account JSON keys
- API tokens
- RPC URLs with embedded secrets
- Browser wallet export files

## Anchor Readiness

An artifact is anchor-ready only when:

- safety scan is green
- CI enforcement is green
- receipt exists
- signing power is not in repo
- operator approves anchoring

## Leaf Lifecycle

INTAKE -> NORMALIZE -> VERIFY -> RECEIPT -> CI_GREEN -> ANCHOR_READY -> ANCHORED -> SEALED

## Operator Rules

1. Start every session at repo root.
2. Run the safety ritual before major work.
3. Commit before anchoring.
4. Push before claiming completion.
5. Verify GitHub Actions before opening a new leaf.
6. Never paste wallet private keys into terminal.
7. Never treat a green narrative as a green gate.

## Start-of-Session Ritual

cd ~/AL
git pull
bash scripts/jay_repo_safety_scan.sh .
bash scripts/jay_ci_enforcement.sh
git status

## Failure Classes

| Class | Meaning |
|---|---|
| SAFETY_FAIL | Possible secret or unsafe repo material |
| CI_FAIL | Enforcement gate failed |
| JSON_FAIL | Invalid JSON detected |
| STRUCTURE_FAIL | Required repo path missing |
| ANCHOR_FAIL | Claimed anchor not verifiable |
| DRIFT | Receipt changed unexpectedly |
| BREAK | Witness or included artifact changed outside boundary |

## Locked Statement

GitHub is the suitcase.

Cloud Shell is the temporary workbench.

Browser wallet is the only signing surface.

Receipts stay. Signing power leaves.
