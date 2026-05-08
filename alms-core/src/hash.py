import hashlib
from copy import deepcopy
from .canonicalize import canonical_bytes

def sha256_prefixed(data: bytes) -> str:
    return 'sha256:' + hashlib.sha256(data).hexdigest()

def hash_object_null_field(obj: dict, field: str) -> str:
    x = deepcopy(obj)
    x[field] = None
    return sha256_prefixed(canonical_bytes(x))
