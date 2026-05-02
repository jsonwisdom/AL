#!/usr/bin/env python3
import hashlib, json, sys
from pathlib import Path
from decimal import Decimal, ROUND_HALF_UP

def sha256_file(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()

def main():
    if len(sys.argv) != 2:
        print(json.dumps({"status":"FAIL","code":"USAGE"}))
        sys.exit(1)
    
    packet_dir = Path(sys.argv[1])
    claim_file = packet_dir / "claim.json"
    evidence_dir = packet_dir / "evidence"
    
    if not claim_file.exists():
        print(json.dumps({"status":"FAIL","code":"MISSING_CLAIM"}))
        sys.exit(1)
    
    claim = json.loads(claim_file.read_text())
    
    # Verify evidence files exist and hashes match
    for fname, expected in [
        ("official_claim.pdf", claim["official_claim"]["source_sha256"]),
        ("valuation.pdf", claim["actuarial_values"]["valuation_sha256"])
    ]:
        f = evidence_dir / fname
        if not f.exists():
            print(json.dumps({"status":"FAIL","code":"MISSING_EVIDENCE","file":fname}))
            sys.exit(1)
        actual = sha256_file(f)
        if actual != expected:
            print(json.dumps({"status":"FAIL","code":"SHA256_MISMATCH","file":fname,"expected":expected,"actual":actual}))
            sys.exit(1)
    
    # Compute funded ratio
    assets = Decimal(str(claim["actuarial_values"]["actuarial_assets"]))
    liabilities = Decimal(str(claim["actuarial_values"]["actuarial_liabilities"]))
    reported = Decimal(str(claim["official_claim"]["reported_funded_ratio"]))
    tolerance = Decimal(str(claim.get("tolerance_percentage_points", 0.5)))
    
    if liabilities == 0:
        print(json.dumps({"status":"FAIL","code":"BAD_LIABILITIES"}))
        sys.exit(1)
    
    computed = (assets / liabilities) * 100
    computed = computed.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
    diff = abs(reported - computed)  # Fixed: use abs() function, not .abs() method
    verdict = "MATCH" if diff <= tolerance else "MISMATCH"
    
    # Bind verdict
    if claim.get("result") != verdict:
        print(json.dumps({
            "status": "FAIL",
            "code": "VERDICT_BINDING_FAIL",
            "claim_result": claim.get("result"),
            "replay_verdict": verdict,
            "computed_funded_ratio": str(computed),
            "absolute_difference": str(diff)
        }))
        sys.exit(1)
    
    print(json.dumps({
        "status": "VERIFIED",
        "verdict": verdict,
        "computed_funded_ratio": str(computed),
        "absolute_difference": str(diff),
        "tolerance": str(tolerance)
    }))

if __name__ == "__main__":
    main()
