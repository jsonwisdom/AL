#!/usr/bin/env python3
"""CI-FIRST read-only structural validator for MN commercial location-data registry.

This validator NEVER contacts agencies, modifies input files, merges, or deploys.
It only authenticates an *original* when --original-document is provided with a
matching SHA-256 digest. A claimed digest in metadata alone is not verification.
Exit 0 = structural PASS; exit 1 = FAIL; exit 2 = HOLD (unverified evidence).
"""
import argparse, hashlib, json, re, sys
from collections import Counter
from pathlib import Path

HEX64 = re.compile(r"^[0-9a-fA-F]{64}$")
FK = re.compile(r"^([a-z_]+) -> ([a-z_]+)\.([a-z_]+)(?: \(nullable(?: for statewide)?\))?$")
ID_FIELDS = {"agencies":"agency_id", "vendors":"vendor_id",
 "contracts":"contract_id", "purchase_orders":"purchase_order_id",
 "invoices":"invoice_id", "payments":"payment_id",
 "datasets":"dataset_id", "authorizations":"authorization_id",
 "source_documents":"document_id", "court_application_reporting":"report_id"}
VALID_STATES = {"UNKNOWN","HOLD","NOT_ESTABLISHED","VERIFIED","REJECTED","NOT_APPLICABLE"}
SEVERE = {"INVALID_SHA256","SHA256_MISMATCH","ORPHAN_FOREIGN_KEY","DUPLICATE_ID",
 "DUPLICATE_CONTRACT","DUPLICATE_CONTRACT_AGENCY","INVALID_CLASSIFICATION",
 "MISSING_REQUIRED_FIELD","UNAUTHORIZED_TRANSMISSION","UNAUTHORIZED_DEPLOYMENT",
 "UNAUTHORIZED_MERGE","INVALID_COUNTY_ROSTER","INCOMPLETE_SOURCE_ORIGINAL"}

def validate(registry, model, original_documents=None):
    errors, holds = [], []
    original_documents = original_documents or {}
    counties = registry.get("counties", [])
    county_ids = [c.get("jurisdiction_id") for c in counties]
    if len(counties)!=87 or len(set(county_ids))!=87 or any(not x for x in county_ids):
        errors.append("INVALID_COUNTY_ROSTER")
    if registry.get("scope_counties")!=87:
        errors.append("INVALID_COUNTY_ROSTER")
    controls = model.get("controls", {})
    if registry.get("external_agency_requests_authorized") is not False or controls.get("transmission_authorized") is not False or any(a.get("status")!="HOLD_NOT_SENT" for a in registry.get("agencies", [])) or controls.get("dps_bca")!="HOLD_NOT_SENT" or controls.get("doc")!="HOLD_NOT_SENT":
        errors.append("UNAUTHORIZED_TRANSMISSION")
    if controls.get("production_merge_authorized") is not False:
        errors.append("UNAUTHORIZED_MERGE")
    if controls.get("cloudflare_deploy_authorized") is not False:
        errors.append("UNAUTHORIZED_DEPLOYMENT")
    tables = model.get("tables", {})
    if any(not isinstance(v,list) for v in tables.values()): errors.append("INVALID_TABLES")
    if "INVALID_TABLES" in errors: return {"verdict":"FAIL","errors":errors,"holds":holds}
    required = model.get("required_fields", {})
    keys = {}
    for table, records in tables.items():
        pk = ID_FIELDS.get(table)
        if pk:
            ids = [r.get(pk) for r in records]
            if len(ids)!=len(set(ids)): errors.append(f"DUPLICATE_ID:{table}")
            keys[table] = set(x for x in ids if x is not None)
        for r in records:
            for field in required.get(table, []):
                if r.get(field) in (None,""): errors.append(f"MISSING_REQUIRED_FIELD:{table}.{field}")
            state = r.get("verification_status")
            if state is not None and state not in VALID_STATES:
                errors.append(f"INVALID_CLASSIFICATION:{table}")
            if state=="VERIFIED":
                doc_id = r.get("document_id") if table=="source_documents" else r.get("source_document_id")
                if not doc_id or doc_id not in original_documents:
                    holds.append(f"INCOMPLETE_SOURCE_ORIGINAL:{table}")
    for table, specs in model.get("foreign_keys", {}).items():
        for s in specs:
            match = FK.fullmatch(s)
            if not match:
                errors.append(f"INVALID_FOREIGN_KEY_SPEC:{table}:{s}");continue
            field, target_table, target_pk = match.groups()
            if target_table=="counties": targets = set(county_ids)
            else: targets = keys.get(target_table)
            if targets is None:
                errors.append(f"INVALID_FOREIGN_KEY_SPEC:{table}:{s}"); continue
            nullable = "(nullable" in s
            for r in tables.get(table, []):
                value = r.get(field)
                if value in (None,""):
                    if not nullable: errors.append(f"ORPHAN_FOREIGN_KEY:{table}.{field}")
                elif value not in targets:
                    errors.append(f"ORPHAN_FOREIGN_KEY:{table}.{field}")
    contract_ids=[r.get("contract_id") for r in tables.get("contracts",[])]
    if len(contract_ids)!=len(set(contract_ids)): errors.append("DUPLICATE_CONTRACT")
    pair_ids=[(r.get("contract_id"),r.get("agency_id")) for r in tables.get("contract_agencies",[])]
    if len(pair_ids)!=len(set(pair_ids)): errors.append("DUPLICATE_CONTRACT_AGENCY")
    for doc in tables.get("source_documents", []):
        did, expected = doc.get("document_id"),doc.get("sha256_original")
        if not isinstance(expected,str) or not HEX64.fullmatch(expected):
            errors.append(f"INVALID_SHA256:{did}");continue
        original=original_documents.get(did)
        if original is None:
            holds.append(f"INCOMPLETE_SOURCE_ORIGINAL:{did}");continue
        if hashlib.sha256(original).hexdigest().lower()!=expected.lower():
            errors.append(f"SHA256_MISMATCH:{did}")
    if errors: verdict="FAIL"
    elif holds: verdict="HOLD"
    else: verdict="PASS"
    return {"verdict":verdict,"errors":sorted(set(errors)),"holds":sorted(set(holds)),
            "county_count":len(counties),
            "record_counts":{k:len(v) for k,v in tables.items()},
            "evidence_claim":"NO PROCUREMENT ESTABLISHED" if not any(tables.values()) else "REQUIRES DOCUMENT-SPECIFIC REVIEW"}

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--registry",required=True)
    ap.add_argument("--model",required=True)
    ap.add_argument("--original-document",action="append",default=[],help="document_id=path to original bytes")
    args=ap.parse_args()
    originals={}
    for item in args.original_document:
        if "=" not in item: ap.error("original document must be document_id=path")
        did,path=item.split("=",1); originals[did]=Path(path).read_bytes()
    report=validate(json.loads(Path(args.registry).read_text()),json.loads(Path(args.model).read_text()),originals)
    print(json.dumps(report,indent=2,sort_keys=True))
    return {"PASS":0,"FAIL":1,"HOLD":2}[report["verdict"]]
if __name__=="__main__":sys.exit(main())
