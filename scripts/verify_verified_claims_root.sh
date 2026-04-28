#!/usr/bin/env bash
set -euo pipefail

MANIFEST="${1:-docs/verified-claims.json}"
ANCHOR="${ANCHOR:-docs/ipfs-anchor.txt}"
EXPECTED_ROOT="${EXPECTED_ROOT:-}"

command -v jq >/dev/null 2>&1 || { echo "VERIFY_ROOT_FAIL reason=missing_jq" >&2; exit 2; }
command -v sha256sum >/dev/null 2>&1 || { echo "VERIFY_ROOT_FAIL reason=missing_sha256sum" >&2; exit 2; }

tmp_manifest=""
cleanup() {
  if [ -n "$tmp_manifest" ] && [ -f "$tmp_manifest" ]; then rm -f "$tmp_manifest"; fi
}
trap cleanup EXIT

case "$MANIFEST" in
  http://*|https://*)
    if command -v curl >/dev/null 2>&1; then
      tmp_manifest="$(mktemp)"
      curl -fsSL "$MANIFEST" -o "$tmp_manifest"
      MANIFEST="$tmp_manifest"
    else
      echo "VERIFY_ROOT_FAIL reason=missing_curl_for_url" >&2
      exit 2
    fi
    ;;
esac

test -f "$MANIFEST" || { echo "VERIFY_ROOT_FAIL reason=missing_manifest path=$MANIFEST" >&2; exit 1; }

computed="$({
  jq -r '.claims[] | [.claim_id, .text_hash, .canonical_json] | @tsv' "$MANIFEST" | LC_ALL=C sort
} | sha256sum | awk '{print $1}')"
computed="sha256:$computed"

if [ -z "$EXPECTED_ROOT" ] && [ -f "$ANCHOR" ]; then
  EXPECTED_ROOT="$(awk -F': ' '/^merkle_root:/ {print $2}' "$ANCHOR" | tail -n 1)"
fi

if [ -z "$EXPECTED_ROOT" ]; then
  echo "VERIFY_ROOT_FAIL reason=missing_expected_root" >&2
  echo "computed_root=$computed" >&2
  exit 1
fi

if [ "$computed" != "$EXPECTED_ROOT" ]; then
  echo "VERIFY_ROOT_FAIL reason=root_mismatch expected=$EXPECTED_ROOT computed=$computed" >&2
  exit 1
fi

echo "VERIFY_ROOT_OK root=$computed manifest=$MANIFEST"
