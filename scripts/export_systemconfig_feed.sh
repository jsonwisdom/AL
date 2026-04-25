#!/usr/bin/env bash
set -euo pipefail

mkdir -p site

if [ -f "_truth/base_mesh/systemconfig_ethereum-mainnet.json" ]; then
  cp "_truth/base_mesh/systemconfig_ethereum-mainnet.json" "site/systemconfig-mainnet.json"
fi

if [ -f "_truth/base_mesh/systemconfig_ethereum-sepolia.json" ]; then
  cp "_truth/base_mesh/systemconfig_ethereum-sepolia.json" "site/systemconfig-sepolia.json"
fi

date -u +"%FT%TZ SYSTEMCONFIG_FEED_EXPORTED" >> site/feed.log
