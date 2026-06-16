#!/usr/bin/env python3
import json
import sys
from pathlib import Path

BASE = Path(__file__).resolve().parent

with open(BASE / "generator_config.json") as f:
    cfg = json.load(f)

try:
    for i in range(1, cfg["card_count"] + 1):
        card = {
            "card_id": f"GPK-{i:03d}",
            "factory": cfg["factory"],
            "seed": cfg["seed"]
        }
        print(json.dumps(card))
except BrokenPipeError:
    sys.exit(0)
