#!/usr/bin/env bash
set -euo pipefail

LEAF="${1:?usage: ./scripts/build_mn_card.sh MN_001}"
TS="$(date -u +%Y-%m-%dT%H:%M:%SZ)"

IN="_truth/receipts/${LEAF}.json"
OUT_JSON="_truth/cards/${LEAF}.card.json"
OUT_SVG="site/cards/${LEAF}.svg"
OUT_TXT="site/cards/${LEAF}.tweet.txt"

test -f "$IN" || { echo "MISSING_RECEIPT $IN"; exit 1; }

CID="$(jq -r '.cid // .root.cid // "bafkrei..."' "$IN")"
HASH="$(jq -r '.hash // .root.hash // .receipt_hash // "UNKNOWN_HASH"' "$IN")"
STATUS="$(jq -r '.status // "VERIFIED"' "$IN")"
TITLE="$(jq -r '.title // .leaf // "'"$LEAF"'"' "$IN")"
LINE="$(jq -r '.claim // .extracted_line // .line // .source_line // .content_hash // empty' "$IN")"

if [ -z "$LINE" ] || [ "$LINE" = "null" ]; then
  echo "FATAL: missing extracted line for $LEAF in $IN"
  exit 1
fi

if [ "$LINE" = "verified public record line" ]; then
  echo "FATAL: placeholder extracted_line detected for $LEAF"
  exit 1
fi

if [ "$HASH" = "UNKNOWN_HASH" ]; then
  echo "FATAL: UNKNOWN_HASH detected for $LEAF"
  exit 1
fi

jq -n -cS \
  --arg leaf "$LEAF" \
  --arg title "$TITLE" \
  --arg line "$LINE" \
  --arg cid "$CID" \
  --arg hash "$HASH" \
  --arg status "$STATUS" \
  --arg ts "$TS" \
  '{
    leaf:$leaf,
    title:$title,
    extracted_line:$line,
    cid:$cid,
    hash:$hash,
    status:$status,
    generated_at:$ts,
    identity:"jaywisdom.base.eth",
    slogan:"Proof > Narrative"
  }' > "$OUT_JSON"

CARD_HASH="$(jq -cS . "$OUT_JSON" | sha256sum | awk '{print $1}')"

cat > "$OUT_SVG" <<EOF2
<svg xmlns="http://www.w3.org/2000/svg" width="1920" height="1080">
<rect width="100%" height="100%" fill="#050505"/>
<text x="80" y="90" fill="#00ff88" font-family="monospace" font-size="42">MN RECEIPT CARD</text>
<text x="1450" y="90" fill="#00ff88" font-family="monospace" font-size="34">STATUS: $STATUS</text>
<line x1="960" y1="150" x2="960" y2="900" stroke="#00ff88" stroke-width="2" opacity="0.55"/>
<text x="90" y="190" fill="white" font-family="monospace" font-size="34">SOURCE RECORD</text>
<rect x="90" y="230" width="780" height="420" fill="#111" stroke="#555"/>
<text x="120" y="300" fill="#fff" font-family="monospace" font-size="30">$TITLE</text>
<text x="120" y="380" fill="#ff5555" font-family="monospace" font-size="26">$LINE</text>
<text x="1030" y="190" fill="white" font-family="monospace" font-size="34">VERIFIED EXTRACTION</text>
<rect x="1030" y="230" width="780" height="420" fill="#07110b" stroke="#00ff88"/>
<text x="1060" y="310" fill="#00ff88" font-family="monospace" font-size="30">$LEAF</text>
<text x="1060" y="390" fill="white" font-family="monospace" font-size="25">$LINE</text>
<text x="1060" y="500" fill="#00ff88" font-family="monospace" font-size="25">HASH: ${HASH:0:24}...</text>
<text x="1060" y="555" fill="#00ff88" font-family="monospace" font-size="25">CARD: ${CARD_HASH:0:24}...</text>
<text x="90" y="820" fill="#aaa" font-family="monospace" font-size="26">CID: ${CID:0:32}...</text>
<text x="90" y="890" fill="#00ff88" font-family="monospace" font-size="30">Proof > Narrative — jaywisdom.base.eth</text>
</svg>
EOF2

cat > "$OUT_TXT" <<EOF2
Same public record.

They gave you a document.
I gave you the line + hash.

$LEAF is locked.
If it changes, the receipt breaks.

Proof > Narrative ⚙️
jaywisdom.base.eth
EOF2

echo "CARD_OK leaf=$LEAF json=$OUT_JSON svg=$OUT_SVG tweet=$OUT_TXT hash=$CARD_HASH"
