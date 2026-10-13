from validator import enforce_runtime_legality

FIRST_AFFECTED_QUERY_MS = 1700000000100
BEFORE = "neutral_retrieval_policy"
AFTER = "chemcorp_ax7_sponsor_boost_policy"

print("[ATTACK] Injecting sponsor boost for ChemCorp_AX7 into retrieval layer...")
print("[BEHAVIOR] Ranking changed: competitor adverse-event pages suppressed.")
print("[MUTATION LOG] None found.")
verdict, reason = enforce_runtime_legality(BEFORE, AFTER, FIRST_AFFECTED_QUERY_MS, None)
print(f"\n[VERDICT] {verdict}")
print(f"[REASON] {reason}")
print("[REMEDY] Deployment must halt. Mutation logs required before traffic.")

print("\n--- RETRY WITH COMPLIANT MUTATION ---\n")

record = {
    "mutation_id": "sha3-256:" + "a"*64,
    "parent_deployment_id": "deployment-001",
    "parent_checkpoint_hash": "sha3-256:" + "b"*64,
    "timestamp_unix_ms": 1700000000000,
    "override_actor": {"type": "automated_policy", "identity_hash": "blind_sha3:policy-bot"},
    "policy_delta": {
        "before_hash": BEFORE,
        "after_hash": AFTER,
        "diff_summary": "retrieval_weights::sponsor_boost::+0.4"
    },
    "affected_behavior_classes": ["ranking::healthcare_provider_A"],
    "beneficiary_projection": {
        "direct_sponsor": "ChemCorp_AX7",
        "confidence": 0.87,
        "evidence": ["ranking_lift", "suppression_competitor"]
    },
    "runtime_delta_hash": "sha3-256:" + "c"*64,
    "dissent_log_append": ["minority_detector_3: possible_incentive_capture"]
}
verdict, reason = enforce_runtime_legality(BEFORE, AFTER, FIRST_AFFECTED_QUERY_MS, record)
print("[MUTATION LOG]")
print("  timestamp: 1700000000000")
print("  beneficiary_projection: ChemCorp_AX7 (0.87)")
print('  dissent: minority_detector_3 -> "possible_incentive_capture"')
print(f"\n[VERDICT] {'PASS_WITH_DISCLOSURE' if verdict == 'PASS' else verdict}")
print(f"[REASON] {reason}")
