# REPLAY.md — jaywisdom.base.eth Receipt Machine

## Purpose

This document explains how to verify the jaywisdom.base.eth Receipt Machine from public GitHub state before IPFS, EAS, or Base anchoring.

## Current Public State

- Repository: jsonwisdom/AL
- Current HEAD: 85395e0739a7462abdbe1c5b9cc292c1a25e5649
- Root receipt commit: 5f110e4aacb57dd9d8a8b2800b16ad608dfc207d
- Root receipt SHA256: 16dc16d0c1774ba14334261ab60ffa64b20ce3e1ed13b5dc94745e8603617c65
- Status: GITHUB_PROOF_READY_IPFS_DEFERRED
- IPFS: DEFERRED
- EAS/Base: PENDING

## Verify Root Receipt

Run:

    git clone https://github.com/jsonwisdom/AL.git
    cd AL
    git checkout 5f110e4aacb57dd9d8a8b2800b16ad608dfc207d
    sha256sum receipts/IDENTITY_ROOT_RECEIPT_001.json

Expected:

    16dc16d0c1774ba14334261ab60ffa64b20ce3e1ed13b5dc94745e8603617c65  receipts/IDENTITY_ROOT_RECEIPT_001.json

## Canon

Receipt first.
Anchor second.
Profit third.
