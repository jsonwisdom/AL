use al_verifier::bootstrap::harness::{
    parse_receipt, parse_verdict, validate_receipt, validate_verdict, RECEIPT_V1,
};
use sha2::{Digest, Sha256};

#[test]
fn receipt_version_matches_constitution() {
    let data = include_str!("fixtures/receipt_valid_v1.json");
    let receipt = parse_receipt(data).unwrap();

    assert_eq!(receipt.receipt_version, RECEIPT_V1);
    validate_receipt(&receipt).unwrap();
}

#[test]
fn receipt_id_is_sha256_prefixed() {
    let data = include_str!("fixtures/receipt_valid_v1.json");
    let receipt = parse_receipt(data).unwrap();

    assert!(receipt.receipt_id.starts_with("sha256:"));
    assert_eq!(receipt.receipt_id.len(), 71);
}

#[test]
fn observed_roots_are_merkle_prefixed() {
    let data = include_str!("fixtures/receipt_valid_v1.json");
    let receipt = parse_receipt(data).unwrap();

    assert!(receipt
        .observed_roots
        .state_transitions_root
        .starts_with("merkle:"));

    assert!(receipt
        .observed_roots
        .tool_graph_root
        .starts_with("merkle:"));
}

#[test]
fn content_hash_matches_payload_fixture_bytes() {
    let receipt_data = include_str!("fixtures/receipt_valid_v1.json");
    let receipt = parse_receipt(receipt_data).unwrap();

    let payload_bytes = include_bytes!("fixtures/payload_valid_v1.json");
    let computed = format!(
        "sha256:{}",
        hex::encode(Sha256::digest(payload_bytes))
    );

    assert_eq!(receipt.content_hash, computed);
}

#[test]
fn invalid_content_hash_is_rejected() {
    let receipt_data = include_str!("fixtures/receipt_bad_content_hash_v1.json");
    let receipt = parse_receipt(receipt_data).unwrap();

    let payload_bytes = include_bytes!("fixtures/payload_valid_v1.json");
    let computed = format!(
        "sha256:{}",
        hex::encode(Sha256::digest(payload_bytes))
    );

    assert_ne!(receipt.content_hash, computed);
}

#[test]
fn invalid_receipt_version_is_rejected() {
    let data = include_str!("fixtures/receipt_invalid_version.json");
    let receipt = parse_receipt(data).unwrap();

    let err = validate_receipt(&receipt).unwrap_err();

    assert!(err.contains("invalid receipt_version"));
}

#[test]
fn verdict_fixture_is_valid() {
    let data = include_str!("fixtures/verdict_verified_v1.json");
    let verdict = parse_verdict(data).unwrap();

    validate_verdict(&verdict).unwrap();
}
