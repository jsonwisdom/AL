# Goblin Court Metadata Fetcher v0 Patch

Authority: false  
Status: PATCH_CANDIDATE  
Target: Zora ContentCoin on Base  
Test contract: `0x4e3804e4e3328fea77cae22cbfc841655bec1cb7`

## Fix

Use bytes input for keccak:

```python
metadata_bytes = metadata_str.encode("utf-8")
metadata_hash = "0x" + keccak(metadata_bytes).hex()
```

## ABI Requirement

Primary method: `contractURI()`  
Also required: `name()`, `symbol()`, `decimals()`

## Acquisition Rule