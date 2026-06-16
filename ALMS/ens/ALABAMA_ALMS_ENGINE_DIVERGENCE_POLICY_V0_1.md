# ALABAMA_ALMS_ENGINE_DIVERGENCE_POLICY_V0_1

STATUS: CANDIDATE_POLICY
TRUTH_STATE: YELLOW
AUTHORITY: FALSE
NO_FAKE_GREEN: TRUE

## ROLE SPLIT

jaywisdom.eth = SEAL
jaywisdom.base.eth = ENGINE

The Engine is not required to remain a dumb clone of the Seal forever.
The checker must preserve integrity while recognizing explained divergence.

## STATE MODEL

MISSING_AND_UNEXPLAINED = RED
MISSING_WITH_PENDING_UPDATE_RECEIPT = YELLOW
BYTE_MATCH_WITH_RESOLVER_ARTIFACT = GREEN

## WORKFLOW BEHAVIOR

1. If required TXT is missing and no pending_update receipt exists:
   - FAIL workflow
   - state = RED

2. If required TXT is missing but a valid pending_update receipt exists:
   - WARN workflow
   - state = YELLOW
   - correction_window = 72h

3. If required TXT matches byte-for-byte against resolver artifact:
   - PASS workflow
   - state = GREEN

4. If correction window expires without repair:
   - FAIL workflow
   - state = RED_EXPIRED

## PENDING UPDATE RECEIPT MUST CONTAIN

- subject_name
- missing_record
- expected_value_hash
- reason
- opened_at_utc
- expires_at_utc
- controller
- signature_or_commit_sha
- no_fake_green = true

## CHALLENGE RECEIPT MUST CONTAIN

- challenger
- subject_name
- challenged_record
- observed_value
- expected_value_hash
- evidence_url_or_commit
- opened_at_utc
- requested_resolution
- no_fake_green = true

## CIVIC-GRADE MINIMUM

A civic-grade version requires:
- public repo receipt
- deterministic checker
- time-bounded correction
- challenge receipt lane
- no automatic promotion from YELLOW to GREEN
- byte match required for GREEN
