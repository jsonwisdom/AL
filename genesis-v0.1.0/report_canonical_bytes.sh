#!/usr/bin/env bash
# Genesis v0.1.0 - Canonicalization Byte Evidence Harness
# Evidence collection only. No normalization. No fixes. No authority.

set -euo pipefail
cd "$(dirname "$0")"

echo "=== GENESIS CANONICALIZATION BYTE REPORT ==="
echo "HARNESS: EVIDENCE_COLLECTION_ONLY"
echo "NO_CANON_WITHOUT_BYTE_LAW: active"
echo "ENV: $(uname -srm)"
echo "NODE_VERSION: $(node --version 2>/dev/null || echo 'not found')"
echo "PYTHON_VERSION: $(python3 --version 2>/dev/null || echo 'not found')"
echo ""

for vector in test-vectors/*.json; do
  [ -f "$vector" ] || { echo "ERROR: no test vectors found"; exit 1; }

  name="$(basename "$vector")"

  PYTHON_HEX="$(python3 - "$vector" <<'PY'
import json, sys
from pathlib import Path
import canonicalize
data = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
print(canonicalize.canonicalize(data).hex())
PY
)"

  JS_HEX="$(node - "$vector" <<'JS'
const fs = require("fs");
const vm = require("vm");
const code = fs.readFileSync("./canonicalize.js", "utf8");
const sandbox = { module: { exports: {} }, exports: {} };
vm.runInNewContext(code, sandbox);
const mod = sandbox.module.exports;
const canonicalize = mod.canonicalize || mod;
const file = process.argv[1] === "-" ? process.argv[2] : process.argv[1];
const data = JSON.parse(fs.readFileSync(file, "utf8"));
console.log(Buffer.from(canonicalize(data), "utf8").toString("hex"));
JS
)"

  MATCH=false
  [ "$PYTHON_HEX" = "$JS_HEX" ] && MATCH=true

  echo "--- Vector: $name ---"
  echo "PYTHON_HEX: $PYTHON_HEX"
  echo "JS_HEX:     $JS_HEX"
  echo "MATCH:      $MATCH"
  echo ""
done

echo "=== END REPORT ==="
