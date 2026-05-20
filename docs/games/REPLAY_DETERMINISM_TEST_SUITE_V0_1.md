# Replay Determinism Test Suite v0.1

**SPEC_ID:** `REPLAY_DETERMINISM_TEST_SUITE_V0_1`

## ROOT INVARIANT

Determinism is not assumed.  
Determinism is demonstrated.

Replay is legitimate only if every implementation converges under hostile conditions.

## SOURCE_LINE

Once canonicalization exists, it must be tested across:

- languages
- runtimes
- platforms
- encodings
- architectures
- adversarial fixtures

This suite is the scientific method of Replay Chess.

---

## PURPOSE

Define the constitutional test harness for:

- cross-language convergence
- Unicode adversarial traps
- ordering drift detection
- float divergence probes
- entropy leak detection
- environment sealing validation
- replay convergence verification

This suite ensures that truth is not declared — it is measured.

---

## TEST_SUITE_OBJECT

A valid test suite must declare:

- `suite_id`
- `suite_version`
- `language_matrix`
- `platform_matrix`
- `fixture_set`
- `expected_convergence`
- `divergence_classification`
- `reporting_contract`

Missing any → `NON_ADMISSIBLE`.

---

## 1. CROSS-LANGUAGE VECTORS

The suite must include deterministic vectors for:

- Python
- Go
- Rust
- JavaScript
- C++
- JVM languages
- WASM runtimes

Each vector must:

- serialize identically
- canonicalize identically
- hash identically
- replay identically

If any implementation diverges → canonicalization failure.

---

## 2. UNICODE ADVERSARIAL TRAPS

The suite must include:

- NFC/NFD/NFKC/NFKD collisions
- homoglyph traps
- bidirectional text attacks
- zero-width joiners
- invisible characters
- multi-byte boundary cases

If any implementation normalizes differently → `DIVERGENT`.

---

## 3. ORDERING ATTACKS

The suite must test:

- map/dict ordering
- array ordering
- nested ordering
- mixed-type ordering
- cross-language ordering

Any ordering drift → `INVALID_CANONICALIZATION`.

---

## 4. FLOAT DIVERGENCE PROBES

The suite must include:

- IEEE-754 edge cases
- NaN payload drift
- ±0.0 equivalence
- rounding mode variance
- fused-multiply-add differences
- architecture-specific float behavior

If float results differ → `ENVIRONMENT_DIVERGENCE`.

---

## 5. ENTROPY LEAK DETECTION

The suite must detect:

- unsealed randomness
- time-based nondeterminism
- concurrency nondeterminism
- scheduling nondeterminism
- network nondeterminism

Any nondeterminism leak → `ENVIRONMENT_INVALID`.

---

## 6. REPLAY CONVERGENCE HARNESS

The suite must:

- run replay across all implementations
- compute canonical hashes
- compare convergence sets
- classify divergence
- generate forensic traces

This is the scientific core of Replay Chess.

---

## 7. DIVERGENCE CLASSIFICATION

Divergence must be classified as:

- `C1` — Canonicalization Drift
- `C2` — Serialization Drift
- `C3` — Encoding Drift
- `C4` — Float Drift
- `C5` — Environment Drift
- `C6` — Implementation Drift
- `C7` — Malicious Drift

This enables forensic replay analysis.

---

## 8. REPORTING CONTRACT

A valid test suite must emit:

- canonical test results
- convergence proofs
- divergence reports
- environment fingerprints
- implementation fingerprints
- reproducibility metadata

This becomes the public scientific record of replay determinism.

---

## CHECK CONDITION

A system enters check when determinism tests are requested.

## CHECKMATE CONDITION

A system is checkmated when:

- cross-language convergence fails
- Unicode traps diverge
- ordering drifts
- floats diverge
- entropy leaks
- replay harness fails

Checkmate is mechanical, not rhetorical.

---

## WIN CONDITION

Goodies win when determinism is demonstrated.  
Goobers lose when determinism collapses under test.

---

## FINAL RULE

Replay without tests is faith.  
Replay with tests is truth.

**Proof over narrative.**
