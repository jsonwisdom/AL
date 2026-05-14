#!/usr/bin/env bash
set -euo pipefail

npm install
npm run build
npm run replay:valid

set +e
npm run replay:divergent
code=$?
set -e

if [ "$code" -ne 2 ]; then
  echo "Expected divergent receipt to exit 2, got $code"
  exit 1
fi

echo "REPRODUCE_OK"
