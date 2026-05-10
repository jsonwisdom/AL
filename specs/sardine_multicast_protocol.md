# Sardine Multicast Protocol

## Status

SMP_V1_DRAFT  
READ_ONLY_DISCOVERY  
NO_CENTRAL_CONVERGENCE_SERVICE  
ALLEGATION_MODE_BLOCKED

## 0. Principles

Sardine Multicast Protocol (SMP) lets independent Sardine Marshals discover each other, publish observations, and compute convergence from public logs without creating a coordinator that can be captured.

Core principles:

- No private context sharing
- No central convergence service
- Deterministic computation from public logs only
- Majority cannot manufacture reality
- Consensus is not convergence
- Trust may degrade automatically
- Trust may not upgrade without fresh replayable evidence

## 1. Discovery

Each Marshal publishes a public manifest:

```txt
/.well-known/sardine-manifest.json
```

Discovery is pull-based.

Any observer may maintain a local set of known manifests.

No registry is required.

Gossip is allowed.

A manifest SHOULD contain:

```json
{
  "type": "SARDINE_MANIFEST",
  "protocol": "SMP_V1",
  "marshal_id": "marshal_a",
  "operator": "REPLACE_WITH_OPERATOR_NAME_OR_KEY",
  "log_base": "https://example.org/sardine/logs",
  "public_key": "REPLACE_WITH_PUBLIC_KEY",
  "signature_algorithm": "REPLACE_WITH_SIGNATURE_ALGORITHM",
  "supported_schemas": [
    "PUBLIC_DOCUMENT_AUDIT_LOG",
    "AUDIT_LOG_ENTRY",
    "PUBLIC_DOCUMENT_HASH_DRIFT_RECEIPT"
  ],
  "max_clock_skew_seconds": 300,
  "allegation_mode": "blocked"
}
```

## 2. Publishing

An observation is posted only to the authoring Marshal's own log.

No cross-posting is required.

No Marshal writes to another Marshal's log.

Suggested endpoint:

```txt
POST {log_base}/uri/{url_hash}
```

The publishing service returns:

```json
{
  "transition_id": "REPLACE_WITH_TRANSITION_ID",
  "entry_hash": "sha256:REPLACE_WITH_ENTRY_HASH"
}
```

Each observation entry MUST include:

- `source_uri`
- `normalized_uri`
- `canonical_hash`
- `event_type`
- `observed_at`
- `from_state`
- `to_state`
- `hash_before`
- `hash_after`
- `replay_path`
- `prev_entry_hash`
- `entry_hash`
- signature or equivalent public authentication
- `allegation_mode: blocked`

## 3. Read Surfaces

Observers retrieve logs by URI or content hash.

```txt
GET {log_base}/audit/uri/{url-encoded-uri}/transitions
GET {log_base}/audit/hash/{sha256}/transitions
```

Results MUST be:

- read-only
- append-only
- oldest-first
- paginated without hiding middle events

Allowed query parameters:

```txt
?since=<timestamp>
?limit=<integer>
```

Forbidden query parameters:

```txt
?state=verified
?only_success=true
?hide_divergence=true
```

The audit surface must show the whole life of the document.

## 4. Convergence Computation

Any observer can compute convergence locally.

No upstream coordinator decides truth.

Algorithm:

```txt
INPUT:
  target normalized_uri OR canonical_hash
  known sardine manifests
  max_clock_skew_seconds

STEPS:
  1. Fetch all known Marshal logs for the target.
  2. Verify each log's hash-chain continuity.
  3. Verify each entry signature or public authentication proof.
  4. Collect observations within the same clock window anchored to the earliest observation.
  5. Group observations by to_state, hash_after, replay_path result, and canonical_hash.
  6. If all required observers match state + hash + replay result, emit converged.
  7. If any state or hash differs, emit divergent.
  8. Include full disagreement_vector.
  9. Write the result as a local convergence record only.
 10. Do not push the result upstream as global truth.
```

## 5. Divergence Rule

A single contradictory drift observation is enough to block an upgrade.

Two Marshals reporting `verified` cannot override one Marshal reporting `hash_mismatch` for the same window.

The result is:

```txt
FINAL_RECORDED_STATE: divergent
UPGRADE_ALLOWED: false
WINNER_DECLARED: false
REVIEW_REQUIRED: true
```

## 6. Worked Example: Vector 005

Input observations:

```json
[
  {
    "marshal_id": "marshal_a",
    "observed_state": "verified",
    "hash_after": "sha256:abc123",
    "replay_path": "download -> sha256 -> compare abc123"
  },
  {
    "marshal_id": "marshal_b",
    "observed_state": "verified",
    "hash_after": "sha256:abc123",
    "replay_path": "download -> sha256 -> compare abc123"
  },
  {
    "marshal_id": "marshal_c",
    "observed_state": "hash_mismatch",
    "hash_before": "sha256:abc123",
    "hash_after": "sha256:def456",
    "replay_path": "download -> sha256 -> observed def456 != previous abc123"
  }
]
```

Expected local convergence record:

```json
{
  "final_recorded_state": "divergent",
  "upgrade_allowed": false,
  "winner_declared": false,
  "review_required": true,
  "disagreement_vector": [
    {
      "claim": "verified",
      "marshals": ["marshal_a", "marshal_b"],
      "hash_after": "sha256:abc123"
    },
    {
      "claim": "hash_mismatch",
      "marshals": ["marshal_c"],
      "hash_before": "sha256:abc123",
      "hash_after": "sha256:def456"
    }
  ]
}
```

## 7. Security Properties

### Fork detection

A hash-chain break means the log has forked, been rewritten, or cannot be fully replayed.

### Coordination resistance

No shared write surface exists.

Each Marshal publishes only to its own log.

Convergence is computed locally by observers.

### Replay laundering blocked

Convergence requires matching:

- observed state
- observed hash
- replay path result
- clock window
- hash-chain validity

A majority cannot vote a drift event away.

### Allegation boundary

SMP transports evidence states.

It does not transport accusations.

```txt
ALLEGATION_MODE: BLOCKED
```

## 8. Constitutional Rule

```txt
CONSENSUS IS NOT CONVERGENCE.
```

Convergence requires public replay alignment.

Majority agreement without replay alignment is only social pressure.

Sardine Marshal records the divergence and stops.
