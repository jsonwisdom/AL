import hashlib
import json
import pathlib
import subprocess
from datetime import datetime, timezone

ROOT = pathlib.Path(__file__).resolve().parent
MODULE_JSON = ROOT.parent / 'MODULE.json'


def sha256_file(path: pathlib.Path) -> str:
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        while True:
            chunk = f.read(8192)
            if not chunk:
                break
            h.update(chunk)
    return 'sha256:' + h.hexdigest()


def run(cmd):
    return subprocess.check_output(cmd, cwd=ROOT).decode().strip()


# Compile circuit
run(['nargo', 'compile'])

# Expected Noir artifacts
program_json = ROOT / 'target' / 'zk_receipt_verifier.json'
verification_key = ROOT / 'target' / 'verification_key'
proving_key = ROOT / 'target' / 'proving_key'

manifest = json.loads(MODULE_JSON.read_text())

manifest['verified_at'] = datetime.now(timezone.utc).isoformat()
manifest['circuit_hash'] = sha256_file(program_json) if program_json.exists() else 'sha256:missing'
manifest['verification_key_hash'] = sha256_file(verification_key) if verification_key.exists() else 'sha256:missing'
manifest['proving_key_hash'] = sha256_file(proving_key) if proving_key.exists() else 'sha256:missing'
manifest['noir_version'] = run(['nargo', '--version'])

build_receipt = hashlib.sha256(json.dumps(manifest, sort_keys=True).encode()).hexdigest()
manifest['build_receipt_hash'] = 'sha256:' + build_receipt

MODULE_JSON.write_text(json.dumps(manifest, indent=2) + '\n')

print(json.dumps({
    'status': 'COMPILED',
    'circuit_hash': manifest['circuit_hash'],
    'verification_key_hash': manifest['verification_key_hash'],
    'proving_key_hash': manifest['proving_key_hash'],
    'build_receipt_hash': manifest['build_receipt_hash']
}, indent=2))
