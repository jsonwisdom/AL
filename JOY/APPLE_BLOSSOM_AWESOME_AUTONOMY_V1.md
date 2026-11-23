# AppleBlossomAwesome — Wisdom Helpers autonomy and advisory contract v1
Date: 2026-11-23
Status: DRAFT / ADVISORY DESIGN ONLY / AUTHORITY FALSE
Parent: JOY/HEIDI_WORKER_001.md
Track: JOY, not MN-DATA-BROKER-2026-11-23 (HOLD)

## Goal
Enable a bounded, user-initiated educational research loop without requiring Jay to hand-operate each source lookup. Keep meaningful human choices and family autonomy intact.

## Roles (labels are not human identities)
- HEIDI_WORKER_001: orchestrator of approved public-safe source lookup, classification, draft receipts and summaries; cannot impersonate Heidee.
- LeahPrime: advisory role to preserve unknowns, dissent, privacy and the right not to participate. No identity or person-specific access is implied.
- MaryDeeBot: advisory role for care, consent, family context and proportionality. A bot role, not a claim that MaryDee has consented or received tasks.
- quadOnionResults: four independently inspectable results, not four assumed live agents:
  1. SOURCE — exact public-safe evidence pointer and observation time.
  2. SAFETY — privacy/consent/boundary status and stop conditions.
  3. REPLAY — reproducible checks, differences and provenance.
  4. HUMAN — approval required or human-reviewed outcome; never auto-fabricate consent.
- Computer Wisdom: receipt verifier and feedback destination, not owner of HEIDEE.

## Allowed autonomous cycle
1. OBSERVE: user starts a bounded question; read permitted public sources.
2. ORIENT: librarian binds pointers; LeahPrime advisory checks unknowns and dissent; MaryDeeBot advisory checks care and consent.
3. DECIDE: select next *read-only* research step automatically, or HOLD if a boundary or missing evidence arises.
4. ACT: produce a local/draft source index and four-result bundle. No outside communications or state changes.
5. REPLAY: compare source hashes and result classifications; return summary to Computer Wisdom's draft JOY ledger and offer next student-directed question.

## Gates
- Automatic read-only analysis and draft creation: permitted by this design.
- Publishing, Cloudflare deployment, recording voice, personal-data retrieval, messages, payments, signatures, account changes, repository merge: require separately authorized human approval.
- Child/minor privacy: no profiles, private voice recordings or automatic identity binding.
- If any of the four results is absent, mark its state UNKNOWN and overall HOLD; do not invent a PASS.
- Neither a role name nor a receipt grants agency or authority.

## Quad result contract
```json
{
  "schema_version": "1.0.0",
  "receipt_type": "apple_blossom_quad_onion",
  "authority": false,
  "source": {"state": "UNKNOWN", "pointers": []},
  "safety": {"state": "HOLD", "consent": "NOT_INFERRED"},
  "replay": {"state": "NOT_TESTED", "hashes": []},
  "human": {"state": "AWAITING_APPROVAL", "approved_action": null},
  "result_state": "HOLD"
}
```

## Next engineering checks
- Unit tests: unknown source => HOLD; missing consent => HOLD; four-result presence != authority; unauthorized action => DENY.
- Integrate with existing JOY epistemic receipt schema using an explicit adapter; do not claim the quad object itself validates against that schema.
- Voice commands remain user-initiated, no ambient listening.
- Cloudflare runtime, live advisors and background agent orchestration: NOT ESTABLISHED.
