#!/usr/bin/env python3
import json
import sys
from pathlib import Path

def get(d, path, default=None):
    cur = d
    for key in path.split("."):
        if not isinstance(cur, dict) or key not in cur:
            return default
        cur = cur[key]
    return cur

def main():
    if len(sys.argv) != 2:
        print("Usage: metrics.py <result_json_path>")
        return 1

    path = Path(sys.argv[1])
    if not path.exists():
        print(f"FAIL: missing result JSON: {path}")
        return 1

    data = json.loads(path.read_text())
    reasons = []

    assigned = set(data.get("tasks_assigned", []))
    completed = set(data.get("tasks_completed", []))
    failed = data.get("tasks_failed", [])

    checks = [
        (data.get("overall_status") == "completed", "overall_status must be completed"),
        (assigned == completed and bool(assigned), "tasks_assigned must equal tasks_completed and be non-empty"),
        (failed == [], "tasks_failed must be empty"),
        (get(data, "metrics.unintended_edits") == 0, "metrics.unintended_edits must equal 0"),
        (get(data, "metrics.state_loss_incidents") == 0, "metrics.state_loss_incidents must equal 0"),
        (get(data, "metrics.hallucinated_commands_executed") == 0, "metrics.hallucinated_commands_executed must equal 0"),
        (get(data, "verification.tests_passed") is True, "verification.tests_passed must be true"),
        (bool(get(data, "verification.commit_hash")), "verification.commit_hash required"),
        (bool(get(data, "verification.pr_url")), "verification.pr_url required"),
        (get(data, "verification.logs_attached") is True, "verification.logs_attached must be true"),
    ]

    for ok, reason in checks:
        if not ok:
            reasons.append(reason)

    status = "PASS" if not reasons else "FAIL"
    print(f"Status: {status}")
    print(f"Run ID: {data.get('run_id')}")
    print(f"Tasks: {len(completed)}/{len(assigned)} completed")
    print(f"Constraints: {', '.join(data.get('constraints_active', []))}")
    if reasons:
        print("Failure Reasons:")
        for r in reasons:
            print(f"- {r}")
    return 0 if status == "PASS" else 1

if __name__ == "__main__":
    raise SystemExit(main())
