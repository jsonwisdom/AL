# CIPHER_COURT_LAB_OUTREACH_PACKET_V1

Status: `OUTREACH_READY`
Related:
- `docs/research/CIPHER_COURT_RESEARCH_PARTNERSHIP_PROSPECTUS_V1.md`
- `docs/research/CIPHER_COURT_SCAM_SUSCEPTIBILITY_PREREGISTRATION_V1.md`
- `schemas/cipher_court/telemetry_v1.schema.json`
- `CITATION.cff`

## Purpose

Provide a short, sendable research outreach packet for labs studying phishing, fraud susceptibility, judgment under uncertainty, calibration, or adversarial decision-making.

## Subject Line

Open calibration instrument for phishing/scam susceptibility research

## Short Email

Hello,

I am developing Cipher Court, an open measurement protocol and playable calibration instrument for studying how humans become confidently wrong under adversarial evidence.

The protocol includes:

- an open telemetry schema for calibration and replay outcomes
- an adaptive adversarial training condition
- a fixed-noise control condition
- a preregistered scam/phishing susceptibility transfer study scaffold
- privacy-aware aggregation rules
- citation metadata for replication

The core research question is:

```text
Does personalized adversarial evidence produce faster recalibration than fixed-difficulty training?
```

The proposed study is straightforward:

```text
N = 200 participants
PRE_TEST = standardized scam / phishing susceptibility battery
INTERVENTION = 10 hours Cipher Court training
POST_TEST = standardized scam / phishing susceptibility battery
GROUPS = adaptive Noise Agent vs fixed-difficulty Noise Agent
```

The measurement layer is open so independent labs can replicate, challenge, or pool results without depending on a proprietary oracle.

Repository:

```text
https://github.com/jsonwisdom/AL
```

Relevant files:

```text
schemas/cipher_court/telemetry_v1.schema.json
docs/research/CIPHER_COURT_SCAM_SUSCEPTIBILITY_PREREGISTRATION_V1.md
docs/research/CIPHER_COURT_AGGREGATION_AND_PRIVACY_V1.md
docs/research/CIPHER_COURT_RESEARCH_PARTNERSHIP_PROSPECTUS_V1.md
CITATION.cff
```

I am looking for a research partner with IRB capacity, participant recruitment, scam/phishing assessment experience, and statistical expertise for mixed-effects modeling.

Would you be open to a brief discussion about whether this instrument could support your lab's work?

Best,
Jay Wisdom
jaywisdom.base.eth

## Partner Fit Checklist

Ideal partner has at least one:

- phishing / scam susceptibility research experience
- judgment and decision-making lab infrastructure
- cognitive security research portfolio
- older-adult fraud prevention work
- intelligence or analyst-training calibration work
- medical / diagnostic calibration expertise

Required capacity:

- IRB or ethics pathway
- participant recruitment
- pre/post assessment battery
- statistical analysis support

## Partnership Boundary

Cipher Court provides the instrument and open schema.

Partner lab provides human subjects infrastructure and scientific review.

```text
YOU_BUILD_THE_EPISTEMIC_ENGINE
THEY_RUN_THE_HUMAN_EXPERIMENTS
```

## Replay Sovereignty

No confidence score, persuasive framing, telemetry trend, or role consensus may override replay.

```text
CONFIDENCE != VERDICT
REPLAY_PASS = VERDICT
TELEMETRY_MUST_NOT_OVERRIDE_REPLAY
```
