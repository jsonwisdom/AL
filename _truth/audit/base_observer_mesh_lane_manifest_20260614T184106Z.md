# Base Observer Mesh Lane Manifest

Timestamp UTC: 20260614T184106Z
Repo: jsonwisdom/AL
Branch: master
Head: 75becfdd2a6250006f2cd52964b336f3c1b0cc94

## Intent

Promote only bounded Base observer mesh artifacts.

## Include Candidates

- _truth/base/
- _truth/base_mesh/
- site/convergence.json
- site/cpv-prev.json
- site/nitro-feed.json
- site/systemconfig-mainnet.json
- site/systemconfig-sepolia.json
- site/unified-mesh.json

## Exclude

- _secrets/
- _quarantine/
- tools/
- ALMS/hunts/
- _truth/logs/
- _truth/detect/
- _truth/doj_data_json/

## Rule

No bulk ingestion. No secrets. Bounded mesh only.
