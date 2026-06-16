#!/usr/bin/env python3
import argparse, hashlib, json, sys

def clean(x):
    return x.lower().replace("0x", "").strip()

def sha256_pair(left_hex, right_hex):
    return hashlib.sha256(bytes.fromhex(clean(left_hex)) + bytes.fromhex(clean(right_hex))).hexdigest()

def verify(leaf, proof, root):
    cur = clean(leaf)
    for step in proof:
        direction = step["direction"]
        sibling = clean(step["sibling"])

        if direction == "left":
            cur = sha256_pair(sibling, cur)
        elif direction == "right":
            cur = sha256_pair(cur, sibling)
        else:
            raise ValueError(f"bad direction: {direction}")

    return cur, clean(root)

def main():
    ap = argparse.ArgumentParser(description="Verify ALMS/Goblin Court Merkle inclusion proof")
    ap.add_argument("--leaf", required=True)
    ap.add_argument("--proof", required=True, help='JSON array: [{"direction":"left|right","sibling":"hex"}]')
    ap.add_argument("--root", required=True)
    args = ap.parse_args()

    try:
        proof = json.loads(args.proof)
        computed, expected = verify(args.leaf, proof, args.root)
    except Exception as e:
        print(f"MERKLE_PROOF_ERROR: {e}")
        sys.exit(2)

    print(f"computed_root={computed}")
    print(f"expected_root={expected}")

    if computed == expected:
        print("MERKLE_PROOF_VALID")
        sys.exit(0)

    print("MERKLE_PROOF_INVALID")
    sys.exit(1)

if __name__ == "__main__":
    main()
