import json
import os
from pathlib import Path

from scripts.emit_mcp_batch import rfc6962_merkle_root

VECTOR_PATH = Path('tests/vectors/mn_mmb_feb2026.json')


def test_rfc6962_empty_tree_stability():
    """Verify empty tree hash to rule out implementation drift."""
    expected = 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855'
    actual = rfc6962_merkle_root([])

    assert actual == expected, (
        'CRITICAL: Merkle Empty Tree Mismatch.\n'
        f'Expected: {expected}\n'
        f'Got:      {actual}'
    )


def test_vector_file_existence():
    """Verify existence of test vector before execution."""
    vector_path = str(VECTOR_PATH)

    assert os.path.exists(vector_path), (
        f'CRITICAL: Vector file not found at: {os.path.abspath(vector_path)}\n'
        f'Current Working Directory: {os.getcwd()}'
    )


def test_known_good_root_shape():
    vector = json.loads(VECTOR_PATH.read_text())

    assert vector['semantic_inference'] is False
    assert vector['authority'] is False
    assert len(vector['known_good_root']) == 64
