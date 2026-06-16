#!/usr/bin/env python3
"""
verify_runtime_green_receipt.py

Gate: receipt_sealed -> receipt_hash_recorded
Outcomes: VALID | NONCONFORMANT_MISSING_ARTIFACT | NONCONFORMANT_HASH_CHAIN | NONCONFORMANT_STATUS
No fourth state.
"""

import hashlib
import json
import sys
from pathlib import Path

RECEIPT_PATH = Path("_truth/security/runtime_green_receipt.json")
HASH_PATH = Path("_truth/security/runtime_green_receipt.sha256")
REQUIRED_STATUS = "FULL_RUNTIME_GREEN"


def fail(code: str, detail: str) -> None:
    print(f"NONCONFORMANT_{code}: {detail}")
    sys.exit(1)


def canonical_json_bytes(path: Path) -> bytes:
    try:
        obj = json.loads(path.read_bytes())
    except json.JSONDecodeError as exc:
        fail("HASH_CHAIN", f"{path} is not valid JSON: {exc}")
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")


def read_recorded_hash(path: Path) -> str:
    text = path.read_text(encoding="utf-8").strip()
    if not text:
        fail("MISSING_ARTIFACT", f"{path} is empty")
    return text.split()[0]


def main() -> None:
    if not RECEIPT_PATH.exists():
        fail("MISSING_ARTIFACT", f"{RECEIPT_PATH} not found")

    if not HASH_PATH.exists():
        fail("MISSING_ARTIFACT", f"{HASH_PATH} not found")

    canonical = canonical_json_bytes(RECEIPT_PATH)
    computed = hashlib.sha256(canonical).hexdigest()
    recorded = read_recorded_hash(HASH_PATH)

    if computed != recorded:
        fail("HASH_CHAIN", f"computed={computed} recorded={recorded}")

    receipt = json.loads(RECEIPT_PATH.read_bytes())
    status = receipt.get("status")
    if status != REQUIRED_STATUS:
        fail("STATUS", f"expected={REQUIRED_STATUS} actual={status}")

    print(f"VALID: {RECEIPT_PATH} hash={computed[:16]}...")
    sys.exit(0)


if __name__ == "__main__":
    main()
