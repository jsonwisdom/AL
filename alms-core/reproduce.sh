#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/alms-core"
export PYTHONDONTWRITEBYTECODE=1
export PYTHONHASHSEED=0
export TZ=UTC
export LC_ALL=C.UTF-8
export LANG=C.UTF-8
python -m pytest -q -W error
python - <<'PY'
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
    print(f'{p} {got}')
    assert got == want, (p, got, want)
PY
