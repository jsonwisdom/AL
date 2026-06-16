#!/usr/bin/env python3
"""Build a Computer Wisdom public verifier URL.

Usage:
  python3 scripts/build_public_verify_link.py \
    --commit <git_commit_sha> \
    --root <sha256_or_merkle_root> \
    --base-url https://jsonwisdom.github.io/AL/_truth/meta/public_exports/verify.html

This script does not sign, attest, or touch a wallet.
It only prepares a public verification link and optional QR-code URL.
"""

import argparse
import json
import urllib.parse


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--commit", required=True, help="GitHub commit SHA")
    parser.add_argument("--root", required=True, help="Expected SHA-256 / Merkle root")
    parser.add_argument(
        "--base-url",
        default="https://jsonwisdom.github.io/AL/_truth/meta/public_exports/verify.html",
        help="Published verify.html URL",
    )
    parser.add_argument("--eas", default="", help="Optional EAS attestation UID")
    args = parser.parse_args()

    params = {
        "commit": args.commit.strip(),
        "root": args.root.strip().replace("sha256:", ""),
    }
    if args.eas.strip():
        params["eas"] = args.eas.strip()

    verify_url = args.base_url + "?" + urllib.parse.urlencode(params)
    qr_url = "https://quickchart.io/qr?" + urllib.parse.urlencode({"text": verify_url})

    out = {
        "artifact": "CW_PUBLIC_VERIFY_LINK",
        "wallet_required": False,
        "signing_required": False,
        "commit": params["commit"],
        "root": params["root"],
        "eas": params.get("eas"),
        "verify_url": verify_url,
        "qr_url": qr_url,
    }
    print(json.dumps(out, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
