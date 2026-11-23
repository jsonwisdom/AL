#!/usr/bin/env python3
"""All fixtures synthetic, no source-document claims about government purchases."""
import copy
import hashlib
import json
import unittest
from pathlib import Path
from validate_registry_v2 import validate

P=Path(__file__).parent
BASE=json.loads((P/'registry-87-counties-v1.json').read_text())
MODEL=json.loads((P/'relationship-model-v1.json').read_text())

class Adversarial(unittest.TestCase):
    def chk(self,mutator,expected,needle=None,originals=None):
        reg,mod=copy.deepcopy(BASE),copy.deepcopy(MODEL)
        mutator(reg,mod)
        out=validate(reg,mod,originals)
        self.assertEqual(out['verdict'],expected,out)
        if needle:self.assertTrue(any(needle in x for x in out['errors']+out['holds']),out)
    def test_roster_complete(self):self.chk(lambda r,m:r['agencies'].pop(),'FAIL','INVALID_AGENCY_ROSTER')
    def test_duplicate_county_name(self):self.chk(lambda r,m:r['counties'][0].update(county_name=r['counties'][1]['county_name']),'FAIL','INVALID_COUNTY_ROSTER')
    def test_substituted_county_name(self):self.chk(lambda r,m:r['counties'][0].update(county_name='Synthetic County'),'FAIL','INVALID_COUNTY_ROSTER')
    def test_invalid_fk_column_empty_table(self):self.chk(lambda r,m:m['foreign_keys']['contracts'].__setitem__(0,'agency_id -> agencies.vendor_id'),'FAIL','INVALID_FOREIGN_KEY_TARGET')
    def test_verified_synthetic_with_matching_hash(self):
        def mutate(r,m):
            m['tables']['agencies'].append({'agency_id':'SYN-A','agency_name':'Synthetic','jurisdiction_level':'state','verification_status':'UNKNOWN'})
            m['tables']['source_documents'].append({'document_id':'SYN-D','agency_id':'SYN-A','source_url_or_identifier':'synthetic://test','verified_at_utc':'2026-11-23T00:00:00Z','sha256_original':hashlib.sha256(b'x').hexdigest(),'source_type':'synthetic','verification_status':'VERIFIED'})
        self.chk(mutate,'FAIL','SYNTHETIC_CANNOT_BE_VERIFIED',{'SYN-D':b'x'})
    def test_missing_document_agency(self):
        def mutate(r,m):
            m['tables']['source_documents'].append({'document_id':'SYN-D','source_url_or_identifier':'synthetic://test','verified_at_utc':'2026-11-23T00:00:00Z','sha256_original':hashlib.sha256(b'x').hexdigest(),'source_type':'synthetic','verification_status':'UNKNOWN'})
        self.chk(mutate,'FAIL','MISSING_REQUIRED_FIELD:source_documents.agency_id')
    def test_missing_original_with_valid_agency_hold(self):
        def mutate(r,m):
            m['tables']['agencies'].append({'agency_id':'SYN-A','agency_name':'Synthetic','jurisdiction_level':'state','verification_status':'UNKNOWN'})
            m['tables']['source_documents'].append({'document_id':'SYN-D','agency_id':'SYN-A','source_url_or_identifier':'synthetic://test','verified_at_utc':'2026-11-23T00:00:00Z','sha256_original':hashlib.sha256(b'x').hexdigest(),'source_type':'synthetic','verification_status':'UNKNOWN'})
        self.chk(mutate,'HOLD','INCOMPLETE_SOURCE_ORIGINAL')
    def test_empty_structural_pass(self):self.chk(lambda r,m:None,'PASS')
if __name__=='__main__':unittest.main(verbosity=2)
