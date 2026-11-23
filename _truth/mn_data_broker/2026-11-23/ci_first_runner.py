#!/usr/bin/env python3
"""CI-FIRST read-only draft-only build; never deploy or send agency requests."""
import hashlib, json, os, subprocess, sys, traceback
from pathlib import Path

ROOT = Path(__file__).resolve().parent
OUT = ROOT / 'ci_artifacts'
PIN = {
 'registry-87-counties-v1.json':('a38b4d63a53837ac09be0509676259e005d0a460','17216186575b843ca992e7acb8f7c00d83eef4fa0a99f201df3da344caaf342e'),
 'relationship-model-v1.json':('aa0b65d72ba5b4ebb85249fd7bc75f4c1e068ea8','e6902390b7691bd156a7800a705d8bbfeaff9fe6aa311929d0492d895546bb4a'),
 'validate_registry.py':('135597a613c41152ee2d4106b8a2ff4e5466bb00','09a8a0bd168bde4f99b575a48b0a3b586e295c4d9a7a5ccf4fb103802c9dce33'),
 'test_registry_validator.py':('83c56cf005a7a3790d4697e83cdd8114b60f93f4','08ab8196afbda2ba3bc29c1750d89b3665fd247fc71f42527702a4d0f11b7191'),
 'validate_registry_v2.py':('9bce3d239fc0c6b4d74fa5a50a5c670664989752','926a195b5b03c13438e8d251de37d102fb0860de627797401a98c8b5422687d0'),
 'test_validator_v2_adversarial.py':('bf028e721441c0bbad5d2c0d74cf8414ec7a4a29','a054c9f8d59c3b9f8792bb07d897effa53681ce841e30233b408655dc63594ed'),
 'fuzz_validator_v2.py':('5b904100401b057f2159257103772c4c775a7687','5e1e3ab922eec419445477dc8609e32117c9f8d1c49d0aadec43d08d38d19916'),
 'test_registry_validator_corrected_v2.py':('54e031e8131078635d8d7eb5eec23a00526584af','31834d315e6c62e35cf0dc549500c087cd5f406c48ebb0edbbbd383d3b3dfb46')
}

def sha(b): return hashlib.sha256(b).hexdigest()
def check(test,msg):
    if not test: raise AssertionError(msg)

def main():
    OUT.mkdir(exist_ok=True)
    succeeded=False
    stage='hash_gate'
    try:
        baseline=[]
        for name,(blob,sha256) in PIN.items():
            b=(ROOT/name).read_bytes()
            gh=subprocess.check_output(['git','hash-object',str(ROOT/name)],text=True).strip()
            check((gh,sha(b))==(blob,sha256),f'SOURCE_HASH_MISMATCH:{name}')
            baseline.append(f'PASS {name} GitBlob={blob} SHA256={sha256}')
        reg=json.loads((ROOT/'registry-87-counties-v1.json').read_text())
        mod=json.loads((ROOT/'relationship-model-v1.json').read_text())
        check(len(reg['counties'])==87,'COUNTY_COUNT')
        check(len({c['county_name'] for c in reg['counties']})==87,'COUNTY_NAME_DUPLICATE')
        check(len({c['jurisdiction_id'] for c in reg['counties']})==87,'COUNTY_ID_DUPLICATE')
        check(all(c['procurement_status']=='UNKNOWN' and c['transmission_status']=='NOT_AUTHORIZED' for c in reg['counties']),'COUNTY_HOLD')
        check(len(mod['tables'])==11 and all(not t for t in mod['tables'].values()),'NONEMPTY_RELATIONSHIP_TABLES')
        check(all(not t for t in reg['records'].values()),'NONEMPTY_BASELINE_EVIDENCE')
        check({a['agency_id'] for a in reg['agencies']}=={'MN-DPS-BCA','MN-DOC'},'AGENCY_ROSTER')
        check(all(a['status']=='HOLD_NOT_SENT' for a in reg['agencies']),'AGENCY_SENT')
        ctl=mod['controls']
        check(reg['external_agency_requests_authorized'] is False,'AGENCY_REQUEST_AUTH')
        check(ctl['dps_bca']==ctl['doc']=='HOLD_NOT_SENT','MGDPA_HOLD')
        for k in ('transmission_authorized','cloudflare_deploy_authorized','production_merge_authorized'):
            check(ctl[k] is False,f'UNAUTHORIZED_GATE:{k}')
        (OUT/'baseline_gate.log').write_text('\n'.join(baseline)+'\nPASS: 87 unique counties; 11 empty tables; all HOLD controls\n')
        stage='unit_adversarial'
        cmd=[sys.executable,'-m','unittest','-v','test_registry_validator_corrected_v2','test_validator_v2_adversarial']
        proc=subprocess.run(cmd,cwd=ROOT,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True)
        (OUT/'unit_adversarial.log').write_text(proc.stdout)
        check(proc.returncode==0,'UNIT_ADVERSARIAL_FAILED')
        check('Ran 17 tests' in proc.stdout and '\nOK\n' in proc.stdout,'UNIT_COUNT_NOT_17')
        stage='seeded_fuzz'
        proc=subprocess.run([sys.executable,'fuzz_validator_v2.py','--seed','20261123','--iterations','280'],cwd=ROOT,capture_output=True,text=True)
        (OUT/'fuzz_stderr.log').write_text(proc.stderr)
        check(proc.returncode==0,'FUZZ_EXIT_NONZERO')
        (OUT/'fuzz_results.json').write_text(proc.stdout)
        f=json.loads(proc.stdout)
        check((f['seed'],f['cases'],f['passed'],f['failed'])==(20261123,280,280,0),'FUZZ_CASE_MISMATCH')
        check(len(f['family_counts'])==7 and set(f['family_counts'].values())=={40},'FUZZ_FAMILY_MISMATCH')
        check(all(x['pass'] for x in f['case_results']),'FUZZ_INVARIANT_MISMATCH')
        digests='\n'.join(x['input_sha256'] for x in f['case_results'])+'\n'
        check(sha(digests.encode())=='6f621036697a7442dbdfa09f803abf1813303398f4d2e7562c1452e9b5906c93','FUZZ_CORPUS_HASH_MISMATCH')
        (OUT/'case_input_digests.txt').write_text(digests)
        (OUT/'fuzz_gate.log').write_text('PASS 280/280 seed=20261123 families=7x40 corpus_sha256='+sha(digests.encode())+'\n')
        succeeded=True
        print('CI-FIRST PASS: pinned hashes, 17 unit/adversarial, 280 fuzz; software only')
    except Exception:
        (OUT/'failure.log').write_text(f'STAGE:{stage}\n'+traceback.format_exc())
        print(f'CI-FIRST FAIL at {stage}',file=sys.stderr)
    finally:
        inputs={n:sha((ROOT/n).read_bytes()) for n in PIN if (ROOT/n).exists()}
        logs={p.name:sha(p.read_bytes()) for p in sorted(OUT.iterdir()) if p.is_file()}
        manifest={'receipt':'MN-DATA-BROKER-2026-11-23','disposition':'STATEWIDE_SCOPE_HOLD',
          'result':'PASS' if succeeded else 'FAIL','last_stage':stage,
          'commit':os.getenv('GITHUB_SHA'),'branch':os.getenv('GITHUB_REF'),
          'build_type':'DRAFT_ONLY','staging_candidate':False,'promotion':False,'deployment':False,
          'agency_contact':False,'mgdpa_sent':False,'procurement_evidence_established':False,
          'input_sha256':inputs,'log_sha256':logs}
        (OUT/'draft_build_manifest.json').write_text(json.dumps(manifest,indent=2,sort_keys=True)+'\n')
        (OUT/'artifact_sha256.txt').write_text(''.join(f'{sha(p.read_bytes())}  {p.name}\n' for p in sorted(OUT.iterdir()) if p.is_file()))
    return 0 if succeeded else 1

if __name__=='__main__':sys.exit(main())
