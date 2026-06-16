#!/usr/bin/env python3
import json, hashlib, sys
from pathlib import Path

def red(reason):
    print(f"RED_STATE:{reason}")
    sys.exit(1)

def load(path):
    p = Path(path)
    if not p.exists():
        red("missing_receipt")
    try:
        return json.loads(p.read_text())
    except Exception:
        red("malformed_receipt")

def canon_hash(receipt):
    body = dict(receipt)
    body.pop("signature", None)
    body.pop("receipt_hash", None)
    b = json.dumps(body, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(b).hexdigest()

def verify(path):
    r = load(path)
    for k in ["receipt_version","doctrine_version","verifier","commit_sha","generated_at","invariants","summary","signature","receipt_hash"]:
        if k not in r:
            red(f"missing:{k}")

    keys = [f"TC{i:03d}" for i in range(1,20)]
    inv = r["invariants"]
    if set(inv.keys()) != set(keys):
        red("tc_set_mismatch")

    statuses = [inv[k].get("status") for k in keys]
    if any(s not in ("PASS","FAIL") for s in statuses):
        red("bad_status")

    passed, failed = statuses.count("PASS"), statuses.count("FAIL")
    s = r["summary"]
    if s.get("passed") != passed or s.get("failed") != failed or s.get("total") != 19:
        red("summary_mismatch")
    if s.get("state") == "GREEN_STATE" and not (passed == 19 and failed == 0):
        red("green_mismatch")
    if s.get("state") == "RED_STATE" and not (failed > 0):
        red("red_mismatch")
    if s.get("state") not in ("GREEN_STATE","RED_STATE"):
        red("bad_state")

    if canon_hash(r) != r["receipt_hash"]:
        red("hash_mismatch")

    sig = r["signature"]
    for k in ["algorithm","signing_key_id","signed_at","value"]:
        if k not in sig or not sig[k]:
            red("bad_signature")

    if s.get("state") != "GREEN_STATE":
        red("not_green_state")

    print("GREEN_STATE:receipt_verified")
    return 0

if __name__ == "__main__":
    sys.exit(verify(sys.argv[1] if len(sys.argv) > 1 else ".doctrine/receipts/latest.json"))
