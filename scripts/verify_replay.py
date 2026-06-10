#!/usr/bin/env python3

import argparse
import json
from pathlib import Path

from scripts.emit_mcp_batch import canonical_json_bytes, rfc6962_merkle_root


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
    receipts.sort(key=lambda item: item['identity_hash'])
    return receipts


def manifest_root(manifest: dict) -> str:
    if 'merkle_root' in manifest:
        return manifest['merkle_root']
    if 'batch_merkle_root' in manifest:
        return manifest['batch_merkle_root']
    raise ValueError('manifest missing merkle_root or batch_merkle_root')


def vector_root(vector: dict) -> str | None:
    if 'expected_root' in vector:
        return vector['expected_root']
    if 'known_good_root' in vector:
        return vector['known_good_root']
    return None


def main() -> int:
    parser = argparse.ArgumentParser(description='Verify replay manifest root against committed receipts.')
    parser.add_argument('--receipts-dir', default='receipts')
    parser.add_argument('--manifest', default='batch_manifest.json')
    parser.add_argument('--vector')
    args = parser.parse_args()

    receipts = load_receipts(Path(args.receipts_dir))
    manifest = json.loads(Path(args.manifest).read_text())
    vector = json.loads(Path(args.vector).read_text()) if args.vector else None

    rebuilt_root = rfc6962_merkle_root([canonical_json_bytes(receipt) for receipt in receipts])
    expected_manifest_root = manifest_root(manifest)
    expected_vector_root = vector_root(vector) if vector else None

    verified = rebuilt_root == expected_manifest_root
    if expected_vector_root is not None:
        verified = verified and rebuilt_root == expected_vector_root

    result = {
        'receipt_count': len(receipts),
        'rebuilt_root': rebuilt_root,
        'manifest_root': expected_manifest_root,
        'vector_root': expected_vector_root,
        'semantic_inference': False,
        'authority': False,
        'verified': verified,
    }
    print(json.dumps(result, indent=2, sort_keys=True))

    return 0 if verified else 1


if __name__ == '__main__':
    raise SystemExit(main())
