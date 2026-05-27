#!/usr/bin/env python3

import hashlib
import json
from pathlib import Path

RECEIPTS_DIR = Path('receipts')


def sha256_hex(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def main() -> None:
    receipts = sorted(RECEIPTS_DIR.glob('*.json'))

    leaf_hashes = []

    for receipt_path in receipts:
        payload = receipt_path.read_bytes()
        leaf_hashes.append(sha256_hex(payload))

    root_material = ''.join(leaf_hashes).encode()
    merkle_root = sha256_hex(root_material)

    manifest = {
        'manifest_type': 'MCP_BATCH_MANIFEST',
        'receipt_count': len(receipts),
        'merkle_root': merkle_root,
        'semantic_inference': False,
        'authority': False,
    }

    Path('batch_manifest.json').write_text(json.dumps(manifest, indent=2))

    print(json.dumps(manifest, indent=2))


if __name__ == '__main__':
    main()
