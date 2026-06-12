import json
from pathlib import Path

from scripts.emit_mcp_batch import rfc6962_merkle_root

VECTOR_PATH = Path('tests/vectors/mn_mmb_feb2026.json')


def test_known_good_root_shape():
    vector = json.loads(VECTOR_PATH.read_text())

    assert vector['semantic_inference'] is False
    assert vector['authority'] is False
    assert len(vector['known_good_root']) == 64


def test_rfc6962_empty_tree_stability():
    expected = 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855'
    assert rfc6962_merkle_root([]) == expected
