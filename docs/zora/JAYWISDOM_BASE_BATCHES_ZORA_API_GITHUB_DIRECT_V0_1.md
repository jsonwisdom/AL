# JAYWISDOM_BASE_BATCHES_ZORA_API_GITHUB_DIRECT_V0_1

## STATUS: COORDINATION_MAP
## AUTHORITY: FALSE
## NO_FAKE_GREEN: TRUE

This document maps the clean relationship between Base batches, Zora artifact discovery, GitHub Direct archiving, and the JAYWISDOM creator namespace.

It is a coordination map only. It does not claim a live Zora API fetch, a live Base RPC query, revenue, holder counts, or full artifact indexing.

## Core Surfaces

```text
base_batches=batch_receipt_layer
zora_api=read_only_discovery_layer_future_or_operator_supplied
github_direct=repo_archive_and_receipt_layer
jaywisdom=creator_profile_token_artifact_namespace
```

## JAYWISDOM Namespace

```text
profile=jaywisdom
x_handle=@JayWisdom12
primary_theme=Onchain systems / AI x crypto x civic infrastructure
visible_artifact_surface=screenshot_observed
full_catalog_indexed=false
seed_catalog_indexed=true
```

## Known Repo Indexes

```text
docs/zora/artifacts/jaywisdom_zora_artifact_index_seed_v0_1.jsonl
docs/zora/artifacts/README.md
tools/replay/query_jaywisdom_artifacts.py
docs/zora/JOY_ZORA_REPO_WIDE_INDEX_V0_1.md
docs/zora/JAYWISDOM_FIRST50_OPERATOR_EXECUTION_PACKET_V0_1.md
docs/zora/JAYWISDOM_TOKEN_AGENT_MANUAL_V0_1.md
```

## Base Batch Layer

Base batches should record groups of artifacts, receipts, or target records only after the underlying records are repo-visible.

```text
batch_input=repo_visible_records
batch_output=batch_manifest_or_receipt
batch_authority=false_until_replayed
chain_write=false_by_default
```

A Base batch may reference:

```text
artifact_index_record_ids
zora_urls
contract_addresses
transaction_hashes
screenshot_receipts
validator_outputs
sha256_hashes
```

But a Base batch must not upgrade:

```text
screenshot_to_revenue
zora_profile_to_full_catalog
transaction_hash_to_contract_verification
operator_report_to_independent_verification
```

## Zora API Layer

The Zora API layer, when used, must be read-only and must write raw or normalized results into repo fixtures before any higher-level claim.

Required output shape for future Zora ingestion:

```text
artifact_id
platform
profile
title
zora_url
contract_or_coin_address
network
created_or_observed_at
source
source_status
verification_status
notes
```

Allowed source statuses:

```text
screenshot_observed
operator_export
api_response
manual_entry
verified_url
```

Forbidden source statuses:

```text
assumed
inferred_as_fact
synthetic
placeholder
```

## GitHub Direct Layer

GitHub Direct is the archive/write surface.

```text
writes_docs=true
writes_fixtures=true
writes_scripts=true
writes_receipts=true
wallet_control=false
chain_write=false
api_execution_claim=false_unless_output_is_committed
```

Every GitHub Direct artifact should answer:

```text
what_is_claimed
what_is_source
what_is_not_verified
what_action_is_required_next
```

## Query Path

Local query for seed artifacts:

```bash
python3 tools/replay/query_jaywisdom_artifacts.py \
  --index docs/zora/artifacts/jaywisdom_zora_artifact_index_seed_v0_1.jsonl \
  --query receipts
```

Future full catalog query requires an actual export or API response committed to repo.

## Next Clean Step

```text
1. obtain Zora artifact export/API JSON/operator title list
2. normalize into JSONL records
3. commit raw source and normalized index
4. query locally
5. batch only repo-visible records
```

## Boundary

```text
full_zora_catalog_indexed=false
zora_api_fetch_performed=false
base_rpc_fetch_performed=false
base_batch_committed_by_this_file=false
revenue_confirmed=false
holder_count_independently_verified=false
market_value_independently_verified=false
chain_write=false
wallet_control=false
signing=false
broadcast=false
authority=false
no_fake_green=true
```

## Ruling

```text
COORDINATION_MAP = LANDED
BASE_BATCH_LAYER = DEFINED
ZORA_API_LAYER = READ_ONLY_PENDING_REAL_FEED
GITHUB_DIRECT_LAYER = ARCHIVE_ONLY
JAYWISDOM_NAMESPACE = QUERYABLE_BY_SEED_INDEX
FULL_CATALOG = NOT_INDEXED
REVENUE = NOT_CONFIRMED
AUTHORITY = FALSE
NO_FAKE_GREEN = TRUE
```
