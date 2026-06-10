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
    expected_count = manifest.get('receipt_count')

    receipt_paths = sorted(receipts_dir.glob('*.json'))
    receipts = []
    for path in receipt_paths:
        receipt = json.loads(path.read_text())
        receipts.append(receipt)

    receipts.sort(key=lambda item: item['identity_hash'])

    leaves = [canonical_json_bytes(receipt) for receipt in receipts]

    rebuilt_root = rfc6962_merkle_root(leaves)
    expected_root = manifest.get('merkle_root') or manifest.get('batch_merkle_root')
    count_matches = expected_count is None or len(receipts) == expected_count

    result = {
        'manifest': str(manifest_path),
        'receipts_dir': str(receipts_dir),
        'expected_root': expected_root,
        'rebuilt_root': rebuilt_root,
        'expected_receipt_count': expected_count,
        'receipt_count': len(receipts),
        'receipt_files': [str(path) for path in receipt_paths],
        'receipt_identity_hashes': [receipt.get('identity_hash') for receipt in receipts],
        'verified': rebuilt_root == expected_root and count_matches,
        'semantic_inference': False,
        'authority': False,
    }

    print(json.dumps(result, indent=2, sort_keys=True), flush=True)

    if expected_count is not None and len(receipts) != expected_count:
        print('DEBUG_RECEIPT_COUNT_MISMATCH:', flush=True)
        print(f'  Expected Count: {expected_count}', flush=True)
        print(f'  Observed Count: {len(receipts)}', flush=True)
        print(f'  Manifest Path: {manifest_path}', flush=True)
        print(f'  Receipts Dir: {receipts_dir}', flush=True)
        print(f'  Receipt Files: {[str(path) for path in receipt_paths]}', flush=True)
        return 1

    if rebuilt_root != expected_root:
        print('DEBUG_MANIFEST_MISMATCH:', flush=True)
        print(f'  Expected: {expected_root}', flush=True)
        print(f'  Rebuilt:  {rebuilt_root}', flush=True)
        print(f'  Manifest Path: {manifest_path}', flush=True)
        print(f'  Receipts Dir: {receipts_dir}', flush=True)
        print(f'  Receipt Count: {len(receipts)}', flush=True)
        print(f'  Receipt Files: {[str(path) for path in receipt_paths]}', flush=True)
        print(f"  Identity Hashes: {[receipt.get('identity_hash') for receipt in receipts]}", flush=True)
        return 1

    return 0


if __name__ == '__main__':
    raise SystemExit(main())
