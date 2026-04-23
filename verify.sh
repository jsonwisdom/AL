#!/usr/bin/env bash
set -euo pipefail
INPUT="${1:-}"
HASH_BASH="$(printf "%s" "$INPUT" | sha256sum | cut -d' ' -f1)"
[[ ${#HASH_BASH} -eq 64 ]] || { echo "FAIL: length" >&2; exit 1; }
HASH_NODE="$(node -e "console.log(require('crypto').createHash('sha256').update(process.argv[1]).digest('hex'))" "$INPUT")"
[[ "$HASH_BASH" == "$HASH_NODE" ]] || { echo "FAIL: mismatch" >&2; exit 1; }
printf '{"hash":"%s","len":%s,"ts":"%s"}\n' "$HASH_BASH" "${#HASH_BASH}" "$(date -u +%FT%TZ)"
