# Goblin Court Metadata Fetcher v0 Patch

**Authority:** false | **Status:** PATCH_CANDIDATE  
**Target:** Zora ContentCoin (Base)  
**Test contract:** `0x4e3804e4e3328fea77cae22cbfc841655bec1cb7`

## Fix
Bytes input for keccak: `metadata_hash = "0x" + keccak(metadata_str.encode("utf-8")).hex()`

## ABI
Primary: `contractURI()` | Also: `name()`, `symbol()`, `decimals()`