#!/usr/bin/env python3
import os, re, json, hashlib
from pathlib import Path
from typing import Optional
from fastapi import FastAPI
from pydantic import BaseModel
from eth_account import Account
from eth_account.messages import encode_typed_data
from web3 import Web3

ETH_RPC=os.getenv("ETH_RPC","https://eth.llamarpc.com")
BASE_RPC=os.getenv("BASE_RPC","https://mainnet.base.org")
ALMS_ANCHOR_BASE=os.getenv("ALMS_ANCHOR_BASE","")
ALMS_ANCHOR_L1=os.getenv("ALMS_ANCHOR_L1","")
VERIFYING_CONTRACT=os.getenv("VERIFYING_CONTRACT","0x0000000000000000000000000000000000000000")

HASH_RE=re.compile(r"^0x[a-fA-F0-9]{64}$")
LEAF_PREFIX="leaf:"
NODE_PREFIX="node:"
MERKLE_DIR=Path("merkle")

ANCHOR_ABI=[{
 "inputs":[{"internalType":"string","name":"namespace","type":"string"}],
 "name":"getAnchor",
 "outputs":[
  {"internalType":"bytes32","name":"root","type":"bytes32"},
  {"internalType":"string","name":"cid","type":"string"},
  {"internalType":"string","name":"manifestHash","type":"string"},
  {"internalType":"uint256","name":"timestamp","type":"uint256"},
  {"internalType":"address","name":"publisher","type":"address"}],
 "stateMutability":"view","type":"function"}]

w3_eth=Web3(Web3.HTTPProvider(ETH_RPC))
w3_base=Web3(Web3.HTTPProvider(BASE_RPC))

app=FastAPI(title="ALMS Full Verifier",version="1.1.0")

class Req(BaseModel):
    typed_data: dict
    signature: str
    receipt_cid: str
    receipt_hash: str
    batch: str="10"

def norm(x): return (x or "").lower().replace("0x","")
def sha(s): return hashlib.sha256(s.encode()).hexdigest()
def node_hash(l,r): return sha(NODE_PREFIX+norm(l)+norm(r))
def leaf_hash(cid,rhash,batch):
    payload=json.dumps({"batch":str(batch),"cid":cid,"hash":norm(rhash)},separators=(",",":"),sort_keys=True)
    return sha(LEAF_PREFIX+payload)

def check_sig(req):
    checks=[]
    td=req.typed_data
    try:
        domain=td["domain"]; msg=td["message"]
        ens=msg.get("ens","").strip().lower()
        checks.append({"step":"parse","ok":True})
    except Exception as e:
        return False, {"status":"ERROR","checks":[{"step":"parse","ok":False,"detail":str(e)}]}

    rules=[
      ("domain", domain.get("name")=="ALMS" and domain.get("version")=="0.2"),
      ("chain", domain.get("chainId")==1),
      ("contract", domain.get("verifyingContract","").lower()==VERIFYING_CONTRACT.lower()),
      ("hash_format", bool(HASH_RE.match(str(msg.get("hash",""))))),
      ("receipt_binding", msg.get("cid")==req.receipt_cid and norm(msg.get("hash"))==norm(req.receipt_hash)),
      ("ens", ens.endswith(".eth")),
    ]
    for step, ok in rules:
        checks.append({"step":step,"ok":ok})
        if not ok: return False, {"status":"INVALID_SIGNATURE","ens":ens,"checks":checks}

    try:
        encoded=encode_typed_data(primitive=td)
        signer=Account.recover_message(encoded, signature=req.signature)
        checks.append({"step":"recover","ok":True,"signer":signer})
    except Exception as e:
        checks.append({"step":"recover","ok":False,"detail":str(e)})
        return False, {"status":"ERROR","ens":ens,"checks":checks}

    try:
        owner=w3_eth.ens.owner(ens) or ""
        resolver=w3_eth.ens.resolver(ens)
        resolver_addr=getattr(resolver,"address","") if resolver else ""
        allowed={a.lower() for a in [owner,resolver_addr] if a}
        ok=signer.lower() in allowed
        checks.append({"step":"authority","ok":ok})
        return ok, {"status":"VALID_SIGNATURE" if ok else "INVALID_SIGNATURE","ens":ens,"signer":signer,"ens_owner":owner,"ens_resolver":resolver_addr,"checks":checks}
    except Exception as e:
        checks.append({"step":"authority","ok":False,"detail":str(e)})
        return False, {"status":"ERROR","ens":ens,"signer":signer,"checks":checks}

def contract_root(w3, addr, namespace):
    c=w3.eth.contract(address=Web3.to_checksum_address(addr), abi=ANCHOR_ABI)
    return "0x"+c.functions.getAnchor(namespace).call()[0].hex()

def check_anchor(req, ens):
    checks=[]; anchors={}; namespace=f"alms.batch{req.batch}"
    f=MERKLE_DIR/f"batch{req.batch}_anchor.json"
    if not f.exists():
        return False, {"status":"ERROR","namespace":namespace,"checks":[{"step":"merkle_load","ok":False,"detail":"anchor file missing"}]}
    data=json.loads(f.read_text())
    root=norm(data["merkle_root"])

    entry=next((r for r in data.get("receipts",[]) if r["receipt"]["cid"]==req.receipt_cid),None)
    if not entry:
        return False, {"status":"INVALID_MULTI_ANCHOR","namespace":namespace,"root":"0x"+root,"checks":[{"step":"merkle_find","ok":False}]}

    computed=leaf_hash(req.receipt_cid,req.receipt_hash,req.batch)
    for st in entry.get("merkle_proof",[]):
        sib=st["sibling"]
        computed=node_hash(computed,sib) if st["position"]=="right" else node_hash(sib,computed)
    merkle_ok=norm(computed)==root
    checks.append({"step":"merkle_proof","ok":merkle_ok})
    if not merkle_ok:
        return False, {"status":"INVALID_MULTI_ANCHOR","namespace":namespace,"root":"0x"+root,"checks":checks}

    try:
        ens_val=w3_eth.ens.get_text(ens,f"alms.batch{req.batch}.root")
        anchors["ens"]=norm(ens_val)==root
    except Exception:
        anchors["ens"]=False

    try:
        anchors["base"]=bool(ALMS_ANCHOR_BASE) and norm(contract_root(w3_base,ALMS_ANCHOR_BASE,namespace))==root
    except Exception:
        anchors["base"]=False

    try:
        anchors["ethereum"]=bool(ALMS_ANCHOR_L1) and norm(contract_root(w3_eth,ALMS_ANCHOR_L1,namespace))==root
    except Exception:
        anchors["ethereum"]=False

    passed=sum(1 for v in anchors.values() if v)
    quorum=passed>=2
    checks.append({"step":"quorum","ok":quorum,"passed":passed,"required":2})
    return quorum, {"status":"VALID_MULTI_ANCHOR" if quorum else "INVALID_MULTI_ANCHOR","namespace":namespace,"root":"0x"+root,"anchors":anchors,"quorum_passed":passed,"quorum_required":2,"checks":checks}

@app.get("/health")
def health():
    return {"status":"ok","eth_connected":w3_eth.is_connected(),"base_connected":w3_base.is_connected()}

@app.post("/verify/full")
def verify_full(req: Req):
    sig_ok,sig=check_sig(req)
    anchor_ok,anchor=check_anchor(req, sig.get("ens",""))
    return {
      "status":"VALID_FULL_PROOF" if sig_ok and anchor_ok else "INVALID_FULL_PROOF",
      "signature":sig,
      "anchor":anchor,
      "checks_summary":{
        "signature":sig_ok,
        "merkle_multi_anchor":anchor_ok
      }
    }
