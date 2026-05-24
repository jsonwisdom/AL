use serde::{Deserialize, Serialize};

#[derive(Debug, Clone, Serialize, Deserialize, PartialEq, Eq)]
#[serde(rename_all = "SCREAMING_SNAKE_CASE")]
pub enum VerdictStatus {
    Verified,
    Divergent,
    VerifierError,
}

#[derive(Debug, Clone, Serialize, Deserialize, PartialEq, Eq)]
pub struct RootSet {
    pub state_transitions_root: String,
    pub tool_graph_root: String,
}

#[derive(Debug, Clone, Serialize, Deserialize, PartialEq, Eq)]
pub struct DiffSet {
    pub diff_required: bool,
    pub divergent_invocations: Vec<String>,
    pub divergent_transitions: Vec<u64>,
    pub diff_root: String,
}

#[derive(Debug, Clone, Serialize, Deserialize, PartialEq, Eq)]
pub struct GovernanceAnchor {
    pub tag: String,
    pub manifest_commit: String,
    pub verifier_schema_ref: String,
}

#[derive(Debug, Clone, Serialize, Deserialize, PartialEq, Eq)]
pub struct VerifierInfo {
    pub verifier_id: String,
    pub verifier_env_hash: String,
    pub verifier_spec_ref: String,
}

#[derive(Debug, Clone, Serialize, Deserialize, PartialEq, Eq)]
pub struct SettlementReadiness {
    pub eligible_for_challenge: bool,
    pub eligible_for_settlement: bool,
    pub recommended_action: String,
}

#[derive(Debug, Clone, Serialize, Deserialize, PartialEq, Eq)]
pub struct VerdictV1 {
    pub verdict_version: String,
    pub verdict_id: String,
    pub created_at: String,
    pub governance_anchor: GovernanceAnchor,
    pub receipt_id: String,
    pub status: VerdictStatus,
    pub expected_roots: RootSet,
    pub observed_roots: RootSet,
    pub diff: DiffSet,
    pub verifier: VerifierInfo,
    pub settlement_readiness: SettlementReadiness,
}
