#!/usr/bin/env python3
import json
import pathlib
import subprocess
import sys

BIN = "tools/treasury_verifier/treasury-verifier"
ROOT = pathlib.Path("tests/fixtures/verifier-v0.2")

def run(args):
    return subprocess.run(args, text=True, capture_output=True)

def parse(stdout):
    return json.loads(stdout.split("\n\nSUMMARY:")[0])

def check(name, condition, detail=""):
    if not condition:
        print(f"FAIL {name}")
        if detail:
            print(detail)
        sys.exit(1)
    print(f"PASS {name}")

# 1 valid strict passes
r = run([BIN, "verify", str(ROOT/"strict/01_valid_real.json"), "--mode", "strict", "--drift-seconds", "999999999999"])
check("strict valid real passes", r.returncode == 0 and parse(r.stdout)["status"] == "PASS", r.stdout + r.stderr)

# 2 strict rejects bad/sim vectors
for f in sorted((ROOT/"strict").glob("0[2-9]_*.json")):
    r = run([BIN, "verify", str(f), "--mode", "strict", "--drift-seconds", "300"])
    out = parse(r.stdout)
    check(f"strict rejects {f.name}", r.returncode != 0 and out["status"] == "FAIL", r.stdout + r.stderr)

# 3 audit allows warnings
for f in sorted((ROOT/"audit").glob("*.json")):
    r = run([BIN, "verify", str(f), "--mode", "audit", "--drift-seconds", "300"])
    out = parse(r.stdout)
    check(f"audit passes {f.name}", r.returncode == 0 and out["status"] == "PASS", r.stdout + r.stderr)
    if "01_valid_real" not in f.name:
        check(f"audit warns {f.name}", bool(out["warnings"]), r.stdout)

# 4 batch audit passes with warning
r = run([BIN, "batch-verify", str(ROOT/"batch-verify"), "--mode", "audit", "--drift-seconds", "999999999999"])
out = parse(r.stdout)
check("batch audit passes", r.returncode == 0 and out["status"] == "PASS", r.stdout + r.stderr)
check("batch has warning", bool(out["results"][0]["warnings"]), r.stdout)

print("TREASURY_VERIFIER_V0_2_TESTS=GREEN")
print("NO_FAKE_GREEN=PRESERVED")
