#!/usr/bin/env bash
set -euo pipefail

mkdir -p site

if [ -f "_truth/base/nitro_observer_feed.json" ]; then
  cp "_truth/base/nitro_observer_feed.json" "site/nitro-feed.json"
  date -u +"%FT%TZ FEED_EXPORTED" >> site/feed.log
else
  date -u +"%FT%TZ ERROR live feed missing" >> site/feed.log
  exit 1
fi
