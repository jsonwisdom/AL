# C0001 Copilot Handoff — Use Existing MN_001 Proof

Jay already did the Minnesota proof work. Do not recreate it as a new PDF capture.

## Existing proof source

Use the existing repo-bound proof artifacts:

- Source text: `_truth/sources/mmb-feb-2026-forecast.txt`
- Receipt: `_truth/receipts/MN_001.json`
- Receipt hash in MN_001: `04368980dc3d501a4131202cc38ce56cfd38054eaf140f56e65f8280e6d5e51c`

## Correct C0001 interpretation

C0001 is not a fresh HTTP/PDF capture yet.
C0001 is a replay corpus entry for the existing verified MN_001 audit source.

Treat this as:

```json
{
  "corpus_id": "C0001",
  "mode": "repo_bound_existing_proof",
  "source": "_truth/sources/mmb-feb-2026-forecast.txt",
  "receipt": "_truth/receipts/MN_001.json",
  "status": "USE_EXISTING_MN_PROOF_DO_NOT_REFETCH"
}
```

## Next implementation task

Patch `ci/replay_corpus_runner.py` or add C0001 manifests so the runner can accept a repo-bound source entry without requiring `source/raw.bin`.

Allowed behavior:

- Read source bytes from `_truth/sources/mmb-feb-2026-forecast.txt`.
- Use repo path identity, not HTTP identity.
- Compare against the existing MN_001 hash/receipt path.
- Emit a truthful PASS/FAIL/INDETERMINATE report.

Forbidden behavior:

- Do not invent a PDF URL.
- Do not invent raw PDF bytes.
- Do not invent hashes.
- Do not mark C0001 PASS unless the existing source and expected hash replay cleanly.

## Expected direction

C0001 should become the first deterministic replay corpus case based on already-verified MN work:

`existing audit source -> replay hash -> compare to MN_001 receipt hash -> corpus_report.json`

No more scaffolding loop.
