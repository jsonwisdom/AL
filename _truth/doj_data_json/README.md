# DOJ Data Pipeline: data.json

**Status:** Operational Lane (Active)
**Repository:** jsonwisdom/AL

## Objective

Establish a persistent, hash-verified archive of the DOJ public `data.json` registry.

## Schema

All captured data points must conform to the manifest schema located at:

`_truth/doj_data_json/manifests/manifest.schema.json`

## Linkage

- Upstream: DOJ federal registry (`https://www.justice.gov/data.json`)
- Downstream: COMPUTERWISDOM cross-reference and policy analysis lanes
- Security: SHA256 receipt generation required for every ingest
- Authority: false

## Verification Membrane

Capture != Interpretation

A successful ingest proves only that bytes were captured and hashed.
No policy, legal, investigative, or factual conclusion is implied by capture alone.
