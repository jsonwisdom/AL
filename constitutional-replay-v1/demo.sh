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
echo "- replay engine not implemented yet"
echo "- canonicalization kernel not implemented yet"
echo "- policy.v1 interpreter not implemented yet"
echo "- golden vectors not implemented yet"
echo ""
echo "Current repo phase:"
echo "docs-first constitutional shell complete"
echo ""
echo "Next implementation order:"
echo "1. src/canonicalize.ts"
echo "2. src/hash.ts"
echo "3. policy.v1 schema + vectors"
echo "4. interpreter.ts"
echo "5. replay.ts"
echo "6. batch.ts"
echo ""
echo "No replay claim emitted."
echo "No witness claim emitted."
echo ""
echo "Demo intentionally exits non-success until replay primitives exist."

exit 2
