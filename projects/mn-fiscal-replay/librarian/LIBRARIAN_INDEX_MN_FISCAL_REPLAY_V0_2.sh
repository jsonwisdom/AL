#!/bin/bash
# LIBRARIAN_INDEX_MN_FISCAL_REPLAY_V0_2.sh
# Purpose: curated lineage index, not a firehose.
# Doctrine: discovery before delegation / public click paths must surface Jay's prior work.

set -euo pipefail

OUT_DIR="projects/mn-fiscal-replay/librarian"
OUT_JSON="$OUT_DIR/MN_FISCAL_REPLAY_LIBRARIAN_INDEX_V0_2.json"
OUT_MD="$OUT_DIR/MN_FISCAL_REPLAY_LIBRARIAN_INDEX_V0_2.md"
TS=$(date -u +%Y-%m-%dT%H:%M:%SZ)

mkdir -p "$OUT_DIR"

python3 - "$OUT_JSON" "$OUT_MD" "$TS" << 'PY'
import json
import sys
from pathlib import Path

out_json = Path(sys.argv[1])
out_md = Path(sys.argv[2])
ts = sys.argv[3]

def files(pattern):
    return sorted(str(p) for p in Path('.').glob(pattern) if p.is_file())

def safe_json(path):
    try:
        return json.loads(Path(path).read_text(encoding='utf-8', errors='replace'))
    except Exception as e:
        return {'_parse_error': str(e), '_path': path}

source_manifests = files('_sources/MN_*/source_manifest.json')
replay_receipts = files('projects/mn-fiscal-replay/replay/MN_*.replay.json')
enriched = files('projects/mn-fiscal-replay/enriched/MN_*.enriched.json')
final_status = files('projects/mn-fiscal-replay/live_fetch/MN_*/MN_*FINAL_SAFE_STATUS*.json')
chunk_reviews = files('projects/mn-fiscal-replay/reviews/MN_*CHUNK_REVIEW*.md')

runs_root = Path('projects/mn-fiscal-replay/boss_bre/runs')
boss_runs = sorted(str(p) for p in runs_root.glob('*') if p.is_dir()) if runs_root.exists() else []

live_root = Path('projects/mn-fiscal-replay/live_fetch')
county_lanes = sorted(str(p.name) for p in live_root.glob('*') if p.is_dir() and p.name.startswith('MN')) if live_root.exists() else []

components = {}

for manifest in source_manifests:
    comp = Path(manifest).parts[1]
    components.setdefault(comp, {})['source_manifest'] = manifest
    data = safe_json(manifest)
    components[comp]['source_url'] = data.get('url') or data.get('source_url') or data.get('official_url') or 'UNKNOWN'
    components[comp]['manifest_status'] = data.get('status', 'UNKNOWN')
    components[comp]['raw_sha256'] = data.get('raw_sha256') or data.get('pdf_sha256') or data.get('source_sha256') or 'UNKNOWN'
    components[comp]['text_sha256'] = data.get('text_sha256') or data.get('extracted_text_sha256') or 'UNKNOWN'

for receipt in replay_receipts:
    comp = Path(receipt).name.replace('.replay.json', '')
    components.setdefault(comp, {})['replay_receipt'] = receipt
    data = safe_json(receipt)
    components[comp]['replay_result'] = data.get('result', data.get('verdict', 'UNKNOWN'))
    components[comp]['replay_status'] = data.get('status', 'UNKNOWN')

for baseline in enriched:
    comp = Path(baseline).name.replace('.enriched.json', '')
    components.setdefault(comp, {})['enriched_baseline'] = baseline

for status in final_status:
    comp = Path(status).parts[-2]
    components.setdefault(comp, {})['final_safe_status'] = status
    data = safe_json(status)
    components[comp]['public_verdict'] = data.get('verdict', 'UNKNOWN')
    components[comp]['possible_content_delta'] = data.get('possible_content_delta', 'UNKNOWN')

for comp in county_lanes:
    components.setdefault(comp, {})

data = {
    'artifact': 'MN_FISCAL_REPLAY_LIBRARIAN_INDEX_V0_2',
    'timestamp': ts,
    'status': 'CURATED_LINEAGE_INDEX_CREATED',
    'rule': 'DISCOVERY_BEFORE_DELEGATION',
    'counts': {
        'source_manifests': len(source_manifests),
        'replay_receipts': len(replay_receipts),
        'enriched_baselines': len(enriched),
        'final_safe_status_receipts': len(final_status),
        'chunk_review_docs': len(chunk_reviews),
        'boss_bre_run_dirs': len(boss_runs),
        'mn_live_fetch_lanes': len(county_lanes)
    },
    'components': components,
    'next_best_target': 'MN_002_FROM_EXISTING_SOURCE_MANIFEST' if 'MN_002' in components else 'RUN_EXPANDED_LIBRARIAN_PREFLIGHT',
    'manual_operator_file_search_required': False,
    'public_content_claim': 'BLOCKED',
    'no_fake_green': True
}

out_json.write_text(json.dumps(data, indent=2) + '\n', encoding='utf-8')

lines = [
    '# MN Fiscal Replay Librarian Index v0.2',
    '',
    '`DISCOVERY_BEFORE_DELEGATION`',
    '',
    '## Public Page Rule',
    '',
    "A visitor must never be asked to rediscover Jay's project history manually. The page must surface lineage first: what exists, where it lives, what is sealed, what is blocked, and what comes next.",
    '',
    '## Counts',
    ''
]

for key, value in data['counts'].items():
    lines.append(f'- `{key}`: `{value}`')

lines += [
    '',
    '## Component Index',
    '',
    '| Component | Manifest | Replay | Enriched | Final Status | Public Verdict | Next |',
    '|---|---|---|---|---|---|---|'
]

for comp, info in sorted(components.items()):
    manifest = info.get('source_manifest', 'missing')
    replay = info.get('replay_receipt', 'missing')
    enriched_path = info.get('enriched_baseline', 'missing')
    final = info.get('final_safe_status', 'missing')
    verdict = info.get('public_verdict', info.get('replay_result', 'PENDING'))
    if comp == 'MN_001':
        nxt = 'maintenance / safe baseline'
    elif comp == 'MN_002':
        nxt = 'run from existing manifest'
    else:
        nxt = 'review candidate'
    lines.append(f'| `{comp}` | `{manifest}` | `{replay}` | `{enriched_path}` | `{final}` | `{verdict}` | `{nxt}` |')

lines += [
    '',
    '## Boss Bre Gate',
    '',
    '`PUBLIC_CONTENT_CLAIM = BLOCKED`',
    '',
    'Source discovery does not equal a public claim. Evidence must still pass replay, classification, and Boss Bre review.',
    '',
    '## Next Best Target',
    '',
    f"`{data['next_best_target']}`",
    '',
    '## No Fake Green',
    '',
    '`manual_operator_file_search_required = false`',
    '',
    'If this index cannot find the lineage, the system must say so explicitly instead of sending the operator to hunt.'
]

out_md.write_text('\n'.join(lines) + '\n', encoding='utf-8')
PY

cat "$OUT_JSON" | jq '.counts, .next_best_target, .components.MN_001, .components.MN_002'
echo ""
echo "=== PUBLIC INDEX PREVIEW ==="
sed -n '1,120p' "$OUT_MD"
