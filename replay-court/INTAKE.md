# Replay Court Intake

Submit claims, agent runs, workflows, governance statements, or AI outputs for adversarial replay and constitutional audit.

We do not sell confidence.
We test whether reasoning survives replay.

## Submission Guidelines

- Provide enough context and artifacts for independent replay.
- Submissions are public by default unless explicitly marked sensitive with justification.
- Verification is replay-first.
- Any optional payment, tip, or settlement is downstream ratification only.
- Tips support the work. They do not create truth.

## Intake Fields

### Submission ID

```text
<GitHub issue number, UUID, or auto-generated identifier>
```

### Submitter

```text
<handle / ENS / public key / organization>
```

### Claim / Question

One sentence.

```text
Example: The agent correctly determined X based on prompt Y.
```

### Full Prompt / Input

```text
<paste prompt, task, workflow, or link to receipt>
```

### Agent Output / Claimed Result

```text
<paste output or attach receipt/artifact link>
```

### Supporting Artifacts

Add any available:

```text
- continuity receipts
- replay receipts
- oath JSON
- verifier output
- model/version metadata
- commit hash
- runtime environment details
- screenshots
- prior replay attempts
- public URLs
```

### Specific Verification Targets

Check all that apply:

```text
[ ] drift / hallucination
[ ] continuity break
[ ] authority creep
[ ] unverifiable assumption
[ ] replay fidelity
[ ] boundary compliance
[ ] settlement / payment confusion
[ ] legal or governance clarity
[ ] other: <describe>
```

### Desired Output Format

```text
[ ] Standard Replay Court report
[ ] Full forensic receipt chain
[ ] Dashboard summary
[ ] Public postmortem
[ ] Zora collectible-ready report
[ ] Other: <describe>
```

### Confidentiality Note

```text
Public by default.
If limited handling is requested, explain why and identify which artifacts should not be public.
```

## Submission Methods

```text
1. Open a GitHub issue in this repo using this template.
2. Include public artifact links whenever possible.
3. Optional: tip/support jaywisdom.base.eth with the issue link.
4. Future: direct Wisdom API / x402 endpoint.
```

## What You Receive

```text
- route used
- level score
- replay verdict
- drift findings
- UNOBSERVED / FAIL distinction
- boundary analysis
- receipt and oath references when available
- recommended next action
```

## Doctrine Reminder

```text
No witness, no claim.
No receipt, no ratification.
No replay, no legitimacy.
Replay before settlement.
Payment never rewrites reality.
```
