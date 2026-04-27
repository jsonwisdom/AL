# Verifiable Claim Ledger Protocol (VCLP)

VCLP is a byte-exact claim verification protocol for public records.

It turns static documents and tabular data into append-only, replayable ledgers where every claim can be checked against source bytes.

## Protocol family

| Layer | Purpose | Trust model |
|---|---|---|
| VCLP-PDF | Verify claims against extracted document lines | SHA256 + preserved extraction |
| VCLP-TAB | Verify CSV rows and row ranges | SHA256 + deterministic CSV bytes |
| VCLP-COMPUTE | Verify derived totals from anchored rows | Trusted parser + deterministic arithmetic |

## Core invariant

```text
source bytes -> claim hash -> ledger-line hash chain -> verifier
```

## Directory

```text
docs/protocols/vclp/
├── SPEC.md
├── VERIFY_BEFORE_YOU_TRUST.md
└── tabular/
    ├── TABULAR_SPEC.md
    ├── COMPUTE_SPEC.md
    ├── csv_to_claims.py
    ├── compute_claims.py
    ├── verify_tabular.sh
    ├── verify_compute.py
    └── examples/
```

## Design boundary

Byte claims prove that source bytes did not drift.

Computation claims prove that a declared operation recomputes from anchored inputs. They are derived claims and carry extra trust assumptions: parser correctness and arithmetic correctness.

## Status

This is AL doctrine-layer protocol material. Runtime watchers, Nitro observers, and application code remain separate.
