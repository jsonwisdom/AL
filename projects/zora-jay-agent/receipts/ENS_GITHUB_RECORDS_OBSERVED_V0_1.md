# ENS_GITHUB_RECORDS_OBSERVED_V0_1

STATUS: UI_OBSERVED_RECEIPT
TRUTH_STATE: YELLOW
NO_FAKE_GREEN: ACTIVE
AUTHORITY: FALSE
EXECUTED_NEW_WRITE: FALSE
RESOLVER_READBACK_VERIFIED: FALSE

## Subject

ENS name:

```text
jaywisdom.eth
```

Observation source:

```text
User-provided ENS app screenshot showing jaywisdom.eth Records tab.
```

Observed date context:

```text
2026-06-13
```

## Operational Finding

The prior assumption that the L1 ENS layer was only available for future anchoring is incomplete.

The screenshot shows that `jaywisdom.eth` already has text records containing proof material linked to the user’s GitHub / ALMS receipt system.

This means the correct state is:

```text
L1_CONTROL_SURFACE: OBSERVED
L1_RECORDS_PRESENT: OBSERVED
GITHUB_LINKAGE_MATERIAL: OBSERVED
NEW_ANCHOR_WRITE: NOT_EXECUTED_BY_THIS_RECEIPT
INDEPENDENT_RESOLVER_READBACK: PENDING
TRUTH_STATE: YELLOW
NO_FAKE_GREEN: ACTIVE
```

## Records Visible In Screenshot

The ENS Records tab shows 7 text records. Visible record labels / values include:

```text
friar.title = Jay's Wisdom
friar.version = 1
alms.public_key = did:key:jaywisdom-v1
```

A visible verification-style record includes:

```text
root=sha256:65377be53afaa04856a5bad16a6f90481ef703e4ce1af35763647f0dbb86d460
commit=03e0e1711a6294d8a35b478a5b90ee17046b2f64
advisory=ipfs://QmbrGfzwy5DmzGhE5Txscs7BfaRknNosc3G5r1pfQEsdqF
```

Additional visible fields include truncated / wrapped values for:

```text
receipts_engi...
friar.image_cid
friar.payload_...
```

These are preserved as observed UI facts only. Exact key names and full values require resolver or ENS app copy/export read-back before promotion.

## Corrected Architecture State

```text
jaywisdom.eth = Seal / L1 ENS records / long-term public witness surface
jaywisdom.base.eth = Engine / L2 mutable state and high-velocity logs
identity_sync_v0.1.json = bridge object between Seal and Engine
```

The L1 ENS text-record layer is not empty. It already contains public proof references.

## Promotion Requirements

This receipt must remain YELLOW until at least one of the following independent checks is completed:

```text
1. Resolver read-back confirms the exact ENS text records for jaywisdom.eth.
2. The referenced GitHub commit resolves and matches the stated commit hash.
3. The stated sha256 root is recomputed from the referenced artifact set.
4. The IPFS advisory object resolves and matches the expected proof payload.
```

## Ruling

```text
CLAIM: jaywisdom.eth already has ENS records linked to GitHub proof material
STATE: UI_OBSERVED
HIGHEST_DEFENSIBLE_TRUTH_STATE: YELLOW
NO_FAKE_GREEN: ACTIVE
```
