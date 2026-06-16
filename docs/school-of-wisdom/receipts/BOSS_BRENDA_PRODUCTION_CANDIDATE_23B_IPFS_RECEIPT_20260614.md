# BOSS BRENDA 23B — IPFS RECEIPT (PRE-FILLED, AWAITING PIN)

**Artifact:** Boss Brenda — The Audit's Enforcer  
**Card ID:** 23B  
**Local path:** `/mnt/data/boss_brenda_the_audit_s_enforcer.png`  
**Dimensions:** 1086×1448 (3:4 portrait)  
**Local SHA256:** `07a1ab126c7dfc34634cb7035292c6559af3a63ea96af26235a2f1f99959ea80`  
**Local bytes:** 3,208,627  

---

## Production Classification

```text
FACTORY_LANE=BOSS_BRENDA_PRODUCTION_CANDIDATE_23B
SOURCE=Render Brenda generation
PRIOR_V2_MASTER_MATCH=NO
STATUS=YELLOW_LOCAL_CANDIDATE
NO_FAKE_GREEN=ACTIVE
```

This receipt records a fresh production artifact. It does **not** replace or satisfy the prior Brenda V2 master receipt.

---

## 🟡 PINNING STATUS: YELLOW (NOT YET PINNED)

| Field | Value | Status |
|-------|-------|--------|
| IPFS CID | `__________` | YELLOW |
| Pinning service | `__________` | YELLOW |
| Pin timestamp UTC | `__________` | YELLOW |

---

## 🟡 GATEWAY READBACK 1

**Gateway URL:** `https://ipfs.io/ipfs/<CID>`  
**Retrieved SHA256:** `__________`  
**Retrieved bytes:** `__________`  
**Match local?** ☐ YES ☐ NO  

---

## 🟡 GATEWAY READBACK 2

**Gateway URL:** `https://cloudflare-ipfs.com/ipfs/<CID>`  
**Retrieved SHA256:** `__________`  
**Retrieved bytes:** `__________`  
**Match local?** ☐ YES ☐ NO  

---

## ✅ FINAL VERDICT (to be filled after readback)

```json
{
  "card_id": "23B",
  "artifact": "Boss Brenda — The Audit's Enforcer",
  "status": "YELLOW_LOCAL_CANDIDATE",
  "ipfs_pin": "YELLOW",
  "gateway_readback": "YELLOW",
  "authority": false,
  "no_fake_green": true
}
```

---

## Promotion Rule

The artifact may become `GREEN_SCOPED` only after:

1. The exact local file is pinned to IPFS.
2. A CID is recorded.
3. At least two public gateway readbacks return the same SHA256 and byte count:
   - SHA256: `07a1ab126c7dfc34634cb7035292c6559af3a63ea96af26235a2f1f99959ea80`
   - Bytes: `3208627`

Until then:

```text
GREEN=FALSE
YELLOW=HONEST
```

---

## Operator Command Block — Pin and Read Back

Run this only from an environment where the exact local file exists and `ipfs` is available.

```bash
set -euo pipefail

MASTER="/mnt/data/boss_brenda_the_audit_s_enforcer.png"
EXPECTED_SHA="07a1ab126c7dfc34634cb7035292c6559af3a63ea96af26235a2f1f99959ea80"
EXPECTED_BYTES="3208627"
EXPECTED_DIMENSIONS="1086x1448"

mkdir -p _truth/audit/boss_brenda_23b

echo "== LOCAL 23B CHECK =="
test -f "$MASTER"
LOCAL_SHA="$(sha256sum "$MASTER" | awk '{print $1}')"
LOCAL_BYTES="$(wc -c < "$MASTER" | tr -d ' ')"

echo "LOCAL_PATH=$MASTER"
echo "LOCAL_SHA256=$LOCAL_SHA"
echo "LOCAL_BYTES=$LOCAL_BYTES"
echo "LOCAL_DIMENSIONS=$EXPECTED_DIMENSIONS"

test "$LOCAL_SHA" = "$EXPECTED_SHA"
test "$LOCAL_BYTES" = "$EXPECTED_BYTES"

echo "== IPFS ADD =="
CID="$(ipfs add -Q "$MASTER")"
echo "CID=$CID"

for GW in "https://ipfs.io/ipfs" "https://cloudflare-ipfs.com/ipfs"; do
  SAFE="$(echo "$GW" | sed 's#https://##;s#[/.]#_#g')"
  OUT="_truth/audit/boss_brenda_23b/${SAFE}.png"

  echo "== GATEWAY READBACK: $GW =="
  curl -L --fail "$GW/$CID" -o "$OUT"

  RB_SHA="$(sha256sum "$OUT" | awk '{print $1}')"
  RB_BYTES="$(wc -c < "$OUT" | tr -d ' ')"

  echo "URL=$GW/$CID"
  echo "READBACK_SHA256=$RB_SHA"
  echo "READBACK_BYTES=$RB_BYTES"

  test "$RB_SHA" = "$EXPECTED_SHA"
  test "$RB_BYTES" = "$EXPECTED_BYTES"
done

echo "== GREEN_SCOPED_READY =="
echo "CID=$CID"
echo "EXPECTED_SHA256=$EXPECTED_SHA"
echo "EXPECTED_BYTES=$EXPECTED_BYTES"
```

---

## Paste-Back Block

After pinning and two readbacks, paste only:

```text
CID=
Gateway 1 SHA256/BYTES=
Gateway 2 SHA256/BYTES=
```

If both gateway readbacks equal the local SHA256 and byte count, this receipt may be updated from `YELLOW_LOCAL_CANDIDATE` to `GREEN_SCOPED`.

---

## Goblin Rule

> You have the local candidate. Pin it. Read it back twice. Until then: YELLOW is honest. GREEN would be fake. No shortcut. No fake green.
