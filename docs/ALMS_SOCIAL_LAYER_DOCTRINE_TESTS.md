# ALMS Social-Layer Doctrine Tests

## Purpose

This file defines adversarial classification tests for the ALMS Social-Layer Doctrine.

Its purpose is to prevent public signals, images, summaries, screenshots, dashboards, and narrative claims from crossing into the verifier boundary.

## Invariant

Narrative may gesture; only artifacts prove.

## Test Cases

| # | Input Object | Expected Classification | Admissible as Proof? | Required Backing |
|---|---|---|---|---|
| 1 | Tweet announcing a synced root | PUBLIC_SIGNAL_LAYER_OK | No | repo commit, batch root, manifest path |
| 2 | Seal graphic or cover image | SIGNAL_ONLY | No | receipt path, manifest path, or commit hash |
| 3 | Screenshot of terminal output | SCREENSHOT_SIGNAL_ONLY | No | reproducible command and stored log artifact |
| 4 | Dashboard screenshot | MIRROR_SCREENSHOT_ONLY | No | canonical `_truth/` source and manifest |
| 5 | Live intel JSON mirror | MIRROR_STATE | No | canonical `_truth/` source and matching root |
| 6 | GitHub commit containing manifest update | RECORD | Yes | commit hash |
| 7 | Merkle root in `_truth/merkle/root.txt` | COMMITMENT | Yes | matching `_truth/merkle/manifest.json` |
| 8 | Receipt JSON with matching canonical hash | PROOF_OBJECT | Yes | replayable verifier state |
| 9 | Copilot summary | NARRATIVE_ONLY | No | machine artifact citation |
| 10 | AI-generated analysis of ALMS state | PUBLIC_SIGNAL_LAYER_OK | No | GitHub record, receipt, or manifest |

## Classifier Table

| Object Type | Classification | Verifier Boundary |
|---|---|---|
| Tweet, post, thread, or reply | PUBLIC_SIGNAL_LAYER_OK | excluded |
| Image, badge, seal, or logo | SIGNAL_ONLY | excluded |
| Terminal screenshot | SCREENSHOT_SIGNAL_ONLY | excluded |
| Dashboard screenshot | MIRROR_SCREENSHOT_ONLY | excluded |
| Live intel JSON | MIRROR_STATE | excluded unless reconciled to `_truth/` |
| GitHub commit | RECORD | included |
| Merkle root | COMMITMENT | included |
| Receipt JSON | PROOF_OBJECT | included |
| Copilot summary | NARRATIVE_ONLY | excluded |
| Human explanation | NARRATIVE_ONLY | excluded |

## Failure Conditions

A social object fails doctrine if it:

- Claims to be a receipt
- Claims final verification without a backing artifact
- Substitutes a screenshot for a replayable command
- Treats a dashboard mirror as canonical truth
- Treats AI summary text as admissible evidence
- Advances claim state without machine proof
- Converts pending attestation logs into UID confirmation

## Expected Behavior

If an object is narrative, visual, conversational, or social:

```txt
admissible: false
purpose: proof_pointer
verifier_boundary: excluded
```
