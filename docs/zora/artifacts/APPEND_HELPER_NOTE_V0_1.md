# APPEND_HELPER_NOTE_V0_1

## STATUS: APPEND_HELPER_NOTE
## AUTHORITY: FALSE
## NO_FAKE_GREEN: TRUE

Use this helper to append one real artifact record to the Jay Wisdom Zora artifact manifest.

```bash
python3 tools/replay/append_jaywisdom_artifact_manifest.py \
  --artifact-id zora-jaywisdom-manual-007 \
  --title "Exact Artifact Title" \
  --source fresh_screenshot \
  --status screenshot_observed \
  --verification-level seed_only \
  --notes "Visible in fresh Zora profile screenshot."
```

Allowed sources:

```text
operator_screenshot
fresh_screenshot
manual_title_list
verified_artifact_url
zora_api_json
csv_export
```

Boundary:

```text
append_helper_does_not_fetch_zora=true
append_helper_does_not_verify_contract=true
append_helper_does_not_confirm_revenue=true
wallet_control=false
signing=false
broadcast=false
authority=false
no_fake_green=true
```
