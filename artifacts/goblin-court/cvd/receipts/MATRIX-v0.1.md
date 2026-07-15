# CVD Failure-State Matrix v0.1 Receipt

## Verified artifact

- Path: `artifacts/goblin-court/cvd/matrix/failure-state-matrix.json`
- Commit: `88cff73756f413635e7a0d7034bfd88bbf909177`
- Branch: `feat/goblin-court-cvd-directories-first`
- Draft PR: `#401`

## Verification result

```text
DIRECTORY_SCAFFOLD_PRESENT   = TRUE
MATRIX_FILE_PRESENT          = TRUE
MATRIX_MACHINE_READABLE      = TRUE
MATRIX_SEMANTICS_TESTED      = FALSE
RUST_STATE_MACHINE_PRESENT   = FALSE
HARNESS_PRESENT              = FALSE
CI_RUN_OBSERVED              = FALSE
PROVISIONAL                  = LOCKED
T                            = 0
```

## Boundary

The JSON matrix is a design artifact. Its state-transition semantics are not yet implemented or tested. `T` does not advance until the matrix is parsed by executable code and the corresponding harness passes in an observed CI run tied to the same commit or a documented descendant.
