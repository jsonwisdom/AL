# Metadata Fetcher v0 Rules

**Authority:** false | **Status:** RULES_CANDIDATE

## Acquisition
Prefer on-chain `contractURI()`. If cached -> `acquisition_class: CACHED_SOURCE`

## Verification
Snapshot + hash before promotion.

## Next
Run fetcher -> capture stdout -> store JSON -> replay hash.
