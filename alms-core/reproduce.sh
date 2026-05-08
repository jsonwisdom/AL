#!/usr/bin/env bash
set -euo pipefail

# ALMS Core v0.1.1 fork-resolution reproducer.
# May be run from repo root (AL/) or from AL/alms-core/.

SCRIPT_DIR="$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)"
cd "$SCRIPT_DIR"

export PYTHONDONTWRITEBYTECODE=1
export PYTHONHASHSEED=0
export TZ=UTC
export LC_ALL=C.UTF-8
export LANG=C.UTF-8
export PYTHONUTF8=1

python3 --version
python3 -m pip install --require-hashes -r requirements.txt
python3 -m pytest -q -W error

sha256sum examples/claim.pass.json examples/bundle.pass.json examples/runtime.pass.json

python3 - <<'PY'
import json, pathlib, sys
sys.path.insert(0, str(pathlib.Path('.').resolve()))
from src.hash import hash_object_null_field
expected = {
  'examples/claim.pass.json': ('claim_hash','sha256:e40ec1f8fbe50938b739a4c8e3ac74ed264e719a5d87b9be7e54d6364db18832'),
  'examples/bundle.pass.json': ('bundle_hash','sha256:2347b91688f2f2e52dfd85080737eea25707273032c283b27d536f46726c3480'),
  'examples/runtime.pass.json': ('runtime_hash','sha256:7ab21151c6096225b549a88381e2a5f0257046359fd50c4cc268183137e5b23e'),
}
for p,(field,want) in expected.items():
    obj=json.loads(pathlib.Path(p).read_text())
    got=hash_object_null_field(obj, field)
    print(f'{p} {field} {got}')
    assert got == want, (p, got, want)
PY
