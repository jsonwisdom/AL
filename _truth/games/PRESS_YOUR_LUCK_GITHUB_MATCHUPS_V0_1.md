# Press Your Luck GitHub Matchups V0.1

**repo:** jsonwisdom/AL  
**anchor_state:** YELLOW_READY  
**no_fake_green:** ACTIVE  
**lane:** game / public readback / mathematical scoring  
**primary_identity:** jaywisdom.base.eth

## Purpose

Create a public game layer where artifacts can face each other in head-to-head GitHub matchups.

This is a game and governance-simulation design. It is not an official election system, not legal authority, and not political endorsement machinery.

## Game Frame

Press Your Luck means each artifact can win momentum, lose momentum, or trigger rollback when evidence is weak.

The board is GitHub. The pieces are commits, issues, pull requests, receipts, hashes, and readbacks.

## Matchup Unit

Each matchup compares two artifacts:

- Artifact A
- Artifact B
- Shared claim or challenge
- Evidence bundle for A
- Evidence bundle for B
- Public readback window
- Mathematical score output
- Final ruling: WIN, LOSS, TIE, ROLLBACK, or NEEDS_MORE_EVIDENCE

## Scoring Inputs

Scores should be reproducible from repo history.

Minimum scoring dimensions:

1. Receipt completeness
2. Hash availability
3. Replay success
4. Source clarity
5. Test or probe output
6. Public readback count
7. Contradiction count
8. Rollback discipline

## Voting Layer

Public votes may be collected as readbacks, comments, reactions, or signed receipts.

Votes are advisory unless the scoring rule says otherwise.

No vote can override missing evidence. A popular artifact without receipts remains YELLOW or RED.

## AI Role

AI agents may summarize, classify, and check replay status.

AI agents may not invent evidence, fake consensus, or promote GREEN without repo or on-chain proof.

## Head-to-Head GitHub Matchups

A GitHub issue or PR can host one matchup.

Suggested format:

```text
MATCHUP_ID:
ARTIFACT_A:
ARTIFACT_B:
CLAIM:
EVIDENCE_A:
EVIDENCE_B:
SCORING_RULE:
PUBLIC_READBACK_WINDOW:
RULING:
```

## Anti-Daft Rules

- No fake GREEN.
- No official election claims.
- No political lane unless source-bound and clearly labeled.
- No popularity override over missing receipts.
- No hidden scoring weights.
- No retroactive score edits without receipt.

## First Game Receipt Target

```text
_truth/games/receipts/PRESS_YOUR_LUCK_MATCHUP_001_RECEIPT.json
```

Minimum Matchup 001 requirements:

- two artifact paths or URLs
- one shared claim
- scoring rule version
- readback window
- computed score JSON
- SHA256SUMS
- final ruling

## Ruling

Press Your Luck GitHub Matchups is approved as a YELLOW_READY game layer.

GREEN requires a completed Matchup 001 receipt with replayable scoring and committed hashes.
