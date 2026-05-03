# ALMS Versioning System

Status: ACTIVE_SPEC
Operator: Jay Wisdom

## Core law

Every system change must be versioned at the layer it changes.

A version is not a vibe. A version is a machine-readable state transition.

---

## 1. Version layers

ALMS uses four version layers:

```json
{
  "protocol_version": "rules and invariants",
  "schema_version": "JSON structure and validation",
  "corpus_version": "replay corpus state",
  "workflow_version": "CI and execution lanes"
}
```

---

## 2. Version format

All versions use:

```text
MAJOR.MINOR.PATCH
```

Meaning:

```json
{
  "MAJOR": "breaks replay or receipt compatibility",
  "MINOR": "adds capability without breaking existing receipts",
  "PATCH": "fixes execution, docs, wiring, or isolation without changing truth semantics"
}
```

---

## 3. State labels

A versioned unit may have one of these states:

```json
[
  "DRAFT",
  "LOCKED",
  "REPLAY_REQUIRED",
  "REPLAY_PASSED",
  "BLOCKED",
  "DEPRECATED"
]
```

No other state labels are allowed for version registry entries.

---

## 4. Promotion rules

### DRAFT -> LOCKED

Allowed when the spec or artifact is structurally complete.

### LOCKED -> REPLAY_REQUIRED

Allowed when a deterministic replay must prove the lock.

### REPLAY_REQUIRED -> REPLAY_PASSED

Allowed only when machine output proves the expected hash or root.

### Any state -> BLOCKED

Allowed when mismatch, missing input, or taint is detected.

### Any state -> DEPRECATED

Allowed when replaced by newer version while preserving historical receipts.

---

## 5. Machine registry

Canonical registry path:

```text
alms/version_registry.json
```

Each entry must include:

```json
{
  "id": "C0001",
  "layer": "corpus_version",
  "version": "1.0.0",
  "state": "REPLAY_PASSED",
  "artifact_path": "corpus/C0001/replay/expected_hashes.json",
  "hash": "sha256:<64-hex>",
  "depends_on": [],
  "notes": "string"
}
```

---

## 6. Receipt rule

Every version bump must emit a receipt at:

```text
alms/version_receipts/<id>-<version>.json
```

Receipt fields:

```json
{
  "event_type": "alms_version_bump",
  "id": "C0001",
  "old_version": "0.0.0",
  "new_version": "1.0.0",
  "old_state": "DRAFT",
  "new_state": "REPLAY_PASSED",
  "artifact_path": "corpus/C0001/replay/expected_hashes.json",
  "artifact_hash": "sha256:<64-hex>",
  "timestamp_utc": "YYYY-MM-DDTHH:MM:SSZ"
}
```

---

## 7. Operator rule

Humans may read the Markdown.
Machines must read the JSON registry and receipts.

If Markdown and JSON disagree, JSON registry wins until corrected by a new version receipt.

---

## 8. Current bootstrap targets

```json
{
  "ALMS_PROTOCOL": "1.0.0",
  "WORKFLOW_SIGNAL_MAP": "1.0.0",
  "C0001": "1.0.0",
  "C0002": "1.0.0",
  "C0003": "0.1.0"
}
```
