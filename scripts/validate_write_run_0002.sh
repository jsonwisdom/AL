#!/usr/bin/env bash
set -euo pipefail

PACKET="${1:-WRITE_RUN_0002_packet.json}"

test -f "$PACKET" || { echo "MISSING_PACKET: $PACKET"; exit 1; }

jq empty "$PACKET" >/dev/null

jq -e '
  .write_run_0002_manifest.run_id=="WRITE_RUN_0002"
  and .write_run_0002_manifest.mode=="WRITE"
  and .write_run_0002_manifest.status=="SUCCESS"
  and .write_run_0002_manifest.hash_verification.all_hashes_ok==true
  and .write_run_0002_manifest.hash_verification.re_run_byte_identical==true
  and (.write_run_0002_manifest.violations|length)==0
  and .replay_result.re_run_byte_identical==true
  and (.replay_result.changed_artifacts|length)==0
  and .rel_0001_integrity.unchanged==true
  and (.rel_0001_integrity.changed_files|length)==0
  and .view_layer_audit.status=="CLEAN"
  and .view_layer_audit.cites_ledger_only==true
  and (.view_layer_audit.uncited_sentences|length)==0
  and .kill_switch.triggered==false
' "$PACKET" >/dev/null

echo "WRITE_RUN_0002_PACKET_VALID"
echo "WRITE_RUN_0003_UNBLOCKED_CANDIDATE"
