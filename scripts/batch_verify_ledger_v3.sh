#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
LOG="$ROOT/_truth/logs/batch_verify_ledger.log"
LEDGER="$ROOT/_truth/ledger/alms_ledger.jsonl"
TMP_DIR="$ROOT/_truth/tmp"
RUNS="$TMP_DIR/v3_results.jsonl"

mkdir -p "$ROOT/_truth/logs" "$ROOT/_truth/ledger" "$ROOT/_truth/snapshots" "$TMP_DIR"
touch "$LEDGER"
: > "$RUNS"

ts="$(date -u +"%Y-%m-%dT%H:%M:%SZ")"
run_id="$(date -u +"%Y%m%dT%H%M%SZ")"

echo "=== ALMS LEDGER V3 RUN $ts ===" >> "$LOG"

"$ROOT/scripts/validate_alms_ledger.sh" >> "$LOG"

find "$ROOT/data" -maxdepth 2 -name claims.json | sort | while read -r file; do
  leaf="$(basename "$(dirname "$file")")"

  jq -r '.fields[].canonical_claim' "$file" | while IFS= read -r claim; do
    if printf '%s\n' "$claim" | "$ROOT/verify.sh" >> "$LOG" 2>&1; then
      jq -cn --arg leaf "$leaf" --arg kind "canonical" --arg result "PASS" \
        '{leaf:$leaf,kind:$kind,result:$result}' >> "$RUNS"
    else
      jq -cn --arg leaf "$leaf" --arg kind "canonical" --arg result "FAIL" \
        '{leaf:$leaf,kind:$kind,result:$result}' >> "$RUNS"
    fi
  done

  jq -r '.fields[].tests[]? | select(.id=="wrong_value") | .claim_text' "$file" | while IFS= read -r claim; do
    printf '%s\n' "$claim" | "$ROOT/verify.sh" >> "$LOG" 2>&1 || true
    jq -cn --arg leaf "$leaf" --arg kind "wrong_value" --arg result "EXPECTED_REJECT" \
      '{leaf:$leaf,kind:$kind,result:$result}' >> "$RUNS"
  done
done

fail_count="$(grep -c '"FAIL"\|"UNEXPECTED_PASS"' "$RUNS" || true)"
pass_count="$(grep -c '"PASS"\|"EXPECTED_REJECT"' "$RUNS" || true)"
claims_count="$(find "$ROOT/data" -maxdepth 2 -name claims.json | wc -l | tr -d ' ')"

[[ "$fail_count" == "0" ]] || {
  echo "V3_GATE_FAIL fail_count=$fail_count" >> "$LOG"
  cat "$RUNS" >> "$LOG"
  exit 1
}

prev_hash="$(tail -n 1 "$LEDGER" | jq -r '.entry_hash // "GENESIS"' 2>/dev/null || echo "GENESIS")"
log_hash="$(sha256sum "$LOG" | awk '{print $1}')"
data_hash="$(find "$ROOT/data" -type f -name claims.json -print0 | sort -z | xargs -0 sha256sum | sha256sum | awk '{print $1}')"
results_hash="$(sha256sum "$RUNS" | awk '{print $1}')"

entry_no_hash="$TMP_DIR/entry_no_hash.json"

jq -cn \
  --arg ts "$ts" \
  --arg run_id "$run_id" \
  --arg prev_hash "$prev_hash" \
  --arg log_hash "$log_hash" \
  --arg data_hash "$data_hash" \
  --arg results_hash "$results_hash" \
  --argjson claims_count "$claims_count" \
  --argjson pass_count "$pass_count" \
  '{
    type:"ALMS_BATCH_RECEIPT",
    version:"v3",
    timestamp:$ts,
    run_id:$run_id,
    previous_hash:$prev_hash,
    claims_count:$claims_count,
    pass_count:$pass_count,
    fail_count:0,
    data_hash:$data_hash,
    results_hash:$results_hash,
    log_hash:$log_hash
  }' > "$entry_no_hash"

entry_hash="$(jq -c . "$entry_no_hash" | sha256sum | awk '{print $1}')"
jq -c --arg entry_hash "$entry_hash" '. + {entry_hash:$entry_hash}' "$entry_no_hash" >> "$LEDGER"

"$ROOT/scripts/validate_alms_ledger.sh" >> "$LOG"

cp "$LEDGER" "$ROOT/_truth/snapshots/alms_ledger_$run_id.jsonl"

echo "V3_LEDGER_ENTRY $entry_hash" >> "$LOG"
echo "=== END $ts ===" >> "$LOG"
