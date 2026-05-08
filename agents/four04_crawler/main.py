import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

import requests
import yaml

from agents.four04_crawler.proof_blob_surface import AllowedSurface
from agents.four04_crawler.runtime_surface import RUNTIME_ALLOWED_404

ROOT = Path(__file__).resolve().parents[2]
TARGETS = ROOT / "agents" / "four04_crawler" / "targets.yaml"
RECEIPTS = ROOT / "receipts"


def sha256_hex(data: bytes) -> str:
    return "sha256:" + hashlib.sha256(data).hexdigest()


def classify(resp, expected_hash=None):
    if resp.status_code == 404:
        return AllowedSurface.NOT_FOUND

    if resp.status_code in (401, 403):
        return AllowedSurface.CRAWLER_BLOCKED

    if resp.status_code == 200:
        body_hash = sha256_hex(resp.content)
        if expected_hash and expected_hash != body_hash:
            return AllowedSurface.VERSION_DRIFT
        return AllowedSurface.FOUND

    return AllowedSurface.CRAWLER_BLOCKED


def main():
    if not TARGETS.exists():
        return

    with TARGETS.open("r", encoding="utf-8") as f:
        targets = yaml.safe_load(f).get("targets", [])

    now = datetime.now(timezone.utc)
    day_dir = RECEIPTS / now.strftime("%Y-%m-%d")
    day_dir.mkdir(parents=True, exist_ok=True)

    for target in targets:
        url = target["url"]
        expected_hash = target.get("expected_hash")

        try:
            resp = requests.get(url, timeout=20)
            verdict = classify(resp, expected_hash)
            observed_hash = sha256_hex(resp.content)
            status_code = resp.status_code
        except Exception:
            verdict = AllowedSurface.CRAWLER_BLOCKED
            observed_hash = None
            status_code = None

        if verdict not in RUNTIME_ALLOWED_404:
            raise RuntimeError(f"Forbidden verdict emitted: {verdict}")

        receipt_id = f"404_{verdict.value}_{sha256_hex(url.encode())[-12:]}"

        receipt = {
            "receipt_id": receipt_id,
            "circuit_id": "404_v1",
            "target_url": url,
            "url_hash": sha256_hex(url.encode()),
            "crawl_timestamp": now.isoformat(),
            "http_status": status_code,
            "observed_hash": observed_hash,
            "expected_hash": expected_hash,
            "verdict": verdict.value,
        }

        out = day_dir / f"{receipt_id}.json"
        with out.open("w", encoding="utf-8") as f:
            json.dump(receipt, f, indent=2, sort_keys=True)


if __name__ == "__main__":
    main()
