# Cleansing Gate v0.1

## Purpose
The Cleansing Gate is a proposed offline export-control boundary. Implementation and enforcement are pending. When implemented, it is intended to mediate outbound Gray Baby media exports while preserving parent control, minimizing metadata disclosure, and failing closed when required checks are unavailable.

## Locked Invariants

| Property | Value |
| :--- | :--- |
| NETWORK_ACCESS_DURING_CLEANSING | FALSE |
| SOURCE_FILE_MUTATION | FALSE |
| PUBLIC_EXPORT_DEFAULT | FALSE |
| PARENT_SIGNATURE_REQUIRED | TRUE |
| TELEMETRY_EMISSION | ZERO |
| STEGO_POLICY | REJECT_IF_DETECTED_OR_UNSUPPORTED |
| RESIDUAL_DISCLOSURE_RISK | NONZERO |
| AUTHORITY | FALSE |

## Rules

1. **No Fingerprinting**: Device identifiers and non-essential application markers must not be retained in exported artifacts.
2. **Temporal Neutrality**: Source EXIF and source-derived temporal metadata must be removed. A normalized filename may contain export time only.
3. **Telemetry Purge**: Behavioral logs, interaction history, analytics identifiers, and rendering telemetry must not cross the export boundary.
4. **Parent Approval Requirement**: Every export request must conform to `PARENT_EXPORT_APPROVAL_V0_1.schema.json` and pass runtime signature verification.
5. **Source Preservation**: Cleansing must operate on a copy in an isolated temporary workspace and must not mutate the source file.
6. **Fail-Closed Steganography Policy**: Export must be rejected when a steganographic payload is detected, when inspection is unsupported, or when inspection is inconclusive.
7. **Network Isolation**: Any network activity during cleansing is a hard failure.
8. **No Fake Green**: Missing implementation, missing fixtures, unsupported inspection, or failed validation must never return a successful test status.

## Runtime Validation Requirements

JSON Schema Draft-07 cannot express all cross-field and cryptographic requirements. Runtime validation must additionally enforce:

- `expires_at` is later than `issued_at`.
- The approval validity window is no greater than five minutes.
- `session_id` and `nonce` have not previously been consumed.
- The Ed25519 signature verifies over the JCS-canonicalized descriptor with `parent_signature` excluded.
- `signing_key_id` matches the SHA-256 digest of the authorized public key.
- Input, preview, and output hashes match the observed artifacts.
- The export destination is unchanged after approval.
- The normalized filename reflects export time only and includes a random collision-resistant suffix.

## Status

`SPECIFICATION_STATUS = SKELETON`

`IMPLEMENTATION_STATUS = NOT_IMPLEMENTED`

`AUTHORITY = FALSE`
