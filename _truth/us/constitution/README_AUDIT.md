# ALMS Constitution Audit (GitHub Direct)

This directory is the **sole trust boundary** for Constitution verification.

## Principles

- No hashes are accepted from chat or memory.
- All proofs are derived from **repo bytes**.
- Verification is performed by deterministic scripts committed here.

## Workflow

1. Commit canonical span files (e.g., `a1_s8_c1_span.txt`).
2. Run verifier:

   ```bash
   python3 _truth/us/constitution/verify_constitution_spans.py
   ```

3. Commit the generated JSONL:

   ```bash
   git add _truth/us/constitution/constitution_span_audit.jsonl
   git commit -m "Update Constitution audit output"
   git push
   ```

4. Only the JSONL artifact is used for Merkle root generation.

## Status Model

- `MISSING` → span not yet anchored
- `OK` → span verified from repo bytes

## Next Steps

- Expand TARGETS to cover all clauses (C1–C18)
- Add Sections 9–10
- Introduce deterministic Merkle script

---

**Rule:** If it isn’t committed, it doesn’t exist.
