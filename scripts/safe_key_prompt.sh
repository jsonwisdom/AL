#!/usr/bin/env bash
set -euo pipefail

echo "SAFE_KEY_PROMPT_V1"
echo "Paste private key only after the hidden prompt appears."
echo "Nothing will print while typing."
read -s -p "PRIVATE_KEY: " PRIVATE_KEY
echo
export PRIVATE_KEY
echo "PRIVATE_KEY_LOADED_IN_MEMORY_ONLY"
