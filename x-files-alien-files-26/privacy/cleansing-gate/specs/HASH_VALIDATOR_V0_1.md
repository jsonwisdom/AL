# Hash Validator v0.1 Contract

## Purpose
Define the pure validation interface for the Cleansing Gate export manifest. This specification mandates a fail-closed implementation.

## Interface (Pure Logic)
`validate(manifest_json, public_key, file_handles) -> Result<ValidationReceipt, ValidationError>`

## Validation Logic
1. **Manifest/Schema Check**: Validate `manifest_json` against `PARENT_EXPORT_APPROVAL_V0_1.schema.json`.
   - Pure error: `MANIFEST_SCHEMA_INVALID` | CLI mapping: exit code `6`
2. **Key Verification**: Ensure `SHA256(public_key) == signing_key_id`.
   - Pure error: `SIGNATURE_OR_KEY_BINDING_FAILURE` | CLI mapping: exit code `5`
3. **Signature Verification**: Verify `parent_signature` (Ed25519) over JCS-canonical JSON (excluding `parent_signature` field).
   - Pure error: `SIGNATURE_OR_KEY_BINDING_FAILURE` | CLI mapping: exit code `5`
4. **Temporal Logic**: Validate strict window:
   - `issued_at <= now <= expires_at`
   - `expires_at > issued_at`
   - `expires_at - issued_at <= 300` seconds
   - Pure error: `APPROVAL_WINDOW_FAILURE` | CLI mapping: exit code `3`
5. **Hash Integrity**: Verify computed file hashes against manifest:
   - `computed(input_file) == input_sha256`
   - `computed(output_file) == output_sha256`
   - `computed(preview_file) == preview_sha256`
   - Pure error: `HASH_INTEGRITY_FAILURE` | CLI mapping: exit code `4`

## Logic Mapping
| Pure Error | CLI Exit Code | Description |
| :--- | :--- | :--- |
| `SYSTEM_OR_IO_ERROR` | 1 | I/O, file access, or unrecoverable runtime failure |
| `NOT_IMPLEMENTED` | 2 | Placeholder implementation state |
| `APPROVAL_WINDOW_FAILURE` | 3 | Window or clock-skew violation |
| `HASH_INTEGRITY_FAILURE` | 4 | Payload or manifest hash mismatch |
| `SIGNATURE_OR_KEY_BINDING_FAILURE` | 5 | Ed25519 verification or key-binding failure |
| `MANIFEST_SCHEMA_INVALID` | 6 | Schema-conformance failure |

## Exit Codes
| Code | Meaning |
| :--- | :--- |
| 0 | Success |
| 1 | System or I/O error |
| 2 | Not implemented |
| 3 | Approval-window failure |
| 4 | Hash-integrity failure |
| 5 | Signature/key-binding failure |
| 6 | Manifest/schema failure |

## Invariants
- **Clock Skew**: Zero for v0.1.
- **Canonicalization**: JCS (RFC 8785).
- **Execution**: Pure function separated from CLI wrapper.
- **Failure Posture**: Any unclassified validation failure must halt; it must not be promoted to success.

## Status
- `SPECIFICATION_STATUS = DEFINED`
- `IMPLEMENTATION_STATUS = NOT_IMPLEMENTED`
- `TEST_SUCCESS = NOT_CLAIMED`
- `AUTHORITY = FALSE`
