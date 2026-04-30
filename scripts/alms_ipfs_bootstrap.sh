#!/usr/bin/env bash
# ALMS IPFS Bootstrap Helper
# Installs kubo/ipfs into user-local bin when ipfs is missing.

set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

mkdir -p "$HOME/.local/bin" "$HOME/.local/src"

if command -v ipfs >/dev/null 2>&1; then
  echo "ALMS_IPFS_READY path=$(command -v ipfs)"
  exit 0
fi

ARCHIVE="$HOME/.local/src/kubo_linux-amd64.tar.gz"
URL="https://dist.ipfs.tech/kubo/latest/kubo_linux-amd64.tar.gz"

curl -L "$URL" -o "$ARCHIVE"
tar -xzf "$ARCHIVE" -C "$HOME/.local/src"
cp "$HOME/.local/src/kubo/ipfs" "$HOME/.local/bin/ipfs"
chmod +x "$HOME/.local/bin/ipfs"

export PATH="$HOME/.local/bin:$PATH"

if [[ ! -d "$HOME/.ipfs" ]]; then
  ipfs init --profile=server >/dev/null
fi

echo "ALMS_IPFS_INSTALLED path=$HOME/.local/bin/ipfs"
echo "NEXT: export PATH=\"$HOME/.local/bin:\$PATH\""
