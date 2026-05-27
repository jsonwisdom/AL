#!/usr/bin/env python3

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any

RECEIPTS_DIR = Path('receipts')


def sha256(data: bytes) -> bytes:
    return hashlib.sha256(data).digest()


def sha256_hex(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def canonical_json_bytes(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(',', ':')).encode('utf-8')


def rfc6962_leaf_hash(data: bytes) -> bytes:
    return sha256(b'\x00' + data)


def rfc6962_node_hash(left: bytes, right: bytes) -> bytes:
    return sha256(b'\x01' + left + right)


def rfc6962_merkle_root(leaves: list[bytes]) -> str:
    if not leaves:
        return sha256(b'').hex()
    level = [rfc6962_leaf_hash(leaf) for leaf in leaves]
    while len(level) > 1:
        next_level: list[bytes] = []
        for i in range(0, len(level), 2):
            if i + 1 < len(level):
                next_level.append(rfc6962_node_hash(level[i], level[i + 1]))
            else:
                next_level.append(level[i])
        level = next_level
    return level[0].hex()


def load_receipts(receipts_dir: Path) -> list[tuple[Path, dict[str, Any]]]:
    loaded: list[tuple[Path, dict[str, Any]]] = []
    for path in sorted(receipts_dir.glob('*.json')):
        receipt = json.loads(path.read_text())
        if receipt.get('semantic_inference') is not False:
            raise ValueError(f'{path}: semantic_inference must be false')
        if receipt.get('authority') is not False:
            raise ValueError(f'{path}: authority must be false')
        if 'identity_hash' not in receipt:
            raise ValueError(f'{path}: missing identity_hash')
        loaded.append((path, receipt))
    return loaded


def main() -> None:
    parser = argparse.ArgumentParser(description='Emit deterministic MCP batch Merkle manifest.')
    parser.add_argument('--receipts-dir', default=str(RECEIPTS_DIR))
    parser.add_argument('--manifest-out', default='batch_manifest.json')
    parser.add_argument('--leaf-order-out', default='leaf_order.json')
    args = parser.parse_args()

    receipts_dir = Path(args.receipts_dir)
    loaded = load_receipts(receipts_dir)
    loaded.sort(key=lambda item: item[1]['identity_hash'])

    leaves = [canonical_json_bytes(receipt) for _, receipt in loaded]
    leaf_order = [
        {
            'leaf_index': index,
            'path': str(path),
            'identity_hash': receipt['identity_hash'],
            'leaf_hash': rfc6962_leaf_hash(canonical_json_bytes(receipt)).hex(),
        }
        for index, (path, receipt) in enumerate(loaded)
    ]

    merkle_root = rfc6962_merkle_root(leaves)

    manifest = {
        'manifest_type': 'MCP_BATCH_MANIFEST',
        'version': '0.1',
        'receipt_count': len(loaded),
        'leaf_ordering': 'identity_hash_lexicographic_ascending',
        'merkle_algorithm': 'RFC6962_SHA256_DOMAIN_SEPARATED',
        'merkle_root': merkle_root,
        'semantic_inference': False,
        'authority': False,
    }

    Path(args.manifest_out).write_text(json.dumps(manifest, indent=2, sort_keys=True) + '\n')
    Path(args.leaf_order_out).write_text(json.dumps(leaf_order, indent=2, sort_keys=True) + '\n')

    print(json.dumps(manifest, indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
