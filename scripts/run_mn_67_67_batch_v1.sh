#!/usr/bin/env bash
set -euo pipefail

CLAIM="The motion did not prevail"

URLS=(
  "https://www.house.mn.gov/cco/journals/2025-26/J0423063.htm"
  "https://www.house.mn.gov/cco/journals/2025-26/J0409055.pdf"
  "https://www.house.mn.gov/cco/journals/2025-26/J0609001.htm"
  "https://www.house.mn.gov/cco/journals/2025-26/J0317012.htm"
  "https://www.house.mn.gov/cco/journals/2025-26/J0323051.htm"
)

for URL in "${URLS[@]}"; do
  echo "--- PROCESSING $URL ---"
  ./scripts/audit_receipt_v1.sh "$URL" "$CLAIM" "US-MN-HOUSE"
done

echo "BATCH_COMPLETE"
