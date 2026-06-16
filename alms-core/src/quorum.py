from .hash import hash_object_null_field

def quorum(verdicts: list[dict], minimum_honest: int) -> dict:
    if len(verdicts) < minimum_honest:
        final, failure = 'INCONCLUSIVE', 'FAIL_INSUFFICIENT_VERDICTS'
    else:
        keys = [(v['claim_id'], v['bundle_id'], v['verdict'], v['failure_code']) for v in verdicts]
        if len(set(keys)) == 1:
            final, failure = verdicts[0]['verdict'], verdicts[0]['failure_code']
        else:
            final, failure = 'INCONCLUSIVE', 'FAIL_CONVERGENCE_FAILED'
    r = {'receipt_version':'ALMS_QUORUM_RECEIPT_V0_1','claim_id':verdicts[0].get('claim_id') if verdicts else None,'bundle_id':verdicts[0].get('bundle_id') if verdicts else None,'quorum_parameters':{'total_observers':len(verdicts),'minimum_honest':minimum_honest,'convergence_rule':'EXACT_MATCH_ON_ALL_FIELDS'},'verdicts_received':len(verdicts),'final_verdict':final,'final_failure_code':failure,'observer_signatures':None,'created_at':'2026-05-08T00:00:00Z','receipt_hash':None}
    r['receipt_hash'] = hash_object_null_field(r, 'receipt_hash')
    return r
