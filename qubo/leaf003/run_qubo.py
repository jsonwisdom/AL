#!/usr/bin/env python3
import json
from itertools import product
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
LEAF_ID = "leaf003"
CLAIMS = ROOT / "data" / LEAF_ID / "claims.json"
OUT = ROOT / "qubo" / LEAF_ID / "result.json"

DRIFT_WEIGHT=10
ATOMICITY_WEIGHT=25
CONSISTENCY_WEIGHT=5

def drift(c,t):
    if c == t: return 0
    s = 1
    if c.replace(" ","") == t.replace(" ",""): s += 4
    if "approximately" in t.lower(): s += 3
    return s

def solve_field(f):
    best = None
    tests = f["tests"]
    c = f["canonical_claim"]
    for bits in product([0,1], repeat=len(tests)):
        e=0; acc=[]; rej=[]; vals={}
        for bit,test in zip(bits,tests):
            d = drift(c,test["claim_text"])
            if bit and d>0: e += DRIFT_WEIGHT*d
            if not bit and d==0: e += ATOMICITY_WEIGHT
            if bit and "approximately" in test["claim_text"].lower(): e += ATOMICITY_WEIGHT
            if bit:
                acc.append(test["id"]); vals[f["id"]] = test.get("value")
            else:
                rej.append(test["id"])
        if len(acc) > 1: e += CONSISTENCY_WEIGHT*(len(acc)-1)**2
        row={"energy":e,"bits":list(bits),"accepted":acc,"rejected":rej,"value":vals.get(f["id"])}
        if best is None or e < best["energy"]: best=row
    return best

def main():
    data=json.loads(CLAIMS.read_text())
    fields={}
    total=0
    values={}
    for f in data["fields"]:
        r=solve_field(f)
        fields[f["id"]]=r
        values[f["id"]]=r["value"]
        total += r["energy"]

    constraints={}
    for con in data.get("computed_constraints",[]):
        ok=False
        if con["id"]=="balance_identity":
            ok = values.get("balance") == values.get("revenue") - values.get("expenses")
        elif con["id"]=="solvency_constraint":
            ok = values.get("expenses") <= values.get("revenue")
        constraints[con["id"]] = ok
        if not ok: total += con.get("weight",100)

    result={
      "leaf_id": data.get("leaf_id",LEAF_ID),
      "model":"truth_energy_qubo_numeric_v1",
      "ground_state":{"total_energy":total,"fields":fields,"values":values,"constraints":constraints}
    }
    OUT.write_text(json.dumps(result,indent=2)+"\n")
    print(json.dumps(result,indent=2))

if __name__=="__main__":
    main()
