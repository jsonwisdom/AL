import json
import sys
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from agents.four04_crawler.runtime_surface import RUNTIME_ALLOWED_404

RECEIPTS_DIR = ROOT / 'receipts'
OUTPUT_DIR = Path(__file__).resolve().parent / 'public'

ALLOWED = {v.value for v in RUNTIME_ALLOWED_404}

FORBIDDEN_FIELDS = {
    'RISK_SCORE',
    'TRUST_SCORE',
    'CORRUPTION_SCORE',
    'SEVERITY',
    'SUSPICIOUS',
    'BLAME',
    'MOTIVE',
    'INTENT'
}


def load_receipts():
    receipts = []

    if not RECEIPTS_DIR.exists():
        return receipts

    for path in RECEIPTS_DIR.rglob('*.json'):
        with path.open('r', encoding='utf-8') as f:
            data = json.load(f)

        if data.get('circuit_id') != '404_v1':
            continue

        verdict = data.get('verdict')

        if verdict not in ALLOWED:
            raise RuntimeError(
                f'Dashboard attempted to render forbidden verdict: {verdict}'
            )

        forbidden_present = FORBIDDEN_FIELDS.intersection(set(data.keys()))

        if forbidden_present:
            raise RuntimeError(
                'Dashboard attempted to render forbidden receipt field(s): '
                + ', '.join(sorted(forbidden_present))
            )

        receipts.append(data)

    return receipts


def build_summary(receipts):
    summary = defaultdict(lambda: defaultdict(int))

    for r in receipts:
        day = r.get('crawl_timestamp', '')[:10]
        verdict = r.get('verdict')
        summary[day][verdict] += 1

    return summary


def build_dashboard():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    receipts = load_receipts()
    summary = build_summary(receipts)

    with (OUTPUT_DIR / 'summary.json').open('w', encoding='utf-8') as f:
        json.dump(summary, f, indent=2, sort_keys=True)

    with (OUTPUT_DIR / 'receipts.json').open('w', encoding='utf-8') as f:
        json.dump(receipts, f, indent=2, sort_keys=True)

    html = f'''<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<title>404 Overview</title>
</head>
<body>
<h1>404 Overview</h1>
<p>Generated: {datetime.now(timezone.utc).isoformat()}</p>
<p>Receipts: {len(receipts)}</p>
<ul>
<li><a href="summary.json">summary.json</a></li>
<li><a href="receipts.json">receipts.json</a></li>
</ul>
<p>Observation layer only. No interpretation.</p>
</body>
</html>'''

    with (OUTPUT_DIR / 'index.html').open('w', encoding='utf-8') as f:
        f.write(html)


if __name__ == '__main__':
    build_dashboard()
