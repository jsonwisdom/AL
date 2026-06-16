# Sardine Score

## Status

SARDINE_SCORE_V1_DRAFT  
SUMMARY_ONLY  
NOT_AUTHORITY  
ALLEGATION_MODE_BLOCKED

## Purpose

Sardine Score summarizes the replay health of a public-document audit chain.

It does not decide truth.

It does not infer guilt, innocence, motive, or hidden content.

It only summarizes how well the document's public verification surface currently replays.

## Constitutional Boundary

```txt
A SCORE IS NOT A VERDICT.
A SCORE IS NOT AUTHORITY.
A SCORE IS A REPLAY HEALTH SUMMARY.
```

## Inputs

A Sardine Score may consider:

- current verification state
- age since last successful replay
- number of independent Marshals
- convergence quality
- hash drift history
- stale replay events
- unavailable source events
- destroyed-with-receipt events
- divergence events
- audit log hash-chain continuity

It may not consider:

- accusation claims
- political preference
- institutional rank
- media popularity
- majority pressure without replay alignment
- hidden evidence speculation

## Output Shape

```json
{
  "type": "SARDINE_SCORE",
  "subject": "REPLACE_WITH_SUBJECT",
  "normalized_uri": "REPLACE_WITH_NORMALIZED_URI",
  "canonical_hash": "sha256:REPLACE_WITH_HASH_OR_NULL",
  "score": 0,
  "score_band": "red",
  "computed_at": "REPLACE_WITH_TIMESTAMP",
  "inputs": {
    "current_state": "pending_public_evidence",
    "independent_marshal_count": 0,
    "last_successful_replay_at": null,
    "hash_drift_count": 0,
    "divergence_count": 0,
    "source_unavailable_count": 0,
    "hash_chain_valid": true
  },
  "allegation_mode": "blocked",
  "summary": "Replay health summary only. Not a verdict."
}
```

## Bands

```txt
GREEN   replay currently succeeds with sufficient independent convergence
YELLOW  replay exists but has weakness, age, limited observers, or review flags
RED     replay absent, broken, divergent, unavailable, or hash-mismatched
GRAY    sealed, unknown, or insufficient public evidence
```

## Hard Rules

```txt
hash_mismatch -> RED
source_unavailable -> RED
pending_public_evidence -> GRAY
sealed -> GRAY
divergent -> RED
verified without recent replay -> YELLOW or STALE
verified with fresh multi-Marshal convergence -> GREEN
```

## Anti-Laundering Rule

A high score cannot override a drift event.

A majority score cannot override minority hash-mismatch evidence.

Vector 005 remains controlling:

```txt
2 verified + 1 hash_mismatch -> divergent -> RED
```

## Teaching Rule

Sardine Score is a dashboard needle, not a judge.

When the score drops, the machine asks for replay, not panic.

When the score rises, the machine requires evidence, not applause.
