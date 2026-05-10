# Jay's Wisdom Reboot Site Plan

Status: DRAFT_REBOOT_SITE_PLAN
Branch: root-law-machine-audit-v1
Root identity: jaywisdom.base

## Repo Audit Summary

The current repository already defines AL as an attestation ledger and verification machine.

Existing authority surfaces:

- README.md identifies AL as public verifiable claims with cryptographic receipts.
- docs/REPO_MAP.md maps public proof pages to docs/proof/ and canonical receipts to _truth/receipts/.
- docs/ARCHITECTURE.md defines AL as a verification machine, not a database.
- docs/DOCTRINE.md locks Verify > Narrative, Receipts > Claims, and Replay > Authority.
- docs/proof/index.html is the existing receipt viewer for _truth/receipts/index.json.

## Reboot Goal

Build a public site that turns the existing proof surface into a learning-first constitutional commons.

The reboot site should not replace the receipt viewer. It should sit in front of it and route people into the machine.

## Site Order

```text
1. Root Law
2. The First Commons
3. Individual Authenticity
4. Learning Lab
5. Receipt Viewer
6. Correction / Repair Workshop
7. Public Proof Surfaces
8. Economy Boundary
9. On-Chain Anchors
10. Public Commons Export
```

## Public Pages

Recommended GitHub Pages layout:

```text
docs/
  index.html                         # Reboot landing page
  learning/index.html                # Jay's Wisdom Learning Lab
  proof/index.html                   # Existing receipt viewer
  proof/computer-wisdom-public-proof.html
  root-law/index.html                # Human-readable root law surface
  repair/index.html                  # Correction + Repair Workshop
  commons/index.html                 # Public Commons export / receipts map
```

## Landing Page Contract

The landing page should answer five things immediately:

```text
Who is the root? jaywisdom.base
What is this? A verification machine and learning commons
What is the law? Family before economy, replay before authority
What can I do? Learn, verify, correct, export receipts
What is forbidden? Hidden scoring, ghost anchors, pay-to-restore trust
```

## Home Page Sections

```text
HERO
Jay's Wisdom
A learning commons for receipts, repair, and replay.

ROOT LAW STRIP
Family -> School -> Receipts -> Roles -> Reputation -> Economy

FIRST COMMONS
Family, care, mentorship, and learning before markets.

INDIVIDUAL AUTHENTICITY
You are not a persona here. You are a participant with agency.

LEARNING LAB
Start with Proof Over Narrative.

RECEIPT VIEWER
Open the existing AL receipt viewer.

REPAIR WORKSHOP
Correction begins neutral. Verified repair becomes positive. Concealment becomes negative.

ECONOMY BOUNDARY
Money may support repair. Money may not purchase trust.

PUBLIC COMMONS
Export receipts. Replay claims. Challenge unresolved states.
```

## Implementation Rules

- Local-first HTML/CSS/JS.
- No CDN dependency for the first reboot page.
- No wallet requirement on landing.
- No auto-anchor.
- No analytics or hidden scoring.
- Link to receipts and proof surfaces that already exist.
- Clearly label draft, pending, verified, and unresolved states.

## First Build Target

Create `docs/index.html` as the reboot landing page.

It should link to:

- `/AL/proof/`
- `/AL/proof/computer-wisdom-public-proof.html`
- GitHub repo README
- root-law docs in this branch once merged

## Audit Verdict

REBOOT_SITE_PLAN_READY

Do not rebuild the entire site first.
Build the constitutional front door first.
Then attach learning, repair, and economy surfaces one receipt at a time.
