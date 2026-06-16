#!/usr/bin/env python3
import json
import sys

REJECTION = {
    "LATEST_EPOCH_AMBIGUITY": "LATEST_EPOCH_AMBIGUITY",
    "UNPROVABLE_OBLIGATION_MET": "UNPROVABLE_OBLIGATION_MET",
    "UNPROVABLE_DEONTIC_STATE": "UNPROVABLE_DEONTIC_STATE",
    "PRIVILEGED_INTERPRETER_ATTEMPT": "PRIVILEGED_INTERPRETER_ATTEMPT",
    "PROOF_BOUNDS_EXCEEDED": "PROOF_BOUNDS_EXCEEDED",
    "RAW_UNBOUNDED_EVIDENCE": "RAW_UNBOUNDED_EVIDENCE",
    "FEDERATION_ENFORCEMENT_ATTEMPT": "FEDERATION_ENFORCEMENT_ATTEMPT",
    "COMPACT_BASELINE_MUTATION_ATTEMPT": "COMPACT_BASELINE_MUTATION_ATTEMPT"
}

FORBIDDEN_KEYS = {
    "latest_epoch",
    "current_state",
    "obligation_met",
    "federation_verdict",
    "global_compliance"
}

DEONTIC_TERMS = {
    "MUST",
    "SHALL",
    "MANDATORY",
    "PENALTY"
}

MAX_FIELD_SIZE = 512


def reject(code):
    print(f"INVALID_ARTIFACT:{code}")
    sys.exit(1)


def scan(obj):
    if isinstance(obj, dict):
        for k, v in obj.items():
            if k in FORBIDDEN_KEYS:
                if k == "latest_epoch":
                    reject(REJECTION["LATEST_EPOCH_AMBIGUITY"])
                if k == "obligation_met":
                    reject(REJECTION["UNPROVABLE_OBLIGATION_MET"])
                reject(REJECTION["FEDERATION_ENFORCEMENT_ATTEMPT"])

            if isinstance(v, str):
                if len(v) > MAX_FIELD_SIZE:
                    reject(REJECTION["PROOF_BOUNDS_EXCEEDED"])

                upper = v.upper()
                for term in DEONTIC_TERMS:
                    if term in upper:
                        reject(REJECTION["UNPROVABLE_DEONTIC_STATE"])

                if "RAW_EVIDENCE" in upper:
                    reject(REJECTION["RAW_UNBOUNDED_EVIDENCE"])

            scan(v)

    elif isinstance(obj, list):
        for item in obj:
            scan(item)


def main():
    if len(sys.argv) != 2:
        print("Usage: validate_federation_v2_artifact.py <artifact.json>")
        sys.exit(1)

    path = sys.argv[1]

    try:
        with open(path, "r", encoding="utf-8") as f:
            artifact = json.load(f)
    except Exception:
        reject("INVALID_JSON")

    scan(artifact)

    print("VALID_FEDERATION_V2_ARTIFACT")
    sys.exit(0)


if __name__ == "__main__":
    main()
