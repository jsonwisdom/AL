#!/usr/bin/env python3

import argparse
import json
from pathlib import Path
from emit_mcp_batch import canonical_json_bytes, rfc6962_merkle_root


def main() -> int:
    parser = argparse.ArgumentParser(description='Verify replay manifest against receipt files.')
    parser.add_argument('--receipts-dir', default='receipts')
    parser.add_argument('--manifest', default='batch_manifest.json')
    args = parser.parse_args()

    receipts_dir = Path(args.receipts_dir)
    manifest_path = Path(args.manifest)

    manifest = json.loads(manifest_path.read_text())

    receipts = []
    for path in sorted(receipts_dir.glob('*.json')):
        receipt = json.loads(path.read_text())
        receipts.append(receipt)

    receipts.sort(key=lambda item: item['identity_hash'])

    leaves = [canonical_json_bytes(receipt) for receipt in receipts]

    rebuilt_root = rfc6962_merkle_root(leaves)
    expected_root = manifest.get('merkle_root') or manifest.get('batch_merkle_root')

    result = {
        'manifest': str(manifest_path),
        'receipts_dir': str(receipts_dir),
        'expected_root': expected_root,
        'rebuilt_root': rebuilt_root,
        'receipt_count': len(receipts),
        'verified': rebuilt_root == expected_root,
        'semantic_inference': False,
        'authority': False,
    }

    print(json.dumps(result, indent=2, sort_keys=True))

    return 0 if result['verified'] else 1


if __name__ == '__main__':
    raise SystemExit(main())
