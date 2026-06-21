#!/usr/bin/env bash
# Boss Bre Manifest Hash Populator v1.2
# Computes component sha256 values for the machine-readable review package manifest.
# Doctrine: NO_FAKE_GREEN. Missing files block population instead of inventing hashes.
set -euo pipefail

ROOT="$(git rev-parse --show-toplevel)"
MANIFEST="$ROOT/projects/mn-fiscal-replay/boss_bre/BOSS_BRE_MACHINE_READABLE_PACKAGE_MANIFEST_V1_1.json"
OUT="$ROOT/projects/mn-fiscal-replay/boss_bre/BOSS_BRE_MACHINE_READABLE_PACKAGE_MANIFEST_V1_1_POPULATED.json"
RECEIPT="$ROOT/projects/mn-fiscal-replay/boss_bre/BOSS_BRE_MANIFEST_HASH_POPULATOR_V1_2_RECEIPT.json"
UTC="$(date -u +%Y-%m-%dT%H:%M:%SZ)"

sha_file() {
  sha256sum "$1" | awk '{print "sha256:" $1}'
}

if [ ! -s "$MANIFEST" ]; then
  jq -n \
    --arg utc "$UTC" \
    '{artifact:"BOSS_BRE_MANIFEST_HASH_POPULATOR_V1_2_RECEIPT",version:"1.2",generated_utc:$utc,status:"POPULATE_BLOCKED",blocked_reason:"MANIFEST_MISSING",public_content_claim:"BLOCKED_PENDING_HUMAN_REVIEW",claim_status:"MANIFEST_HASH_POPULATOR_ONLY",human_review_required:true,no_fake_green:true}' \
    > "$RECEIPT"
  echo "POPULATE_BLOCKED: MANIFEST_MISSING"
  exit 0
fi

missing=""
while IFS= read -r path; do
  if [ ! -s "$ROOT/$path" ]; then
    missing="$missing $path"
  fi
done < <(jq -r '.components[].path' "$MANIFEST")

if [ -n "${missing// }" ]; then
  jq -n \
    --arg utc "$UTC" \
    --arg missing "$missing" \
    '{artifact:"BOSS_BRE_MANIFEST_HASH_POPULATOR_V1_2_RECEIPT",version:"1.2",generated_utc:$utc,status:"POPULATE_BLOCKED",blocked_reason:"COMPONENT_FILE_MISSING",missing_paths:$missing,public_content_claim:"BLOCKED_PENDING_HUMAN_REVIEW",claim_status:"MANIFEST_HASH_POPULATOR_ONLY",human_review_required:true,no_fake_green:true}' \
    > "$RECEIPT"
  echo "POPULATE_BLOCKED: COMPONENT_FILE_MISSING"
  echo "$missing"
  exit 0
fi

tmp="$OUT.tmp"
cp "$MANIFEST" "$tmp"

count="$(jq '.components | length' "$tmp")"
for i in $(seq 0 $((count - 1))); do
  path="$(jq -r ".components[$i].path" "$tmp")"
  sha="$(sha_file "$ROOT/$path")"
  jq --arg sha "$sha" ".components[$i].sha256 = \$sha" "$tmp" > "$tmp.next"
  mv "$tmp.next" "$tmp"
  echo "HASHED $path $sha"
done

component_hashes="$(jq -r '.components[] | [.component,.version,.path,.commit_ref,.sha256] | @tsv' "$tmp")"
full_package_sha="sha256:$(printf '%s\n' "$component_hashes" | sha256sum | awk '{print $1}')"
manifest_id="boss-bre-package-$(date -u +%Y%m%dT%H%M%SZ)"

jq \
  --arg manifest_id "$manifest_id" \
  --arg utc "$UTC" \
  --arg status "POPULATED" \
  --arg package_version "1.2" \
  --arg full_sha "$full_package_sha" \
  '.manifest_id=$manifest_id | .release_utc=$utc | .manifest_status=$status | .package_version=$package_version | .full_package_sha256=$full_sha' \
  "$tmp" > "$OUT"
rm -f "$tmp"

out_sha="$(sha_file "$OUT")"

jq -n \
  --arg utc "$UTC" \
  --arg manifest_path "${MANIFEST#$ROOT/}" \
  --arg output_path "${OUT#$ROOT/}" \
  --arg output_sha "$out_sha" \
  --arg full_sha "$full_package_sha" \
  --argjson component_count "$count" \
  '{artifact:"BOSS_BRE_MANIFEST_HASH_POPULATOR_V1_2_RECEIPT",version:"1.2",generated_utc:$utc,status:"POPULATE_COMPLETE",manifest_template_path:$manifest_path,populated_manifest_path:$output_path,populated_manifest_sha256:$output_sha,full_package_sha256:$full_sha,component_count:$component_count,public_content_claim:"BLOCKED_PENDING_HUMAN_REVIEW",claim_status:"MANIFEST_HASH_POPULATOR_ONLY",human_review_required:true,no_fake_green:true}' \
  > "$RECEIPT"

echo "POPULATE_COMPLETE"
echo "populated_manifest=$OUT"
echo "populated_manifest_sha256=$out_sha"
echo "full_package_sha256=$full_package_sha"
echo "receipt=$RECEIPT"
echo "NO_FAKE_GREEN=ACTIVE"
