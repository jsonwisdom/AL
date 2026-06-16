# CIPHER_COURT_LAB_OUTREACH_EMAIL_TEMPLATE_V1

Status: `SEND_READY`
Related:
- `docs/research/CIPHER_COURT_LAB_OUTREACH_PACKET_V1.md`
- `docs/research/CIPHER_COURT_RESEARCH_PARTNERSHIP_PROSPECTUS_V1.md`
- `docs/research/CIPHER_COURT_SCAM_SUSCEPTIBILITY_PREREGISTRATION_V1.md`
- `schemas/cipher_court/telemetry_v1.schema.json`
- `CITATION.cff`

## Subject

Open calibration instrument for phishing/scam susceptibility research

## Email Template

Hello [Name],

I’m reaching out because your work on [phishing / scam susceptibility / judgment under uncertainty / calibration / adversarial decision-making] appears closely aligned with a research instrument I’m developing called Cipher Court.

Cipher Court is an open measurement protocol and playable calibration intervention for studying how humans become confidently wrong under adversarial evidence.

The core question is:

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

What is already available:

- open telemetry schema
- privacy-aware aggregation rules
- preregistration scaffold
- scam/phishing transfer-study scaffold
- research partnership prospectus
- citation metadata

Repository:

```text
https://github.com/jsonwisdom/AL
```

Key files:

```text
schemas/cipher_court/telemetry_v1.schema.json
docs/research/CIPHER_COURT_SCAM_SUSCEPTIBILITY_PREREGISTRATION_V1.md
docs/research/CIPHER_COURT_AGGREGATION_AND_PRIVACY_V1.md
docs/research/CIPHER_COURT_RESEARCH_PARTNERSHIP_PROSPECTUS_V1.md
CITATION.cff
```

The measurement layer is open by design. A partner lab would bring IRB / ethics review, participant recruitment, scam/phishing battery expertise, and statistical analysis support. Cipher Court provides the instrument, protocol, schema, and replay-governed intervention design.

Core boundary:

```text
CONFIDENCE != VERDICT
REPLAY_PASS = VERDICT
TELEMETRY_MUST_NOT_OVERRIDE_REPLAY
```

Would you be open to a short discovery call to evaluate whether this instrument could support your lab’s work?

Best,
Jay Wisdom
jaywisdom.base.eth
https://github.com/jsonwisdom/AL

## Tracking Rule

After sending, update Issue #138 with:

```text
[LAB]
STATUS: CONTACTED
CONTACT_DATE: YYYY-MM-DD
INTEREST_LEVEL: UNKNOWN
IRB_CAPACITY: UNKNOWN
SCAM_BATTERY_AVAILABLE: UNKNOWN
NOTES: Initial outreach sent using CIPHER_COURT_LAB_OUTREACH_EMAIL_TEMPLATE_V1.
NEXT_ACTION: Await reply / follow up in 7 days.
```
