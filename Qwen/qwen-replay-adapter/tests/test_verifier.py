from qwen_replay.verifier import verify_receipt

BASE = {
    "run_id": "R",
    "call_index": 0,
    "tool_name": "t",
    "requested_arguments_hash": "sha256:a",
    "executed_arguments_hash": "sha256:a",
    "authorization": "ALLOWED",
    "mode": "OBSERVE",
    "execution_status": "COMPLETED",
    "output_hash": "sha256:o",
}


def test_missing_requested_hash_rejected():
    receipt = dict(BASE)
    del receipt["requested_arguments_hash"]
    assert verify_receipt(receipt).code == "MISSING_REQUESTED_HASH"


def test_missing_executed_hash_rejected():
    receipt = dict(BASE)
    del receipt["executed_arguments_hash"]
    assert verify_receipt(receipt).code == "MISSING_EXECUTED_HASH"


def test_mutation_without_source_rejected():
    receipt = dict(BASE, executed_arguments_hash="sha256:b")
    assert verify_receipt(receipt).code == "MUTATION_WITHOUT_SOURCE"
