#!/usr/bin/env python3
import json
import sys
from pathlib import Path

try:
    import neal
except Exception:
    neal = None

ROOT = Path(__file__).resolve().parents[2]
leaf = sys.argv[1] if len(sys.argv) > 1 else "la_001"
claims_path = ROOT / "data" / leaf / "claims.json"

claims = json.loads(claims_path.read_text())

Q = {}
vars_by_field = {}

def add(i, j, bias):
    key = tuple(sorted((i, j)))
    Q[key] = Q.get(key, 0.0) + float(bias)

for field in claims["fields"]:
    fid = field["id"]
    vars_by_field[fid] = []

    for test in field["tests"]:
        vid = f'{fid}::{test["id"]}'
        vars_by_field[fid].append(vid)

        drift = 0 if test["claim_text"] == field["canonical_claim"] else 1
        add(vid, vid, drift)

    vids = vars_by_field[fid]

    # exactly-one constraint: penalty * (sum(x)-1)^2
    penalty = 5.0
    for v in vids:
        add(v, v, -penalty)

    for i in range(len(vids)):
        for j in range(i + 1, len(vids)):
            add(vids[i], vids[j], 2 * penalty)

if neal:
    sampler = neal.SimulatedAnnealingSampler()
    result = sampler.sample_qubo(Q, num_reads=100)
    sample = result.first.sample
    energy = result.first.energy
else:
    # deterministic fallback
    sample = {}
    for fid, vids in vars_by_field.items():
        best = min(vids, key=lambda v: Q.get((v, v), 0))
        for v in vids:
            sample[v] = 1 if v == best else 0
    energy = sum(Q.get((v, v), 0) * x for v, x in sample.items())

accepted = {}
rejected = {}

for field in claims["fields"]:
    fid = field["id"]
    accepted[fid] = []
    rejected[fid] = []

    for test in field["tests"]:
        vid = f'{fid}::{test["id"]}'
        if sample.get(vid, 0) == 1:
            accepted[fid].append(test["id"])
        else:
            rejected[fid].append(test["id"])

out = {
    "leaf_id": claims["leaf_id"],
    "model": claims["model"],
    "ground_state": {
        "total_energy": energy,
        "fields": {
            fid: {
                "accepted": accepted[fid],
                "rejected": rejected[fid]
            }
            for fid in accepted
        }
    }
}

print(json.dumps(out, indent=2, sort_keys=True))
