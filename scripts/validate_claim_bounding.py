#!/usr/bin/env python3
import json
import sys

TEMPORAL_LEAKS = ["as of today","currently","still","now","at present"]


def references_external(statement):
    s = statement.lower()
    return any(t in s for t in TEMPORAL_LEAKS)


def validate_claim(c):
    ctype = c["type"]
    status = c["status"]
    stmt = c["statement"]

    if ctype == "EXISTENCE":
        return "PASS"

    if ctype == "FACTUAL":
        if references_external(stmt):
            return "DOWNGRADE"
        return "DOWNGRADE"  # default: cannot verify factual from bytes

    if ctype == "INTERPRETATION":
        if status == "VERIFIED":
            return "REJECT"
        return "PASS"

    return "REJECT"


def main():
    if len(sys.argv) != 2:
        print("Usage: validate_claim_bounding.py <ledger.json>")
        sys.exit(1)

    with open(sys.argv[1]) as f:
        ledger = json.load(f)

    failures = []

    for c in ledger["claims"]:
        result = validate_claim(c)
        expected = c.get("expected_validator_result", "PASS")

        if result != expected:
            failures.append((c["claim_id"], result, expected))

    if failures:
        print("BOUNDING FAILURE:")
        for f in failures:
            print(f)
        sys.exit(1)

    print("ALL CLAIMS WITHIN BOUNDS")


if __name__ == "__main__":
    main()
