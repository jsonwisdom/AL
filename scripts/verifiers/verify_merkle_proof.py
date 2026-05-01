#!/usr/bin/env python3
import argparse, hashlib, json

def h(hex_left, hex_right):
    return hashlib.sha256((hex_left + hex_right).encode()).hexdigest()

p = argparse.ArgumentParser()
p.add_argument("--leaf", required=True)
p.add_argument("--proof", required=True, help="JSON array: [{\"direction\":\"left|right\",\"sibling\":\"hex\"}]")
p.add_argument("--root", required=True)
args = p.parse_args()

cur = args.leaf.lower().replace("0x","")
root = args.root.lower().replace("0x","")
proof = json.loads(args.proof)

for step in proof:
    sib = step["sibling"].lower().replace("0x","")
    direction = step["direction"]
    if direction == "left":
        cur = h(sib, cur)
    elif direction == "right":
        cur = h(cur, sib)
    else:
        raise SystemExit("BAD_DIRECTION")

print("computed_root=" + cur)
print("expected_root=" + root)

if cur == root:
    print("MERKLE_PROOF_VALID")
else:
    print("MERKLE_PROOF_INVALID")
    raise SystemExit(1)
