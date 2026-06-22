# JSONWisdom World Map

Status: COMMITTED CONTINUITY MAP

This file exists to prevent continuity loss across GitHub, ChatGPT, Pages, receipts, and public artifacts.

## Current World State

### Layer 0: Family

Family remains the root layer. Project narratives do not outrank family.

### Layer 1: Trust and Source Foundation

- **ALMS** — Trust Engine
  - Role: provenance, verification, receipt authority, replay discipline
  - Core rule: no anchor without proof
  - Core rule: no fake green

- **PDF Empire** — Source Asset
  - Role: public-record source layer
  - Scope: Minnesota records, city records, fiscal records, meeting minutes, future state expansion
  - Consumers depend on this layer for source material

### Layer 2: Consumers

- **Goblin Court**
  - Role: funny proof receipt consumer
  - Output: Goblin Docket Receipts and shareable proof cards

- **Meme Court**
  - Role: shareability and meme-review layer
  - Rule: the joke is funny, the source still matters

- **Clown Court**
  - Role: absurdity review layer
  - Rule: bureaucracy may be ridiculous without being promoted to unsupported claims

- **ZTVS Replay Map**
  - Role: zero-trust replay and verification surface
  - Rule: replay proves; dashboard display does not confer authority

### Layer 3: Public Artifacts

- Receipts
- Replay maps
- Goblin receipt images
- GitHub Pages surfaces
- Zora artifacts
- Public identity anchors

## Dynamic Nodes v1

Dynamic nodes convert the static continuity spine into a live index surface without changing authority rules.

- **Layer 0 (Family Root)**: Static anchor. Never auto-promoted by UI.
- **Layer 1 (Trust)**: ALMS, receipt discipline, continuity gates.
- **Layer 2 (Consumers)**: Goblin Court, Meme Court, Clown Court, ZTVS Replay Map.
- **Layer 3 (Public)**: Live projection may pull from `ACTIVE_LANES.json`.

### Live Index Feed

The live homepage may parse `ACTIVE_LANES.json` on load and render lane nodes as a projection.

```json
{
  "nodes": [
    {
      "id": "AL",
      "source": "ACTIVE_LANES.json",
      "overlay": "Audit Ledger",
      "authority": "projection_only"
    },
    {
      "id": "ZTVS",
      "source": "ACTIVE_LANES.json",
      "overlay": "Replay Map",
      "authority": "projection_only"
    },
    {
      "id": "COMPUTERWISDOM",
      "source": "ACTIVE_LANES.json",
      "overlay": "Agent Systems",
      "authority": "projection_only"
    },
    {
      "id": "JOY",
      "source": "ACTIVE_LANES.json",
      "overlay": "Family/Public Artifacts",
      "authority": "projection_only"
    },
    {
      "id": "CWaaS",
      "source": "ACTIVE_LANES.json",
      "overlay": "Service Layer",
      "authority": "projection_only"
    }
  ]
}
```

Dynamic rendering does not confer authority. `ACTIVE_LANES.json` remains the source for lane status. Replay remains the validator.

## Active Identities

- Jason Wisdom
- Jay Wisdom
- JSONWisdom
- jaywisdom.eth
- jaywisdom.base.eth

## Known Continuity Anchors

- Receipts over Narrative
- Replay First
- No Fake Green
- Layer 0 Family
- Cumulative Existence

## Current Working Files in jsonwisdom/AL

- `index.html` — live Jay's World Map homepage and continuity front door
- `WORLD_MAP.md` — continuity map and replay spine
- `CONTINUITY_INDEX.json` — committed continuity anchor
- `ACTIVE_LANES.json` — active lane source projection
- `docs/index.html` — generated/public distribution surface in workflow lanes
- `site/data/payment-config.json` — Goblin Rendering configuration in PR work
- `site/data/states/mn.index.json` — Minnesota docket data
- `site/data/audits/` — audit data lane

## Current Open PRs

- PR #364 — Add Goblin Rendering payment adapter v0.1
  - Branch: `goblin-payment-adapter-v0-1`
  - Status: OPEN_PR
  - Green status: NOT MERGED

## Continuity Anchors

- Anchor 001 / `jsonwisdom/Welcome-to-JSONWISDOM`
  - Status: PUBLIC_REPLAYABLE_IDENTITY_ROOT
  - Evidence: repository exists, is public, and README defines the identity root / orientation layer / canonical doorway for Jay Wisdom / JSONWisdom
  - Boundary: narrator and orientation layer only; it does not promote claims into proof

- Anchor 002 / Challengeable Genesis Receipt v0.2
  - Status: CONTINUITY_NODE_SEALED
  - Doctrine: Genesis is version 0 of the constraint set, not sacred ground.
  - Core invariant: preserve enough lineage that future correction remains possible.
  - Completeness rule: preserved, traversable, comprehensible, challengeable, and supersedable without mutation.
  - Authority rule: authority is a participant in the lineage, not an exception outside the graph.
  - Replay boundary: this anchor records continuity doctrine only; it does not promote any downstream lane to GREEN without receipts.
  - Required schema hooks: `special_exemption_claimed: false`, `PROVISIONAL_VALID`, `not_immutable_truth: true`, `superseded_by_uid: null`, `challenge_hook`, `comprehensibility_artifacts`.
  - Comprehensibility artifacts: `GENESIS_HUMAN_SUMMARY.md`, `GENESIS_GRAPH_DIAGRAM.svg`, `GENESIS_REPLAY_WALKTHROUGH.md`.
  - Failure classes: disappearance, severance, semantic thinning, complexity overload.

## Replay Rule

Before creating new work, replay this map and ask:

1. What already exists?
2. What changed?
3. What is active?
4. What is stale?
5. What should be continued rather than rebuilt?

## Authority Status

This file is a committed continuity map. It is presented by the live homepage but does not become authority through UI display. Authority comes from committed receipts and replayable references.
