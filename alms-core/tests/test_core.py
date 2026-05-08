import json, pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from src.validate import validate_claim, validate_bundle, validate_runtime
from src.judge_runtime import judge
from src.quorum import quorum

ROOT = pathlib.Path(__file__).resolve().parents[1]
def load(name): return json.loads((ROOT/'examples'/name).read_text())

def test_golden_hashes():
    claim=load('claim.pass.json'); bundle=load('bundle.pass.json'); runtime=load('runtime.pass.json')
    assert claim['claim_hash']=='sha256:e40ec1f8fbe50938b739a4c8e3ac74ed264e719a5d87b9be7e54d6364db18832'
    assert bundle['bundle_hash']=='sha256:2347b91688f2f2e52dfd85080737eea25707273032c283b27d536f46726c3480'
    assert runtime['runtime_hash']=='sha256:7ab21151c6096225b549a88381e2a5f0257046359fd50c4cc268183137e5b23e'
    validate_claim(claim); validate_bundle(bundle); validate_runtime(runtime)

def test_judge_pass_and_state_path():
    v=judge(load('claim.pass.json'), load('bundle.pass.json'), load('runtime.pass.json'))
    assert v['verdict']=='PASS'
    assert v['state_path'][0]=='INIT' and v['state_path'][-1]=='HALT'

def test_hash_forgery_rejected():
    c=load('claim.pass.json'); c['claimant_id']='evil'
    try: validate_claim(c)
    except ValueError as e: assert 'FAIL_CLAIM_HASH_MISMATCH' in str(e)
    else: raise AssertionError('forgery accepted')

def test_quorum_exact_match_and_divergence():
    c,b,r=load('claim.pass.json'),load('bundle.pass.json'),load('runtime.pass.json')
    v1=judge(c,b,r,'o1'); v2=judge(c,b,r,'o2')
    assert quorum([v1,v2],2)['final_verdict']=='PASS'
    v2['failure_code']='DIFFERENT_WHITESPACE_OR_FIELD'
    assert quorum([v1,v2],2)['final_failure_code']=='FAIL_CONVERGENCE_FAILED'
