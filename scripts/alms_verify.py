#!/usr/bin/env python3
"""
ALMS Replay Engine Skeleton v1

Subordinate to ALMS Constitutional Kernel v0.1.

Kernel rules enforced by design:
- No replay, no proof.
- No canonical bytes, no replay.
- No declared transform policy, no admissibility.
- No trace, no opinion.
- No network calls during replay.
- Identity resolves discovery.
- Replay resolves truth.

This skeleton intentionally supports only local JSON fixture/replay packets.
It does not fetch remote sources and does not infer transform policy.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional

PASS = "PASS"
FAIL = "FAIL"
INDETERMINATE = "INDETERMINATE"
TAINTED = "TAINTED"
REVIEW_REQUIRED = "REVIEW_REQUIRED"
HIGH_RISK_VARIANT = "HIGH_RISK_VARIANT"

NONE = "NONE"
V1_BYTE_VARIANT = "V1_BYTE_VARIANT"
V2_TRANSFORM_VARIANT = "V2_TRANSFORM_VARIANT"
V3_PROVENANCE_VARIANT = "V3_PROVENANCE_VARIANT"
V4_IDENTITY_VARIANT = "V4_IDENTITY_VARIANT"
V5_SEMANTIC_VARIANT = "V5_SEMANTIC_VARIANT"
TRACE_CLOSED = "TRACE_CLOSED"

EXIT_CODES = {
    PASS: 0,
    FAIL: 1,
    INDETERMINATE: 2,
    TAINTED: 3,
    REVIEW_REQUIRED: 4,
    HIGH_RISK_VARIANT: 5,
    "INVALID_INPUT": 64,
    "INTERNAL_ERROR": 70,
}


@dataclass
class TraceStep:
    step: int
    name: str
    status: str
    input_ref: Optional[str] = None
    output_ref: Optional[str] = None
    message: Optional[str] = None
    verdict: Optional[str] = None
    trace_hash: Optional[str] = None
    closed_at: Optional[str] = None


@dataclass
class VerificationState:
    input_path: Path
    packet: Dict[str, Any]
    run_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    verdict: str = INDETERMINATE
    cvd_class: str = NONE
    errors: List[str] = field(default_factory=list)
    trace: List[TraceStep] = field(default_factory=list)
    expected_digest: Optional[str] = None
    computed_digest: Optional[str] = None
    fixture_id: Optional[str] = None
    artifact_id: Optional[str] = None
    source_uri: Optional[str] = None
    source_type: Optional[str] = None
    trace_closed: bool = False

    def add_trace(self, name: str, status: str, message: Optional[str] = None) -> None:
        if self.trace_closed:
            raise RuntimeError("trace is sealed; no further events may be appended")
        self.trace.append(
            TraceStep(
                step=len(self.trace) + 1,
                name=name,
                status=status,
                input_ref=str(self.input_path),
                output_ref=None,
                message=message,
            )
        )


def canonical_json_bytes(obj: Any) -> bytes:
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")


def sha256_hex(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def trace_hash(trace: List[TraceStep]) -> str:
    trace_body = [step.__dict__ for step in trace]
    return "sha256:" + sha256_hex(canonical_json_bytes(trace_body))


def load_packet(path: Path) -> Dict[str, Any]:
    if not path.exists() or not path.is_file():
        raise ValueError(f"input file not found: {path}")
    if path.suffix.lower() != ".json":
        raise ValueError("skeleton verifier accepts only local JSON packets")
    return json.loads(path.read_text(encoding="utf-8"))


def validate_schema(state: VerificationState) -> None:
    packet = state.packet
    fixture_spec = packet.get("fixture_spec")
    replay_spec = packet.get("replay", {}).get("replay_spec") or packet.get("spec")

    if fixture_spec != "FIXTURE_SPEC_V1" and replay_spec != "REPLAY_SPEC_V1":
        state.verdict = INDETERMINATE
        state.errors.append("missing FIXTURE_SPEC_V1 or REPLAY_SPEC_V1 declaration")
        state.add_trace("schema_validation", "FAIL", state.errors[-1])
        return

    state.fixture_id = packet.get("fixture_id")
    state.artifact_id = packet.get("artifact_id")
    state.add_trace("schema_validation", "PASS", "declared ALMS v0.1-compatible packet")


def validate_provenance(state: VerificationState) -> None:
    source = state.packet.get("source", {})
    state.source_uri = source.get("uri") or state.packet.get("source_uri")
    state.source_type = source.get("source_type") or state.packet.get("source_type")

    if not state.source_uri:
        state.verdict = INDETERMINATE
        state.errors.append("missing source URI/provenance declaration")
        state.add_trace("provenance_validation", "FAIL", state.errors[-1])
        return

    if str(state.source_uri).startswith(("http://", "https://", "ipfs://")):
        state.add_trace("provenance_validation", "PASS", "remote source declared but not fetched during replay")
        return

    state.add_trace("provenance_validation", "PASS", "local/source provenance declared")


def validate_transform_policy(state: VerificationState) -> None:
    transform = state.packet.get("transform", {})
    policy_id = transform.get("policy_id") or state.packet.get("transform_policy_id")
    policy_hash = transform.get("policy_hash") or state.packet.get("transform_policy_hash")
    canonical_method = transform.get("canonicalization_method") or state.packet.get("canonicalization_method")

    if not policy_id or not canonical_method:
        state.verdict = INDETERMINATE
        state.cvd_class = V2_TRANSFORM_VARIANT
        state.errors.append("missing declared transform policy or canonicalization method")
        state.add_trace("transform_policy_validation", "FAIL", state.errors[-1])
        return

    if policy_hash and not str(policy_hash).startswith("sha256:"):
        state.verdict = TAINTED
        state.cvd_class = V2_TRANSFORM_VARIANT
        state.errors.append("transform policy hash must use sha256:<hex>")
        state.add_trace("transform_policy_validation", "FAIL", state.errors[-1])
        return

    state.add_trace("transform_policy_validation", "PASS", f"policy={policy_id}")


def recompute_digest_placeholder(state: VerificationState) -> None:
    canonical = state.packet.get("canonical", {})
    digest = canonical.get("digest") or state.packet.get("expected_digest")
    digest_method = canonical.get("digest_method") or state.packet.get("digest_method") or "sha256"

    if not digest:
        state.verdict = INDETERMINATE
        state.errors.append("missing expected canonical digest")
        state.add_trace("digest_recompute", "FAIL", state.errors[-1])
        return

    if digest_method != "sha256":
        state.verdict = INDETERMINATE
        state.errors.append("skeleton verifier currently supports sha256 only")
        state.add_trace("digest_recompute", "FAIL", state.errors[-1])
        return

    state.expected_digest = digest
    inline_json = canonical.get("inline_json")
    if inline_json is None:
        state.verdict = INDETERMINATE
        state.errors.append("no local canonical.inline_json provided; refusing network/source fetch")
        state.add_trace("digest_recompute", "INDETERMINATE", state.errors[-1])
        return

    computed = "sha256:" + sha256_hex(canonical_json_bytes(inline_json))
    state.computed_digest = computed

    if computed != digest:
        state.verdict = FAIL
        state.cvd_class = V1_BYTE_VARIANT
        state.errors.append("computed digest does not match expected digest")
        state.add_trace("digest_recompute", "FAIL", state.errors[-1])
        return

    state.add_trace("digest_recompute", "PASS", "computed digest matches expected digest")


def verify_receipt_placeholder(state: VerificationState) -> None:
    receipt = state.packet.get("receipt", {})
    if not receipt:
        state.verdict = INDETERMINATE
        state.errors.append("missing receipt object")
        state.add_trace("receipt_verification", "FAIL", state.errors[-1])
        return
    state.add_trace("receipt_verification", "PASS", "receipt object present; full binding check pending")


def finalize_verdict(state: VerificationState) -> None:
    if state.trace_closed:
        return

    if state.errors:
        if state.verdict == FAIL:
            status = FAIL
            message = "observable contradiction detected"
        elif state.verdict == TAINTED:
            status = TAINTED
            message = "policy divergence detected"
        else:
            state.verdict = INDETERMINATE
            status = INDETERMINATE
            message = "failed closed without observable contradiction"
    else:
        state.verdict = PASS
        state.cvd_class = NONE
        status = PASS
        message = "declared evidence recomputed under skeleton constraints"

    closure = TraceStep(
        step=len(state.trace) + 1,
        name=TRACE_CLOSED,
        status=status,
        input_ref=str(state.input_path),
        output_ref=None,
        message=message,
        verdict=state.verdict,
        trace_hash=None,
        closed_at=datetime.now(timezone.utc).isoformat(),
    )
    state.trace.append(closure)
    closure.trace_hash = trace_hash(state.trace)
    state.trace_closed = True


def assert_trace_closed(state: VerificationState) -> None:
    if not state.trace or state.trace[-1].name != TRACE_CLOSED or not state.trace_closed:
        raise RuntimeError("verdict void: TRACE_CLOSED terminal event missing")


def emit_cvd_report(state: VerificationState) -> Dict[str, Any]:
    assert_trace_closed(state)
    now = datetime.now(timezone.utc).isoformat()
    report = {
        "schema": "CVD_OUTPUT_SCHEMA_V1",
        "schema_version": "1.0.0",
        "report_id": None,
        "run": {
            "run_id": state.run_id,
            "run_at": now,
            "verifier_spec": "VERIFIER_SPEC_V1",
            "verifier_name": "alms_verify.py",
            "verifier_version": "skeleton-v1",
            "environment_ref": "python3-local-no-network",
        },
        "subject": {
            "fixture_id": state.fixture_id,
            "artifact_id": state.artifact_id,
            "jurisdiction": state.packet.get("jurisdiction"),
            "domain": state.packet.get("domain"),
            "source_uri": state.source_uri,
            "source_type": state.source_type,
        },
        "specs": {
            "replay_spec": "REPLAY_SPEC_V1",
            "fixture_spec": state.packet.get("fixture_spec"),
            "transform_policy_id": state.packet.get("transform", {}).get("policy_id"),
            "transform_policy_hash": state.packet.get("transform", {}).get("policy_hash"),
        },
        "verdict": {
            "state": state.verdict,
            "cvd_class": state.cvd_class,
            "confidence": "COMPUTED" if state.verdict == PASS else "PARTIAL",
            "summary": "skeleton verifier report",
        },
        "comparison": {
            "expected_digest": state.expected_digest,
            "computed_digest": state.computed_digest,
            "expected_manifest_root": None,
            "computed_manifest_root": None,
            "match": state.expected_digest is not None and state.expected_digest == state.computed_digest,
        },
        "evidence_graph": {"nodes": [], "edges": []},
        "replay_trace": [step.__dict__ for step in state.trace],
        "diff": {"available": False, "type": "none", "uri": None, "summary": None},
        "provenance_chain": [],
        "witnesses": [],
        "errors": state.errors,
        "human_readable": {
            "title": "ALMS Replay Engine Skeleton Report",
            "finding": state.verdict,
            "operator_note": None,
        },
        "hash": {"canonicalization": "json.dumps sort_keys compact self-hash-excluded", "digest": None},
    }

    digest_report = dict(report)
    digest_report["hash"] = dict(report["hash"])
    digest_report["hash"]["digest"] = None
    report_hash = "sha256:" + sha256_hex(canonical_json_bytes(digest_report))
    report["hash"]["digest"] = report_hash
    report["report_id"] = f"cvd:{state.run_id}:{report_hash}"
    return report


def run_verifier(path: Path) -> VerificationState:
    packet = load_packet(path)
    state = VerificationState(input_path=path, packet=packet)

    try:
        validate_schema(state)
        if not state.errors:
            validate_provenance(state)
        if not state.errors:
            validate_transform_policy(state)
        if not state.errors:
            recompute_digest_placeholder(state)
        if not state.errors:
            verify_receipt_placeholder(state)
    finally:
        finalize_verdict(state)

    return state


def main() -> int:
    parser = argparse.ArgumentParser(description="ALMS replay engine skeleton v1")
    parser.add_argument("input", help="local FIXTURE_SPEC_V1 or REPLAY_SPEC_V1 JSON packet")
    parser.add_argument("--out", help="write CVD_OUTPUT_SCHEMA_V1 report to path")
    args = parser.parse_args()

    try:
        state = run_verifier(Path(args.input))
        report = emit_cvd_report(state)
        output = json.dumps(report, sort_keys=True, indent=2, ensure_ascii=False)
        if args.out:
            Path(args.out).write_text(output + "\n", encoding="utf-8")
        else:
            print(output)
        return EXIT_CODES.get(state.verdict, EXIT_CODES["INTERNAL_ERROR"])
    except ValueError as exc:
        print(json.dumps({"error": str(exc), "verdict": "INVALID_INPUT"}, sort_keys=True), file=sys.stderr)
        return EXIT_CODES["INVALID_INPUT"]
    except Exception as exc:
        print(json.dumps({"error": str(exc), "verdict": "INTERNAL_ERROR"}, sort_keys=True), file=sys.stderr)
        return EXIT_CODES["INTERNAL_ERROR"]


if __name__ == "__main__":
    raise SystemExit(main())
