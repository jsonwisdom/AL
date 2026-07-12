# Gray Baby validation bundle

This directory contains the fail-closed validation substrate for the GB-015 C01-C10 runtime-test-plan set.

## Current state

- Validator source: present
- Runtime-plan schema: present and non-empty
- Test-receipt schema: present and non-empty
- Test-authorization schema: present and non-empty
- C01-C10 full plan files: **not yet present on this branch**
- Validation receipt: **not generated on this branch**
- Fixture creation: **not authorized**
- Runtime execution: **not authorized**
- Canon promotion: **false**
- Authority: **false**

The validator intentionally exits nonzero when expected files are absent, malformed, duplicated, incomplete, or inconsistent with the schemas. It also runs built-in negative checks for missing execution action, `authority: true`, invalid result enums, and placeholder plans.

## Local validation

```bash
python3 -m pip install -r validation/requirements.txt
python3 validation/validate.py > validation/raw_stdout.txt 2> validation/raw_stderr.txt
printf '%s\n' "$?" > validation/exit_code.txt
```

A zero exit code is admissible only after all ten complete plan files exist and all schema and negative tests pass. The generated receipt is evidence of that execution only; it is not a compliance certificate or authority elevation.
