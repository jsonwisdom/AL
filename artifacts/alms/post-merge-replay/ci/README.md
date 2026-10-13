# CI

Reserved for the dispatchable post-merge replay workflow and its strict gate wiring.

Requirements:

- checkout the exact requested replay SHA
- fail on every required gate failure
- no `|| true` on constitutional checks
- no synthetic or hard-coded GREEN verdict
- upload the CRO receipt even when RED, where technically possible
- attach the final status to the replay root

No workflow is implemented yet.
