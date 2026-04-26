#!/usr/bin/env bash
set -euo pipefail

LEAF_ID="leaf003"
BRUTE="qubo/${LEAF_ID}/bruteforce_result.json"
NEAL="qubo/${LEAF_ID}/neal_result.json"

echo "⚙️ VERIFYING ${LEAF_ID}"

[ -f "qubo/${LEAF_ID}/run_qubo.py" ] || { echo "MISSING brute runner"; exit 1; }
[ -f "qubo/_engine/run_neal.py" ] || { echo "MISSING neal runner"; exit 1; }

python3 "qubo/${LEAF_ID}/run_qubo.py" > "$BRUTE"
python3 "qubo/_engine/run_neal.py" "$LEAF_ID" > "$NEAL"

BRUTE_ENERGY="$(python3 -c 'import json;print(json.load(open("'"$BRUTE"'"))["ground_state"]["total_energy"])')"
NEAL_ENERGY="$(python3 -c 'import json;print(json.load(open("'"$NEAL"'"))["ground_state"]["total_energy"])')"

echo "Exact energy: $BRUTE_ENERGY"
echo "Neal energy:  $NEAL_ENERGY"

if [ "$BRUTE_ENERGY" != "$NEAL_ENERGY" ]; then
  echo "FAIL: ENERGY_MISMATCH"
  exit 1
fi

if [ "$BRUTE_ENERGY" != "0" ]; then
  echo "FAIL: NONZERO_GROUND_STATE"
  exit 1
fi

echo
echo "PASS: EXACT_SOLVER_MATCHED_NEAL"
echo
cat <<'CLAIM'
Leaf003 crossed the line ⚙️

Exact solver found the truth ground state.
Simulated annealing reproduced it.

Text matched.
Math balanced.
Solvency constraint held.

This is no longer string checking.

It’s institutional verification as an energy landscape.
CLAIM
