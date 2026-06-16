# MN Receipt Lane Manifest

Timestamp UTC: 20260614T183411Z
Repo: jsonwisdom/AL
Branch: master
Head: 845715bfb025bc166fd1ec238563429922a6c39c

Intent: Promote only Minnesota civic receipt artifacts.

Include:
- _truth/mn/
- _sources/MN_001/
- _sources/MN_002/
- _truth/cards/MN_002.card.json
- _truth/receipts/MN_002.json

Exclude:
- _secrets/
- _quarantine/
- tools/al-verifier/target/
- ALMS/hunts/
- Base observer mesh
- Leaf006 replay lane
- DOJ raw bulk snapshots

Rule: No bulk ingestion. No secrets. No fake green.
