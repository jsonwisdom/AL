import json
import os
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from scripts.emit_mcp_batch import rfc6962_merkle_root

VECTOR_PATH = Path('tests/vectors/mn_mmb_feb2026.json')


def merkle_debug() -> str:
    return (
        "\n--- MERKLE_DEBUG_STATE ---\n"
        f"REPO_ROOT={REPO_ROOT}\n"
        f"VECTOR_PATH={VECTOR_PATH.resolve()}\n"
        f"CWD={os.getcwd()}\n"
        f"PYTHONPATH_HEAD={sys.path[:3]}\n"
        f"VECTOR_EXISTS={VECTOR_PATH.exists()}\n"
        f"EMPTY_ROOT={rfc6962_merkle_root([])}\n"
        "--------------------------"
    )


def test_rfc6962_empty_tree_stability():
    """Verify empty tree hash to rule out implementation drift."""
    expected = 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855'
    actual = rfc6962_merkle_root([])

    assert actual == expected, (
        'CRITICAL: Merkle Empty Tree Mismatch.\n'
        f'Expected: {expected}\n'
        f'Got:      {actual}'
        f'{merkle_debug()}'
    )


def test_vector_file_existence():
    """Verify existence of test vector before execution."""
    vector_path = str(VECTOR_PATH)

    assert os.path.exists(vector_path), (
        f'CRITICAL: Vector file not found at: {os.path.abspath(vector_path)}\n'
        f'Current Working Directory: {os.getcwd()}'
        f'{merkle_debug()}'
    )


def test_known_good_root_shape():
    vector = json.loads(VECTOR_PATH.read_text())

    assert vector['semantic_inference'] is False, (
        'CRITICAL: semantic_inference must remain false'
        f'{merkle_debug()}'
    )
    assert vector['authority'] is False, (
        'CRITICAL: authority must remain false'
        f'{merkle_debug()}'
    )
    assert len(vector['known_good_root']) == 64, (
        'CRITICAL: known_good_root must be 64 hex characters\n'
        f"Got: {vector.get('known_good_root')}"
        f'{merkle_debug()}'
    )
