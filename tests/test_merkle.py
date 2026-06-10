import json
import os
from pathlib import Path

from scripts.emit_mcp_batch import rfc6962_merkle_root

VECTOR_PATH = Path('tests/vectors/mn_mmb_feb2026.json')


def print_merkle_debug() -> None:
    print(f"MERKLE_DEBUG_VECTOR_PATH={VECTOR_PATH.resolve()}")
    print(f"MERKLE_DEBUG_CWD={os.getcwd()}")
    print(f"MERKLE_DEBUG_VECTOR_EXISTS={VECTOR_PATH.exists()}")
    print(f"MERKLE_DEBUG_EMPTY_ROOT={rfc6962_merkle_root([])}")


def test_rfc6962_empty_tree_stability():
    """Verify empty tree hash to rule out implementation drift."""
    print_merkle_debug()
    expected = 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855'
    actual = rfc6962_merkle_root([])

    assert actual == expected, (
        'CRITICAL: Merkle Empty Tree Mismatch.\n'
        f'Expected: {expected}\n'
        f'Got:      {actual}'
    )


def test_vector_file_existence():
    """Verify existence of test vector before execution."""
    print_merkle_debug()
    vector_path = str(VECTOR_PATH)

    assert os.path.exists(vector_path), (
        f'CRITICAL: Vector file not found at: {os.path.abspath(vector_path)}\n'
        f'Current Working Directory: {os.getcwd()}'
    )


def test_known_good_root_shape():
    print_merkle_debug()
    vector = json.loads(VECTOR_PATH.read_text())

    assert vector['semantic_inference'] is False
    assert vector['authority'] is False
    assert len(vector['known_good_root']) == 64
