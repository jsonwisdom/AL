# AL Doctrine Linter v1

Deterministic, replay-oriented validation for doctrine artifacts.

## Supported layouts

### Structured, sealable layout

```text
doctrine-directory/
├── envelope.yaml
├── sovereign.md
└── civic.md
```

The envelope must contain:

```yaml
verification_contract:
  doctrine_id: "string"
  sovereign_hash: "lowercase SHA-256"
  replay_manifest_ref: null  # optional; traceability only, grants no authority
```

### Monolithic transition layout

A single Markdown doctrine may be linted during migration. Monolithic mode can verify basic doctrine markers and calculate an artifact hash, but it returns `INDETERMINATE` because envelope integrity and file-level sovereign/civic separation cannot be certified.

## Usage

```bash
python3 -m pip install -r scripts/doctrine-lint/requirements.txt
python3 scripts/doctrine-lint/lint_doctrine.py docs/doctrines/NATIONAL_SECURITY_JOURNALISM_DOCTRINE.md
```

Structured replay:

```bash
python3 scripts/doctrine-lint/lint_doctrine.py docs/doctrines/<doctrine-id>/
```

## Exit contract

| Status | Exit | Meaning |
|---|---:|---|
| `PASS` | `0` | Required checks completed successfully. |
| `FAIL` | `1` | A deterministic invariant failed. |
| `INDETERMINATE` | `1` | Evidence or structure is insufficient to certify. |

`INDETERMINATE` is intentionally non-green. Unknown is preserved rather than converted into success.

## Output

Output is machine-readable YAML with stable key ordering. If PyYAML is unavailable and no envelope parsing is required, the serializer falls back to canonical, sorted JSON.

## CI trigger suggestion

Run when either surface changes:

```text
docs/doctrines/**
scripts/doctrine-lint/**
```

A CI workflow should enumerate doctrine targets explicitly or from a governed index. It must not infer successful coverage merely because the linter process ran.
