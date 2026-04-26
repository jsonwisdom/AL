#!/usr/bin/env python3
import json, hashlib
from pathlib import Path

OUT = Path("testdata/legislative_receipts")

def canon(o):
    return json.dumps(o, sort_keys=True, separators=(",", ":")).encode()

def sha(o):
    return "sha256:" + hashlib.sha256(canon(o)).hexdigest()

def finalize(obj):
    tmp = json.loads(json.dumps(obj))
    tmp["chain"]["receipt_hash"] = None
    obj["chain"]["receipt_hash"] = sha(tmp)
    return obj

base = {
  "schema": "alms.legislative_receipt.v0.1",
  "receipt_id": "vote_test_001",
  "event_type": "floor_vote",
  "jurisdiction": "US_CONGRESS",
  "chamber": "HOUSE",
  "session": "119",
  "actor": {
    "member_id": "HOUSE_MN_06",
    "display_name": "Representative Test",
    "ens": "member.mn06.transparency.eth",
    "public_key": "did:key:test"
  },
  "object": {
    "bill_id": "HR-1234",
    "bill_title": "Example Act",
    "bill_text_cid": "ipfs://bafyexample",
    "bill_text_hash": "sha256:billhash"
  },
  "action": {
    "vote": "YES",
    "timestamp_utc": "2026-04-26T18:30:00Z",
    "source_system": "house_clerk_vote_system",
    "device_attestation": "sig:hardware-key"
  },
  "chain": {
    "prev_hash": "sha256:previous",
    "receipt_hash": None,
    "merkle_leaf_hash": "sha256:leaf"
  },
  "signature": {
    "algorithm": "ed25519",
    "signed_by": "member.mn06.transparency.eth",
    "signature": "base64:test"
  },
  "witnesses": [
    {"operator":"house_clerk_node","root":"sha256:root","signed_root":"sig:1"},
    {"operator":"university_monitor_001","root":"sha256:root","signed_root":"sig:2"},
    {"operator":"ngo_monitor_001","root":"sha256:root","signed_root":"sig:3"}
  ],
  "anchor": {
    "network": "base",
    "ens_name": "votes.transparency.eth",
    "ens_text_key": "alms.root.latest",
    "root": "sha256:root",
    "tx_hash": "0xabc"
  },
  "verification": {
    "status": "VERIFIED",
    "inclusion_proof": ["sha256:a","sha256:b"],
    "witness_quorum": "3_of_5",
    "verified_at": "2026-04-26T18:32:00Z"
  }
}

# VALID
valid = finalize(json.loads(json.dumps(base)))

# TAMPERED (hash NOT recomputed on purpose)
tampered = json.loads(json.dumps(valid))
tampered["action"]["vote"] = "NO"

# BAD QUORUM (hash recomputed AFTER change)
bad_quorum = json.loads(json.dumps(base))
bad_quorum["witnesses"] = bad_quorum["witnesses"][:2]
bad_quorum = finalize(bad_quorum)

for name, obj in {
  "valid_vote_receipt.json": valid,
  "tampered_vote_receipt.json": tampered,
  "missing_witness_quorum.json": bad_quorum
}.items():
    (OUT / name).write_text(json.dumps(obj, indent=2) + "\n")
