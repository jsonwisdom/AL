# Jay Wisdom Zora Artifact Index

## Status

Seed index only.

This folder makes visible Jay Wisdom Zora artifacts queryable from repository text files.

## Current Index

```text
jaywisdom_zora_artifact_index_seed_v0_1.jsonl
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
