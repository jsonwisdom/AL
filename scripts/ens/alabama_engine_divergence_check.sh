#!/usr/bin/env bash
# Alabama Engine CI-FIRST guard: fail closed until independent resolver proof exists.
set -euo pipefail
EXPECTED="${ALMS_EXPECTED:-ALMS/ens/expected/jaywisdom.base.eth.required_txt_v0_1.json}"
OBSERVED="${ALMS_OBSERVED:-ALMS/ens/observed/jaywisdom.base.eth.resolver_txt_v0_1.json}"
PENDING="${ALMS_PENDING:-ALMS/ens/receipts/PENDING_UPDATE_jaywisdom.base.eth_REQUIRED_TXT_V0_1.json}"
for tool in jq date sha256sum; do command -v "$tool" >/dev/null || { echo "RED_MISSING_TOOL tool=$tool"; exit 2; }; done
if ! test -f "$EXPECTED" || ! jq -e '
 .subject_name == "jaywisdom.base.eth" and .no_fake_green == true
 and (.required_txt | type=="array" and length==3)
 and (.required_txt | sort == ["alms.matrix.hash","alms.packet.cid","alms.packet.sha256"])
' "$EXPECTED" >/dev/null 2>&1; then
 echo "RED_EXPECTED_MANIFEST_INVALID"; exit 1
fi
# The current manifest only lists key names, not authoritative expected values.
# A self-supplied resolver JSON cannot authenticate its own chain provenance.
if ! test -f "$OBSERVED"; then
  if test -f "$PENDING" && jq -e '.receipt_type=="PENDING_UPDATE_RECEIPT_V0_1" and .subject_name=="jaywisdom.base.eth" and .no_fake_green==true and (.expires_at_utc|type=="string")' "$PENDING" >/dev/null 2>&1; then
    expiry="$(jq -r '.expires_at_utc' "$PENDING")"
    if exp_epoch="$(date -u -d "$expiry" +%s 2>/dev/null)"; then
      now_epoch="$(date -u +%s)"
      if ((now_epoch > exp_epoch)); then
        echo "RED_EXPIRED subject=jaywisdom.base.eth expired_at=$expiry reason=resolver_artifact_missing"; exit 1
      fi
      echo "YELLOW_PENDING subject=jaywisdom.base.eth expires_at=$expiry reason=resolver_artifact_missing"; exit 0
    fi
  fi
  echo "RED_MISSING_RESOLVER_EVIDENCE subject=jaywisdom.base.eth"; exit 1
fi
if ! jq -e '
 .artifact_type=="ALABAMA_ENGINE_RESOLVER_ARTIFACT_V0_1"
 and .subject_name=="jaywisdom.base.eth" and .chain_id==8453
 and .no_fake_green==true
 and (.resolver_address_or_endpoint|type=="string" and length>0)
 and (.observed_at_utc|type=="string" and length>0)
 and (.block_number_or_resolution_epoch != null)
 and (.workflow_run_id|type=="number")
 and (.checker_output|type=="string")
 and (.txt_records|type=="object")
 and (.txt_records_sha256|type=="string" and test("^[a-fA-F0-9]{64}$"))
 and (.txt_records as $records | [ "alms.packet.cid", "alms.packet.sha256", "alms.matrix.hash" ] | all(. as $k | ($records[$k] | type == "string")))
' "$OBSERVED" >/dev/null 2>&1; then
  echo "RED_INVALID_RESOLVER_ARTIFACT subject=jaywisdom.base.eth"; exit 1
fi
# Hash is over canonical sorted compact JSON; this detects mismatched artifact contents,
# not forged provenance. Do not promote based on a self-declared hash alone.
actual="$(jq -cS '.txt_records' "$OBSERVED" | sha256sum | cut -d' ' -f1)"
claimed="$(jq -r '.txt_records_sha256|ascii_downcase' "$OBSERVED")"
if [[ "$actual" != "$claimed" ]]; then
 echo "RED_RESOLVER_HASH_MISMATCH subject=jaywisdom.base.eth"; exit 1
fi
if ! jq -e '(.expected_txt_values|type=="object") and
  (.expected_txt_values as $values | [ "alms.packet.cid", "alms.packet.sha256", "alms.matrix.hash" ] |
    all(. as $k | ($values[$k] | type == "string" and length > 0)))' "$EXPECTED" >/dev/null 2>&1; then
 echo "RED_EXPECTED_VALUES_UNBOUND subject=jaywisdom.base.eth"; exit 1
fi
if ! jq -e --slurpfile expected "$EXPECTED" '
  .txt_records as $observed |
  ($expected[0].expected_txt_values) as $wanted |
  ["alms.packet.cid","alms.packet.sha256","alms.matrix.hash"] |
  all(. as $k | ($observed[$k]|type=="string") and ($observed[$k]|length>0) and $observed[$k]==$wanted[$k])
' "$OBSERVED" >/dev/null 2>&1; then
 echo "RED_BYTE_MISMATCH subject=jaywisdom.base.eth"; exit 1
fi
# An independent on-chain resolver proof verifier is not yet wired into CI.
# Never accept a claimed 'verified' field in an artifact as cryptographic proof.
echo "RED_PROVENANCE_UNVERIFIED subject=jaywisdom.base.eth reason=independent_resolver_proof_not_implemented"
exit 1
