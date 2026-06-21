import json, subprocess, pathlib

BIN = "tools/treasury_verifier/treasury-verifier"
ROOT = pathlib.Path("tests/fixtures/verifier-v0.2")

def run(args):
    return subprocess.run(args, text=True, capture_output=True)

def parse(stdout):
    return json.loads(stdout.split("\n\nSUMMARY:")[0])

def test_strict_valid_real_passes():
    r = run([BIN, "verify", str(ROOT/"strict/01_valid_real.json"), "--mode", "strict", "--drift-seconds", "999999999999"])
    assert r.returncode == 0, r.stdout + r.stderr
    assert parse(r.stdout)["status"] == "PASS"

def test_strict_rejects_simulated_and_bad_vectors():
    for f in sorted((ROOT/"strict").glob("0[2-9]_*.json")):
        r = run([BIN, "verify", str(f), "--mode", "strict", "--drift-seconds", "300"])
        assert r.returncode != 0, f"{f} unexpectedly passed\n{r.stdout}"
        assert parse(r.stdout)["status"] == "FAIL"

def test_audit_warns_not_blocks_simulated_vectors():
    for f in sorted((ROOT/"audit").glob("*.json")):
        r = run([BIN, "verify", str(f), "--mode", "audit", "--drift-seconds", "300"])
        assert r.returncode == 0, f"{f} unexpectedly failed\n{r.stdout}"
        out = parse(r.stdout)
        assert out["status"] == "PASS"
        if "01_valid_real" not in f.name:
            assert out["warnings"], f"{f} expected warnings"

def test_batch_verify_audit_passes_with_warnings():
    r = run([BIN, "batch-verify", str(ROOT/"batch-verify"), "--mode", "audit", "--drift-seconds", "999999999999"])
    assert r.returncode == 0, r.stdout + r.stderr
    out = parse(r.stdout)
    assert out["status"] == "PASS"
    assert out["count"] >= 1
    assert out["results"][0]["warnings"]
