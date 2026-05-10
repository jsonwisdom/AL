#!/usr/bin/env python3
"""
Placeholder for key generation manifest.
Run when proving stack (nargo prove/verify or bb) is available.
"""

import json
import sys
from pathlib import Path

def main():
    print("⚠️ Key generation requires full proving stack (nargo with prove/verify)")
    print("   Current nargo: compiler-only (1.0.0-beta.21)")
    print("")
    print("   To enable key generation:")
    print("   1. Install nargo with prove/verify subcommands")
    print("   2. Or install bb (Barretenberg) separately")
    print("   3. Run: nargo verify-key && nargo prove-key")
    print("   4. Then re-run this script")
    
    # Update MODULE.json with note
    module_json = Path(__file__).parent.parent / "MODULE.json"
    if module_json.exists():
        with open(module_json, 'r') as f:
            data = json.load(f)
        data["key_generation_status"] = "deferred_placeholder"
        data["key_generation_note"] = "Run nargo verify-key and nargo prove-key in circuit/ directory when proving stack available"
        with open(module_json, 'w') as f:
            json.dump(data, f, indent=2)
        print("✅ MODULE.json updated with deferred status")
    else:
        print("⚠️ MODULE.json not found")
    
    sys.exit(0)

if __name__ == "__main__":
    main()
