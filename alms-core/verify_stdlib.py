#!/usr/bin/env python3
"""ALMS Core v0.1.1 stdlib-only verifier.

No pytest. No network. No dependency installation.
Runs the constitutional checks required for fork-resolution candidate v0.1.1.
"""
import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))

from src.validate import validate_claim, validate_bundle, validate_runtime
from src.judge_runtime import judge
from src.quorum import quorum
from src.hash import hash_object_null_field


def load(name: str):
    return json.loads((ROOT / "examples" / name).read_text(encoding="utf-8"))


def assert_equal(got, want, label: str) -> None:
    if got != want:
        raise AssertionError(f"{label}: got={got!r} want={want!r}")


def main() -> int:
    claim = load("claim.pass.json")
    bundle = load("bundle.pass.json")
    runtime = load("runtime.pass.json")

    expected_embedded = {
        "claim_hash": "sha256:e40ec1f8fbe50938b739a4c8e3ac74ed264e719a5d87b9be7e54d6364db18832",
        "bundle_hash": "sha256:2347b91688f2f2e52dfd85080737eea25707273032c283b27d536f46726c3480",
        "runtime_hash": "sha256:7ab21151c6096225b549a88381e2a5f0257046359fd50c4cc268183137e5b23e",
    }

    assert_equal(claim["claim_hash"], expected_embedded["claim_hash"], "claim embedded hash")
    assert_equal(bundle["bundle_hash"], expected_embedded["bundle_hash"], "bundle embedded hash")
    assert_equal(runtime["runtime_hash"], expected_embedded["runtime_hash"], "runtime embedded hash")

    validate_claim(claim)
    validate_bundle(bundle)
    validate_runtime(runtime)

    recomputed = {
        "claim_hash": hash_object_null_field(claim, "claim_hash"),
        "bundle_hash": hash_object_null_field(bundle, "bundle_hash"),
        "runtime_hash": hash_object_null_field(runtime, "runtime_hash"),
    }
    for key, want in expected_embedded.items():
        assert_equal(recomputed[key], want, f"{key} recompute")

    verdict = judge(claim, bundle, runtime)
    assert_equal(verdict["verdict"], "PASS", "judge verdict")
    assert_equal(verdict["state_path"][0], "INIT", "state path starts")
    assert_equal(verdict["state_path"][-1], "HALT", "state path ends")

    forged = dict(claim)
    forged["claimant_id"] = "evil"
    try:
        validate_claim(forged)
    except ValueError as exc:
        if "FAIL_CLAIM_HASH_MISMATCH" not in str(exc):
            raise
    else:
        raise AssertionError("hash forgery accepted")

    v1 = judge(claim, bundle, runtime, "o1")
    v2 = judge(claim, bundle, runtime, "o2")
    assert_equal(quorum([v1, v2], 2)["final_verdict"], "PASS", "quorum exact match")
    v2["failure_code"] = "DIFFERENT_WHITESPACE_OR_FIELD"
    assert_equal(
        quorum([v1, v2], 2)["final_failure_code"],
        "FAIL_CONVERGENCE_FAILED",
        "quorum divergence",
    )

    print("ALMS_CORE_V0_1_1_STDLIB_VERIFY_PASS")
    for path in ["examples/claim.pass.json", "examples/bundle.pass.json", "examples/runtime.pass.json"]:
        print(path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
