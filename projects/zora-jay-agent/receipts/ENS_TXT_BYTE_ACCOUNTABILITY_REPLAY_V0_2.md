# ENS_TXT_BYTE_ACCOUNTABILITY_REPLAY_V0_2

STATUS: BASELINE_REPAIR_RECEIPT
TRUTH_STATE: YELLOW
NO_FAKE_GREEN: ACTIVE
AUTHORITY: FALSE
ONCHAIN_WRITE: FALSE
RESOLVER_READBACK_VERIFIED: FALSE

## User Replay

The user requested byte-by-byte accountability and transparency for both:

```text
jaywisdom.eth
jaywisdom.base.eth
```

The immediate issue was that the visible ENS screen for `jaywisdom.eth` showed 7 TXT records, while the daily checker baseline only covered a partial subset.

## Repair

Updated baseline:

```text
projects/zora-jay-agent/config/ens_txt_byte_baseline_v0_1.json
```

The baseline is now version `0.2` and requires `BYTE_FOR_BYTE_UTF8_AND_HEX` accountability.

## Required Record Set

Both the L1 Seal and L2 Engine names now carry the same required 7-record accountability set:

```text
receipts_engine
friar.image_cid
friar.title
friar.version
friar.payload_hash
alms.public_key
key: al.verified
```

## Expected Values Preserved

```text
receipts_engine=9f73ce11d4bc0f9870ee1a9e46d45c9526632b8defd14a7f378f50d0497d3942
friar.image_cid=bafybeiaqsfol2ke33jhpyjylhsxflt2izmxzd3qwj7brj7m3yd5qra6ahja
friar.title=Jay's Wisdom
friar.version=1
friar.payload_hash=0x8b7df5e6c9d2f4a1e3b5c7d9f1a3c5e7b9d1f3a5c7e9b1d3f5a7c9e1b3d5f7c9
alms.public_key=did:key:jaywisdom-v1
key: al.verified=root=sha256:65377be53afaa04856a5bad16a6f90481ef703e4ce1af35763647f0dbb86d460;commit=03e0e1711a6294d8a35b478a5b90ee17046b2f64;advisory=ipfs://QmbrGfzwy5DmzGhE5Txscs7BfaRknNosc3G5r1pfQEsdqF
```

## NO_FAKE_GREEN Rule

This is not GREEN yet.

Promotion requires:

```text
1. Daily workflow or manual dispatch runs.
2. Resolver read-back succeeds for jaywisdom.eth.
3. Resolver read-back succeeds for jaywisdom.base.eth.
4. Every required TXT value matches byte-for-byte.
5. The report artifact exists.
```

## Ruling

```text
CONFIG_REPAIRED: TRUE
FULL_VISIBLE_L1_RECORD_SET_ADDED: TRUE
ENGINE_MIRROR_PRESSURE_ADDED: TRUE
TRUTH_STATE: YELLOW_UNTIL_RUN
NO_FAKE_GREEN: ACTIVE
```
