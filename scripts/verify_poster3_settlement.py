#!/usr/bin/env python3
import json, hashlib, sys

def canonical_dumps(obj):
    return json.dumps(obj, sort_keys=True, separators=(',', ':'), ensure_ascii=False)

def sha256_hex(data):
    return "0x" + hashlib.sha256(data).hexdigest()

prehash_path = "receipts/poster3/canonical_settlement_poster3_testnet.prehash.json"
final_path  = "receipts/poster3/canonical_settlement_poster3_testnet.final.json"

with open(prehash_path, 'r') as f:
    prehash = json.load(f)
with open(final_path, 'r') as f:
    final = json.load(f)

assert prehash["receiptHash"] is None
assert prehash["settlement_hash"] is None

computed = sha256_hex(canonical_dumps(prehash).encode('utf-8'))

print(f"  Computed receiptHash: {computed}")
print(f"  Final receiptHash:    {final['receiptHash']}")
print(f"  Final settlement_hash: {final['settlement_hash']}")

c1 = final["receiptHash"] == final["settlement_hash"]
c2 = final["receiptHash"] == computed
c3 = final["settlement_hash"] == computed

print(f"  [{'PASS' if c1 else 'FAIL'}] receiptHash == settlement_hash")
print(f"  [{'PASS' if c2 else 'FAIL'}] receiptHash matches computed")
print(f"  [{'PASS' if c3 else 'FAIL'}] settlement_hash matches computed")

ok = c1 and c2 and c3
print(f"\nRESULT: {'PASS' if ok else 'FAIL'}")
sys.exit(0 if ok else 1)
