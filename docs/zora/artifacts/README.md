# Jay Wisdom Zora Artifact Index

## Status

Seed index only.

This folder makes visible Jay Wisdom Zora artifacts queryable from repository text files.

## Current Gap

```text
zora_profile=jaywisdom
screenshot_observed_posts=approximately_1000
repo_manifest_indexed_artifacts=6
full_catalog_indexed=false
assistant_live_zora_fetch=false
```

The Zora profile surface appears much larger than the current repo index. The repo currently indexes only artifacts with visible screenshot evidence or explicit provided metadata.

## Current Files

```text
jaywisdom_zora_artifact_index_seed_v0_1.jsonl
jaywisdom_zora_artifact_manifest_v0_1.csv
```

## Query Tool

```bash
python3 tools/replay/query_jaywisdom_artifacts.py \
  --index docs/zora/artifacts/jaywisdom_zora_artifact_index_seed_v0_1.jsonl \
  --query receipts
```

For JSON output:

```bash
python3 tools/replay/query_jaywisdom_artifacts.py \
  --query receipts \
  --json
```

## Boundary

```text
source=operator_screenshot
profile_posts_count=screenshot_observed_only
manifest_rows=6
full_catalog=false
zora_api_fetch=false
chain_call=false
wallet_control=false
revenue_confirmed=false
authority=false
no_fake_green=true
```

## Upgrade Path

To index the full profile, add records from one of:

```text
operator CSV export
Zora API JSON
manual title list
screenshots with visible titles
verified artifact URLs
```

Each record should remain explicit about source and verification status.

## Ruling

```text
VISIBLE_PROFILE_COUNT = APPROXIMATELY_1000_SCREENSHOT_OBSERVED
QUERYABLE_REPO_MANIFEST = 6_SEED_ARTIFACTS
FULL_CATALOG_INDEXED = FALSE
NO_FAKE_GREEN = TRUE
```
