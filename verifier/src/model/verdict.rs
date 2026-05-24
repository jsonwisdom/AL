use serde::{Deserialize, Serialize};

#[derive(Debug, Clone, Serialize, Deserialize, PartialEq, Eq)]
pub struct VerdictV1 {
    pub verdict_version: String,
    pub receipt_id: String,
    pub status: VerdictStatus,
    pub verifier_version: String,
    pub verified_at: String,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub error: Option<VerifierError>,
}

#[derive(Debug, Clone, Serialize, Deserialize, PartialEq, Eq)]
#[serde(rename_all = "SCREAMING_SNAKE_CASE")]
pub enum VerdictStatus {
    Verified,
    Divergent,
    VerifierError,
}

#[derive(Debug, Clone, Serialize, Deserialize, PartialEq, Eq)]
pub struct VerifierError {
    pub code: String,
    pub message: String,
}
