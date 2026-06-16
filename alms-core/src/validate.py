from .hash import hash_object_null_field

SHA_PREFIX = 'sha256:'

def require_hash(value: str) -> None:
    if not isinstance(value, str) or not value.startswith(SHA_PREFIX) or len(value) != 71:
        raise ValueError('invalid sha256 hash')
    int(value[7:], 16)

def validate_claim(claim: dict) -> None:
    for k in ['skill_hash','policy_hash','input_hash','tool_graph_hash','trace_hash','output_hash','eval_suite_hash','replay_bundle_hash','claim_hash']:
        require_hash(claim[k])
    if hash_object_null_field(claim, 'claim_hash') != claim['claim_hash']:
        raise ValueError('FAIL_CLAIM_HASH_MISMATCH')

def validate_bundle(bundle: dict) -> None:
    require_hash(bundle['bundle_hash'])
    if hash_object_null_field(bundle, 'bundle_hash') != bundle['bundle_hash']:
        raise ValueError('FAIL_BUNDLE_HASH_MISMATCH')

def validate_runtime(runtime: dict) -> None:
    require_hash(runtime['runtime_hash'])
    if hash_object_null_field(runtime, 'runtime_hash') != runtime['runtime_hash']:
        raise ValueError('FAIL_RUNTIME_HASH_MISMATCH')
