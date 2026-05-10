# Public Document Audit API

## Status

READ_ONLY  
APPEND_ONLY  
ALLEGATION_MODE_BLOCKED

## Purpose

Expose the full temporal memory of a public document.

The API is designed for replayability, not narrative curation.

Every transition remains visible.

No hidden middle states.

## Retrieval Surfaces

### By URI

```txt
GET /audit/uri/{url-encoded-uri}/transitions
```

### By Canonical Hash

```txt
GET /audit/hash/{sha256}/transitions
```

A stranger possessing only the file hash must still be able to retrieve the temporal audit chain.

## Ordering Rules

Results MUST be:

- oldest-first
- append-only
- chronologically ordered
- stable under replay

## Allowed Query Parameters

```txt
?since=<timestamp>
?limit=<integer>
```

## Forbidden Query Parameters

```txt
?state=verified
?only_success=true
?hide_divergence=true
```

The audit surface must expose the full life of the document, not a curated trust summary.

## Entry Integrity

Each audit entry includes:

```txt
prev_entry_hash
entry_hash
```

This creates a cryptographically replayable append-only chain.

Silent overwrite invalidates downstream hashes.

## Replay Rule

A replay observer must be able to:

1. fetch all entries
2. verify hash-chain continuity
3. verify temporal ordering
4. inspect every downgrade event
5. inspect every divergence event

without requiring private authority.

## Allegation Boundary

```txt
ALLEGATION_MODE: BLOCKED
```

The API may expose:

- replay outcomes
- custody transitions
- drift events
- divergence events
- verification decay

The API may not expose:

- accusation claims
- guilt inference
- motive inference
- hidden-content speculation

## Constitutional Rule

Consensus is not convergence.

Replay agreement, hash agreement, and temporal agreement must all remain publicly inspectable.
