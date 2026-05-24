use al_verifier::{Receipt, Verdict};

#[test]
fn parse_valid_receipt() {
    let data = include_str!("fixtures/receipt_valid_v1.json");
    let receipt: Receipt = serde_json::from_str(data).unwrap();

    assert_eq!(receipt.receipt_version, "RECEIPT_V1");
    assert!(!receipt.receipt_id.is_empty());
}

#[test]
fn parse_verified_verdict() {
    let data = include_str!("fixtures/verdict_verified_v1.json");
    let verdict: Verdict = serde_json::from_str(data).unwrap();

    assert_eq!(verdict.verdict_version, "VERDICT_V1");
}
