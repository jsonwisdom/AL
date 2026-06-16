# File: core/immune/attack_adapter.py
# Version: v0.1.0-REFERENCE
# Status: INERT / DRY-RUN ADAPTER ONLY
# Dependency Hash: 8138bc6543d97d8ef01c69ef264cbdf61a55459c

import json
import tempfile
import os
from typing import Tuple, Dict, Any
from core.immune.cross_biome_hook import CrossBiomeDryCheckHook


class CorporateAttackAdapter:
    def __init__(self, hook_instance: CrossBiomeDryCheckHook):
        self.hook = hook_instance

    def execute_nested_attack_dry(self, attack_fixture_path: str) -> Tuple[str, Dict[str, Any]]:
        """
        Reads a nested corporate attack fixture, unwraps its payload layers
        into temporary flat structures, and executes a dry validation run.
        """
        try:
            with open(attack_fixture_path, 'r') as f:
                attack_data = json.load(f)
        except FileNotFoundError as e:
            return "ATTACK_FIXTURE_MISSING", {"error": str(e)}

        payload = attack_data.get("payload", {})

        # Extract the deep structures intended for specific verification scopes
        spine_override = payload.get("attempted_spine_override", {})
        malicious_manifest = payload.get("malicious_manifest", {})
        malicious_trace = payload.get("malicious_trace_signals", {})

        # Create localized temporary files to act as flat inputs for the hook
        with tempfile.TemporaryDirectory() as tmpdir:
            compliance_tmp = os.path.join(tmpdir, "compliance.json")
            manifest_tmp = os.path.join(tmpdir, "manifest.json")
            trace_tmp = os.path.join(tmpdir, "trace.json")

            with open(compliance_tmp, 'w') as f:
                json.dump(spine_override, f)
            with open(manifest_tmp, 'w') as f:
                json.dump(malicious_manifest, f)
            with open(trace_tmp, 'w') as f:
                json.dump(malicious_trace, f)

            # Route the unwrapped paths down the exact hook execution lane
            return self.hook.evaluate_manifest_dry(
                compliance_path=compliance_tmp,
                brp_manifest_path=manifest_tmp,
                target_trace_path=trace_tmp
            )
