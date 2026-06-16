use crate::{Receipt, Verdict};

pub const RECEIPT_V1: &str = "RECEIPT_V1";
pub const VERDICT_V1: &str = "VERDICT_V1";

pub fn parse_receipt(input: &str) -> Result<Receipt, serde_json::Error> {
    serde_json::from_str(input)
}

pub fn parse_verdict(input: &str) -> Result<Verdict, serde_json::Error> {
    serde_json::from_str(input)
}

pub fn validate_receipt(receipt: &Receipt) -> Result<(), String> {
    if receipt.receipt_version != RECEIPT_V1 {
        return Err(format!("invalid receipt_version: {}", receipt.receipt_version));
    }

    validate_sha256(&receipt.receipt_id)?;
    validate_sha256(&receipt.intent.request_hash)?;
    validate_sha256(&receipt.intent.actor_hash)?;
    validate_sha256(&receipt.intent.constraints_hash)?;
    validate_sha256(&receipt.execution.verifier_env_hash)?;
    validate_sha256(&receipt.execution.fixture_hash)?;
    validate_sha256(&receipt.execution.replay_contract_hash)?;
    validate_sha256(&receipt.execution.execution_block_hash)?;

    validate_merkle_root(&receipt.observed_roots.state_transitions_root)?;
    validate_merkle_root(&receipt.observed_roots.tool_graph_root)?;

    match receipt.replay.requested_action.as_str() {
        "REPLAY" | "INVALIDATE" | "ESCALATE" => Ok(()),
        other => Err(format!("invalid requested_action: {}", other)),
    }
}

pub fn validate_verdict(verdict: &Verdict) -> Result<(), String> {
    if verdict.verdict_version != VERDICT_V1 {
        return Err(format!("invalid verdict_version: {}", verdict.verdict_version));
    }

    validate_sha256(&verdict.receipt_id)?;

    Ok(())
}

pub fn validate_sha256(value: &str) -> Result<(), String> {
    let Some(hex) = value.strip_prefix("sha256:") else {
        return Err(format!("missing sha256 prefix: {}", value));
    };

    if hex.len() != 64 {
        return Err(format!("invalid sha256 hex length: {}", hex.len()));
    }

    if !hex.chars().all(|c| c.is_ascii_hexdigit()) {
        return Err("sha256 value contains non-hex characters".into());
    }

    Ok(())
}

pub fn validate_merkle_root(value: &str) -> Result<(), String> {
    if value.starts_with("merkle:") {
        Ok(())
    } else {
        Err(format!("missing merkle prefix: {}", value))
    }
}
