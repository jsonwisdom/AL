#!/usr/bin/env bash
set -euo pipefail

OUT="${1:-docs/verified-claims.json}"
CLAIMS_DIR="${CLAIMS_DIR:-claims/mn}"

command -v jq >/dev/null 2>&1 || { echo "BUILD_MANIFEST_FAIL reason=missing_jq" >&2; exit 2; }

mkdir -p "$(dirname "$OUT")"

TMP="$(mktemp)"
trap 'rm -f "$TMP"' EXIT

find "$CLAIMS_DIR" -type f -name "*.canonical.json" | LC_ALL=C sort | while read -r f; do
  jq --arg file "../$f" '
    {
      claim_number: (input_filename | capture("mn_(?<n>[0-9]+)_").n // null),
      claim_id,
      claim_text,
      claim_type,
      line_hint: .source.line_hint,
      status,
      canonical_json: $file,
      ledger_entry: "../_truth/ledger.jsonl",
      text_hash: .artifacts.text_hash
    }
  ' "$f"
done | jq -s '
  {
    version: "2026.04",
    jurisdiction: "MN",
    generated_at: "generated_by_scripts/build_verified_claims_manifest.sh",
    verifier: "AL VCLP",
    ledger: "../_truth/ledger.jsonl",
    source: {
      agency: "Minnesota Management and Budget",
      document: "February 2026 Budget and Economic Forecast",
      source_pdf: "../sources/mn/mmb-feb-2026-forecast.pdf",
      source_hash: "sha256:c4ac46e46b80b42a6abc24edbe0480ac4983cb0090a758bd7458b2ea62faca69",
      extract_file: "../_truth/sources/mmb-feb-2026-forecast.txt",
      extract_hash: "sha256:da5ad1bbe192eae56c96cf574025b8f915839d29c78c69e8d6b98a0ad9d7d917"
    },
    claims: .
  }
' > "$TMP"

mv "$TMP" "$OUT"
echo "BUILD_MANIFEST_OK out=$OUT claims=$(jq '.claims|length' "$OUT")"
