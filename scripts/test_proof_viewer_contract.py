#!/usr/bin/env python3
import json, hashlib, sys
from pathlib import Path

INDEX = Path("_truth/receipts/index.json")

def fail(code, msg):
    print(f"{code}: {msg}")
    sys.exit(1)

if not INDEX.exists():
    fail("INDEX_MISSING", str(INDEX))

try:
    index = json.loads(INDEX.read_text())
except Exception as e:
    fail("INDEX_PARSE_ERROR", str(e))

receipts = index.get("index", {}).get("receipts")
if not isinstance(receipts, list):
    fail("INVALID_INDEX_SCHEMA", "index.receipts[] missing")

loaded = 0
errors = []

for i, entry in enumerate(receipts):
    path = entry.get("path")
    expected_hash = entry.get("hash")

    if not path:
        errors.append((i, "RECEIPT_PATH_MISSING", "missing path"))
        continue

    p = Path(path)
    if not p.exists():
        errors.append((i, "RECEIPT_MISSING", path))
        continue

    raw = p.read_bytes()
    actual_hash = "sha256:" + hashlib.sha256(raw).hexdigest()

    if expected_hash and actual_hash != expected_hash:
        errors.append((i, "HASH_MISMATCH", f"{path} expected={expected_hash} actual={actual_hash}"))
        continue

    try:
        receipt = json.loads(raw)
    except Exception as e:
        errors.append((i, "RECEIPT_PARSE_ERROR", f"{path}: {e}"))
        continue

    required = ["claim", "algorithm", "timestamp", "signature"]
    missing = [k for k in required if not receipt.get(k)]
    if missing:
        errors.append((i, "RECEIPT_SCHEMA_INVALID", f"{path} missing={missing}"))
        continue

    loaded += 1

if errors:
    for i, code, msg in errors:
        print(f"{code}: receipt[{i}] {msg}")
    if loaded > 0:
        print(f"PARTIAL_LOAD: loaded={loaded} total={len(receipts)} errors={len(errors)}")
        sys.exit(0)
    sys.exit(1)

print(f"FULL_LOAD_OK: loaded={loaded} total={len(receipts)}")
