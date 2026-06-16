import glob
import json
from replayloop.did import decode_did_key, DidKeyError

VALID_FIXTURE = "testdata/v1/did-key-valid.json"
INVALID_GLOB = "testdata/v1/invalid/did-key/*.json"

with open(VALID_FIXTURE, "r") as f:
    valid = json.load(f)

expected_raw = valid["raw_public_key_hex"]
did = valid["did"]
actual_raw = decode_did_key(did).hex()

if actual_raw != expected_raw:
    raise SystemExit(
        f"VALID FIXTURE FAILED: got {actual_raw}, expected {expected_raw}"
    )

for path in sorted(glob.glob(INVALID_GLOB)):
    with open(path, "r") as f:
        fixture = json.load(f)

    did = fixture["did"]
    expected = fixture["expected_error"]

    try:
        decode_did_key(did)
        raise SystemExit(f"INVALID FIXTURE DID NOT FAIL: {path}")
    except DidKeyError as exc:
        if str(exc) != expected:
            raise SystemExit(
                f"INVALID FIXTURE WRONG ERROR in {path}:\n"
                f"  got:      {str(exc)}\n"
                f"  expected: {expected}"
            )

print("Python decoder: OK")
