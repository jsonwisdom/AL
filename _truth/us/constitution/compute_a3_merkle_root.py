#!/usr/bin/env python3
import json, hashlib
from pathlib import Path
p=Path(__file__).resolve().parent/"article_iii_audit.jsonl"
lines=[json.loads(l) for l in p.read_text().splitlines() if l.strip()]
lines=sorted(lines,key=lambda x:x['id'])
leaves=[hashlib.sha256(f"{l['id']}:{l['sha256']}".encode()).hexdigest() for l in lines]
def build(h):
    if len(h)==1: return h[0]
    nxt=[]
    for i in range(0,len(h),2):
        if i+1<len(h):
            nxt.append(hashlib.sha256(bytes.fromhex(h[i]+h[i+1])).hexdigest())
        else:
            nxt.append(h[i])
    return build(nxt)
print(build(leaves))
