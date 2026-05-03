#!/usr/bin/env bash
set -euo pipefail

EXPECTED_COMMIT="18af5459899b12ed609b9098aed1b6ec43ebfc13"
EXPECTED_ROOT="sha256:272bd90e5b2682c75ab07a49c4491929f39280a2d391ab6742a421e844852105"
EXPECTED_MN="PASS"
EXPECTED_AL="INDETERMINATE"
EXPECTED_TX="INDETERMINATE"
EXPECTED_NATIONAL="INDETERMINATE"
OUTPUT_PATH="alms/national/national_root_ci_latest.json"

fail() {
  echo "MACHINE_LIVE_2_REPLAY_FAIL"
  echo "reason=$1"
  exit 1
}

need_cmd() {
  command -v "$1" >/dev/null 2>&1 || fail "missing command: $1"
}

need_cmd git
need_cmd python3

if [ ! -f "scripts/compute_national_root_ci.py" ]; then
  fail "run from repo root: jsonwisdom/AL"
fi

CURRENT_COMMIT="$(git rev-parse HEAD 2>/dev/null || true)"
if [ "$CURRENT_COMMIT" != "$EXPECTED_COMMIT" ]; then
  echo "MACHINE_LIVE_2_REPLAY_WARN"
  echo "expected_commit=$EXPECTED_COMMIT"
  echo "current_commit=${CURRENT_COMMIT:-UNKNOWN}"
  echo "note=For baseline replay, run: git checkout $EXPECTED_COMMIT"
fi

python3 scripts/compute_national_root_ci.py >/tmp/machine_live_2_replay.json

[ -f "$OUTPUT_PATH" ] || fail "missing output: $OUTPUT_PATH"

read_json() {
  python3 - "$1" "$2" <<'PY'
import json
import sys
path, expr = sys.argv[1], sys.argv[2]
with open(path, "r", encoding="utf-8") as f:
    data = json.load(f)
cur = data
for part in expr.split('.'):
    if part == "":
        continue
    if part.isdigit():
        cur = cur[int(part)]
    else:
        cur = cur[part]
print(cur)
PY
}

ROOT="$(read_json "$OUTPUT_PATH" "national_root")"
NATIONAL="$(read_json "$OUTPUT_PATH" "status")"
MN="$(read_json "$OUTPUT_PATH" "states.0.status")"
AL="$(read_json "$OUTPUT_PATH" "states.1.status")"
TX="$(read_json "$OUTPUT_PATH" "states.2.status")"

[ "$ROOT" = "$EXPECTED_ROOT" ] || fail "root mismatch: expected=$EXPECTED_ROOT actual=$ROOT"
[ "$NATIONAL" = "$EXPECTED_NATIONAL" ] || fail "national verdict mismatch: expected=$EXPECTED_NATIONAL actual=$NATIONAL"
[ "$MN" = "$EXPECTED_MN" ] || fail "MN verdict mismatch: expected=$EXPECTED_MN actual=$MN"
[ "$AL" = "$EXPECTED_AL" ] || fail "AL verdict mismatch: expected=$EXPECTED_AL actual=$AL"
[ "$TX" = "$EXPECTED_TX" ] || fail "TX verdict mismatch: expected=$EXPECTED_TX actual=$TX"

echo "MACHINE_LIVE_2_REPLAY_OK"
echo "root_match=true"
echo "national_root=$ROOT"
echo "mn=$MN"
echo "al=$AL"
echo "tx=$TX"
echo "national=$NATIONAL"
echo "boundary=GitHub Direct replay proof only; no Base/EAS, ENS, or on-chain claim"
