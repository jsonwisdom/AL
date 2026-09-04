# Epstein Law Knobs v0.1

**Authority:** false  
**Legal conclusion:** none  
**Write model:** append-only sidecar  
**Evaluation state:** NOT_RUN

## Purpose

This directory defines a deterministic comparison surface between Public Law 119-38 (Epstein Files Transparency Act) and observed public justice.gov Epstein/EFTA surfaces.

The model is intentionally fail-closed:

```text
LAW TEXT != COMPLIANCE FINDING
DOJ PUBLICATION != PROOF OF COMPLETE COMPLIANCE
MISSING PUBLIC ARTIFACT != PROOF OF CONCEALMENT
MODEL OUTPUT != LEGAL AUTHORITY
PARODY != EVIDENCE
```

## Physics

Treat source evidence as conserved input. Downstream normalization, scoring, QUBO compilation, replay, or parody may not manufacture evidentiary support.

```text
SUPPORTED_OUTPUT <= VERIFIED_INPUT
```

## Math

- 32 statutory law knobs: `LAW_KNOB_SET_001.json`
- 32 justice.gov observation slots: `OBSERVATION_SLOT_REGISTRY_001.json`
- 32 x 32 = 1024 logical comparison cells
- physical D-Wave qubit count: UNKNOWN until embedding
- QUBO energy: not a confidence score

All law knobs begin `UNRESOLVED`. Four observation slots are initially bound to public official URLs; 28 remain `UNSET`. No PASS/FAIL compliance evaluation has been run.

## Current official anchors

- Public Law 119-38: https://www.congress.gov/119/plaws/publ38/PLAW-119publ38.htm
- DOJ Epstein Library: https://www.justice.gov/epstein
- DOJ Jan. 30, 2026 release statement: https://www.justice.gov/opa/pr/department-justice-publishes-35-million-responsive-pages-compliance-epstein-files
- DOJ/FBI July 2025 memo: https://www.justice.gov/opa/media/1407001/dl

These URLs are referenced as official public sources. Their exact bytes were **not** captured or sealed in this build.

## Next lawful transition

1. Bind additional justice.gov / Federal Register / congressional report observations into unused O05-O32 slots.
2. Capture and hash exact source bytes where feasible.
3. Cross each observation against only the law knobs it can actually support.
4. Emit `PASS`, `FAIL`, `UNRESOLVED`, or `NOT_APPLICABLE` with evidence refs.
5. Only after the classical comparison matrix is reproducible may a QUBO projection be compiled.

## JOY narrator lane 😂

> Your Honor, the knobs are installed. Turning one does not create a statute, and turning all thirty-two at once does not summon a compliance finding from the quantum realm.

The joke is disposable. The receipts are not.
