import json
from pathlib import Path

from scripts.emit_mcp_batch import rfc6962_merkle_root

VECTOR_PATH = Path('tests/vectors/mn_mmb_feb2026.json')


def test_expected_root_shape():
    vector = json.loads(VECTOR_PATH.read_text())

    print(
        'DEBUG_VECTOR_SHAPE: '
        + json.dumps(
            {
                'semantic_inference': vector.get('semantic_inference'),
                'authority': vector.get('authority'),
                'expected_root_len': len(vector.get('expected_root', '')),
            },
            sort_keys=True,
        )
    )

    assert vector['semantic_inference'] is False
    assert vector['authority'] is False
    assert len(vector['expected_root']) == 64


def test_rfc6962_empty_tree_stability():
    expected = 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855'
    actual = rfc6962_merkle_root([])

    print(f'DEBUG_MERKLE_EMPTY_ROOT: Expected={expected}, Actual={actual}')

    assert actual == expected
