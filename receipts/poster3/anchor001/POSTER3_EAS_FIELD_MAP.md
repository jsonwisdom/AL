# Poster 3 EAS Field Map

Schema UID:

```txt
0x3bab210b4da3faff084e146075caf9168efb5c9c87f18509bca2c07d7f2e49c
```

Visible EAS fields:

```txt
recipient
merkleRoot bytes32
leafKeccak bytes32
recordRef string
repoCommit string
```

Poster 3 values:

```txt
recipient: jaywisdom.base.eth
merkleRoot: 0xcd45ea74afe9a545d971de87a1710ab3e3db0535d028dd09a9b55c23e4c28193
leafKeccak: 0xe404ae49823e24f9d957ba9a2842cd4419fcd55bd9cc4ee3f8c0a3722f6fd0d2
recordRef: jsonwisdom/AL:receipts/poster3/canonical_settlement_poster3_testnet.final.json
repoCommit: d432715bf0d1578dfb2698fb9f3139dbef478d73
```

Classification:

```json
{
  "merkle_model": "SINGLE_LEAF_ROOT",
  "merkleRoot": "sha256(canonical Poster 3 JSON)",
  "leafKeccak": "keccak256(canonical Poster 3 JSON)",
  "status": "READY_FOR_BASE_EAS_ATTESTATION"
}
```

Operator decision:

- On chain: yes.
- Revocable: no, unless there is a specific reason to support revocation.

Reason: this is a historical proof receipt. If it is wrong later, create a superseding correction receipt. Do not erase or revoke the old evidence path.
