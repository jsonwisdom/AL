import json
from pathlib import Path

from scripts.emit_mcp_batch import rfc6962_merkle_root

VECTOR_PATH = Path('tests/vectors/mn_mmb_feb2026.json')
DEBUG_PATH = Path('merkle_debug.json')


def write_debug(payload):
    DEBUG_PATH.write_text(json.dumps(payload, indent=2, sort_keys=True) + '\n')


def test_expected_root_shape():
    vector = json.loads(VECTOR_PATH.read_text())
    payload = {
        'test': 'test_expected_root_shape',
        'vector_path': str(VECTOR_PATH),
        'semantic_inference': vector.get('semantic_inference'),
        'authority': vector.get('authority'),
        'expected_root': vector.get('expected_root'),
        'expected_root_len': len(vector.get('expected_root', '')),
        'vector_keys': sorted(vector.keys()),
    }
    write_debug(payload)
    print('DEBUG_VECTOR_SHAPE: ' + json.dumps(payload, sort_keys=True))

    assert vector['semantic_inference'] is False
    assert vector['authority'] is False
    assert len(vector['expected_root']) == 64


def test_rfc6962_empty_tree_stability():
    expected = 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855'
    actual = rfc6962_merkle_root([])
    payload = {
        'test': 'test_rfc6962_empty_tree_stability',
        'expected': expected,
        'actual': actual,
        'verified': actual == expected,
    }
    write_debug(payload)
    print('DEBUG_MERKLE_EMPTY_ROOT: ' + json.dumps(payload, sort_keys=True))

    assert actual == expected
