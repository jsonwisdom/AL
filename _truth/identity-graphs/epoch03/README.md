# Epoch03 — Witness Primitive 001

This folder contains the public discovery surface for **Witness Primitive 001** — a minimal, replay-first identity graph.

It provides a stable, zero-cost, independently verifiable identity component using GitHub commit history and standard tools.

## Purpose

Separate concerns for maximum verifiability:

- Identity discovers
- Receipts prove
- Hashes anchor
- Attestations challenge, optionally
- Runtimes execute and disappear

No live services, mandatory blockchain lookups, runtime hosting, dashboards, or API endpoints are required for verification.

## Files

| File | Description |
|---|---|
| `witness-primitive-001.json` | Canonical identity graph object. |
| `witness-primitive-001.receipt.json` | Receipt binding the graph to the commit, Git blob SHA, and portable SHA-256. |
| `witness-primitive-001.diagram.json` | Diagram specification derived from the graph and receipt. |
| `witness-primitive-001.render.svg` | SVG visual render of the identity topology. This is derived, not authoritative. |
| `ens-pointer-spec-v1.json` | Optional ENS / Basename TXT pointer specification. Discovery only. |
| `attestation-payload-v1.json` | Base Sepolia attestation payload for the graph hash. Optional reference surface. |

## Portable SHA-256 verification

Expected SHA-256 for `witness-primitive-001.json`:

```text
bd14d54188da6f98a18ef2e5dd0dee8edd08a89b9e5a890104ac07d176c2d139
```

### macOS / Linux

```bash
shasum -a 256 witness-primitive-001.json
```

### Windows PowerShell / Command Prompt

```powershell
certUtil -hashfile witness-primitive-001.json SHA256
```

### Python

```bash
python3 -c 'import hashlib; print(hashlib.sha256(open("witness-primitive-001.json", "rb").read()).hexdigest())'
```

## How to use this surface

1. Clone or browse this folder.
2. Verify the SHA-256 hash matches `witness-primitive-001.json`.
3. Review Git commit history for replay and lineage verification.
4. Optionally review:
   - `witness-primitive-001.render.svg` for a visual representation
   - `attestation-payload-v1.json` for the Base Sepolia reference payload

The SVG and diagram artifacts are derived visualization surfaces. They are not authoritative sources of truth.

This folder is a public discovery and verification surface, not a runtime, dashboard, API, or execution environment.

## Status

- Public discovery: ready
- Verification: fully offline / portable
- Attestations: optional reference surface
- Infrastructure cost: $0

## Doctrine

No ghost anchors. Replay first. Scale later.

## Repository path

```text
https://github.com/jsonwisdom/AL/tree/master/_truth/identity-graphs/epoch03
```
