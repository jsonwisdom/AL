#!/usr/bin/env bash
set -u

# Jay Runtime Parity Capture
# Safe to run from repo root, audit-zero-state, or parent folder containing AL.
# This script never exits your interactive shell; it only exits this script process.

if [ -d "audit-zero-state" ]; then
  cd audit-zero-state || { echo "FAIL: cannot enter audit-zero-state"; exit 1; }
elif [ -d "AL/audit-zero-state" ]; then
  cd AL/audit-zero-state || { echo "FAIL: cannot enter AL/audit-zero-state"; exit 1; }
elif [ "$(basename "$PWD")" = "audit-zero-state" ]; then
  :
else
  echo "FAIL: audit-zero-state directory not found"
  echo "Run this from AL, from audit-zero-state, or from the folder containing AL."
  exit 1
fi

mkdir -p receipts

if ! command -v npm >/dev/null 2>&1; then
  echo "FAIL: npm not found"
  exit 1
fi

if ! command -v node >/dev/null 2>&1; then
  echo "FAIL: node not found"
  exit 1
fi

if ! command -v bun >/dev/null 2>&1; then
  echo "FAIL: bun not found"
  exit 1
fi

if ! command -v deno >/dev/null 2>&1; then
  echo "FAIL: deno not found"
  exit 1
fi

npm install || { echo "FAIL: npm install failed"; exit 1; }

{
  echo "node=$(node --version)"
  echo "bun=$(bun --version)"
  echo "deno=$(deno --version | head -n 1)"
} > receipts/runtime-versions.txt

npm run audit:node > receipts/node-receipt.json || { echo "FAIL: Node audit failed"; exit 1; }
bun src/audit.ts > receipts/bun-receipt.json || { echo "FAIL: Bun audit failed"; exit 1; }
deno run src/audit.ts > receipts/deno-receipt.json || { echo "FAIL: Deno audit failed"; exit 1; }

if command -v sha256sum >/dev/null 2>&1; then
  HASH_CMD="sha256sum"
elif command -v shasum >/dev/null 2>&1; then
  HASH_CMD="shasum -a 256"
else
  echo "FAIL: no sha256sum or shasum found"
  exit 1
fi

$HASH_CMD receipts/node-receipt.json receipts/bun-receipt.json receipts/deno-receipt.json > receipts/receipt-file-hashes.txt

echo "=== runtime versions ==="
cat receipts/runtime-versions.txt

echo "=== receipt file hashes ==="
cat receipts/receipt-file-hashes.txt

echo "=== receipt files written ==="
echo "receipts/node-receipt.json"
echo "receipts/bun-receipt.json"
echo "receipts/deno-receipt.json"

echo "PASS: Jay runtime parity capture completed"
