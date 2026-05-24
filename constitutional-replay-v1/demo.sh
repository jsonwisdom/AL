#!/bin/bash

set -e

echo "constitutional-replay-v1 — local-first replay demo"
echo ""
echo "Kernel rule:"
echo "If it cannot replay locally, it does not count."
echo ""

echo "Checking governance surfaces..."

required_files=(
  "BUILD_MATRIX.md"
  "README.md"
  "DESIGN.md"
  "CONTRIBUTING.md"
  "docs/LOCAL_REPLAY_PROTOCOL.md"
  "docs/BASE_NAVIGATION.md"
  "docs/MERKLE_VERIFICATION_EXAMPLES.md"
  "src/canonicalize.ts"
  "src/hash.ts"
  "src/policy.ts"
  "src/interpreter.ts"
  "src/receipt.ts"
  "src/replay.ts"
  "src/batch.ts"
  "examples/treasury-agent/policies/treasury-basic-v1.json"
  "examples/treasury-agent/emit-demo.js"
)

for file in "${required_files[@]}"; do
  if [ ! -f "$file" ]; then
    echo "MISSING_REQUIRED_FILE: $file"
    exit 1
  fi
done

echo "Governance surfaces present."
echo ""
echo "v0.1 runtime status:"
echo "- deterministic canonicalization: PRESENT"
echo "- deterministic hashing: PRESENT"
echo "- frozen policy.v1 schema: PRESENT"
echo "- deterministic interpreter: PRESENT"
echo "- receipt binding: PRESENT"
echo "- local replay engine: PRESENT"
echo "- deterministic Merkle batching: PRESENT"
echo ""
echo "No Base witness claim emitted."
echo "No production readiness claim emitted."
echo ""
echo "Executing strict build/runtime alignment gates..."
echo ""

echo "[1/3] Typecheck"
npm run typecheck

echo "[2/3] Emit build artifacts"
npm run build:emit

echo "[3/3] Execute emitted replay demo"
npm run emit:demo

echo ""
echo "SUCCESS_CONFIRMED and REFUSAL_CONFIRMED paths executed."
echo "WITNESS_STATUS=NOT_CHECKED"
echo ""
echo "Constitutional loop complete."
echo "Replay remains semantic authority."
echo "Base remains witness-only."