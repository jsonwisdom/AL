# Constitutional Replay v0.1

Local-first replay infrastructure for autonomous economic receipts.

```text
If it cannot replay locally, it does not count.
```

## Current Status

v0.1 is docs-first and local-first.

The implementation is governed by:

- `BUILD_MATRIX.md`
- `docs/LOCAL_REPLAY_PROTOCOL.md`
- `docs/BASE_NAVIGATION.md`
- `docs/MERKLE_VERIFICATION_EXAMPLES.md`

## Doctrine

```text
No witness, no claim.
No receipt, no ratification.
No replay, no settlement.
```

## Quickstart Target

Once v0.1 runtime files are implemented, the intended flow is:

```bash
git clone https://github.com/jsonwisdom/AL.git
cd AL/constitutional-replay-v1
npm install
./demo.sh
npm run replay examples/treasury-agent/receipts/refusal-001.json
```

Expected final output:

```text
✅ Constitutional loop complete.
Receipts are sovereign and replayable.
```

## v0.1 Constraints

- No Base RPC.
- No network in replay.
- No live clock in replay.
- No entropy in replay.
- No floats.
- No free-text refusal reasons.
- Canonical replay hash must be `sha256:` over canonical bytes.

## Authority Separation

```text
Replay status = semantic truth.
Base witness status = public commitment visibility.
```

Base may witness commitment later.

Base must not become replay authority.

## Build Order

1. Local replay protocol.
2. Canonical bytes.
3. SHA-256 receipt binding.
4. Policy v1 schema and vectors.
5. Refusal interpreter.
6. Demo replay.
7. Merkle batch.
8. Static dashboard.
9. Read-only Base witness in v0.2.

## Final Line

Base can witness the forest.

Replay proves the path.
