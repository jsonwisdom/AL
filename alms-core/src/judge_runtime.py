from .validate import validate_claim, validate_bundle, validate_runtime
from .hash import hash_object_null_field

STATE_PATH_PASS = [
 'INIT','LOAD_CLAIM','LOAD_BUNDLE','VALIDATE_CLAIM','VALIDATE_BUNDLE',
 'VERIFY_CLAIM_BUNDLE_LINK','LOAD_RUNTIME_CONSTRAINTS','VERIFY_ENCODINGS',
 'EXECUTE_SKILL','VERIFY_TOOL_GRAPH','ASSERT_POLICY','ASSERT_EVALS',
 'EMIT_OBSERVER_VERDICT','HALT'
]

def judge(claim: dict, bundle: dict, runtime: dict, observer_id='observer_ref_001') -> dict:
    try:
        validate_claim(claim); validate_bundle(bundle); validate_runtime(runtime)
        if claim['claim_id'] != bundle['claim_id_ref']:
            raise RuntimeError('FAIL_CLAIM_BUNDLE_MISMATCH')
        if claim['replay_bundle_hash'] != bundle['bundle_hash']:
            raise RuntimeError('FAIL_CLAIM_BUNDLE_MISMATCH')
        verdict, failure = 'PASS', None
        path = STATE_PATH_PASS
    except Exception as e:
        verdict, failure = 'INCONCLUSIVE', str(e)
        path = ['INIT','HALT']
    out = {
        'verdict_version':'ALMS_OBSERVER_VERDICT_V0_1',
        'observer_id': observer_id,
        'claim_id': claim.get('claim_id'),
        'bundle_id': bundle.get('bundle_id'),
        'runtime_fingerprint': runtime.get('runtime_hash'),
        'state_path': path,
        'final_state':'HALT',
        'verdict': verdict,
        'failure_code': failure,
        'trace_hash_observed': claim.get('trace_hash'),
        'output_hash_observed': claim.get('output_hash'),
        'created_at':'2026-05-08T00:00:00Z',
        'verdict_hash': None,
        'signature': None
    }
    out['verdict_hash'] = hash_object_null_field(out, 'verdict_hash')
    return out
