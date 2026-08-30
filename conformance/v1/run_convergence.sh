#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
OUT_DIR="$ROOT_DIR/conformance/v1/out"
TS_RUNNER="$ROOT_DIR/conformance/v1/runners/ts_reference_runner.ts"
PY_RUNNER="$ROOT_DIR/conformance/v1/runners/py_observer_b.py"

mkdir -p "$OUT_DIR"

TS_OUT="$OUT_DIR/observer_a_ts.json"
PY_OUT="$OUT_DIR/observer_b_python.json"
CONVERGENCE_OUT="$OUT_DIR/convergence_report.json"

STATE="NOT_RUN"

if command -v deno >/dev/null 2>&1; then
  deno run --allow-read "$TS_RUNNER" > "$TS_OUT"
elif command -v bun >/dev/null 2>&1; then
  bun "$TS_RUNNER" > "$TS_OUT"
else
  echo '{"observer":"ts_reference","verdict":"SKIPPED","reason":"deno_or_bun_required_for_json_imports"}' > "$TS_OUT"
fi

python3 "$PY_RUNNER" > "$PY_OUT"

python3 - "$TS_OUT" "$PY_OUT" "$CONVERGENCE_OUT" <<'PY'
import json
import sys
from pathlib import Path


def load(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


ts_path, py_path, out_path = map(Path, sys.argv[1:4])
ts = load(ts_path)
py = load(py_path)

report = {
    "receipt_type": "FIRST_CROSS_OBSERVER_CONVERGENCE_RECEIPT",
    "status": "NOT_CONVERGED",
    "observers": {
        "observer_a": "minimal-verifiable-kernel-ts-v1",
        "observer_b": "observer-b-python-v1"
    },
    "inputs": {
        "observer_a_output": str(ts_path),
        "observer_b_output": str(py_path)
    },
    "vectors": [],
    "mismatches": []
}

if isinstance(ts, dict) and ts.get("verdict") == "SKIPPED":
    report["mismatches"].append(ts)
else:
    ts_by_id = {v.get("vector_id"): v for v in ts}
    py_by_id = {v.get("vector_id"): v for v in py}

    all_ids = sorted(set(ts_by_id) | set(py_by_id))
    for vector_id in all_ids:
        a = ts_by_id.get(vector_id)
        b = py_by_id.get(vector_id)
        item = {"vector_id": vector_id, "status": "UNKNOWN"}

        if a is None or b is None:
            item["status"] = "MISSING_OBSERVER_OUTPUT"
            report["mismatches"].append(item)
            report["vectors"].append(item)
            continue

        a_comp = a.get("computed", {}) or {}
        b_comp = b.get("computed", {}) or {}
        keys = ["final_root", "event_count", "degraded", "degradation_notes"]
        mismatch = []
        for key in keys:
            if a_comp.get(key) != b_comp.get(key):
                mismatch.append({"field": key, "observer_a": a_comp.get(key), "observer_b": b_comp.get(key)})

        if a.get("verdict") != b.get("verdict"):
            mismatch.append({"field": "verdict", "observer_a": a.get("verdict"), "observer_b": b.get("verdict")})

        item["observer_a_verdict"] = a.get("verdict")
        item["observer_b_verdict"] = b.get("verdict")
        item["status"] = "CONVERGED" if not mismatch else "DIVERGED"
        item["mismatch"] = mismatch
        report["vectors"].append(item)
        if mismatch:
            report["mismatches"].append(item)

    if not report["mismatches"]:
        report["status"] = "CONVERGED"

with open(out_path, "w", encoding="utf-8") as f:
    json.dump(report, f, indent=2, sort_keys=True)
    f.write("\n")

print(json.dumps(report, indent=2, sort_keys=True))
sys.exit(0 if report["status"] == "CONVERGED" else 1)
PY
