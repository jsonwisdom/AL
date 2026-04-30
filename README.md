# Alabama Machine Speed

[![ALMS Daily Audit](https://github.com/jsonwisdom/AL/actions/workflows/alms-daily-json-audit.yml/badge.svg)](https://github.com/jsonwisdom/AL/actions/workflows/alms-daily-json-audit.yml)

## CORECHAIN

**CORECHAIN = `contracts/` + `docs/` + `studio/`**

This repository is organized as a single chain of custody from code to
culture:

| Directory | Purpose |
|-----------|---------|
| `contracts/` | Protocol code, deployment scripts, legal compact — machine trust and execution |
| `docs/` | Cross-cutting legal, technical, and operational doctrine |
| `studio/` | Monetization, learning modules, publishing, visual command — human adoption layer |

**Build the protocol. Define the doctrine. Ship the studio.**

No drift between what the machine does, what the system claims, and what the
public sees.

---

## Overview

Alabama Machine Speed is a state-level truth arbitration system that turns
policy claims into verifiable, receipt-backed proof artifacts at machine speed.

Read the full State Chess Board explainer: [studio/STATE_CHESS_BOARD.md](studio/STATE_CHESS_BOARD.md)

---

## Operator Guides

- [ALMS Operator Guide](docs/ALMS_OPERATOR_GUIDE.md) — receipts, Merkle roots, preflight audit, and verification flow.
- [ALMS Social-Layer Doctrine](docs/ALMS_SOCIAL_LAYER_DOCTRINE.md) — tweets, images, and announcements are proof pointers only; narrative may gesture, only artifacts prove.

## Verifying This Repository

ALMS is designed so reviewers can verify the repository locally without trusting narrative claims.

The verification path is:

```txt
receipt → segment manifest → rollover link → GitHub CI

### Verify Segment 002 → Segment 003 rollover

```bash
./scripts/verify_rollover.sh receipts/rollover/segment_002_to_003.json
