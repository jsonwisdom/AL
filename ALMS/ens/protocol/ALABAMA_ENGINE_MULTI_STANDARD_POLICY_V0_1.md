# ALABAMA_ENGINE_MULTI_STANDARD_POLICY_V0_1

STATUS: MULTI_STANDARD_POLICY
TRUTH_STATE: YELLOW
AUTHORITY: FALSE
NO_FAKE_GREEN: TRUE

## PURPOSE

This policy separates creative, social, settlement, and verification standards.

Not every layer requires the same proof threshold.

## STANDARD STACK

### GOBLIN STANDARDS

Goblin Standards govern creative iteration, adversarial humor, stress testing, and build momentum.

- 89% match may continue building
- suggestions remain open
- jokes are allowed
- chaos is allowed
- GREEN is not allowed from Goblin evidence alone

RULING:

GOBLIN_MATCH_89 = BUILD_CONTINUATION_ALLOWED

### ZORA STANDARDS

Zora Standards govern public cultural artifacts, drops, editions, attribution, and provenance signaling.

- artifact should be public
- creator identity should be visible
- receipt link should be included when possible
- no claim of verification unless backed by Jay Standards

RULING:

ZORA_PUBLIC_ARTIFACT = CULTURAL_PROOF
ZORA_PUBLIC_ARTIFACT != VERIFICATION

### BASE STANDARDS

Base Standards govern settlement, transaction records, Basename identity, and chain evidence.

- tx hash matters
- address matters
- resolver state matters
- timestamp/block evidence matters
- missing resolver records block GREEN

RULING:

BASE_SETTLEMENT = OBSERVED_EVIDENCE
BASE_SETTLEMENT != FINAL_AUTHORITY

### JAY STANDARDS

Jay Standards govern truth promotion.

- verification over narrative
- receipts decide reality
- no source, no score
- no resolver match, no GREEN
- no workflow observation, no workflow claim
- no fake green

RULING:

JAY_GREEN = 100_PERCENT_MATCH_REQUIRED

## MATCH POLICY

100_PERCENT_MATCH = GREEN

89_TO_99_PERCENT_MATCH = YELLOW_CONTINUE

BELOW_89_PERCENT_MATCH = RED_REVIEW

## FINAL RULING

Goblin Standards allow play.
Zora Standards allow public culture.
Base Standards allow settlement evidence.
Jay Standards decide truth promotion.

89% keeps the build alive.

100% is required for GREEN.

NO_FAKE_GREEN remains active.
