# GEN_SPEC_V1

## Purpose

Define byte-stable artifact generation for ALMS intake artifacts.

## Canonical Artifact Rule

ALMS artifacts must be emitted in canonical JSON / JSONL form before precheck.

Required canonicalization command:

```bash
jq -cS . input.jsonl > input.canonical.jsonl
```

The canonical artifact becomes the working artifact only after explicit operator promotion:

```bash
cp input.canonical.jsonl input.jsonl
```

Then precheck must pass:

```bash
cmp -s input.jsonl input.canonical.jsonl && echo PRECHECK_PASS || echo PRECHECK_FAIL
```

## Bash-Only Operator Rule

For Cloud Shell ALMS runs:

- No nano.
- No Python.
- No manual editor dependency.
- Use `cat <<'EOF'`, `jq -cS`, `cmp`, `sha256sum`, `wc -c`, `sed`, `grep`, `tar`, and `curl`.

## Failure Rule

If `PRECHECK_FAIL` occurs, do not anchor, batch, or derive. Promote canonical bytes or regenerate from a canonical source.

## Doctrine

Same meaning is insufficient. Same bytes are required.
