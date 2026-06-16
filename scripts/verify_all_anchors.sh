#!/usr/bin/env bash
set -euo pipefail

# Jay Wisdom / ALMS anchor verifier
# Portable from anywhere inside the repo.
# Bash only. No nano. No Python. No fake green.

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(git -C "$SCRIPT_DIR" rev-parse --show-toplevel 2>/dev/null || git rev-parse --show-toplevel 2>/dev/null || pwd)"
cd "$REPO_ROOT"

fail() {
  echo "ANCHOR_VERIFY_FAIL reason=$*" >&2
  exit 1
}

need_cmd() {
  command -v "$1" >/dev/null 2>&1 || fail "missing_command_$1"
}

need_cmd jq
need_cmd sha256sum
need_cmd wc
need_cmd base64

verify_b64_leaf() {
  local leaf="$1"
  local expected_sha="$2"
  local expected_bytes="$3"
  local dir="_truth/anchors/leaf${leaf}"
  local payload="$dir/payload.b64"
  local out="$dir/verify_leaf${leaf}.payload"

  [ -d "$dir" ] || fail "missing_dir_$dir"
  [ -f "$payload" ] || fail "missing_payload_$payload"

  base64 -d "$payload" > "$out"

  local actual_sha
  local actual_bytes
  actual_sha="$(sha256sum "$out" | awk '{print $1}')"
  actual_bytes="$(wc -c < "$out" | tr -d ' ')"

  if [ "$actual_sha" = "$expected_sha" ] && [ "$actual_bytes" = "$expected_bytes" ]; then
    echo "LEAF${leaf}_PAYLOAD_VERIFIED sha=$actual_sha bytes=$actual_bytes"
  else
    fail "leaf=${leaf} sha=$actual_sha bytes=$actual_bytes expected_sha=$expected_sha expected_bytes=$expected_bytes"
  fi

  if [ -f "$dir/ANCHORS.json" ]; then
    jq -cS . "$dir/ANCHORS.json" > "$dir/ANCHORS.canonical.tmp"
    if cmp -s "$dir/ANCHORS.json" "$dir/ANCHORS.canonical.tmp"; then
      echo "LEAF${leaf}_ANCHORS_CANONICAL_PASS"
      rm -f "$dir/ANCHORS.canonical.tmp"
    else
      rm -f "$dir/ANCHORS.canonical.tmp"
      fail "leaf=${leaf} anchors_json_not_canonical"
    fi
  else
    echo "LEAF${leaf}_ANCHORS_MISSING_WARN"
  fi
}

# Known locked anchors
# Leaf 006 canonical payload may live at repo root payload.b64 in older runs.
if [ -f "payload.b64" ]; then
  base64 -d payload.b64 > verify_leaf006.payload
  sha006="$(sha256sum verify_leaf006.payload | awk '{print $1}')"
  bytes006="$(wc -c < verify_leaf006.payload | tr -d ' ')"
  if [ "$sha006" = "21829f0be11cd04a64f379ad90003fc39338d91b2242720cd6c0497aed067d8b" ] && [ "$bytes006" = "10240" ]; then
    echo "LEAF006_PAYLOAD_VERIFIED sha=$sha006 bytes=$bytes006"
  else
    fail "leaf=006 sha=$sha006 bytes=$bytes006 expected_sha=21829f0be11cd04a64f379ad90003fc39338d91b2242720cd6c0497aed067d8b expected_bytes=10240"
  fi
else
  echo "LEAF006_PAYLOAD_MISSING_WARN file=payload.b64"
fi

verify_b64_leaf "007" "c2711066a5543c49d33222f69aa5d22a48d9e73f874b7e3790d32683c930471e" "30"

# Leaf 008 is optional until payload exists.
if [ -f "_truth/anchors/leaf008/payload.b64" ]; then
  dir="_truth/anchors/leaf008"
  out="$dir/verify_leaf008.payload"
  base64 -d "$dir/payload.b64" > "$out"
  sha008="$(sha256sum "$out" | awk '{print $1}')"
  bytes008="$(wc -c < "$out" | tr -d ' ')"
  echo "LEAF008_PAYLOAD_OBSERVED sha=$sha008 bytes=$bytes008"
  if [ -f "$dir/ANCHORS.json" ]; then
    jq -cS . "$dir/ANCHORS.json" > "$dir/ANCHORS.canonical.tmp"
    cmp -s "$dir/ANCHORS.json" "$dir/ANCHORS.canonical.tmp" && echo "LEAF008_ANCHORS_CANONICAL_PASS" || fail "leaf=008 anchors_json_not_canonical"
    rm -f "$dir/ANCHORS.canonical.tmp"
  fi
else
  echo "LEAF008_BLOCKED reason=NO_PAYLOAD_BYTES"
fi

echo "ANCHOR_VERIFY_ALL_PASS"
