#!/usr/bin/env python3
import argparse, hashlib, json, subprocess, sys
from datetime import datetime, timezone
from pathlib import Path

LEDGER_PATH = Path("_truth/audit/quarantine_ledger.json")
INVENTORY_PATH = Path("_truth/audit/truth_surface_inventory.json")
REPLAY_SCRIPT = Path("_truth/audit/replay.py")

def run(cmd, check=True):
    r = subprocess.run(cmd, text=True, capture_output=True)
    if check and r.returncode != 0:
        print("❌", " ".join(cmd))
        print(r.stdout)
        print(r.stderr)
        sys.exit(r.returncode)
    return r

def sha256_file(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()

def load_json(p):
    return json.loads(Path(p).read_text())

def save_json(p, data):
    Path(p).write_text(json.dumps(data, indent=2, sort_keys=True) + "\n")

def note_root():
    r = run(["git", "notes", "--ref=commits", "show", "HEAD"], check=False)
    for line in r.stdout.splitlines():
        if line.startswith("MERKLE_ROOT="):
            return line.split("=", 1)[1].strip()
    return ""

def replay_root():
    r = run([sys.executable, str(REPLAY_SCRIPT), "--commit", "HEAD", "--quiet"])
    out = r.stdout.strip().splitlines()
    return out[-1] if out else ""

def pick_next(ledger):
    for x in ledger["legacy_paths"]:
        if x.get("status") == "QUARANTINED":
            return x["path"]
    return None

def promote(candidate, dry_run):
    p = Path(candidate)
    for required in [LEDGER_PATH, INVENTORY_PATH, REPLAY_SCRIPT]:
        if not required.exists():
            sys.exit(f"❌ missing required file: {required}")

    if not p.exists():
        sys.exit(f"❌ file not found: {candidate}")

    ledger = load_json(LEDGER_PATH)
    inventory = load_json(INVENTORY_PATH)

    entry = next((x for x in ledger["legacy_paths"] if x.get("path") == candidate), None)
    if not entry:
        sys.exit(f"❌ path not in quarantine ledger: {candidate}")
    if entry.get("status") != "QUARANTINED":
        sys.exit(f"❌ not promotable; status={entry.get('status')}")

    actual = sha256_file(p)
    if actual != entry.get("sha256"):
        print("❌ SHA-256 mismatch")
        print("ledger=", entry.get("sha256"))
        print("actual=", actual)
        sys.exit(1)

    old_root = note_root()
    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    entry["status"] = "PROMOTED"
    entry["promoted_track"] = "TRACK_007"
    entry["promoted_at_utc"] = now

    ledger["promoted_count"] = sum(x.get("status") == "PROMOTED" for x in ledger["legacy_paths"])
    ledger["quarantined_count"] = sum(x.get("status") == "QUARANTINED" for x in ledger["legacy_paths"])
    ledger["status"] = "PROMOTION_AUTOMATED"
    ledger["promotion_allowed"] = False
    ledger["timestamp_utc"] = now

    if not any(x.get("path") == candidate for x in inventory["truth_surfaces"]):
        inventory["truth_surfaces"].append({
            "path": candidate,
            "role": "promoted receipt",
            "track": "TRACK_007",
            "leaf_id": p.stem,
            "state": "PROMOTED_FROM_QUARANTINE",
            "boundary": "File remains under _truth; promotion is ledger/inventory status, not filesystem move."
        })

    save_json(LEDGER_PATH, ledger)
    save_json(INVENTORY_PATH, inventory)

    run(["git", "add", str(LEDGER_PATH), str(INVENTORY_PATH)])
    run(["git", "commit", "-m", f"Track 007: auto-promote {p.name}"])

    new_root = replay_root()
    if old_root and new_root == old_root:
        sys.exit("❌ root did not change")

    run(["git", "notes", "--ref=commits", "add", "-f", "-m", f"MERKLE_ROOT={new_root}", "HEAD"])

    print(f"✅ promoted={candidate}")
    print(f"OLD_ROOT={old_root}")
    print(f"NEW_ROOT={new_root}")

    if dry_run:
        print("DRY_RUN=true; local commit only, no push")
        return

    run(["git", "push", "origin", "HEAD:master", "refs/notes/commits"])
    print("✅ pushed commit + note")

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--path")
    ap.add_argument("--next", action="store_true")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    ledger = load_json(LEDGER_PATH)
    candidate = args.path or (pick_next(ledger) if args.next else None)
    if not candidate:
        sys.exit("❌ provide --path or --next")

    promote(candidate, args.dry_run)

if __name__ == "__main__":
    main()
