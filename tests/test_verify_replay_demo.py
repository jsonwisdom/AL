import hashlib
import json
import subprocess
from pathlib import Path

from tools.verify_replay_demo import run_audit


def write_json(path: Path, data: dict) -> None:
    path.write_text(json.dumps(data, indent=2), encoding="utf-8")


def minimal_schema() -> dict:
    return {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "type": "object",
        "required": [
            "schema_version",
            "artifact_id",
            "artifact_type",
            "root_identity",
            "l0_vault",
            "l2_chronology",
            "witness",
            "repair",
            "replay",
        ],
        "properties": {},
    }


def schema_compliant_sample(content_hash: str) -> dict:
    return {
        "schema_version": "lapis.replayable_audit_demo.v0.1",
        "artifact_id": "lapis-genesis-commit-edcec6f",
        "artifact_type": "code_commit",
        "root_identity": "jaywisdom.eth",
        "l0_vault": {
            "provider": "gcs",
            "bucket": "wisdom-family-vault",
            "object_path": "lapis/genesis/docs/LAPIS_PROTOCOL_STEWARDSHIP_INVARIANT.md",
            "content_sha256": content_hash,
        },
        "l2_chronology": {
            "chain": "base",
            "tx_hash": None,
            "block_number": None,
            "attestation_uid": None,
        },
        "witness": {
            "identity": "jaywisdom.eth",
            "statement": "Test witness statement.",
            "statement_sha256": "0" * 64,
            "timestamp": "2026-05-14T06:45:00-05:00",
        },
        "repair": {
            "is_repair": True,
            "parent_artifact_id": "lapis-genesis-commit-edcec6f",
            "rationale": "Test repair rationale.",
            "lineage_scar": "test-lineage-scar",
        },
        "replay": {
            "instructions": [
                "hash artifact bytes",
                "compare resulting hash against content_sha256",
                "verify genesis commit exists",
            ],
            "expected_result": "Replay verifier produces deterministic pass or fail.",
        },
    }


def init_git_repo(path: Path) -> None:
    subprocess.run(["git", "init"], cwd=path, check=True, stdout=subprocess.DEVNULL)
    subprocess.run(["git", "config", "user.email", "test@example.com"], cwd=path, check=True)
    subprocess.run(["git", "config", "user.name", "Lapis Test"], cwd=path, check=True)

    doctrine_path = path / "docs"
    doctrine_path.mkdir(parents=True)
    (doctrine_path / "LAPIS_PROTOCOL_STEWARDSHIP_INVARIANT.md").write_text(
        "Continuity is a cared-for practice, not a static state.\n",
        encoding="utf-8",
    )

    subprocess.run(["git", "add", "."], cwd=path, check=True)
    subprocess.run(["git", "commit", "-m", "test genesis"], cwd=path, check=True, stdout=subprocess.DEVNULL)


def test_audit_pass_when_schema_texture_chronology_witness_and_replay_align(tmp_path, monkeypatch):
    init_git_repo(tmp_path)
    monkeypatch.chdir(tmp_path)

    artifact = tmp_path / "docs" / "LAPIS_PROTOCOL_STEWARDSHIP_INVARIANT.md"
    content_hash = hashlib.sha256(artifact.read_bytes()).hexdigest()

    schema_path = tmp_path / "schema.json"
    sample_path = tmp_path / "sample.json"
    output_path = tmp_path / "REPLAY_SUMMARY.json"

    write_json(schema_path, minimal_schema())
    write_json(sample_path, schema_compliant_sample(content_hash))

    summary = run_audit(sample_path=sample_path, schema_path=schema_path, output_path=output_path)

    assert summary["verdict"] == "PASS"
    assert summary["lapis_filter"]["texture_present"] is True
    assert summary["lapis_filter"]["chronology_present"] is True
    assert summary["lapis_filter"]["witness_present"] is True
    assert summary["lapis_filter"]["replay_path_present"] is True
    assert output_path.exists()


def test_audit_fails_on_byte_mutation(tmp_path, monkeypatch):
    init_git_repo(tmp_path)
    monkeypatch.chdir(tmp_path)

    artifact = tmp_path / "docs" / "LAPIS_PROTOCOL_STEWARDSHIP_INVARIANT.md"
    original_hash = hashlib.sha256(artifact.read_bytes()).hexdigest()
    artifact.write_text("Continuity is a sterile snapshot.\n", encoding="utf-8")

    schema_path = tmp_path / "schema.json"
    sample_path = tmp_path / "sample.json"
    output_path = tmp_path / "REPLAY_SUMMARY.json"

    write_json(schema_path, minimal_schema())
    write_json(sample_path, schema_compliant_sample(original_hash))

    summary = run_audit(sample_path=sample_path, schema_path=schema_path, output_path=output_path)

    assert summary["verdict"] == "FAIL"
    assert summary["forensics"]["content_match"] is False
    assert summary["lapis_filter"]["silent_overwrite_detected"] is True


def test_audit_fails_when_schema_is_invalid(tmp_path, monkeypatch):
    init_git_repo(tmp_path)
    monkeypatch.chdir(tmp_path)

    artifact = tmp_path / "docs" / "LAPIS_PROTOCOL_STEWARDSHIP_INVARIANT.md"
    content_hash = hashlib.sha256(artifact.read_bytes()).hexdigest()

    schema_path = tmp_path / "schema.json"
    sample_path = tmp_path / "sample.json"
    output_path = tmp_path / "REPLAY_SUMMARY.json"

    write_json(schema_path, minimal_schema())
    sample = schema_compliant_sample(content_hash)
    del sample["witness"]
    write_json(sample_path, sample)

    summary = run_audit(sample_path=sample_path, schema_path=schema_path, output_path=output_path)

    assert summary["verdict"] == "FAIL"
    assert summary["lapis_filter"]["schema_valid"] is False
    assert summary["lapis_filter"]["witness_present"] is False
