# Human in the Loop

Status: CURRENT

This is where a human in the loop comes into play.

## Current Operators

- Jason
- ChatGPT
- Microsoft

## Rule

ChatGPT can assist.
Microsoft can provide infrastructure.
Jason makes the final decision.

No signer.
No private key.
No transaction.
No irreversible action.

Until Jason explicitly authorizes the next gate.

## Current ALMS Gate

PREVIEW_SCRIPT_LOCKED
LIVE_SCRIPT_NOT_CREATED_YET
SIGNER_NOT_AUTHORIZED
WAITING_FOR_REAL_ROOT_PREVIEW

## Human Authority

Jason is the human operator.

A live transaction may only proceed after:

1. Preview witness exists
2. Witness contains expected schema_uid
3. Witness contains expected merkle_root
4. Witness contains expected func_sig
5. Witness contains expected request
6. Witness contains expected data
7. Witness contains NO_SIGNER_USED
8. Witness contains NO_TX_SENT
9. Jason explicitly authorizes live sender creation

## Boundary

If any condition fails:

STOP
DO_NOT_SIGN
DO_NOT_SEND_TX
RETURN_TO_PREVIEW
