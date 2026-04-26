#!/usr/bin/env python3
import json, hashlib, sys, subprocess, os
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
BASE = ROOT / "validators/alms_legislative_receipt_v0.1"
KEYS = BASE / "keys/ens_keys.json"
ADAPTER = BASE / "adapters/resolve_public_key.sh"

def canon(obj):
    return json.dumps(obj, sort_keys=True, separators=(",", ":")).encode()

def sha(obj):
    return "sha256:" + hashlib.sha256(canon(obj)).hexdigest()

def load(path):
    return json.loads(Path(path).read_text())

def fail(msg):
    print(json.dumps({"status":"INVALID","reason":msg}, indent=2))
    sys.exit(1)

def ok(extra):
    print(json.dumps({"status":"VALID", **extra}, indent=2))
    sys.exit(0)

def resolve_ens_key(ens):
    try:
        out = subprocess.check_output(
            [str(ADAPTER), ens, "alms.public_key"],
            stderr=subprocess.DEVNULL,
            env=os.environ,
            timeout=12
        ).decode().strip()
        return out if out else None
    except Exception:
        return None

if len(sys.argv) != 2:
    fail("usage: validate_receipt.py receipt.json")

r = load(sys.argv[1])
keys = load(KEYS)

required = ["schema","receipt_id","event_type","actor","object","action","chain","signature","witnesses","anchor","verification"]
for k in required:
    if k not in r:
        fail(f"missing field: {k}")

if r["schema"] != "alms.legislative_receipt.v0.1":
    fail("wrong schema")

ens = r["actor"].get("ens")
pub = r["actor"].get("public_key")
signed_by = r["signature"].get("signed_by")

if signed_by != ens:
    fail("signature signed_by does not match actor ENS")

live_key = resolve_ens_key(ens)
key_source = "ens_live"

if not live_key:
    key_source = "local_registry"
    if ens not in keys:
        fail("ENS key not found in live ENS or local registry")
    if keys[ens].get("status") != "active":
        fail("ENS key is not active")
    live_key = keys[ens].get("public_key")

if live_key != pub:
    fail("actor public_key does not match resolved ENS key")

receipt_copy = dict(r)
claimed_hash = receipt_copy["chain"].get("receipt_hash")
receipt_copy["chain"] = dict(receipt_copy["chain"])
receipt_copy["chain"]["receipt_hash"] = None

actual_hash = sha(receipt_copy)

if claimed_hash != actual_hash:
    fail("receipt_hash mismatch")

roots = [w.get("root") for w in r["witnesses"]]
root = r["anchor"].get("root")

if roots.count(root) < 3:
    fail("missing witness quorum: need >= 3 witnesses on anchor root")

if r["verification"].get("status") != "VERIFIED":
    fail("verification.status is not VERIFIED")

ok({
    "receipt_id": r["receipt_id"],
    "ens": ens,
    "key_source": key_source,
    "receipt_hash": claimed_hash,
    "root": root,
    "witness_quorum": roots.count(root)
})
