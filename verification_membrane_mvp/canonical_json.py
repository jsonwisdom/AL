import json
from typing import Any, Dict


def canonical_json(obj: Dict[str, Any]) -> str:
    """Serialize to canonical JSON: sorted keys, no extra spaces, deterministic."""
    return json.dumps(obj, sort_keys=True, separators=(",", ":"))


def sha256_canonical(obj: Dict[str, Any]) -> str:
    import hashlib
    return hashlib.sha256(canonical_json(obj).encode()).hexdigest()
