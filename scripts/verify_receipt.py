#!/usr/bin/env python3
"""Independent receipt verification CLI."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from alms.receipt_verifier import ReceiptVerifier


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--storage-path", required=True)
    parser.add_argument("--receipt-hash", required=True)
    args = parser.parse_args()

    verifier = ReceiptVerifier(Path(args.storage_path))
    result = verifier.verify_receipt_hash(args.receipt_hash)

    print(json.dumps(result, indent=2))

    if result.get("status") == "RECEIPT_VERIFIED":
        return 0

    return 1


if __name__ == "__main__":
    raise SystemExit(main())
