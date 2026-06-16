#!/usr/bin/env python3
"""
Track 009: Policy Compliance Engine
"""

import json
import re
from pathlib import Path
from typing import Dict, List, Tuple

class PolicyEngine:
    def __init__(self, policy_path: Path = Path("_truth/audit/policy.json")):
        self.policy_path = policy_path
        self.policy = self._load_policy()
    
    def _load_policy(self) -> Dict:
        if not self.policy_path.exists():
            print("⚠️ Policy file not found, using minimal default")
            return {"policy_version": "1.0", "rules": []}
        with open(self.policy_path) as f:
            return json.load(f)
    
    def _evaluate_rule(self, rule: Dict, file_data: Dict) -> Tuple[bool, str]:
        field = rule.get('field')
        operator = rule['operator']
        expected = rule.get('value')
        actual = file_data.get(field) if field is not None else None

        if operator == 'absent':
            for f in (expected if isinstance(expected, list) else [expected]):
                if f in file_data:
                    return False, f"Deprecated field present: {f}"
            return True, ""
        if operator == 'present':
            if field not in file_data or file_data.get(field) is None:
                return False, f"Required field missing: {field}"
            return True, ""

        if operator == 'eq':
            return actual == expected, f"{field}: expected {expected}, got {actual}"
        if operator == 'in':
            return actual in expected, f"{field}: {actual} not in allowed set"
        if operator == 'regex':
            return bool(re.match(str(expected), str(actual or ""))), f"{field} failed regex"
        
        return False, f"Unknown operator {operator}"

    def validate(self, file_data: Dict) -> Dict:
        result = {"valid": True, "blocked": False, "warnings": [], "violations": []}
        for rule in self.policy.get("rules", []):
            passed, message = self._evaluate_rule(rule, file_data)
            if not passed:
                if rule.get("severity") == "block":
                    result["blocked"] = True
                    result["valid"] = False
                    result["violations"].append(f"[{rule['name']}] {message}")
                else:
                    result["warnings"].append(f"[{rule['name']}] {message}")
        return result

    def get_summary(self) -> Dict:
        rules = self.policy.get("rules", [])
        return {
            "policy_version": self.policy.get("policy_version"),
            "total_rules": len(rules),
            "block_rules": sum(1 for r in rules if r.get("severity") == "block")
        }
