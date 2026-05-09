# AL — Audit Ledger / ALMS Verification Machine

AL is a zero-trust civic verification repository.

It turns claims, datasets, documents, and public proof pages into replayable artifacts that can be checked by humans, courts, agents, and machines.

> Verify > Narrative.
> Receipts > claims.
> Replay > authority.

## What You Can Verify Today

- NY median household income coverage: 62/62 counties
- NY climate observation coverage: sparse station counties only
- Public proof surface: https://jsonwisdom.github.io/AL/proof/computer-wisdom-public-proof.html

## How To Verify

    git clone https://github.com/jsonwisdom/AL.git
    cd AL
    find _truth/receipts -type f | sort
    find docs -type f | sort

Pick a receipt from `_truth/receipts/index.json`, open the referenced JSON, inspect `claim`, `algorithm`, `commitment`, `timestamp`, and `signature`. A claim is public only when the receipt is present, indexed, and replay-linked.

## Claim Boundaries

* No statewide climate validation
* No risk atlas or hazard map
* No attribution or causality
* No interpolation to uncovered counties
* No simulated data

## System Layers

1. Civic Proof
2. Constitutional Machine
3. Agent Infrastructure

See:

* docs/ARCHITECTURE.md
* docs/DOCTRINE.md
* docs/REPO_MAP.md
