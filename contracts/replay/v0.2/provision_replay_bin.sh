#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../../.." && pwd)"
SRC="${ROOT}/contracts/replay/v0.2/replay-bin"
DEST_DIR="/usr/local/alms/bin"
DEST="${DEST_DIR}/replay-bin"

if [[ ! -f "${SRC}" ]]; then
  echo "REPLAY_PROVISION_FAILED: source replay-bin missing" >&2
  exit 1
fi

mkdir -p "${DEST_DIR}"
cp "${SRC}" "${DEST}"
chmod 0755 "${DEST}"

echo "REPLAY_BIN_PROVISIONED ${DEST}"
