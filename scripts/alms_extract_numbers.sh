#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat <<'EOF'
Usage:
  echo "Balance $3.7B [source:url:https://example.com/report.pdf|sha256:<64hex>|ipfs:bafy...|ens:alms.key]" | scripts/alms_extract_numbers.sh

Supported anchors:
  [source:inline]
  [source:sentence:s1]
  [source:citation:ref1]
  [source:url:https://example.com/report.pdf]
  [source:url:https://example.com/report.pdf|sha256:<64 lowercase hex chars>]
  [source:url:https://example.com/report.pdf|sha256:<64 lowercase hex chars>|ipfs:<cid>|ens:<text_record_key>]
EOF
}

if [ "${1:-}" = "-h" ] || [ "${1:-}" = "--help" ]; then usage; exit 0; fi
if [ "$#" -gt 0 ]; then echo "ALMS_NUMERIC_EXTRACT_ERROR too_many_arguments" >&2; usage >&2; exit 2; fi

TEXT=$(cat)

python3 - "$TEXT" <<'PY'
from decimal import Decimal, InvalidOperation, getcontext
import hashlib, json, re, sys
getcontext().prec = 50
text = sys.argv[1]
anchor_pattern = re.compile(r'\[source:(?P<body>[^\]]+)\]', re.IGNORECASE)

def parse_anchor(body):
    b = body.strip()
    bl = b.lower()
    base = {'type':'unknown','location':b,'expected_raw_hash':None,'ipfs_cid':None,'ens_key':None}
    if bl == 'inline': return {'type':'inline','location':None,'expected_raw_hash':None,'ipfs_cid':None,'ens_key':None}
    if bl.startswith('sentence:'): return {'type':'sentence','location':b.split(':',1)[1],'expected_raw_hash':None,'ipfs_cid':None,'ens_key':None}
    if bl.startswith('citation:'): return {'type':'citation','location':b.split(':',1)[1],'expected_raw_hash':None,'ipfs_cid':None,'ens_key':None}
    if bl.startswith('url:'):
        payload = b[4:]
        parts = payload.split('|')
        obj = {'type':'url','location':parts[0],'expected_raw_hash':None,'ipfs_cid':None,'ens_key':None}
        for part in parts[1:]:
            p = part.strip()
            pl = p.lower()
            if pl.startswith('sha256:'):
                obj['expected_raw_hash'] = pl
            elif pl.startswith('ipfs:'):
                obj['ipfs_cid'] = p.split(':',1)[1]
            elif pl.startswith('ens:'):
                obj['ens_key'] = p.split(':',1)[1]
        return obj
    return base
anchors=[(m.start(),m.end(),parse_anchor(m.group('body'))) for m in anchor_pattern.finditer(text)]
scale_aliases={'k':'thousand','thousand':'thousand','m':'million','mm':'million','mn':'million','million':'million','b':'billion','bn':'billion','billion':'billion','t':'trillion','tn':'trillion','trillion':'trillion','':''}
scale_multipliers={'':Decimal('1'),'thousand':Decimal('1000'),'million':Decimal('1000000'),'billion':Decimal('1000000000'),'trillion':Decimal('1000000000000')}
number_pattern=re.compile(r'(?P<prefix>[$])?(?<![A-Za-z0-9.])(?P<number>\d+(?:,\d{3})*(?:\.\d+)?|\d*\.\d+)(?P<percent>%)?(?:\s*(?P<scale>thousand|million|billion|trillion|bn|mn|mm|tn|k|m|b|t))?(?![A-Za-z0-9])', re.IGNORECASE)
def canonical_decimal(value):
    if value == value.to_integral_value(): return str(value.quantize(Decimal('1')))
    return format(value.normalize(),'f')
def anchor_for_number(num_end,next_num_start):
    c=[]
    for start,end,obj in anchors:
        if start < num_end: continue
        if next_num_start is not None and start > next_num_start: continue
        if start-num_end <= 240: c.append((start,obj))
    return sorted(c,key=lambda x:x[0])[0][1] if c else None
matches=list(number_pattern.finditer(text)); numbers=[]
for idx,match in enumerate(matches):
    cleaned=match.group('number').replace(',','')
    try: value_decimal=Decimal(cleaned)
    except InvalidOperation: continue
    percent=bool(match.group('percent'))
    scale=scale_aliases.get((match.group('scale') or '').lower(),(match.group('scale') or '').lower())
    unit='percent' if percent else ('usd' if match.group('prefix') else 'number')
    base=value_decimal*(Decimal('1') if percent else scale_multipliers.get(scale,Decimal('1')))
    next_start=matches[idx+1].start() if idx+1 < len(matches) else None
    numbers.append({'index':idx,'raw':match.group(0),'canonical_number':canonical_decimal(value_decimal),'scale':scale,'unit':unit,'base_value':canonical_decimal(base),'source_anchor':anchor_for_number(match.end(),next_start),'start':match.start(),'end':match.end()})
fingerprint=[{'index':n['index'],'unit':n['unit'],'base_value':n['base_value'],'scale':n['scale']} for n in numbers]
digest=hashlib.sha256(json.dumps(fingerprint,sort_keys=True,separators=(',',':')).encode()).hexdigest()
print(json.dumps({'extractor_version':'alms_numeric_extractor_v1','numbers':numbers,'numbers_fingerprint':fingerprint,'numbers_hash':'sha256:'+digest},indent=2,sort_keys=True))
PY
