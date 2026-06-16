# Replay Node v0.1 — Runtime Specification

Status: PR #260-bounded specification
Scope: civic-document replay only
Authority: false
Merge permission: false

## 1. Purpose

Replay Node v0.1 replays one official public civic PDF source through a deterministic extraction and hashing pipeline.

It verifies whether the emitted output CSV hash matches the claimed CSV hash under the declared runtime steps.

It does not adjudicate, certify, merge, crawl, summarize, or assign authority.

## 2. In Scope

Replay Node v0.1 includes only the behavior proven by PR #260:

1. fetch official public PDF URL
2. compute PDF SHA256
3. identity gate by expected date plus proceedings/minutes text
4. extract text with `pdftotext -layout`
5. compute text SHA256
6. emit deterministic rows
7. compute output CSV SHA256
8. compare output CSV SHA256 to claimed CSV hash
9. emit receipt JSON on MATCH
10. fail closed on missing dependency
11. fail closed on identity mismatch
12. fail closed on output hash mismatch
13. preserve `authority: false`
14. preserve `merge_permission: false`

## 3. Explicitly Not In Scope

Replay Node v0.1 does not include:

- PDF hash comparison to a claimed source hash
- CSV source input
- daily ingestion
- crawler behavior
- size limit guarantees
- timeout guarantees
- debug flags
- soft failure continuation
- cross-jurisdiction joins
- institutional certification
- merge authority assignment
- narrative summary generation

## 4. Accepted Inputs

| Input | Format | Rule |
|---|---|---|
| Official public PDF URL | HTTPS URL | Must identify a documented civic source system or relevant government publication surface |
| Expected date | YYYY-MM-DD rendered to display date | Used by the identity gate |
| Expected document type text | proceedings or minutes text | Used by the identity gate |
| Claimed CSV SHA256 | lowercase SHA256 hex | Compared only against emitted output CSV SHA256 |

## 5. Runtime Steps

1. Fetch the PDF from the official public URL.
2. Compute the SHA256 hash of the downloaded PDF bytes.
3. Check that `pdftotext` is available.
4. Extract the first page.
5. Apply the identity gate using expected date plus proceedings/minutes text.
6. Extract full text with `pdftotext -layout`.
7. Compute the SHA256 hash of the extracted text.
8. Run the deterministic row emitter.
9. Compute the SHA256 hash of the emitted output CSV.
10. Compare the output CSV SHA256 to the claimed CSV SHA256.
11. Emit receipt JSON only on MATCH.
12. Exit with failure on missing dependency, identity mismatch, or hash mismatch.

## 6. Fail-Closed Conditions

| Condition | Result |
|---|---|
| `pdftotext` missing | fail closed |
| PDF fetch empty or unavailable | fail closed |
| identity gate mismatch | fail closed |
| output CSV SHA256 mismatch | fail closed |

Failure does not grant authority or merge permission.

## 7. Receipt Fields on MATCH

A successful replay emits receipt JSON containing:

```json
{
  "replay_result": "MATCH",
  "authority": false,
  "merge_permission": false,
  "commit_hash": "git SHA",
  "source_url": "official public PDF URL",
  "meeting_date": "YYYY-MM-DD",
  "expected_display_date": "Month D, YYYY",
  "pdf_sha256": "sha256:<hex>",
  "extracted_text_sha256": "sha256:<hex>",
  "output_csv_sha256": "<hex>",
  "claimed_csv_sha256": "<hex>",
  "row_count": 0
}
```

## 8. Membrane Rule

NO_NARRATIVE_MUTATION_OF_RUNTIME.

The operator layer may explain these runtime steps, but it may not add behavior, expand scope, modify verdict semantics, or imply authority not present in this specification.
