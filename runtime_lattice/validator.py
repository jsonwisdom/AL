import json, sys
from pathlib import Path

PASS = "PASS"
WARN = "WARN"
FAIL = "FAIL"
UNSAFE = "CONSTITUTIONALLY_UNSAFE"
REQUIRED = ["mutation_id", "parent_deployment_id", "parent_checkpoint_hash", "timestamp_unix_ms", "override_actor", "policy_delta", "affected_behavior_classes", "beneficiary_projection", "runtime_delta_hash", "dissent_log_append"]

def validate_record(record):
    missing = [k for k in REQUIRED if k not in record]
    if missing:
        return FAIL, f"missing required fields: {missing}"
    confidence = record["beneficiary_projection"].get("confidence", 0)
    if confidence < 0.7:
        return WARN, "beneficiary confidence below threshold"
    if not record.get("runtime_delta_hash"):
        return FAIL, "missing runtime_delta_hash"
    return PASS, "record valid"

def enforce_runtime_legality(policy_before, policy_after, first_affected_query_ms, mutation_record):
    if policy_before == policy_after:
        return PASS, "no runtime behavior fork"
    if mutation_record is None:
        return UNSAFE, "behavior changed without prior mutation record"
    status, reason = validate_record(mutation_record)
    if status == FAIL:
        return FAIL, reason
    if mutation_record["timestamp_unix_ms"] >= first_affected_query_ms:
        return UNSAFE, "mutation timestamp is not prior to first affected query"
    if status == WARN:
        return WARN, reason
    return PASS, "mutation logged before affected behavior"

if __name__ == "__main__":
    record = json.loads(Path(sys.argv[1]).read_text()) if len(sys.argv) > 1 else None
    print(validate_record(record))
