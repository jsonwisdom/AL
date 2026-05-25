#!/usr/bin/env python3
"""
Proof-007 Zora Creator Coin scanner scaffold.

Purpose:
  Find a public evidence case where a Zora/Base creator/deployer address
  differs from the first minter/buyer address.

Boundary:
  This script accepts wallet/factory targeting inputs, but it does not claim
  live chain discovery unless transaction/event evidence is supplied or a
  future API-backed scanner module is added.

Example manual evidence run:
  python tools/replay/proof_007_zora_creator_coin_scanner.py \
    --coin 0x... \
    --creator-tx 0x... \
    --first-mint-tx 0x... \
    --creator-address 0x... \
    --first-minter-address 0x... \
    --source BASESCAN_MANUAL

Example target-only run:
  python tools/replay/proof_007_zora_creator_coin_scanner.py \
    --wallet 0x829AdfEdBe565F9885a7eA6Bc78912acAef055E2 \
    --network base \
    --factory 0x777777751622c0d3258f214F9DF38E35BF45baF3
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
    network: str
    factory_address: Optional[str]
    target_wallet: Optional[str]
    coin_or_contract_address: Optional[str]
    source_surface: str
    creation_tx_hash_or_event_reference: Optional[str]
    first_mint_or_buy_tx_hash_or_event_reference: Optional[str]
    creator_or_deployer_address: Optional[str]
    first_minter_or_buyer_address: Optional[str]
    comparison_result: ComparisonResult
    evidence_links_or_hashes: list[str]
    neutral_summary: str
    next_required_action: str
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
    for item in [args.coin, args.creator_tx, args.first_mint_tx, args.factory, args.wallet]:
        if item:
            evidence.append(item)

    if result == "DIFFERENT_ADDRESS":
        summary = "Creator or deployer address differs from first minter or buyer address based on supplied evidence fields."
        next_action = "Review evidence links and commit Proof-007 receipt candidate."
    elif result == "SAME_ADDRESS":
        summary = "Creator or deployer address matches first minter or buyer address based on supplied evidence fields."
        next_action = "Record as non-mismatch case or continue scanning."
    else:
        summary = "Insufficient evidence to compare creator or deployer address against first minter or buyer address."
        next_action = "Fetch creation transaction/event and first mint/buy transaction/event for a specific coin contract."

    return Proof007Case(
        proof_id="PROOF_007_ZORA_CREATOR_COIN_DEPLOYER_VS_FIRST_MINTER",
        network=args.network,
        factory_address=normalize_address(args.factory),
        target_wallet=normalize_address(args.wallet),
        coin_or_contract_address=normalize_address(args.coin),
        source_surface=args.source,
        creation_tx_hash_or_event_reference=args.creator_tx,
        first_mint_or_buy_tx_hash_or_event_reference=args.first_mint_tx,
        creator_or_deployer_address=creator,
        first_minter_or_buyer_address=first_minter,
        comparison_result=result,
        evidence_links_or_hashes=evidence,
        neutral_summary=summary,
        next_required_action=next_action,
        boundary="Result depends only on supplied or queried transaction/event evidence. Token branding, holder lists, profile pages, or narrative claims are not sufficient.",
    )


def main() -> int:
    parser = argparse.ArgumentParser(description="Proof-007 Zora/Base creator coin scanner scaffold")
    parser.add_argument("--wallet", default=None, help="Target wallet to scan")
    parser.add_argument("--network", default="base", help="Network label")
    parser.add_argument("--factory", default=None, help="Factory contract address")
    parser.add_argument("--coin", default=None, help="Coin or contract address")
    parser.add_argument("--creator-tx", default=None, help="Creation transaction hash or event reference")
    parser.add_argument("--first-mint-tx", default=None, help="First mint/buy transaction hash or event reference")
    parser.add_argument("--creator-address", default=None, help="Creator/deployer address from evidence")
    parser.add_argument("--first-minter-address", default=None, help="First minter/buyer address from evidence")
    parser.add_argument("--source", default="MANUAL_OR_TARGET_INPUT", help="Evidence source surface")
    args = parser.parse_args()

    case = build_case(args)
    print(json.dumps(asdict(case), indent=2, sort_keys=True))
    return 0 if case.comparison_result != "INSUFFICIENT_EVIDENCE" else 1


if __name__ == "__main__":
    raise SystemExit(main())
