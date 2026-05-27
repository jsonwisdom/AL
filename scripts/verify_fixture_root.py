#!/usr/bin/env python3

import argparse
import json
from pathlib import Path

from emit_mcp_batch import canonical_json_bytes, rfc6962_merkle_root


def load_receipts(receipts_dir: Path):
    receipts = []
    for path in sorted(receipts_dir.glob('*.json')):
        receipt = json.loads(path.read_text())
        if receipt.get('semantic_inference') is not False:
            raise ValueError(f'{path}: semantic_inference must be false')
        if receipt.get('authority') is not False:
            raise ValueError(f'{path}: authority must be false')
        if 'identity_hash' not in receipt:
            raise ValueError(f'{path}: missing identity_hash')
        receipts.append(receipt)
    receipts.sort(key=lambda receipt: receipt['identity_hash'])
    return receipts


def main() -> int:
    parser = argparse.ArgumentParser(description='Verify committed fixture root against vector and manifest.')
    parser.add_argument('--receipts-dir', required=True)
    parser.add_argument('--vector', required=True)
    parser.add_argument('--manifest', required=True)
    args = parser.parse_args()

    receipts = load_receipts(Path(args.receipts_dir))
    vector = json.loads(Path(args.vector).read_text())
    manifest = json.loads(Path(args.manifest).read_text())

    rebuilt_root = rfc6962_merkle_root([canonical_json_bytes(receipt) for receipt in receipts])
    expected_root = vector['expected_root']
    manifest_root = manifest['batch_merkle_root']

    result = {
        'receipt_count': len(receipts),
        'rebuilt_root': rebuilt_root,
        'expected_root': expected_root,
        'manifest_root': manifest_root,
        'semantic_inference': False,
        'authority': False,
        'verified': rebuilt_root == expected_root == manifest_root,
    }
    print(json.dumps(result, indent=2, sort_keys=True))

    return 0 if result['verified'] else 1


if __name__ == '__main__':
    raise SystemExit(main())
