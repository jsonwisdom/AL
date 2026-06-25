"""
receiptctl.py — Constitutional Receipt Control Surface v0.1
"""

import argparse
import json
import sys

from claim_pipeline import create_claim_verification_receipt, save_receipt
from map_query import find_by_claim_text, find_by_receipt_id, summarize_map
from receipt import verify_receipt
from world_map import append_world_map_entry


def cmd_verify(args) -> int:
    result = verify_receipt(args.receipt)
    print(json.dumps(result, indent=2))
    return 0 if result.get("valid") else 1


def cmd_claim(args) -> int:
    receipt = create_claim_verification_receipt(args.text, human_approved=args.approve)
    saved_path = save_receipt(receipt)
    print(f"Receipt created: {receipt['receipt_id']}")
    print(f"Authorization: {receipt['authorization']['result']}")
    if args.approve and args.ingest:
        map_id = append_world_map_entry(saved_path)
        print(f"Ingested: {map_id}" if map_id else "Ingest rejected")
        return 0 if map_id else 1
    if args.ingest and not args.approve:
        print("Ingest skipped: --ingest requires explicit --approve")
    return 0


def cmd_map(args) -> int:
    if args.summary:
        print(json.dumps(summarize_map(args.map), indent=2))
    elif args.receipt:
        print(json.dumps(find_by_receipt_id(args.receipt, args.map), indent=2))
    elif args.search:
        print(json.dumps(find_by_claim_text(args.search, args.map), indent=2))
    else:
        print("Use --summary, --receipt, or --search")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(prog="receiptctl", description="Constitutional Receipt CLI")
    subparsers = parser.add_subparsers(dest="command", required=True)

    p_verify = subparsers.add_parser("verify", help="Verify a receipt")
    p_verify.add_argument("receipt")
    p_verify.set_defaults(func=cmd_verify)

    p_claim = subparsers.add_parser("claim", help="Process a claim")
    p_claim.add_argument("text")
    p_claim.add_argument("--approve", action="store_true")
    p_claim.add_argument("--ingest", action="store_true")
    p_claim.set_defaults(func=cmd_claim)

    p_map = subparsers.add_parser("map", help="Query world map")
    p_map.add_argument("--summary", action="store_true")
    p_map.add_argument("--receipt")
    p_map.add_argument("--search")
    p_map.add_argument("--map", default="world_map.jsonl")
    p_map.set_defaults(func=cmd_map)

    args = parser.parse_args()
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
