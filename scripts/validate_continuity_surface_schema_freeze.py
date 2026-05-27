#!/usr/bin/env python3
import json, hashlib, sys
from pathlib import Path

SCHEMA_PATH = Path("schemas/continuity_surface.v1.schema.json")
RECEIPT_PATH = Path("receipts/continuity_surface_schema_freeze.v1.json")

def load_json(path):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        print(f"[ERROR] Missing file: {path}", file=sys.stderr); sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"[ERROR] Invalid JSON in {path}: {e}", file=sys.stderr); sys.exit(1)

def canonicalize_jcs(obj):
    return json.dumps(obj, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")

def main():
    schema_obj = load_json(SCHEMA_PATH)
    receipt_obj = load_json(RECEIPT_PATH)

    if receipt_obj.get("canonicalization") != "JCS": sys.exit("[ERROR] receipt.canonicalization must be JCS")
    if receipt_obj.get("hash_algorithm") != "sha256": sys.exit("[ERROR] receipt.hash_algorithm must be sha256")
    if receipt_obj.get("status") != "FROZEN": sys.exit("[ERROR] receipt.status must be FROZEN")

    expected = receipt_obj.get("schema_sha256")
    actual = "sha256:" + hashlib.sha256(canonicalize_jcs(schema_obj)).hexdigest()

    if actual != expected:
        print("[ERROR] Continuity surface schema hash mismatch", file=sys.stderr)
        print(f"  Expected: {expected}", file=sys.stderr)
        print(f"  Actual:   {actual}", file=sys.stderr)
        sys.exit(1)

    print("[OK] Continuity surface schema matches frozen commitment")

if __name__ == "__main__":
    main()
