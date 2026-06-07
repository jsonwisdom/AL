#!/usr/bin/env python3
import json
from pathlib import Path

EXPECTED = {
    "HANDSHAKE/004-moment-to-story-example.json": "admissible",
    "HANDSHAKE/005-expression-only-example.json": "expression_only",
    "HANDSHAKE/006-narrative-missing-receipt.json": "invalid",
}

root = Path(__file__).resolve().parents[1]
failed = False

for rel, verdict in EXPECTED.items():
    path = root / rel
    data = json.loads(path.read_text())