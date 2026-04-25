#!/usr/bin/env bash
set -euo pipefail

# Jay's Math Class 001: Compounding Public Value Calculator

# ─── Inputs (override via env) ───────────────────────────
STATE_VELOCITY="${STATE_VELOCITY:-5}"
VERIFIED_MATH_USD="${VERIFIED_MATH_USD:-12955000}"
HUMAN_MULTIPLIER="${HUMAN_MULTIPLIER:-1.93}"
TIME_WINDOW="${TIME_WINDOW:-1 week}"

# ─── Deterministic deps check ────────────────────────────
command -v bc >/dev/null || { echo "bc required"; exit 1; }
command -v sha256sum >/dev/null || { echo "sha256sum required"; exit 1; }

# ─── Clamp multiplier [1.0, 3.0] ─────────────────────────
if (( $(echo "$HUMAN_MULTIPLIER < 1.0" | bc -l) )); then HUMAN_MULTIPLIER="1.0"; fi
if (( $(echo "$HUMAN_MULTIPLIER > 3.0" | bc -l) )); then HUMAN_MULTIPLIER="3.0"; fi

# ─── Compute CPV (integer index) ─────────────────────────
CPV_INDEX=$(echo "scale=0; ($STATE_VELOCITY * $VERIFIED_MATH_USD * $HUMAN_MULTIPLIER) / 1000000" | bc)

# ─── Timestamp ───────────────────────────────────────────
TIMESTAMP="$(date -u +%FT%TZ)"

# ─── Canonical JSON (sorted keys) ────────────────────────
JSON_OUTPUT=$(cat <<JSON
{
  "class": "JayMathClass001",
  "computed_at": "${TIMESTAMP}",
  "cpv_index": ${CPV_INDEX},
  "human_multiplier": ${HUMAN_MULTIPLIER},
  "model": "Compounding Public Value",
  "state_velocity": ${STATE_VELOCITY},
  "time_window": "${TIME_WINDOW}",
  "verified_math_usd": ${VERIFIED_MATH_USD},
  "constraints": {
    "fixed_time_window": true,
    "multiplier_bounded": true,
    "multiplier_range": "[1.0,3.0]",
    "receipt_required": true,
    "statute_required": true
  }
}
JSON
)

# ─── Hash (receipt anchor) ───────────────────────────────
CPV_HASH=$(printf "%s" "$JSON_OUTPUT" | sha256sum | awk '{print $1}')

# ─── Final output ────────────────────────────────────────
cat <<FINAL
{
  "cpv_receipt": {
    "hash": "${CPV_HASH}",
    "payload": ${JSON_OUTPUT}
  }
}
FINAL

# ─── Optional: write to feed (idempotent overwrite) ──────
mkdir -p site
printf "%s\n" "$JSON_OUTPUT" > site/cpv-feed.json

