#!/usr/bin/env python3
"""Synthetic tests ONLY. Never use synthetic fixtures as procurement evidence."""
import copy,hashlib,json,sys,unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).parent))
from validate_registry import validate

class Tests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
    p=Path(__file__).parent
    cls.reg=json.loads((p/"registry-87-counties-v1.json").read_text())
    cls.mod=json.loads((p/"relationship-model-v1.json").read_text())
 def check(self, mut, status, prefix=None, originals=None):
    r,m=copy.deepcopy(self.reg),copy.deepcopy(self.mod)
    mut(r,m)
    out=validate(r,m,originals)
    self.assertEqual(out["verdict"],status,out)
    if prefix:self.assertTrue(any(x.startswith(prefix) for x in out["errors"]+out["holds"]),out)
 def test_empty_holds_structurally_pass(self):
    self.check(lambda r,m:None,"PASS")
 def test_county_duplicate(self):
    self.check(lambda r,m:r["counties"].append(r["counties"][0]),"FAIL","INVALID_COUNTY_ROSTER")
 def test_transmission_fail(self):
    self.check(lambda r,m:m["controls"].update(transmission_authorized=True),"FAIL","UNAUTHORIZED_TRANSMISSION")
 def test_orphan_contract_fail(self):
    self.check(lambda r,m:m["tables"]["contract_agencies"].append({"contract_id":"C1","agency_id":"A1"}),"FAIL","ORPHAN_FOREIGN_KEY")
 def test_duplicate_contract_agency_fail(self):
    def change(r,m):
        m["tables"]["agencies"].append({"agency_id":"A1","agency_name":"SYNTHETIC","jurisdiction_level":"state","verification_status":"UNKNOWN"})
        m["tables"]["vendors"].append({"vendor_id":"V1","vendor_name":"SYNTHETIC","verification_status":"UNKNOWN"})
        m["tables"]["source_documents"].append({"document_id":"D1","agency_id":"A1","source_url_or_identifier":"synthetic","verified_at_utc":"2026-11-23T00:00:00Z","sha256_original":hashlib.sha256(b"x").hexdigest(),"source_type":"synthetic","verification_status":"UNKNOWN"})
        m["tables"]["contracts"].append({"contract_id":"C1","agency_id":"A1","vendor_id":"V1","source_document_id":"D1","verification_status":"UNKNOWN"})
        m["tables"]["contract_agencies"].extend([{"contract_id":"C1","agency_id":"A1"}]*2)
    self.check(change,"FAIL","DUPLICATE_CONTRACT_AGENCY")
 def test_invalid_hash_fail(self):
    self.check(lambda r,m:m["tables"]["source_documents"].append({"document_id":"D","agency_id":"A","source_url_or_identifier":"synthetic","verified_at_utc":"2026-11-23T00:00:00Z","sha256_original":"abc","source_type":"synthetic","verification_status":"UNKNOWN"}),"FAIL","INVALID_SHA256")
 def test_bad_classification_fail(self):
    self.check(lambda r,m:m["tables"]["vendors"].append({"vendor_id":"V","vendor_name":"SYNTHETIC","verification_status":"PURCHASE_PROVEN_BY_ASSUMPTION"}),"FAIL","INVALID_CLASSIFICATION")
 def test_original_required_hold(self):
    def change(r,m):
        m["tables"]["source_documents"].append({"document_id":"D","agency_id":None,"source_url_or_identifier":"synthetic","verified_at_utc":"2026-11-23T00:00:00Z","sha256_original":hashlib.sha256(b"x").hexdigest(),"source_type":"synthetic","verification_status":"UNKNOWN"})
    self.check(change,"HOLD","INCOMPLETE_SOURCE_ORIGINAL")
 def test_original_hash_mismatch_fail(self):
    def change(r,m):
        m["tables"]["source_documents"].append({"document_id":"D","agency_id":None,"source_url_or_identifier":"synthetic","verified_at_utc":"2026-11-23T00:00:00Z","sha256_original":hashlib.sha256(b"x").hexdigest(),"source_type":"synthetic","verification_status":"UNKNOWN"})
    self.check(change,"FAIL","SHA256_MISMATCH",{"D":b"y"})
if __name__=="__main__": unittest.main(verbosity=2)
