#!/usr/bin/env python3

import json
from pathlib import Path
from emit_mcp_batch import canonical_json_bytes, rfc6962_leaf_hash, rfc6962_merkle_root

RECEIPTS_DIR = Path('receipts')
MANIFEST_PATH = Path('batch_manifest.json')


def main() -> int:
    manifest = json.loads(MANIFEST_PATH.read_text())

    receipts = []
    for path in sorted(RECEIPTS_DIR.glob('*.json')):
        receipt = json.loads(path.read_text())
        receipts.append(receipt)

    receipts.sort(key=lambda item: item['identity_hash'])

    leaves = [canonical_json_bytes(receipt) for receipt in receipts]

    rebuilt_root = rfc6962_merkle_root(leaves)
    expected_root = manifest['merkle_root']

    print(json.dumps({
        'expected_root': expected_root,
        'rebuilt_root': rebuilt_root,
        'receipt_count': len(receipts),
        'verified': rebuilt_root == expected_root,
        'semantic_inference': False,
        'authority': False,
    }, indent=2))

    return 0 if rebuilt_root == expected_root else 1


if __name__ == '__main__':
    raise SystemExit(main())
