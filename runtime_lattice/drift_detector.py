import hashlib, time

def sha3_text(value: str) -> str:
    return "sha3-256:" + hashlib.sha3_256(value.encode("utf-8")).hexdigest()

def now_ms() -> int:
    return int(time.time() * 1000)

def detect_runtime_drift(model_api, baseline_logits, protected_classes, threshold=0.05):
    for class_name, queries in protected_classes.items():
        for query in queries:
            current = model_api.logits(query)
            baseline = baseline_logits[query]
            refusal_shift = current["refusal_prob"] - baseline["refusal_prob"]
            if abs(refusal_shift) > threshold:
                return {
                    "drift_type": "refusal_rate",
                    "behavior_class": class_name,
                    "delta": refusal_shift,
                    "query_hash": sha3_text(query),
                    "timestamp_unix_ms": now_ms()
                }
    return None
