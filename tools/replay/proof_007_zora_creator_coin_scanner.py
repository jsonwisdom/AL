#!/usr/bin/env python3
"""
Proof-007 Zora Creator Coin scanner scaffold.

Purpose:
  Find a public evidence case where a Zora/Base creator/deployer address
  differs from the first minter/buyer address.

Boundary:
  This script is a scaffold. It does not claim a mismatch until real event
  sources, transaction hashes, and decoded addresses are supplied or queried.

Inputs:
  --coin  Optional coin/contract address
  --creator-tx Optional creation transaction hash
  --first-mint-tx Optional first mint/buy transaction hash
  --source Optional source surface label

Output:
  JSON matching the Proof-007 evidence shape.
"""

from __future__ import annotations

import argparse
import json
from dataclasses import dataclass, asdict
from typing import Optional, Literal

ComparisonResult = Literal["SAME_ADDRESS", "DIFFERENT_ADDRESS", "INSUFFICIENT_EVIDENCE"]


@dataclass
class Proof007Case:
    proof_id: str
    coin_or_contract_address: Optional[str]
    source_surface: str
    creation_tx_hash_or_event_reference: Optional[str]
    first_mint_or_buy_tx_hash_or_event_reference: Optional[str]
    creator_or_deployer_address: Optional[str]
    first_minter_or_buyer_address: Optional[str]
    comparison_result: ComparisonResult
    evidence_links_or_hashes: list[str]
    neutral_summary: str
    boundary: str


def normalize_address(value: Optional[str]) -> Optional[str]:
    if not value:
        return None
    value = value.strip()
    if value.startswith("0x") and len(value) == 42:
        return value.lower()
    return value


def compare_addresses(creator: Optional[str], first_minter: Optional[str]) -> ComparisonResult:
    creator_norm = normalize_address(creator)
    first_norm = normalize_address(first_minter)
    if not creator_norm or not first_norm:
        return "INSUFFICIENT_EVIDENCE"
    if creator_norm == first_norm:
        return "SAME_ADDRESS"
    return "DIFFERENT_ADDRESS"


def build_case(args: argparse.Namespace) -> Proof007Case:
    creator = normalize_address(args.creator_address)
    first_minter = normalize_address(args.first_minter_address)
    result = compare_addresses(creator, first_minter)

    evidence = []
    for item in [args.coin, args.creator_tx, args.first_mint_tx]:
        if item:
            evidence.append(item)

    if result == "DIFFERENT_ADDRESS":
        summary = "Creator or deployer address differs from first minter or buyer address based on supplied evidence fields."
    elif result == "SAME_ADDRESS":
        summary = "Creator or deployer address matches first minter or buyer address based on supplied evidence fields."
    else:
        summary = "Insufficient evidence to compare creator or deployer address against first minter or buyer address."

    return Proof007Case(
        proof_id="PROOF_007_ZORA_CREATOR_COIN_DEPLOYER_VS_FIRST_MINTER",
        coin_or_contract_address=normalize_address(args.coin),
        source_surface=args.source,
        creation_tx_hash_or_event_reference=args.creator_tx,
        first_mint_or_buy_tx_hash_or_event_reference=args.first_mint_tx,
        creator_or_deployer_address=creator,
        first_minter_or_buyer_address=first_minter,
        comparison_result=result,
        evidence_links_or_hashes=evidence,
        neutral_summary=summary,
        boundary="Result depends only on supplied or queried transaction/event evidence. Token branding, holder lists, or narrative claims are not sufficient.",
    )


def main() -> int:
    parser = argparse.ArgumentParser(description="Proof-007 Zora/Base creator coin scanner scaffold")
    parser.add_argument("--coin", default=None, help="Coin or contract address")
    parser.add_argument("--creator-tx", default=None, help="Creation transaction hash or event reference")
    parser.add_argument("--first-mint-tx", default=None, help="First mint/buy transaction hash or event reference")
    parser.add_argument("--creator-address", default=None, help="Creator/deployer address from evidence")
    parser.add_argument("--first-minter-address", default=None, help="First minter/buyer address from evidence")
    parser.add_argument("--source", default="MANUAL_INPUT", help="Evidence source surface")
    args = parser.parse_args()

    case = build_case(args)
    print(json.dumps(asdict(case), indent=2, sort_keys=True))
    return 0 if case.comparison_result != "INSUFFICIENT_EVIDENCE" else 1


if __name__ == "__main__":
    raise SystemExit(main())
