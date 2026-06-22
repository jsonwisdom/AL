# ACTIVE_LANES.md

Schema Version: `1.0`

> Generated from `ACTIVE_LANES.json`. Do not hand-edit this file.

## Policy

NO LANE STATUS WITHOUT RECEIPT.

`GREEN` requires `status_source=VERIFIED_RECEIPT`, `receipt_ptr != null`, `replay_verdict=PASS`, and `delta_h=0`.

## Lanes

| LANE | STATUS | STATUS_SOURCE | RECEIPT_PTR | REPLAY_VERDICT | DELTA_H |
| :--- | :--- | :--- | :--- | :--- | ---: |
| AL | REPORTED_UNVERIFIED | REPORTED_RECEIPT | NULL | UNAVAILABLE | 0 |
| ZTVS | REPORTED_UNVERIFIED | REPORTED_RECEIPT | NULL | UNAVAILABLE | 0 |
| COMPUTERWISDOM | REPORTED | INFERRED | NULL | UNAVAILABLE | 0 |
| JOY | REPORTED | INFERRED | NULL | UNAVAILABLE | 0 |
| CWaaS | REPORTED | INFERRED | NULL | UNAVAILABLE | 0 |

## Replay Note

This file is a projection artifact. The admissible source is `ACTIVE_LANES.json`.
