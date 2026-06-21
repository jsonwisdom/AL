#!/usr/bin/env python3
import json
import hashlib
import requests
import sys
import inspect
from datetime import datetime, timezone
from pathlib import Path
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey


def sha256_hex(data: bytes) -> str:
    return "sha256:" + hashlib.sha256(data).hexdigest()


def load_private_key(key_path: Path = Path("private_key.pem")):
    if not key_path.exists():
        print("⚠️  private_key.pem not found → generating new key (keep this safe and local)")
        private_key = Ed25519PrivateKey.generate()
        pem = private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption(),
        )
        key_path.write_bytes(pem)
    else:
        private_key = serialization.load_pem_private_key(key_path.read_bytes(), password=None)
    return private_key


def get_public_key_str(private_key) -> str:
    public_key = private_key.public_key()
    pub_bytes = public_key.public_bytes(
        encoding=serialization.Encoding.Raw,
        format=serialization.PublicFormat.Raw,
    )
    return "ed25519:" + pub_bytes.hex()


def normalize_table_i(raw_data: dict) -> dict:
    """v0.1.1 Deterministic normalization for DTS Table I"""
    if not raw_data.get("data"):
        raise ValueError("No 'data' field in API response")

    records = []
    for item in raw_data["data"]:
        if item.get("table_nbr") != "I":
            continue
        record = {
            "record_date": item["record_date"],
            "account_type": item["account_type"],
            "open_today_bal": int(item.get("open_today_bal", 0) or 0),
            "close_today_bal": int(item.get("close_today_bal", 0) or 0),
            "open_month_bal": int(item.get("open_month_bal", 0) or 0),
            "open_fiscal_year_bal": int(item.get("open_fiscal_year_bal", 0) or 0),
            "src_line_nbr": int(item.get("src_line_nbr", 0)),
        }
        records.append(record)

    records.sort(key=lambda x: x["src_line_nbr"])
    return {"table_i": records, "normalizer_version": "0.1.1"}


def create_failure_receipt(target_date: str, replay_status: str, reason: str, receipt_dir: Path, private_key, public_key_str):
    receipt = {
        "schema_version": "0.1.1",
        "target_date": target_date,
        "authority_level": "OBSERVATION_ONLY",
        "replay_status": replay_status,
        "diff_status": "NOT_EVALUATED",
        "source_url": None,
        "source_fetched_at_utc": datetime.now(timezone.utc).isoformat(),
        "raw_snapshot_hash": None,
        "normalized_receipt_hash": None,
        "normalizer_version": "0.1.1",
        "normalizer_code_hash": None,
        "parent_receipt_hash": None,
        "signature_profile": "ed25519-detached",
        "public_key": public_key_str,
        "key_metadata": {
            "created_at": "2026-06-21T00:00:00Z",
            "purpose": "Treasury Can Audit v0.1.1",
        },
        "normalized_data": None,
        "reason": reason,
    }

    canon = json.dumps(receipt, sort_keys=True, separators=(",", ":")).encode("utf-8")
    signature = private_key.sign(canon)
    receipt["signature"] = signature.hex()

    with open(receipt_dir / "normalized_receipt.json", "w", encoding="utf-8") as f:
        json.dump(receipt, f, indent=2)
    with open(receipt_dir / "normalized_receipt.cose", "wb") as f:
        f.write(signature)
    with open(receipt_dir / "public_key.pub", "w") as f:
        f.write(public_key_str)

    print(f"⚠️  Signed failure receipt created: {replay_status}")


def main():
    if len(sys.argv) < 2:
        print("Usage: python treasury_can_audit_intake.py YYYY-MM-DD")
        sys.exit(1)

    target_date = sys.argv[1]
    receipt_dir = Path(f"receipts/{target_date}")
    receipt_dir.mkdir(parents=True, exist_ok=True)

    SOURCE_URL = (
        "https://api.fiscaldata.treasury.gov/services/api/fiscal_service/"
        f"v1/accounting/dts/operating_cash_balance?filter=record_date:eq:{target_date}&page[size]=100"
    )

    private_key = load_private_key()
    public_key_str = get_public_key_str(private_key)

    try:
        resp = requests.get(SOURCE_URL, timeout=30)
        resp.raise_for_status()
        raw_bytes = resp.content
        raw_hash = sha256_hex(raw_bytes)

        with open(receipt_dir / "raw_snapshot.json", "wb") as f:
            f.write(raw_bytes)
        with open(receipt_dir / "raw_snapshot.hash", "w") as f:
            f.write(raw_hash)

        raw_json = json.loads(raw_bytes)
        normalized = normalize_table_i(raw_json)

        canon_norm = json.dumps(normalized, sort_keys=True, separators=(",", ":")).encode("utf-8")
        norm_hash = sha256_hex(canon_norm)

        normalizer_source = inspect.getsource(normalize_table_i)
        normalizer_code_hash = sha256_hex(normalizer_source.encode("utf-8"))

        signature = private_key.sign(canon_norm)

        receipt = {
            "schema_version": "0.1.1",
            "target_date": target_date,
            "authority_level": "OBSERVATION_ONLY",  # upgraded after successful verify
            "replay_status": "PASS",
            "diff_status": "NOT_EVALUATED",
            "source_url": SOURCE_URL,
            "source_fetched_at_utc": datetime.now(timezone.utc).isoformat(),
            "source_mime_type": resp.headers.get("content-type"),
            "source_etag": resp.headers.get("etag"),
            "source_last_modified": resp.headers.get("last-modified"),
            "raw_snapshot_hash": raw_hash,
            "normalized_receipt_hash": norm_hash,
            "normalizer_version": "0.1.1",
            "normalizer_code_hash": normalizer_code_hash,
            "parent_receipt_hash": None,  # GENESIS
            "signature_profile": "ed25519-detached",
            "public_key": public_key_str,
            "key_metadata": {
                "created_at": "2026-06-21T00:00:00Z",
                "purpose": "Treasury Can Audit v0.1.1",
            },
            "normalized_data": normalized,
            "signature": signature.hex(),
        }

        with open(receipt_dir / "normalized_receipt.json", "w", encoding="utf-8") as f:
            json.dump(receipt, f, indent=2)
        with open(receipt_dir / "normalized_receipt.cose", "wb") as f:
            f.write(signature)
        with open(receipt_dir / "public_key.pub", "w") as f:
            f.write(public_key_str)

        print(f"✅ SUCCESS: Receipt generated for {target_date} | replay_status: PASS")

    except requests.exceptions.RequestException as e:
        create_failure_receipt(target_date, "FETCH_BLOCKED", str(e), receipt_dir, private_key, public_key_str)
    except ValueError as e:
        create_failure_receipt(target_date, "NO_PUBLICATION_AVAILABLE", str(e), receipt_dir, private_key, public_key_str)
    except Exception as e:
        create_failure_receipt(target_date, "NORMALIZATION_FAILED", str(e), receipt_dir, private_key, public_key_str)


if __name__ == "__main__":
    main()
