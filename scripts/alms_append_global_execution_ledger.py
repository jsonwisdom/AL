#!/usr/bin/env python3
"""Compatibility entrypoint for the canonical execution-receipt consumer.

The v0.1 skeleton originally exposed a direct ledger append writer. The canonical
path is now receipt-first:

    alms/execution_receipts/*.json
        -> scripts/alms_consume_execution_receipts.py
        -> alms/JSONWISDOM_GLOBAL_EXECUTION_LEDGER.jsonl

Direct synthetic ledger appends are intentionally disabled so every ledger entry
must resolve back to a sealed execution receipt.
"""

from __future__ import annotations

from alms_consume_execution_receipts import main


if __name__ == "__main__":
    raise SystemExit(main())
