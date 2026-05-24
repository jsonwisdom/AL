use al_verifier::bootstrap::harness::run_verifier;
use al_verifier::hash::content_hash::ContentHash;
use al_verifier::io::resolver::AnchorResolver;
use serde_json::Value;

struct FailingResolver;

impl AnchorResolver for FailingResolver {
    type Error = String;

    fn resolve(&self, _hash: &ContentHash) -> Result<Vec<u8>, Self::Error> {
        Err("intentional failure".into())
    }
}

#[test]
fn verifier_error_matches_fixture_shape() {
    let receipt_bytes = std::fs::read("../tests/fixtures/receipt_valid_v1.json")
        .expect("receipt fixture");

    let mut output = Vec::new();

    run_verifier(
        receipt_bytes.as_slice(),
        &mut output,
        FailingResolver,
    )
    .expect("verifier execution");

    let parsed: Value = serde_json::from_slice(&output)
        .expect("valid VERDICT_V1 json");

    assert_eq!(parsed["verdict_version"], "VERDICT_V1");
    assert_eq!(parsed["status"], "VERIFIER_ERROR");
    assert_eq!(parsed["governance_anchor"]["tag"], "GOVERNANCE_V1");
}
