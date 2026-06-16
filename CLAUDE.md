STATUS: ACTIVE

# AL Claude Guardrails

This repository uses AI assistance only as a soft workflow scaffold.

Prompt rules reduce drift and make failure easier to detect. They do not prove truth, complete verification, create anchors, or replace deterministic checks.

## Core boundaries

- Do not invent commit hashes, transaction hashes, contract addresses, attestations, command output, or file hashes.
- Do not claim a receipt, anchor, settlement, schema freeze, or verification is complete unless a visible artifact proves it.
- If evidence is missing, classify the result as `NEEDS_SOURCE`.
- Treat schemas, canonicalization, hashing, git lineage, and external witnesses as separate evidence layers.
