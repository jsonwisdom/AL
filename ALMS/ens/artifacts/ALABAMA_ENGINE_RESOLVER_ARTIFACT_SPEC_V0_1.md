# ALABAMA_ENGINE_RESOLVER_ARTIFACT_SPEC_V0_1

STATUS: RESOLVER_ARTIFACT_SPEC
TRUTH_STATE: YELLOW
AUTHORITY: FALSE
NO_FAKE_GREEN: TRUE

## PURPOSE

This file defines the minimum resolver evidence required before Alabama ALMS Engine may move from YELLOW to GREEN.

## GREEN IS BLOCKED UNTIL

A resolver artifact proves jaywisdom.base.eth contains:

- alms.packet.cid
- alms.packet.sha256
- alms.matrix.hash

## REQUIRED ARTIFACT FIELDS

- subject_name
- chain_id
- resolver_address_or_endpoint
- observed_at_utc
- block_number_or_resolution_epoch
- txt_records
- txt_records_sha256
- checker_output
- workflow_run_id
- no_fake_green

## GREEN RULE

GREEN requires byte-for-byte match between expected TXT records and observed resolver artifact.

No resolver artifact means no GREEN.
