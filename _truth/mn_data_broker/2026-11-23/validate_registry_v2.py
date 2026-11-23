#!/usr/bin/env python3
"""CI-FIRST v1.3, read-only structural/evidence-state validator.

PASS means checks passed, not that a procurement occurred. Missing evidence remains HOLD.
Never contacts an agency or changes an input. External-original bytes must be supplied
through --original-document to make a digest meaningful.
"""
import argparse
import hashlib
import json
import re
import sys
from pathlib import Path

HEX64 = re.compile(r"^[a-fA-F0-9]{64}$")
FK = re.compile(r"^([a-z_]+) -> ([a-z_]+)\.([a-z_]+)(?: \(nullable(?: for statewide)?\))?$")
ID_FIELDS = {
    "agencies": "agency_id", "vendors": "vendor_id", "contracts": "contract_id",
    "purchase_orders": "purchase_order_id", "invoices": "invoice_id",
    "payments": "payment_id", "datasets": "dataset_id",
    "authorizations": "authorization_id", "source_documents": "document_id",
    "court_application_reporting": "report_id",
}
VALID_STATES = {"UNKNOWN", "HOLD", "NOT_ESTABLISHED", "VERIFIED", "REJECTED", "NOT_APPLICABLE"}
EXPECTED_AGENCIES = {"MN-DPS-BCA", "MN-DOC"}
EXPECTED_TABLES = {
    "agencies", "vendors", "contracts", "contract_agencies", "purchase_orders",
    "invoices", "payments", "datasets", "authorizations", "source_documents",
    "court_application_reporting",
}
# Pinned hash of (jurisdiction_id, county_name) pairs from the verified
# 87-county baseline roster; locks against silent substitution, NOT an
# independent verification that an agency made any purchase.
EXPECTED_ROSTER_SHA256 = "548fadddf7baeeac0ae6f7ce6f6ada9f03a22711bf185a44063d5ccf463cb1dc"


def _roster_digest(counties):
    pairs = [[row.get("jurisdiction_id"), row.get("county_name")] for row in counties]
    return hashlib.sha256(json.dumps(pairs, separators=(",", ":"), ensure_ascii=False).encode()).hexdigest()


def validate(registry, model, original_documents=None):
    errors, holds = [], []
    originals = original_documents or {}
    counties = registry.get("counties", [])
    if not isinstance(counties, list):
        return {"verdict": "FAIL", "errors": ["INVALID_COUNTY_ROSTER"], "holds": []}
    county_ids = [c.get("jurisdiction_id") for c in counties]
    county_names = [c.get("county_name") for c in counties]
    if (len(counties) != 87 or registry.get("scope_counties") != 87
            or len(set(county_ids)) != 87 or len(set(county_names)) != 87
            or any(not v for v in county_ids + county_names)
            or any(c.get("jurisdiction_id") != f"MN-COUNTY-{i:03d}" for i, c in enumerate(counties, 1))
            or _roster_digest(counties) != EXPECTED_ROSTER_SHA256):
        errors.append("INVALID_COUNTY_ROSTER")

    listed_agencies = registry.get("agencies")
    if (not isinstance(listed_agencies, list) or len(listed_agencies) != 2
            or {a.get("agency_id") for a in listed_agencies} != EXPECTED_AGENCIES
            or any(a.get("status") != "HOLD_NOT_SENT" for a in listed_agencies)):
        errors.append("INVALID_AGENCY_ROSTER")
    controls = model.get("controls", {})
    if (registry.get("external_agency_requests_authorized") is not False
            or controls.get("transmission_authorized") is not False
            or controls.get("dps_bca") != "HOLD_NOT_SENT"
            or controls.get("doc") != "HOLD_NOT_SENT"):
        errors.append("UNAUTHORIZED_TRANSMISSION")
    if controls.get("production_merge_authorized") is not False:
        errors.append("UNAUTHORIZED_MERGE")
    if controls.get("cloudflare_deploy_authorized") is not False:
        errors.append("UNAUTHORIZED_DEPLOYMENT")

    tables = model.get("tables", {})
    if (not isinstance(tables, dict) or set(tables) != EXPECTED_TABLES
            or any(not isinstance(v, list) or any(not isinstance(r, dict) for r in v)
                   for v in tables.values())):
        errors.append("INVALID_TABLES")
        return {"verdict": "FAIL", "errors": sorted(set(errors)), "holds": []}

    required = model.get("required_fields", {})
    keys = {}
    for table, rows in tables.items():
        pk = ID_FIELDS.get(table)
        if pk:
            ids = [r.get(pk) for r in rows]
            if len(ids) != len(set(ids)):
                errors.append(f"DUPLICATE_ID:{table}")
            keys[table] = {x for x in ids if x not in (None, "")}
        for row in rows:
            for field in required.get(table, []):
                if row.get(field) in (None, ""):
                    errors.append(f"MISSING_REQUIRED_FIELD:{table}.{field}")
            state = row.get("verification_status")
            if state is not None and state not in VALID_STATES:
                errors.append(f"INVALID_CLASSIFICATION:{table}")
            elif state in {"UNKNOWN", "HOLD", "NOT_ESTABLISHED"}:
                holds.append(f"UNVERIFIED_RECORD:{table}")

    fk_spec = model.get("foreign_keys", {})
    if set(fk_spec) != EXPECTED_TABLES:
        errors.append("INVALID_FOREIGN_KEY_SPEC:TABLE_SET")
    all_foreign_keys = {}
    for table, specifications in fk_spec.items():
        all_foreign_keys[table] = []
        for spec in specifications:
            parsed = FK.fullmatch(spec)
            if not parsed:
                errors.append(f"INVALID_FOREIGN_KEY_SPEC:{table}:{spec}")
                continue
            field, parent, parent_field = parsed.groups()
            expected_field = ("jurisdiction_id" if parent == "counties"
                              else ID_FIELDS.get(parent))
            if parent_field != expected_field or parent not in (EXPECTED_TABLES | {"counties"}):
                errors.append(f"INVALID_FOREIGN_KEY_TARGET:{table}.{field}")
                continue
            # The FK field must exist in the model's requirements or be a
            # documented optional FK with known meaning. A made-up FK field
            # cannot be used to defeat verification on an empty table.
            if field not in required.get(table, []) and (table, field) not in {
                ("agencies", "county_id"), ("purchase_orders", "contract_id"),
                ("invoices", "purchase_order_id"), ("payments", "invoice_id")
            }:
                errors.append(f"INVALID_FOREIGN_KEY_FIELD:{table}.{field}")
            all_foreign_keys[table].append((field, parent, "(nullable" in spec))

    # Required relations absent from the original v1.1 metadata are still
    # enforced. Source document agency is mandatory, not silently nullable.
    for table, field, parent in [
        ("source_documents", "agency_id", "agencies"),
        ("court_application_reporting", "source_document_id", "source_documents")
    ]:
        if (field, parent, False) not in all_foreign_keys.get(table, []):
            all_foreign_keys.setdefault(table, []).append((field, parent, False))

    for table, fks in all_foreign_keys.items():
        for field, parent, nullable in fks:
            targets = set(county_ids) if parent == "counties" else keys.get(parent, set())
            for row in tables.get(table, []):
                value = row.get(field)
                if value in (None, ""):
                    if not nullable:
                        errors.append(f"ORPHAN_FOREIGN_KEY:{table}.{field}")
                elif value not in targets:
                    errors.append(f"ORPHAN_FOREIGN_KEY:{table}.{field}")

    contract_ids = [r.get("contract_id") for r in tables["contracts"]]
    if len(contract_ids) != len(set(contract_ids)):
        errors.append("DUPLICATE_CONTRACT")
    relationships = [(r.get("contract_id"), r.get("agency_id"))
                     for r in tables["contract_agencies"]]
    if len(relationships) != len(set(relationships)):
        errors.append("DUPLICATE_CONTRACT_AGENCY")
    relationship_set = set(relationships)
    for contract in tables["contracts"]:
        if (contract.get("contract_id"), contract.get("agency_id")) not in relationship_set:
            errors.append("MISSING_CONTRACT_AGENCY_LINK")

    docs = {d.get("document_id"): d for d in tables["source_documents"]}
    verified_docs = set()
    for document in tables["source_documents"]:
        did, expected = document.get("document_id"), document.get("sha256_original")
        if not isinstance(expected, str) or not HEX64.fullmatch(expected):
            errors.append(f"INVALID_SHA256:{did}")
            continue
        original = originals.get(did)
        if original is None:
            holds.append(f"INCOMPLETE_SOURCE_ORIGINAL:{did}")
            if document.get("verification_status") == "VERIFIED":
                errors.append(f"INVALID_VERIFICATION_CLAIM:{did}")
            continue
        if not isinstance(original, bytes) or hashlib.sha256(original).hexdigest().lower() != expected.lower():
            errors.append(f"SHA256_MISMATCH:{did}")
            continue
        if document.get("verification_status") == "VERIFIED":
            if (str(document.get("source_type", "")).casefold() in {"synthetic", "fixture", "test"}
                    or str(document.get("source_url_or_identifier", "")).casefold().startswith("synthetic")):
                errors.append(f"SYNTHETIC_CANNOT_BE_VERIFIED:{did}")
            else:
                verified_docs.add(did)
    for table, records in tables.items():
        if table in {"source_documents", "agencies", "vendors", "contract_agencies"}:
            continue
        for record in records:
            if record.get("verification_status") == "VERIFIED":
                did = record.get("source_document_id")
                if did not in verified_docs:
                    errors.append(f"UNVERIFIED_PROVENANCE:{table}")

    if errors:
        verdict = "FAIL"
    elif holds:
        verdict = "HOLD"
    else:
        verdict = "PASS"
    return {"verdict": verdict, "errors": sorted(set(errors)), "holds": sorted(set(holds)),
            "county_count": len(counties),
            "record_counts": {k: len(v) for k, v in tables.items()},
            "evidence_claim": "NO PROCUREMENT ESTABLISHED" if not any(tables.values())
            else "REQUIRES DOCUMENT-SPECIFIC REVIEW"}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--registry", required=True)
    parser.add_argument("--model", required=True)
    parser.add_argument("--original-document", action="append", default=[])
    opts = parser.parse_args()
    originals = {}
    for item in opts.original_document:
        if "=" not in item:
            parser.error("expected document_id=path")
        did, path = item.split("=", 1)
        originals[did] = Path(path).read_bytes()
    report = validate(json.loads(Path(opts.registry).read_text()),
                      json.loads(Path(opts.model).read_text()), originals)
    print(json.dumps(report, sort_keys=True, indent=2))
    return {"PASS": 0, "FAIL": 1, "HOLD": 2}[report["verdict"]]


if __name__ == "__main__":
    sys.exit(main())
