# Standard Evidence Log v1

This ledger records observer drift reports as human-readable telemetry with replayable SHA-256 receipts.

## Doctrine

- One report = one row = one SHA-256.
- Scope defaults to `cluster_level_breach` unless explicitly proven otherwise.
- `full_model_failure` is not claimed by this ledger.
- Closed/API model weight hashes are not claimed.
- Screenshots are sanity checks, not proof artifacts.
- External anchors such as IPFS, EAS, Base, or ENS are not claimed unless a visible receipt exists.
- Corrections must be appended as new entries, not silent edits.

## Entries

| UTC | Report | Schema | Scope | Status | Style | Truth | Structure | SHA-256 |
|-----|--------|--------|-------|--------|-------|-------|-----------|---------|
| 2026-05-01T20:59Z | 20260501_cheese_truth | 0.2 | cluster_level_breach | TRUTH_ALERT | 0.0 | 0.94 | 0.08 | 894d607b54197eb36fc5cd688303db3b23581f823a150f10bcd3fc6b0dc549b4 | |

<details>
<summary>Receipt: 894d607b</summary>

**Anchor**
- **report_id:** `20260501_cheese_truth`
- **report_path:** `reports/20260501_cheese_truth.json`
- **report_sha256:** `894d607b54197eb36fc5cd688303db3b23581f823a150f10bcd3fc6b0dc549b4`
- **schema_version:** `0.2`
- **utc_observed:** `2026-05-01T20:59Z`

**Attestation**
- **scope:** `cluster_level_breach`
- **not:** `full_model_failure`

**Control Surface Triangle**
```json
{"style":{"status":"NOMINAL","metric":{"D":0.0}},"truth":{"status":"TRUTH_ALERT","metric":{"confidence_gap":0.94}},"structure":{"status":"NOMINAL","metric":{"decay_score":0.08}}}
```

</details>

| 2026-05-01T20:58Z | 20260501_goblin_style | 0.2 | cluster_level_breach | SOVEREIGNTY_ALERT | 14.2 | 0.0 | 0.12 | 3b5965deaa9e3ce0bcb94b49f1b9877a853a74fefbabb71b7727327b8fa57c6b | |

<details>
<summary>Receipt: 3b5965de</summary>

**Anchor**
- **report_id:** `20260501_goblin_style`
- **report_path:** `reports/20260501_goblin_style.json`
- **report_sha256:** `3b5965deaa9e3ce0bcb94b49f1b9877a853a74fefbabb71b7727327b8fa57c6b`
- **schema_version:** `0.2`
- **utc_observed:** `2026-05-01T20:58Z`

**Attestation**
- **scope:** `cluster_level_breach`
- **not:** `full_model_failure`

**Control Surface Triangle**
```json
{"style":{"status":"SOVEREIGNTY_ALERT","metric":{"D":14.2}},"truth":{"status":"NOMINAL","metric":{"confidence_gap":0.0}},"structure":{"status":"NOMINAL","metric":{"decay_score":0.12}}}
```

</details>

| 2026-05-01T21:00Z | 20260501_repetition_structure | 0.2 | cluster_level_breach | STRUCTURAL_ALERT | 0.0 | 0.0 | 0.82 | 644355a7d6dae6d6d83dfab741c2b22d2c61e14d1f5399bd2299adf4c48636e9 | |

<details>
<summary>Receipt: 644355a7</summary>

**Anchor**
- **report_id:** `20260501_repetition_structure`
- **report_path:** `reports/20260501_repetition_structure.json`
- **report_sha256:** `644355a7d6dae6d6d83dfab741c2b22d2c61e14d1f5399bd2299adf4c48636e9`
- **schema_version:** `0.2`
- **utc_observed:** `2026-05-01T21:00Z`

**Attestation**
- **scope:** `cluster_level_breach`
- **not:** `full_model_failure`

**Control Surface Triangle**
```json
{"style":{"status":"NOMINAL","metric":{"D":0.0}},"truth":{"status":"NOMINAL","metric":{"confidence_gap":0.0}},"structure":{"status":"STRUCTURAL_ALERT","metric":{"decay_score":0.82}}}
```

</details>

