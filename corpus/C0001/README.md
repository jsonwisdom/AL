# C0001 — Minnesota Budget PDF (Deterministic Replay Corpus)

Status: SCAFFOLD (INDETERMINATE)

This entry becomes valid only after the following are provided:

1. source/raw.bin — exact frozen bytes of the PDF
2. source/headers.json — real HTTP headers from fetch
3. replay/expected_hashes.json — populated with:
   - normalized_artifact_hash (sha256 of normalized text)
   - identity tuple (source_url, canonical_url, FETCH_FINGERPRINT)

Once those are committed, CI will:

- Run ci/replay_corpus_runner.py
- Compare replay output to expected_hashes.json
- Emit ci/corpus_report.json

No partial validity is allowed. Until then, this case is INDETERMINATE by design.
