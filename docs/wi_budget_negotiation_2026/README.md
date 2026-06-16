# WI_BUDGET_NEGOTIATION_2026 Receipt Machine

Status: PACKAGE_READY_FOR_OPERATOR_PDF

This package captures only operator-provided local PDF bytes.

## Boundaries

- No autonomous fetch
- No news hashing for canon
- No social-media hashing for canon
- No legal inference at intake
- No anchoring until enacted canonical text is operator-verified

## State Path

1. AWAITING_PRIMARY_ARTIFACT_UPLOAD
2. ARTIFACT_BYTES_RECEIVED
3. ARTIFACT_ROLE_ASSIGNED
4. TEXT_HASH_VERIFIED
5. ANCHOR_READY

## Valid Artifact Roles

- governor_press_release_pdf
- special_session_order_pdf
- lfb_fiscal_memo_pdf
- enrolled_bill_text_pdf
- unknown

Default role: unknown.
