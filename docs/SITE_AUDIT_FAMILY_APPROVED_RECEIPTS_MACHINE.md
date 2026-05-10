# Site Audit — Family Approved Receipts Machine

Status: FAMILY_APPROVED_SITE_AUDIT_V1
Branch: root-law-machine-audit-v1
Root identity: jaywisdom.base

## Instruction Applied

Do not reinvent the wheel.
Use what already exists in the repository.
Apply Wisdom from the existing doctrine, architecture, proof viewer, and root-law additions.

## Existing Machine Parts

The repo already has the core machine:

- README.md defines AL as public verifiable claims with cryptographic receipts.
- docs/DOCTRINE.md defines Verify > Narrative, Receipts > Claims, and Replay > Authority.
- docs/ARCHITECTURE.md defines AL as a verification machine, not a database.
- docs/REPO_MAP.md identifies docs/proof/ as the public proof surface and _truth/receipts/ as the truth layer.
- docs/proof/index.html is the existing receipt viewer.

## Reuse Rule

```text
Do not replace the receipt viewer.
Do not duplicate the truth layer.
Do not invent a parallel proof system.
Wrap the existing machine with a better front door.
```

## Family Approved Root Order

```text
Family
School
Receipts
Roles
Reputation
Rewards
Economy
```

Family Approved means:

- human development before markets
- care before extraction
- learning before payments
- correction before punishment
- replay before authority
- no hidden behavioral scoring
- no ghost anchors

## Site Fix Needed

The current public machine is strong but too technical at the front door.

Users land near proof infrastructure before they understand:

- who the root is
- why receipts matter
- what they can learn
- how correction works
- why family comes before economy

## Minimal Reboot Strategy

Build only a constitutional front door at `docs/index.html`.

It should link into existing surfaces instead of replacing them:

```text
/AL/proof/                         existing receipt viewer
_truth/receipts/index.json         canonical receipt index
README.md                          operator overview
docs/DOCTRINE.md                   doctrine
docs/ARCHITECTURE.md               machine architecture
docs/REPO_MAP.md                   map
```

## Authority Link Rule

Only link to files confirmed present.

If a README or map references a proof page that is not fetched successfully during audit, mark it as UNCONFIRMED until a file audit proves it exists.

## New Front Door Requirements

`docs/index.html` should be:

- static
- local-first
- no CDN
- no analytics
- no wallet gate
- no hidden tracking
- no auto-chain action
- no pay-to-restore trust
- explicit links to proof surfaces

## Required Site Sections

```text
1. Jay's Wisdom / AL
2. Family Approved Root Law
3. What This Machine Does
4. Learn Before Economy
5. Verify Receipts
6. Repair and Correction
7. Public Commons
8. Open Existing Receipt Viewer
```

## Copy Lock

Use this line above the machine:

```text
Family approved. Receipt governed. Replay before authority.
```

Use this line near the economy boundary:

```text
Money may support repair. Money may not purchase trust.
```

Use this line near the learning path:

```text
You are not a persona here. You are a participant with agency.
```

## Audit Verdict

FAMILY_APPROVED_RECEIPTS_MACHINE_AUDIT_READY

The right move is a wrapper/front door, not a rebuild.
The existing receipts machine remains authority.
The site reboot teaches people how to enter it.
