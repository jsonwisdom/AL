# Goblin Court CVD

Status: directory scaffold only.

This path will hold implementation evidence for Issue #400.

## Required structure

```text
artifacts/goblin-court/cvd/
├── source/
├── tests/
├── matrix/
├── ci/
└── receipts/
```

## Current gate

```text
DIRECTORY_SCAFFOLD_PRESENT = TRUE
CVD_CODE_PRESENT           = FALSE
HARNESS_PRESENT            = FALSE
MATRIX_IMPLEMENTED         = FALSE
CI_CONFIG_PRESENT          = FALSE
CI_RUN_OBSERVED            = FALSE
PROVISIONAL                = LOCKED
T                          = 0
```

No child directory or receipt inherits implementation status from this scaffold.
