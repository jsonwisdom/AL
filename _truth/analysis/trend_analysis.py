#!/usr/bin/env python3
import json
import re
from pathlib import Path
from datetime import datetime, timezone
from collections import Counter

LEDGER_PATH = Path("LEDGER.md")
OUTPUT_DIR = Path("_truth/analysis")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

ROW_RE = re.compile(
    r"^\|\s*(?P<utc>[^|]+?)\s*\|\s*(?P<report>[^|]+?)\s*\|\s*(?P<schema>[^|]+?)\s*\|\s*"
    r"(?P<scope>[^|]+?)\s*\|\s*(?P<status>[^|]+?)\s*\|\s*(?P<style>[^|]+?)\s*\|\s*"
    r"(?P<truth>[^|]+?)\s*\|\s*(?P<structure>[^|]+?)\s*\|\s*(?P<sha>[0-9a-f]{64})\s*\|"
)

def to_float(value: str) -> float:
    return float(str(value).strip())

def parse_rows():
    rows = []
    for line in LEDGER_PATH.read_text(encoding="utf-8").splitlines():
        m = ROW_RE.match(line)
        if not m:
            continue
        row = {k: v.strip() for k, v in m.groupdict().items()}
        row["style"] = to_float(row["style"])
        row["truth"] = to_float(row["truth"])
        row["structure"] = to_float(row["structure"])
        rows.append(row)
    rows.sort(key=lambda r: r["utc"])
    return rows

def avg(values):
    return sum(values) / len(values) if values else None

def main():
    rows = parse_rows()
    status_counts = Counter(r["status"] for r in rows)

    analysis = {
        "schema": "trend_analysis_v0.1.1",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "source": "LEDGER.md",
        "mode": "READ_ONLY",
        "total_records": len(rows),
        "status_distribution": dict(status_counts),
        "style": {
            "min": min([r["style"] for r in rows], default=None),
            "max": max([r["style"] for r in rows], default=None),
            "avg": avg([r["style"] for r in rows]),
        },
        "truth": {
            "min": min([r["truth"] for r in rows], default=None),
            "max": max([r["truth"] for r in rows], default=None),
            "avg": avg([r["truth"] for r in rows]),
        },
        "structure": {
            "min": min([r["structure"] for r in rows], default=None),
            "max": max([r["structure"] for r in rows], default=None),
            "avg": avg([r["structure"] for r in rows]),
        },
        "recent_trend": rows[-5:],
    }

    ts = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
    out = OUTPUT_DIR / f"trend_data_{ts}.json"
    out.write_text(json.dumps(analysis, indent=2) + "\n", encoding="utf-8")

    print("📊 Trend Analysis v0.1.1")
    print("=" * 50)
    print(f"✅ Found {len(rows)} rows in LEDGER.md")
    print("✅ Sorted chronologically by UTC")
    print(f"✅ Data saved: {out}")
    print()
    print("📈 Summary:")
    print(f"   Total: {analysis['total_records']}")
    print(f"   Status: {analysis['status_distribution']}")
    print(f"   Style max: {analysis['style']['max']}")
    print(f"   Truth max: {analysis['truth']['max']}")
    print(f"   Structure max: {analysis['structure']['max']}")

if __name__ == "__main__":
    main()
