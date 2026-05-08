#!/usr/bin/env bash
set -euo pipefail

export PYTHONHASHSEED=0
export LC_ALL=C
export TZ=UTC
export PYTHONUTF8=1

python3 --version
python3 -m pytest -q
sha256sum examples/claim.pass.json examples/bundle.pass.json examples/runtime.pass.json
