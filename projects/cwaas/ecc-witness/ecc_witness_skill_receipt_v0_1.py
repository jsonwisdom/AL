"""
ECC Witness Skill Receipt v0.1

Purpose:
    Fail-closed ToolGate wrapper for ECC-style skill registries.

Doctrine:
    No receipt, no execution.
    No manifest hash, no boot.
    No post-tool receipt, no return to agent.

This module is intentionally stdlib-only for the v0.1 security boundary.
Telemetry such as token accounting belongs in a v0.2 overlay.
"""

from __future__ import annotations

import functools
import hashlib
import json
import logging
import os
import re
import sys
import tempfile
import time
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Callable, Dict, Iterable, List, Literal, Optional

logger = logging.getLogger("ECC_Witness_Gate")

RECEIPT_LOG_PATH = os.getenv(
    "ECC_WITNESS_RECEIPT_LOG",
    "logs/witness_receipt_chain.jsonl",
)

LOCAL_EXPECTED_MANIFEST_HASH_PATH = os.getenv(
    "ECC_LOCAL_EXPECTED_MANIFEST_HASH_PATH",
    "receipts/ecc/manifest/ECC_EXPECTED_MANIFEST_HASH.v0.1",
)

BootStatus = Literal[
    "DUAL_ANCHOR_VERIFIED",
    "LOCAL_ANCHOR_VERIFIED",
    "ENV_ANCHOR_VERIFIED_PROVISIONAL",
    "BOOT_WIRE_BLOCKED",
]

_BOOT_INFO: Dict[str, Any] = {
    "manifest_hash": None,
    "boot_status": "BOOT_WIRE_BLOCKED",
    "sequence_nonce": 0,
}

_WRAPPER_ATTR = "__witness_wrapped__"


@dataclass(frozen=True)
class PreflightReceiptV01:
    receipt_type: str
    schema_version: str
    skill_id: str
    sub_agent_id: str
    tool_id: Optional[str]
    manifest_hash: str
    boot_status: BootStatus
    sequence_nonce: int
    input_hash: str
    allowed_tools_hash: str
    timestamp_ns: int
    process_id: int
    disposition: str

    def canonical_json(self) -> str:
        return canonical_json(asdict(self))

    def receipt_hash(self) -> str:
        return sha256_text(self.canonical_json())


@dataclass(frozen=True)
class PostToolReceiptV01:
    receipt_type: str
    schema_version: str
    preflight_receipt_hash: str
    output_hash: str
    mutation_delta_hash: str
    status: str
    timestamp_ns: int
    disposition: str

    def canonical_json(self) -> str:
        return canonical_json(asdict(self))

    def receipt_hash(self) -> str:
        return sha256_text(self.canonical_json())


# Tier 1-5 registry. v0.1 records the first winning tier only.
EXFIL_PATTERNS_V0_1: List[Dict[str, Any]] = [
    {
        "id": "ENV_ASSIGNMENT_SECRET",
        "tier": 1,
        "severity": "CRITICAL",
        "pattern": re.compile(
            r"(?i)\b("
            r"api[_-]?key|secret|token|password|passwd|private[_-]?key|"
            r"access[_-]?key|client[_-]?secret|auth[_-]?token"
            r")\b\s*=\s*['\"]?[^'\"\s]{12,}"
        ),
    },
    {
        "id": "AWS_ACCESS_KEY_ID",
        "tier": 1,
        "severity": "CRITICAL",
        "pattern": re.compile(r"\bAKIA[0-9A-Z]{16}\b"),
    },
    {
        "id": "PRIVATE_KEY_BLOCK",
        "tier": 3,
        "severity": "CRITICAL",
        "pattern": re.compile(r"-----BEGIN (RSA |EC |OPENSSH |DSA )?PRIVATE KEY-----"),
    },
    {
        "id": "CLOUD_CONFIG_PATH",
        "tier": 2,
        "severity": "HIGH",
        "pattern": re.compile(r"(?i)(\.aws/credentials|\.aws/config|\.kube/config|gcloud/configurations)"),
    },
    {
        "id": "HOST_SSH_PATH",
        "tier": 3,
        "severity": "HIGH",
        "pattern": re.compile(r"(?i)(~?/\.ssh/(id_rsa|id_ed25519|config|known_hosts))"),
    },
    {
        "id": "WORKSPACE_CONFIG_CLAUDE",
        "tier": 4,
        "severity": "HIGH",
        "pattern": re.compile(r"(?i)(^|[\s/])CLAUDE\.md\b"),
    },
    {
        "id": "WORKSPACE_CONFIG_CURSORRULES",
        "tier": 4,
        "severity": "HIGH",
        "pattern": re.compile(r"(?i)(^|[\s/])\.cursorrules\b"),
    },
    {
        "id": "WORKSPACE_CONFIG_GITHUB_WORKFLOWS",
        "tier": 4,
        "severity": "HIGH",
        "pattern": re.compile(r"(?i)\.github/workflows/[^\s]+"),
    },
    {
        "id": "INDIRECT_PROMPT_INJECTION_TRIGGER",
        "tier": 5,
        "severity": "MEDIUM",
        "pattern": re.compile(
            r"(?i)(ignore previous instructions|developer message|system prompt|reveal hidden|exfiltrate)"
        ),
    },
]


def canonical_json(value: Any) -> str:
    return json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
        default=str,
    )


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def sha256_obj(value: Any) -> str:
    return sha256_text(canonical_json(value))


def _write_atomic_receipt(receipt_dict: Dict[str, Any]) -> None:
    """Append one JSONL receipt and fsync. Fail-closed on any I/O fault."""
    try:
        log_path = Path(RECEIPT_LOG_PATH)
        log_path.parent.mkdir(parents=True, exist_ok=True)
        line = canonical_json(receipt_dict) + "\n"

        # O_APPEND gives append atomicity at the file-descriptor level for local filesystems.
        fd = os.open(str(log_path), os.O_WRONLY | os.O_CREAT | os.O_APPEND, 0o600)
        try:
            os.write(fd, line.encode("utf-8"))
            os.fsync(fd)
        finally:
            os.close(fd)
    except Exception as exc:  # pragma: no cover - intentionally terminal
        logger.critical("FAIL_CLOSED: receipt append failed: %s", exc)
        sys.exit("FAIL_CLOSED: Evidence chain compromised.")


def _read_local_expected_manifest_hash() -> Optional[str]:
    path = Path(LOCAL_EXPECTED_MANIFEST_HASH_PATH)
    if not path.exists():
        return None
    return path.read_text(encoding="utf-8").strip()


def _resolve_boot_status(actual_manifest_hash: str) -> BootStatus:
    local_hash = _read_local_expected_manifest_hash()
    env_hash = os.getenv("ECC_EXPECTED_MANIFEST_HASH")

    if local_hash and env_hash:
        if local_hash == env_hash == actual_manifest_hash:
            return "DUAL_ANCHOR_VERIFIED"
        return "BOOT_WIRE_BLOCKED"

    if local_hash:
        return "LOCAL_ANCHOR_VERIFIED" if local_hash == actual_manifest_hash else "BOOT_WIRE_BLOCKED"

    if env_hash:
        return "ENV_ANCHOR_VERIFIED_PROVISIONAL" if env_hash == actual_manifest_hash else "BOOT_WIRE_BLOCKED"

    return "BOOT_WIRE_BLOCKED"


def _skill_identity_payload(skill_id: str, handler: Callable[..., Any], allowed_tools: Iterable[str]) -> Dict[str, Any]:
    return {
        "skill_id": skill_id,
        "handler_module": getattr(handler, "__module__", None),
        "handler_qualname": getattr(handler, "__qualname__", None),
        "handler_name": getattr(handler, "__name__", None),
        "allowed_tools": sorted([str(tool) for tool in allowed_tools]),
    }


def run_coverage_manifest(ecc_skill_registry: Any) -> Dict[str, Any]:
    """Generate a deterministic wrapper-coverage manifest over registry.skills."""
    discovered_skills = getattr(ecc_skill_registry, "skills", {}) or {}
    skill_entries: List[Dict[str, Any]] = []
    unwrapped_ids: List[str] = []
    wrapped_count = 0
    already_wrapped_count = 0

    for skill_id in sorted(discovered_skills.keys()):
        skill_object = discovered_skills[skill_id]
        handler = getattr(skill_object, "handler", None)
        allowed_tools = getattr(skill_object, "allowed_tools", []) or []
        is_callable = callable(handler)
        is_wrapped = bool(getattr(handler, _WRAPPER_ATTR, False))

        if is_callable and is_wrapped:
            wrapped_count += 1
            already_wrapped_count += 1
        elif is_callable:
            unwrapped_ids.append(str(skill_id))

        skill_entries.append(
            {
                **_skill_identity_payload(str(skill_id), handler, allowed_tools),
                "callable": is_callable,
                "witness_wrapped": is_wrapped,
            }
        )

    manifest_body = {
        "manifest_type": "ECC_WITNESS_EXECUTION_MANIFEST_V0_1",
        "schema_version": "0.1",
        "registry_skill_count": len(discovered_skills),
        "wrapped_skill_count": wrapped_count,
        "already_wrapped_count": already_wrapped_count,
        "unwrapped_skill_ids": unwrapped_ids,
        "skill_entries": skill_entries,
        "scan_registry_version": "exfil_pattern_registry_v0_1",
        "receipt_log_path": RECEIPT_LOG_PATH,
    }
    manifest_hash = sha256_obj(manifest_body)
    boot_status = _resolve_boot_status(manifest_hash)

    return {
        **manifest_body,
        "manifest_hash": manifest_hash,
        "boot_status": boot_status,
        "boot_wire_allowed": boot_status != "BOOT_WIRE_BLOCKED" and len(unwrapped_ids) == 0,
        "total_discovered": len(discovered_skills),
        "total_wrapped": wrapped_count,
        "unwrapped_ids": unwrapped_ids,
    }


def scan_output(raw_output: Any) -> Dict[str, Any]:
    """Scan raw tool output. First winning tier only. Never expose offsets to agent."""
    text = raw_output if isinstance(raw_output, str) else canonical_json(raw_output)
    for tier in (1, 2, 3, 4, 5):
        for entry in EXFIL_PATTERNS_V0_1:
            if entry["tier"] != tier:
                continue
            if entry["pattern"].search(text):
                return {
                    "status": "BLOCKED",
                    "failure_class": "EXFIL_PATTERN_MATCHED",
                    "tier": tier,
                    "pattern_id": entry["id"],
                    "severity": entry["severity"],
                }
    return {"status": "PASS", "tier": None, "matches": []}


def contain_exfil(
    *,
    tier: int,
    pattern_id: str,
    raw_output: Any,
    preflight_receipt_hash: str,
) -> Dict[str, Any]:
    """Write quarantine receipt. Never return raw output or regex internals to agent."""
    raw_output_hash = sha256_obj(raw_output)
    quarantine_body = {
        "receipt_type": "QUARANTINE_RECEIPT_V0_1",
        "schema_version": "0.1",
        "preflight_receipt_hash": preflight_receipt_hash,
        "failure_class": "EXFIL_PATTERN_MATCHED",
        "tier": tier,
        "pattern_id": pattern_id,
        "raw_output_hash": raw_output_hash,
        "raw_output_returned": False,
        "timestamp_ns": time.time_ns(),
        "disposition": "BLOCK_AND_QUARANTINE",
    }
    quarantine_hash = sha256_obj(quarantine_body)
    _write_atomic_receipt(
        {
            "receipt_hash": quarantine_hash,
            "type": "QUARANTINE_RECEIPT_V0_1",
            "body": quarantine_body,
        }
    )
    return {
        "status": "BLOCKED",
        "disposition": "BLOCK_AND_QUARANTINE",
        "failure_class": "EXFIL_PATTERN_MATCHED",
        "tier": tier,
        "quarantine_id": quarantine_hash,
        "raw_output_returned": False,
        "agent_visible_message": "Tool output blocked by ToolGate policy.",
    }


def capture_host_delta() -> Dict[str, Any]:
    """v0.1 structural placeholder: cwd/env key set only; no env values are logged."""
    return {
        "cwd": os.getcwd(),
        "env_keys_hash": sha256_obj(sorted(os.environ.keys())),
        "timestamp_ns": time.time_ns(),
    }


def witness_skill_wrapper(
    skill_id: str,
    skill_fn: Callable[..., Any],
    allowed_tools: Optional[List[str]] = None,
    sub_agent_id: str = "ecc-global-orchestrator",
    tool_id: Optional[str] = None,
) -> Callable[..., Any]:
    """Wrap one skill callable with preflight, execution, scan, and post-tool receipts."""
    if getattr(skill_fn, _WRAPPER_ATTR, False):
        return skill_fn

    allowed_tools = allowed_tools or []

    @functools.wraps(skill_fn)
    def protected_execution(*args: Any, **kwargs: Any) -> Any:
        if not _BOOT_INFO.get("manifest_hash") or _BOOT_INFO.get("boot_status") == "BOOT_WIRE_BLOCKED":
            raise RuntimeError("FAIL_CLOSED: Boot identity missing or blocked.")

        _BOOT_INFO["sequence_nonce"] += 1
        current_nonce = int(_BOOT_INFO["sequence_nonce"])

        try:
            input_payload = {"args": args, "kwargs": kwargs}
            input_hash = sha256_obj(input_payload)
            allowed_tools_hash = sha256_obj(sorted([str(tool) for tool in allowed_tools]))
        except Exception as exc:
            logger.error("FAIL_CLOSED: input serialization failed for %s: %s", skill_id, exc)
            raise RuntimeError("FAIL_CLOSED: Preflight generation failure.") from exc

        preflight = PreflightReceiptV01(
            receipt_type="ECC_PREFLIGHT_RECEIPT_V0_1",
            schema_version="0.1",
            skill_id=skill_id,
            sub_agent_id=sub_agent_id,
            tool_id=tool_id,
            manifest_hash=str(_BOOT_INFO["manifest_hash"]),
            boot_status=_BOOT_INFO["boot_status"],
            sequence_nonce=current_nonce,
            input_hash=input_hash,
            allowed_tools_hash=allowed_tools_hash,
            timestamp_ns=time.time_ns(),
            process_id=os.getpid(),
            disposition="PREFLIGHT_PASS",
        )
        preflight_receipt_hash = preflight.receipt_hash()
        _write_atomic_receipt(
            {
                "receipt_hash": preflight_receipt_hash,
                "type": "PREFLIGHT_RECEIPT_V0_1",
                "body": asdict(preflight),
            }
        )

        try:
            base_mutation = capture_host_delta()
            raw_output = skill_fn(*args, **kwargs)
            scan_result = scan_output(raw_output)

            if scan_result["status"] == "BLOCKED":
                return contain_exfil(
                    tier=int(scan_result["tier"]),
                    pattern_id=str(scan_result["pattern_id"]),
                    raw_output=raw_output,
                    preflight_receipt_hash=preflight_receipt_hash,
                )

            post_mutation = capture_host_delta()
            if post_mutation is None or base_mutation is None:
                raise ValueError("MUTATION_HASH_MISSING")

            post = PostToolReceiptV01(
                receipt_type="ECC_POST_TOOL_RECEIPT_V0_1",
                schema_version="0.1",
                preflight_receipt_hash=preflight_receipt_hash,
                output_hash=sha256_obj(raw_output),
                mutation_delta_hash=sha256_obj(
                    {
                        "base": base_mutation,
                        "post": post_mutation,
                    }
                ),
                status="SUCCESS",
                timestamp_ns=time.time_ns(),
                disposition="RETURN_TO_AGENT",
            )
            _write_atomic_receipt(
                {
                    "receipt_hash": post.receipt_hash(),
                    "type": "POST_TOOL_RECEIPT_V0_1",
                    "body": asdict(post),
                }
            )
            return raw_output

        except Exception as exc:
            logger.error("FAIL_CLOSED: internal execution fault on skill %s: %s", skill_id, exc)
            raise RuntimeError("FAIL_CLOSED: Integrity gate termination.") from exc

    setattr(protected_execution, _WRAPPER_ATTR, True)
    return protected_execution


def inject_witness_canopy(ecc_skill_registry: Any) -> Dict[str, Any]:
    """Wrap all registry.skills handlers in-place, then verify coverage."""
    discovered_skills = getattr(ecc_skill_registry, "skills", {}) or {}
    logger.info("Witness canopy sweeping %s registered ECC skills.", len(discovered_skills))

    for skill_id in sorted(discovered_skills.keys()):
        skill_object = discovered_skills[skill_id]
        handler = getattr(skill_object, "handler", None)
        if not callable(handler):
            continue
        allowed_tools = getattr(skill_object, "allowed_tools", []) or []
        if not getattr(handler, _WRAPPER_ATTR, False):
            skill_object.handler = witness_skill_wrapper(
                str(skill_id),
                handler,
                allowed_tools=list(allowed_tools),
                sub_agent_id=getattr(skill_object, "sub_agent_id", "ecc-global-orchestrator"),
                tool_id=getattr(skill_object, "tool_id", None),
            )

    return run_coverage_manifest(ecc_skill_registry)


def execute_boot_wire(ecc_skill_registry: Any) -> Dict[str, Any]:
    """Definitive boot gate. Exits before engine start if coverage or anchors fail."""
    logger.info("Initializing Zero-Trust Boot Wire Sequence.")
    try:
        manifest_report = inject_witness_canopy(ecc_skill_registry)
    except Exception as exc:  # pragma: no cover - terminal path
        logger.critical("BOOT_WIRE_BLOCKED: manifest sweep failed: %s", exc)
        sys.exit("BOOT_WIRE_BLOCKED: Manifest execution failure.")

    if not manifest_report.get("boot_wire_allowed", False):
        logger.critical(
            "BOOT_WIRE_BLOCKED: coverage failed. discovered=%s wrapped=%s unwrapped=%s",
            manifest_report.get("total_discovered"),
            manifest_report.get("total_wrapped"),
            manifest_report.get("unwrapped_ids"),
        )
        sys.exit("BOOT_WIRE_BLOCKED: Unverified execution surfaces present.")

    _BOOT_INFO["manifest_hash"] = manifest_report["manifest_hash"]
    _BOOT_INFO["boot_status"] = manifest_report["boot_status"]
    _BOOT_INFO["sequence_nonce"] = 0

    _write_atomic_receipt(
        {
            "receipt_hash": sha256_obj(manifest_report),
            "type": "ECC_WITNESS_EXECUTION_MANIFEST_V0_1",
            "body": manifest_report,
        }
    )

    logger.info(
        "Boot Wire Verified: status=%s manifest_hash=%s",
        _BOOT_INFO["boot_status"],
        _BOOT_INFO["manifest_hash"],
    )
    return manifest_report
