# ARCHITECTURE

AL is built as a verification machine, not a database.

## Three Layers

**1. Civic Proof** — public datasets + verification
- What the public sees and can check
- NY income/climate receipts, proof pages, methodology notes
- No hidden steps

**2. Constitutional Machine** — replay / receipts / doctrine
- Deterministic transforms
- Every claim produces a receipt with source, query, parameters, output_hash
- Replay is the only authority

**3. Agent Infrastructure** — observers / validators / automation
- Watchdogs that continuously re-run receipts
- Validators check hashes and anchors
- Automation prevents drift

## Verification Flow

~~~mermaid
flowchart TD
    A[Raw Source Material] --> B[Intake]
    B --> C[Normalize]
    C --> D[Canonical Output]
    D --> E[Receipt]
    E --> F
    F --> G[Public Proof Surface]
    F --> H[Anchor / Attestation]
    E --> I[Replay]
    I --> J[Observer Verification]
    J --> K[Verdict]
    subgraph Civic Proof
      G
      K
    end
    subgraph Constitutional Machine
      C
      D
      E
      F
      I
    end
    subgraph Agent Infrastructure
      J
    end
~~~

## Data Path

1. Intake: pull from authoritative source (ACS, GSOD, etc.)
2. Normalize: deterministic SQL, no manual edits
3. Canonical Output: CSV/JSON with stable ordering
4. Receipt: JSON with query, params, hashes, timestamp
5. Hash: sha256 of output
6. Public Proof: rendered HTML table linking receipts
7. Anchor: optional on-chain attestation via ENS
8. Replay: anyone reruns step 2-4 and compares hash

## Current Implementation

- NY Climate-Economic Stack preserved as first civic proof
- Receipts: NY-001 through NY-012
- Guardrails: $0 BigQuery-only, no interpolation, honest sparsity
- Public proof: https://jsonwisdom.github.io/AL/computer-wisdom-public-proof.html
