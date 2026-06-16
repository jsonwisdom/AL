#!/usr/bin/env python3
"""
Deterministic circuit compilation and hash extraction.
Usage: python3 compile_and_hash.py [--json] [--verify <expected_hash>]
"""

import json
import hashlib
import subprocess
import sys
import argparse
from pathlib import Path
from datetime import datetime

def sha256_json(obj):
    canonical = json.dumps(obj, sort_keys=True, separators=(',', ':'))
    return f"sha256:{hashlib.sha256(canonical.encode()).hexdigest()}"

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--json', action='store_true', help='Output as JSON')
    parser.add_argument('--verify', type=str, help='Expected circuit_hash to verify against')
    args = parser.parse_args()
    
    target_dir = Path("target")
    result = {"status": "unknown", "circuit_hash": None, "build_receipt_hash": None}
    
    # Find ACIR file
    acir_files = list(target_dir.glob("*.json"))
    if not acir_files:
        result["status"] = "error"
        result["error"] = "No .json files found in target/ (run nargo compile first)"
        if args.json:
            print(json.dumps(result, indent=2))
        else:
            print(f"❌ {result['error']}")
        sys.exit(1)
    
    acir_file = acir_files[0]
    with open(acir_file, 'r') as f:
        acir_data = json.load(f)
    
    circuit_hash = sha256_json(acir_data)
    result["circuit_hash"] = circuit_hash
    result["circuit_file"] = str(acir_file)
    
    # Get noir version
    noir_version = subprocess.run(['nargo', '--version'], capture_output=True, text=True).stdout.strip()
    result["noir_version"] = noir_version
    
    # Build receipt hash
    receipt_parts = {
        "circuit_hash": circuit_hash,
        "noir_version": noir_version,
        "timestamp": datetime.now(timezone.utc).isoformat()
    }
    build_receipt_hash = sha256_json(receipt_parts)
    result["build_receipt_hash"] = build_receipt_hash
    result["status"] = "success"
    
    # Verify against expected if provided
    if args.verify:
        expected_raw = args.verify.replace('sha256:', '')
        actual_raw = circuit_hash.replace('sha256:', '')
        if expected_raw == actual_raw:
            result["verification"] = "passed"
        else:
            result["verification"] = "failed"
            result["expected"] = args.verify
            result["status"] = "mismatch"
    
    if args.json:
        print(json.dumps(result, indent=2))
    else:
        print(f"✅ circuit_hash: {circuit_hash}")
        print(f"✅ build_receipt_hash: {build_receipt_hash}")
        if args.verify:
            print(f"✅ Verification: {result['verification']}")
    
    sys.exit(0 if result["status"] in ["success", "passed"] else 1)

if __name__ == "__main__":
    main()
