import json
import unicodedata
from decimal import Decimal
from typing import Any

class CanonicalizationError(ValueError): pass

def _normalize(x: Any) -> Any:
    if isinstance(x, str):
        return unicodedata.normalize('NFC', x)
    if isinstance(x, list):
        return [_normalize(i) for i in x]
    if isinstance(x, dict):
        return {unicodedata.normalize('NFC', str(k)): _normalize(v) for k, v in x.items()}
    if isinstance(x, float):
        raise CanonicalizationError('floats forbidden; use integers or decimal strings')
    return x

def canonical_bytes(obj: Any) -> bytes:
    obj = _normalize(obj)
    return json.dumps(obj, sort_keys=True, separators=(',', ':'), ensure_ascii=False).encode('utf-8')

def load_json_bytes(raw: bytes) -> Any:
    return json.loads(raw.decode('utf-8'))
