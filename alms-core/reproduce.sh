#!/usr/bin/env bash
set -euo pipefail

# ALMS Core v0.1.1 fork-resolution reproducer.
# stdlib-only execution path.

SCRIPT_DIR="$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)"
cd "$SCRIPT_DIR"

export PYTHONDONTWRITEBYTECODE=1
export PYTHONHASHSEED=0
export TZ=UTC
export LC_ALL=C.UTF-8
export LANG=C.UTF-8
export PYTHONUTF8=1

python3 --version
python3 verify_stdlib.py
sha256sum examples/claim.pass.json examples/bundle.pass.json examples/runtime.pass.json
