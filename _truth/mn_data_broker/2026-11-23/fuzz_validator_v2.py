#!/usr/bin/env python3
"""CI-FIRST seeded in-memory fuzz tests; all records SYNTHETIC and never evidence."""
import argparse
import copy
import hashlib
import json
import random
from collections import Counter
from pathlib import Path
from validate_registry_v2 import validate

ROOT = Path(__file__).parent
BASE = json.loads((ROOT / "registry-87-counties-v1.json").read_text())
MODEL = json.loads((ROOT / "relationship-model-v1.json").read_text())
VALID_B = b"synthetic original document bytes (not procurement evidence)"
VALID_SHA = hashlib.sha256(VALID_B).hexdigest()


def mutate_valid_fixture(r, m, *, doc_status="UNKNOWN", doc_type="synthetic"):
    m["tables"]["agencies"].append({
        "agency_id": "SYN-A1", "agency_name": "SYNTHETIC A1",
        "jurisdiction_level": "state", "verification_status": "UNKNOWN"})
    m["tables"]["vendors"].append({
        "vendor_id": "SYN-V1", "vendor_name": "SYNTHETIC V1",
        "verification_status": "UNKNOWN"})
    m["tables"]["source_documents"].append({
        "document_id": "SYN-D1", "agency_id": "SYN-A1",
        "source_url_or_identifier": "synthetic://test",
        "verified_at_utc": "2026-11-23T00:00:00Z",
        "sha256_original": VALID_SHA, "source_type": doc_type,
        "verification_status": doc_status})
    m["tables"]["contracts"].append({
        "contract_id": "SYN-C1", "agency_id": "SYN-A1",
        "vendor_id": "SYN-V1", "source_document_id": "SYN-D1",
        "verification_status": "UNKNOWN"})
    m["tables"]["contract_agencies"].append({
        "contract_id": "SYN-C1", "agency_id": "SYN-A1"})


def produce(seed=20261123, iterations=280):
    rng = random.Random(seed)
    reports=[]
    for i in range(iterations):
        r, m = copy.deepcopy(BASE), copy.deepcopy(MODEL)
        originals={}
        family = i % 7
        if family == 0:
            label="agency_roster"
            variant=rng.randrange(4)
            if variant==0: r["agencies"].pop()
            if variant==1: r["agencies"].append(dict(r["agencies"][0]))
            if variant==2: r["agencies"][0]["agency_id"]="SYN-OTHER"
            if variant==3: r["agencies"][1]["status"]="SENT"
            expected="FAIL"; marker="INVALID_AGENCY_ROSTER"
        elif family == 1:
            label="county_uniqueness"
            a,b=rng.sample(range(87),2)
            variant=rng.randrange(3)
            if variant==0: r["counties"][a]["county_name"]=r["counties"][b]["county_name"]
            if variant==1: r["counties"][a]["jurisdiction_id"]=r["counties"][b]["jurisdiction_id"]
            if variant==2: r["counties"][a]["county_name"]="SYNTHETIC COUNTY"
            expected="FAIL";marker="INVALID_COUNTY_ROSTER"
        elif family == 2:
            label="foreign_key_target"
            table=rng.choice(["contracts","payments","datasets","invoices","contract_agencies"])
            spec=rng.randrange(len(m["foreign_keys"][table]))
            item=m["foreign_keys"][table][spec]
            m["foreign_keys"][table][spec]=item.replace(".agency_id",".vendor_id").replace(".vendor_id",".document_id").replace(".document_id",".contract_id").replace(".contract_id",".invoice_id").replace(".invoice_id",".fake_id").replace(".purchase_order_id",".fake_id")
            expected="FAIL";marker="INVALID_FOREIGN_KEY_TARGET"
        elif family == 3:
            label="hash_classification"
            mutate_valid_fixture(r,m,doc_status="VERIFIED")
            originals={"SYN-D1":VALID_B}
            expected="FAIL";marker="SYNTHETIC_CANNOT_BE_VERIFIED"
        elif family == 4:
            label="missing_agency_identifier"
            mutate_valid_fixture(r,m)
            m["tables"]["source_documents"][0].pop("agency_id")
            expected="FAIL";marker="MISSING_REQUIRED_FIELD:source_documents.agency_id"
        elif family == 5:
            label="cardinality"
            mutate_valid_fixture(r,m)
            if rng.randrange(2):
                m["tables"]["contract_agencies"].append(dict(m["tables"]["contract_agencies"][0]))
                marker="DUPLICATE_CONTRACT_AGENCY"
            else:
                m["tables"]["contract_agencies"].clear()
                marker="MISSING_CONTRACT_AGENCY_LINK"
            expected="FAIL"
        else:
            label="classification_boundary"
            variant=rng.randrange(4)
            if variant==0:
                mutate_valid_fixture(r,m)
                expected="HOLD";marker="INCOMPLETE_SOURCE_ORIGINAL"
            elif variant==1:
                mutate_valid_fixture(r,m)
                originals={"SYN-D1":b"different content"}
                expected="FAIL";marker="SHA256_MISMATCH"
            elif variant==2:
                mutate_valid_fixture(r,m)
                originals={"SYN-D1":VALID_B}
                expected="HOLD";marker="UNVERIFIED_RECORD"
            else:
                expected="PASS";marker=""
        # Full mutated input corpus fingerprint; deterministic seed and source
        # hashes allow replay without publishing synthetic transaction fixtures.
        corpus = json.dumps({"registry":r,"model":m,
            "original_sha256":{k:hashlib.sha256(v).hexdigest() for k,v in sorted(originals.items())}},
            sort_keys=True,separators=(",",":"),ensure_ascii=False).encode()
        input_sha256=hashlib.sha256(corpus).hexdigest()
        report=validate(r,m,originals)
        matches=(report["verdict"]==expected and (not marker or any(x.startswith(marker) for x in report["errors"]+report["holds"])))
        case={"case":i,"family":label,"expected":expected,"actual":report["verdict"],
              "marker":marker,"pass":matches,"input_sha256":input_sha256,"errors":report["errors"],"holds":report["holds"]}
        reports.append(case)
    return {"seed":seed,"cases":iterations,"passed":sum(x["pass"] for x in reports),
            "failed":sum(not x["pass"] for x in reports),
            "family_counts":dict(Counter(x["family"] for x in reports)),
            "failures":[x for x in reports if not x["pass"]],"case_results":reports}


def main():
    ap=argparse.ArgumentParser();ap.add_argument("--seed",type=int,default=20261123);ap.add_argument("--iterations",type=int,default=280)
    a=ap.parse_args()
    result=produce(a.seed,a.iterations)
    print(json.dumps(result,indent=2,sort_keys=True))
    return 0 if not result["failed"] else 1

if __name__=="__main__":
    raise SystemExit(main())
