use chrono::{DateTime, Utc};
use serde::{Deserialize, Serialize};
use sha2::{Digest, Sha256};

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub enum CeremonyState {
    HeartbeatStable,
    ReadyForCeremony,
    CeremonyInProgress,
    ConstitutionFrozen,
    ActivationComplete,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct CeremonyReceipt {
    pub track_id: String,
    pub previous_state: CeremonyState,
    pub next_state: CeremonyState,
    pub verifier_path: String,
    pub receipt_hash: String,
    pub verified_at: String,
}

fn is_lawful_transition(previous: &CeremonyState, next: &CeremonyState) -> bool {
    use CeremonyState::*;

    matches!(
        (previous, next),
        (HeartbeatStable, ReadyForCeremony)
            | (ReadyForCeremony, CeremonyInProgress)
            | (CeremonyInProgress, ConstitutionFrozen)
            | (ConstitutionFrozen, ActivationComplete)
    )
}

pub fn verify_transition(
    track_id: &str,
    previous: CeremonyState,
    next: CeremonyState,
    verifier_path: &str,
    verifier_artifact: &[u8],
) -> Result<CeremonyReceipt, String> {
    if !is_lawful_transition(&previous, &next) {
        return Err(format!(
            "Forbidden transition: {:?} → {:?}",
            previous, next
        ));
    }

    if verifier_artifact.is_empty() {
        return Err("Verifier artifact is empty; cannot issue receipt".to_string());
    }

    let mut hasher = Sha256::new();
    hasher.update(verifier_artifact);
    let digest = hasher.finalize();
    let hash_hex = hex::encode(digest);
    let receipt_hash = format!("sha256:{hash_hex}");

    let now: DateTime<Utc> = Utc::now();
    let verified_at = now.to_rfc3339();

    Ok(CeremonyReceipt {
        track_id: track_id.to_string(),
        previous_state: previous,
        next_state: next,
        verifier_path: verifier_path.to_string(),
        receipt_hash,
        verified_at,
    })
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn forbidden_transition_is_rejected() {
        let result = verify_transition(
            "TRACK_001",
            CeremonyState::HeartbeatStable,
            CeremonyState::ActivationComplete,
            "_truth/governance/N_consecutive_green.json",
            b"dummy",
        );

        assert!(result.is_err());
        let err = result.unwrap_err();
        assert!(err.contains("Forbidden transition"));
    }

    #[test]
    fn heartbeat_to_ready_is_allowed_with_verifier() {
        let mock_verifier = b"3 consecutive GREEN commits log";

        let result = verify_transition(
            "TRACK_001",
            CeremonyState::HeartbeatStable,
            CeremonyState::ReadyForCeremony,
            "_truth/governance/3_consecutive_green.json",
            mock_verifier,
        );

        assert!(result.is_ok());

        let receipt = result.unwrap();

        assert_eq!(receipt.track_id, "TRACK_001");
        assert_eq!(
            receipt.verifier_path,
            "_truth/governance/3_consecutive_green.json"
        );
        assert!(receipt.receipt_hash.starts_with("sha256:"));
        assert!(!receipt.verified_at.is_empty());
    }
}
