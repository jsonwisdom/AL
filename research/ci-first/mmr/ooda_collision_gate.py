#!/usr/bin/env python3
"""OODA collision gate: synthetic data, in-memory SQLite, no cloud access."""
import hashlib
import json
import sqlite3

def canon(obj):
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")

def sha(obj):
    return hashlib.sha256(canon(obj)).hexdigest()

db = sqlite3.connect(":memory:", isolation_level=None)
db.execute("CREATE TABLE state (key TEXT PRIMARY KEY, revision INTEGER NOT NULL, payload_sha TEXT NOT NULL)")
db.execute("CREATE TABLE events (event_id TEXT PRIMARY KEY, key TEXT NOT NULL, base_rev INTEGER, committed_rev INTEGER, verdict TEXT, payload_sha TEXT)")
key = "synthetic/heidee-joy/update-collision"
initial_hash = sha({"fixture": "v0", "synthetic": True})
db.execute("INSERT INTO state VALUES (?,?,?)", (key, 7, initial_hash))
checks, receipts = {}, []

def observe():
    return db.execute("SELECT revision,payload_sha FROM state WHERE key=?", (key,)).fetchone()

def attempt(event_id, expected_revision, payload):
    digest = sha(payload)
    existing = db.execute("SELECT verdict,payload_sha,committed_rev FROM events WHERE event_id=?", (event_id,)).fetchone()
    if existing:
        verdict = "EXISTS" if existing[1] == digest else "FAIL_IDEMPOTENCY_COLLISION"
        receipts.append({"event_id": event_id, "expected_revision": expected_revision, "verdict": verdict, "payload_sha": digest})
        return verdict
    cur = db.execute("UPDATE state SET revision=revision+1,payload_sha=? WHERE key=? AND revision=?", (digest, key, expected_revision))
    committed_revision = expected_revision + 1 if cur.rowcount == 1 else None
    verdict = "PASS" if committed_revision is not None else "HOLD_STALE_VERSION"
    db.execute("INSERT INTO events VALUES (?,?,?,?,?,?)", (event_id, key, expected_revision, committed_revision, verdict, digest))
    receipts.append({"event_id": event_id, "expected_revision": expected_revision, "verdict": verdict, "payload_sha": digest})
    return verdict

# Observe two readers at the same revision, then orient proposals and decide atomically.
a, b = observe(), observe()
pa = {"synthetic": True, "field": "label", "value": "candidate-A"}
pb = {"synthetic": True, "field": "label", "value": "candidate-B"}
checks["same_observed_revision"] = a == b and a[0] == 7
checks["distinct_payload_hashes"] = sha(pa) != sha(pb)
checks["first_writer_pass"] = attempt("synthetic-A", a[0], pa) == "PASS"
checks["second_writer_held"] = attempt("synthetic-B", b[0], pb) == "HOLD_STALE_VERSION"
checks["revision_advanced_once"] = observe()[0] == 8
checks["first_payload_preserved"] = observe()[1] == sha(pa)
checks["idempotent_retry_exists"] = attempt("synthetic-A", a[0], pa) == "EXISTS"
checks["duplicate_id_conflicting_bytes_fails"] = attempt("synthetic-A", a[0], pb) == "FAIL_IDEMPOTENCY_COLLISION"
checks["loser_can_retry_after_reorient"] = attempt("synthetic-B-retry", observe()[0], pb) == "PASS"
checks["revision_advanced_twice_only_after_reorient"] = observe()[0] == 9
checks["final_payload_matches_retry"] = observe()[1] == sha(pb)
checks["distinct_receipt_ids"] = len({r["event_id"] for r in receipts[:2]}) == 2
checks["fail_closed_stale_event_recorded"] = db.execute("SELECT verdict FROM events WHERE event_id=?", ("synthetic-B",)).fetchone()[0] == "HOLD_STALE_VERSION"
checks["no_personal_data"] = all(r["event_id"].startswith("synthetic-") for r in receipts)
checks["wrong_expected_revision_held"] = attempt("synthetic-C", 7, {"synthetic": True, "value": "stale"}) == "HOLD_STALE_VERSION"
checks["failed_write_does_not_mutate"] = observe() == (9, sha(pb))
checks["event_count_consistent"] = db.execute("SELECT COUNT(*) FROM events").fetchone()[0] == 4
report = {
    "schema": "computer-wisdom.ooda-collision-v1",
    "fixture": "Heidee Joy (synthetic label; no person records)",
    "checks": checks, "test_count": len(checks), "passed": sum(checks.values()),
    "failed": [name for name, passed in checks.items() if not passed],
    "receipts": receipts, "final_revision": observe()[0],
    "authority_created": False, "production_write": False, "deployment": False,
    "external_anchor": False, "production_ledger": "HOLD"
}
print(json.dumps(report, sort_keys=True, indent=2))
raise SystemExit(1 if report["failed"] else 0)
