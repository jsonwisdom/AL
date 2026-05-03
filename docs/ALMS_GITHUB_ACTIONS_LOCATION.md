# ALMS GitHub Actions Location

Status: NAVIGATION_RECEIPT

The active GitHub Actions workflow for Jay's AL repo is in:

```text
jsonwisdom/AL
```

Default branch:

```text
master
```

Workflow file:

```text
.github/workflows/alms-github-direct-anchor.yml
```

Actions page:

```text
https://github.com/jsonwisdom/AL/actions
```

Important correction:

```text
Do not look in jsonwisdom/layered-proofing-state-level-alms for the AL repo workflow.
That was the experimental scaffold repo.
The Jay Cloud Shell repo folder named AL maps to jsonwisdom/AL on branch master.
```

Current workflow behavior:

- Runs manually via workflow_dispatch.
- Runs on pushes touching anchor/docs/fixtures/scripts paths.
- Records GitHub Direct anchor runtime state.
- Does not claim Base/EAS/ENS anchoring.

Allowed label:

```text
GITHUB_ANCHORED_ONLY
```

Blocked labels:

```text
ANCHORED_ON_BASE
EAS_ATTESTED
ENS_COMPLETE
VERIFIED_NATIONAL_ROOT
ONCHAIN_CONFIRMED
```
