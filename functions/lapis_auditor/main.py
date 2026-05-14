"""
Lapis Auditor Cloud Function.

GCS-triggered wrapper around tools.verify_replay_demo.run_audit.
This function performs L0 replay verification and emits a REPLAY_SUMMARY.json.

No Base/EAS settlement should be triggered unless this function emits PASS.
"""

from __future__ import annotations

import json
from pathlib import Path

import functions_framework
from google.cloud import storage

from tools.verify_replay_demo import run_audit


SCHEMA_PATH = Path("schemas/lapis/replayable_audit_demo.v0.1.schema.json")


@functions_framework.cloud_event
def audit_gcs_mutation(cloud_event):
    """
    Triggered by GCS object finalization.

    Only .sample.json replay objects are audited. Other objects are ignored.
    """
    data = cloud_event.data
    bucket_name = data["bucket"]
    object_name = data["name"]

    if not object_name.endswith(".sample.json"):
        print(f"[*] Skipping non-replay object: {object_name}")
        return

    print(f"[*] Audit triggered for {bucket_name}/{object_name}")

    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)

    local_sample = Path("/tmp/replay_sample.json")
    local_summary = Path("/tmp/REPLAY_SUMMARY.json")

    bucket.blob(object_name).download_to_filename(local_sample)

    summary = run_audit(
        sample_path=local_sample,
        schema_path=SCHEMA_PATH,
        output_path=local_summary,
    )

    summary_name = f"summaries/{Path(object_name).stem}.REPLAY_SUMMARY.json"
    bucket.blob(summary_name).upload_from_string(
        json.dumps(summary, indent=2, sort_keys=True),
        content_type="application/json",
    )

    if summary["verdict"] != "PASS":
        print(f"[!] VERIFICATION FAILURE: {object_name}. Summary written to {summary_name}.")
        raise RuntimeError(f"Lapis verification failed for {object_name}")

    print(f"[+] VERIFICATION PASSED: {summary_name} notarized in L0.")
