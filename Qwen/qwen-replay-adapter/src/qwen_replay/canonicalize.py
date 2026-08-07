from __future__ import annotations

import hashlib
import json
import unicodedata
from typing import Any


def normalize(value: Any) -> Any:
    if isinstance(value, str):
        return unicodedata.normalize("NFC", value)
    if isinstance(value, list):
        return [normalize(item) for item in value]
    if isinstance(value, dict):
        return {
            unicodedata.normalize("NFC", str(key)): normalize(val)
            for key, val in value.items()
        }
    return value


def canonical_bytes(value: Any) -> bytes:
    return json.dumps(
        normalize(value),
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
        allow_nan=False,
    ).encode("utf-8")


def sha256_value(value: Any) -> str:
    return "sha256:" + hashlib.sha256(canonical_bytes(value)).hexdigest()


def sha256_file(path: str) -> str:
    digest = hashlib.sha256()
    with open(path, "rb") as handle:
        for chunk in iter(lambda: handle.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()


def parse_receipt_input(params: str | dict) -> object:
    if not isinstance(params, str):
        return params
    try:
        return json.loads(params)
    except (json.JSONDecodeError, TypeError):
        return {"_encoding": "raw-string", "_raw": params}
