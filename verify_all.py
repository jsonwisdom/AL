#!/usr/bin/env python3
"""
Constitutional Receipts Independent Verifier v0.1

One-command replay + policy + map verification.
Outputs: CONSTITUTIONAL_REPLAY_PASS | CONSTITUTIONAL_REPLAY_FAIL
"""

import subprocess
import sys
from pathlib import Path


def run_command(cmd: str, description: str) -> bool:
    print(f"▶️  {description}")
    try:
        result = subprocess.run(
            cmd,
            shell=True,
            capture_output=True,
            text=True,
            cwd=Path(__file__).parent,
        )
        if result.returncode == 0:
            print(f"✅ {description} passed")
            if result.stdout.strip():
                output = result.stdout.strip()
                print(output[:500] + ("..." if len(output) > 500 else ""))
            return True
        print(f"❌ {description} failed")
        if result.stdout.strip():
            print(result.stdout)
        if result.stderr.strip():
            print(result.stderr)
        return False
    except Exception as exc:
        print(f"💥 Error running {description}: {exc}")
        return False


def main() -> int:
    print("🔍 Constitutional Receipts Replay Verifier v0.1")
    print("Receipts prove process only. No authority granted.\n")

    all_pass = True
    all_pass = run_command("pytest -q", "Pytest suite") and all_pass
    all_pass = run_command("python replay_engine.py --batch", "Replay engine batch") and all_pass
    all_pass = run_command("python receiptctl.py map --summary", "Receiptctl map summary") and all_pass

    print("\n" + "=" * 60)
    if all_pass:
        print("🎉 CONSTITUTIONAL_REPLAY_PASS")
        print("All invariants hold. Replay is reproducible.")
        return 0
    print("⚠️  CONSTITUTIONAL_REPLAY_FAIL")
    print("One or more verification steps failed.")
    return 1


if __name__ == "__main__":
    sys.exit(main())
