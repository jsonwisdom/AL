use crate::model::verdict::{
    DiffSet, GovernanceAnchor, RootSet, SettlementReadiness, VerdictStatus, VerdictV1,
    VerifierInfo,
};

#[derive(Debug, thiserror::Error)]
pub enum InternalError {
    #[error("anchor resolution failed")]
    AnchorResolutionFailed,

    #[error("receipt decode failed")]
    ReceiptDecodeFailed,

    #[error("replay engine unavailable")]
    ReplayUnavailable,
}

impl InternalError {
    pub fn into_verdict(
        self,
        receipt_id: String,
        expected_roots: RootSet,
        verifier_env_hash: String,
    ) -> VerdictV1 {
        VerdictV1 {
            verdict_version: "VERDICT_V1".into(),
            verdict_id: "verifier-error-auto".into(),
            created_at: "2026-05-24T08:41:00Z".into(),
            governance_anchor: GovernanceAnchor {
                tag: "GOVERNANCE_V1".into(),
                manifest_commit: "0ef5076170008ff428a0c9163c7c4822c42ebfdd".into(),
                verifier_schema_ref: "VERIFIER_V1".into(),
            },
            receipt_id,
            status: VerdictStatus::VerifierError,
            expected_roots: expected_roots.clone(),
            observed_roots: expected_roots,
            diff: DiffSet {
                diff_required: false,
                divergent_invocations: vec![],
                divergent_transitions: vec![],
                diff_root: "sha256:9999999999999999999999999999999999999999999999999999999999999999"
                    .into(),
            },
            verifier: VerifierInfo {
                verifier_id: "noop-court-v1".into(),
                verifier_env_hash,
                verifier_spec_ref: "VERIFIER_V1".into(),
            },
            settlement_readiness: SettlementReadiness {
                eligible_for_challenge: true,
                eligible_for_settlement: false,
                recommended_action: "NONE".into(),
            },
        }
    }
}
