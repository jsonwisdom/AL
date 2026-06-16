#!/usr/bin/env python3
import json

with open("generator_config.json") as f:
    cfg = json.load(f)

for i in range(1, cfg["card_count"] + 1):
    card = {
        "card_id": f"GPK-{i:03d}",
        "factory": cfg["factory"],
        "seed": cfg["seed"]
    }
    print(json.dumps(card))
