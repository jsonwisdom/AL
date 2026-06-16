"""
Target governance membrane tests.

Six independent gates:
1. Schema validation
2. Provenance
3. Deprecate-over-delete
4. Tag vocabulary
5. Red-team injection
6. Governance linkage
"""
import json
import pathlib
import tempfile

import jsonschema
import pytest
import yaml

ROOT = pathlib.Path(__file__).resolve().parents[2]
SCHEMA_PATH = ROOT / "schemas" / "targets_v1.schema.json"
TAG_VOCAB_PATH = ROOT / "schemas" / "target_tags_v1.json"

FORBIDDEN_TARGET_FIELDS = {
    "priority",
    "risk_level",
    "risk_score",
    "sensitive",
    "editorial_note",
    "interpretation",
    "concern_level",
    "trust_level",
    "watch_priority",
    "threat_level",
}


def _load_targets_files():
    agents_dir = ROOT / "agents"
    if not agents_dir.exists():
        return
    for targets_file in agents_dir.rglob("targets.yaml"):
        with targets_file.open("r", encoding="utf-8") as f:
            yield targets_file, yaml.safe_load(f)


@pytest.fixture(scope="module")
def targets_schema():
    with SCHEMA_PATH.open("r", encoding="utf-8") as f:
        return json.load(f)


def test_all_targets_files_validate_against_schema(targets_schema):
    failures = []

    for path, data in _load_targets_files():
        try:
            jsonschema.validate(data, targets_schema)
        except jsonschema.ValidationError as e:
            failures.append(f"{path.relative_to(ROOT)}: {e.message}")

    assert not failures, (
        "CONSTITUTIONAL BREACH: targets.yaml files failed schema validation:\n"
        + "\n".join(failures)
    )


def test_all_targets_have_provenance():
    failures = []

    for path, data in _load_targets_files():
        for i, target in enumerate(data.get("targets", [])):
            added = target.get("added_by_pr", "")
            if not added or not added.startswith("#"):
                failures.append(
                    f"{path.relative_to(ROOT)} entry {i}: invalid added_by_pr"
                )

            if target.get("deprecated"):
                if not target.get("deprecated_by_pr"):
                    failures.append(
                        f"{path.relative_to(ROOT)} entry {i}: missing deprecated_by_pr"
                    )
                if not target.get("deprecation_reason"):
                    failures.append(
                        f"{path.relative_to(ROOT)} entry {i}: missing deprecation_reason"
                    )

    assert not failures, (
        "CONSTITUTIONAL BREACH: targets missing provenance:\n"
        + "\n".join(failures)
    )


@pytest.fixture(scope="module")
def allowed_tags():
    with TAG_VOCAB_PATH.open("r", encoding="utf-8") as f:
        tag_schema = json.load(f)
    return set(
        tag_schema.get("properties", {})
        .get("tags", {})
        .get("items", {})
        .get("enum", [])
    )


def test_all_tags_in_closed_vocabulary(allowed_tags):
    failures = []

    for path, data in _load_targets_files():
        for i, target in enumerate(data.get("targets", [])):
            for tag in target.get("tags", []):
                if tag not in allowed_tags:
                    failures.append(
                        f"{path.relative_to(ROOT)} entry {i}: invalid tag {tag}"
                    )

    assert not failures, (
        "CONSTITUTIONAL BREACH: invalid tags detected:\n"
        + "\n".join(failures)
    )


RED_TEAM_FIELDS = [
    ("priority", "high"),
    ("risk_level", "elevated"),
    ("sensitive", True),
    ("editorial_note", "watch this"),
    ("interpretation", "problematic"),
]


def test_forbidden_fields_rejected_by_schema(targets_schema):
    for field_name, field_value in RED_TEAM_FIELDS:
        malicious = {
            "targets": [
                {
                    "url": "https://example.gov/opinion.pdf",
                    "tags": ["court_opinion"],
                    "added_by_pr": "#42",
                    field_name: field_value,
                }
            ]
        }

        with pytest.raises(jsonschema.ValidationError):
            jsonschema.validate(malicious, targets_schema)


def test_forbidden_fields_detected_in_raw_yaml():
    for field_name, field_value in RED_TEAM_FIELDS:
        malicious = {
            "targets": [
                {
                    "url": "https://example.gov/opinion.pdf",
                    "tags": ["court_opinion"],
                    "added_by_pr": "#42",
                    field_name: field_value,
                }
            ]
        }

        with tempfile.NamedTemporaryFile(mode="w", suffix=".yaml", delete=False) as f:
            yaml.dump(malicious, f)
            temp_path = pathlib.Path(f.name)

        try:
            with temp_path.open("r", encoding="utf-8") as f:
                data = yaml.safe_load(f)

            violations = []
            for target in data.get("targets", []):
                extra = set(target.keys()) - {
                    "url",
                    "tags",
                    "added_by_pr",
                    "deprecated",
                    "deprecated_by_pr",
                    "deprecation_reason",
                    "rationale",
                    "operational_state",
                }
                violations.extend(extra & FORBIDDEN_TARGET_FIELDS)

            assert violations
        finally:
            temp_path.unlink()


def test_targets_governance_spec_exists():
    spec_path = ROOT / "specs" / "targets_governance_v0.1.md"
    assert spec_path.exists()


def test_tag_vocabulary_schema_exists():
    assert TAG_VOCAB_PATH.exists()
