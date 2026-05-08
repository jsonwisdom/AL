# ALMS Threshold Awareness Doctrine V1

Status: `CANONICAL_DRAFT`

Binding principle:

```text
Correctly scoped. Remainder guaranteed.
```

Core ledger rule:

```text
The ledger records the transformation, not the world.
```

---

## 1. Purpose

This doctrine defines the receipt boundary rule for ALMS receipts and replay artifacts.

A receipt is not an oracle, a total event record, or a proof that the world was exhaustively captured.

A valid ALMS receipt records a scoped transformation that crossed a declared intake threshold under a declared policy, tolerance, and transform procedure.

The receipt must preserve evidence of its own boundary.

---

## 2. Constitutional Problem

Receipts can drift toward false totality even when every individual receipt is honest.

This happens when a receipt system repeatedly records outputs without preserving threshold awareness.

Over time, users and downstream systems may begin to assume:

- anything not receipted did not happen,
- anything receipted was fully captured,
- conversion into receipt state was frictionless,
- and the ledger represents the world rather than the scoped transformation.

This is calibration drift at the attestation layer.

ALMS rejects that drift.

---

## 3. Three Receipt Territories

Every ALMS receipt must distinguish or acknowledge three territories.

### 3.1 Inside Scope

Phenomena explicitly converted into receipt state.

Inside-scope material is:

- declared,
- transformed,
- hashed,
- replayable,
- and governed by the receipt policy.

### 3.2 Outside Scope

Phenomena not addressed by the receipt system or transform policy.

Outside-scope material is not invalidated by the receipt.

No correspondence claim is made.

### 3.3 Latent / Unconverted

Phenomena materially or operationally compatible with possible receipt conversion, but not converted during this intake cycle.

Latent material is neither failure nor irrelevance.

It is compatible-but-unconverted remainder.

The receipt must not silently collapse latent material into either captured truth or irrelevant noise.

---

## 4. Threshold Awareness

A valid ALMS receipt must acknowledge that conversion into receipt state is an event.

Conversion requires contact with an intake mechanism.

The intake mechanism has:

- boundaries,
- rate limits,
- policy limits,
- transform limits,
- observer limits,
- and temporal placement.

The threshold existed.

Some phenomena may not have crossed it.

Their status remains ambient unless and until separately converted.

---

## 5. Minimum Receipt Boundary Fields

Future ALMS receipt schemas SHOULD include explicit boundary fields equivalent to:

```text
SCOPE: [defined]
TRANSFORMED: [explicit]
TOLERANCE: [stated]
THRESHOLD: [declared]
LATENT: [acknowledged / unresolved]
REMAINDER: [guaranteed / unaddressed]
CORRESPONDENCE_OUTSIDE_SCOPE: [not claimed]
```

These fields are not bureaucratic overhead.

They are constitutional hygiene.

They prevent the receipt from becoming the thing ALMS was built to avoid: an oracle surface.

---

## 6. Required Anti-Oracle Language

Receipt language MUST NOT imply:

```text
This receipt captures the whole event.
This receipt proves the world state.
Unreceipted phenomena are irrelevant.
Unreceipted phenomena did not happen.
Receipted output exhausts correspondence.
```

Preferred receipt language:

```text
This receipt records a scoped transformation.
The threshold existed.
Some phenomena did not cross it.
Their status remains ambient.
Correspondence outside scope is not claimed.
```

---

## 7. Relationship to Sparse Proofs

Sparse coverage is not a defect when honestly declared.

For sparse ALMS surfaces, receipts must preserve the distinction between:

- covered entities,
- uncovered entities,
- and latent or pending entities that may be compatible with future conversion but were not converted in the current cycle.

No interpolation, simulation, or implied coverage may replace this boundary.

---

## 8. Replay Boundary

Replay resolves the transformation.

Replay does not resolve the world.

A successful replay means:

```text
Given declared inputs, declared policy, declared threshold, and declared transform, the output is reproducible within tolerance.
```

It does not mean:

```text
All relevant reality was captured.
All ambient phenomena were converted.
No latent material existed.
The receipt is a total truth object.
```

---

## 9. Final Rule

A receipt becomes more trustworthy when it remembers what it did not convert.

The hash stabilizes.

The threshold is noted.

Ambient phenomena continue at their own rates.

The ledger records the transformation, not the world.

The system continues.
