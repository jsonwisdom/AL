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

## Session Start

```bash
cd ~/AL
git status
git pull
