use serde::{Deserialize, Serialize};

#[derive(Debug, Clone, Serialize, Deserialize, PartialEq, Eq)]
pub struct ReceiptV1 {
    pub receipt_version: String,
    pub receipt_id: String,
    pub created_at: String,
    pub intent: IntentBlock,
    pub execution: ExecutionBlock,
    pub observed_roots: RootSet,
    pub replay: ReplayBlock,
}

#[derive(Debug, Clone, Serialize, Deserialize, PartialEq, Eq)]
pub struct IntentBlock {
    pub request_hash: String,
    pub actor_hash: String,
    pub constraints_hash: String,
}

#[derive(Debug, Clone, Serialize, Deserialize, PartialEq, Eq)]
pub struct ExecutionBlock {
    pub verifier_env_hash: String,
    pub fixture_hash: String,
    pub replay_contract_hash: String,
    pub execution_block_hash: String,
    #[serde(default)]
    pub tool_calls: Vec<ToolCall>,
    #[serde(default)]
    pub state_transitions: Vec<StateTransition>,
}

#[derive(Debug, Clone, Serialize, Deserialize, PartialEq, Eq)]
pub struct ToolCall {
    pub tool_call_hash: String,
}

#[derive(Debug, Clone, Serialize, Deserialize, PartialEq, Eq)]
pub struct StateTransition {
    pub transition_hash: String,
}

#[derive(Debug, Clone, Serialize, Deserialize, PartialEq, Eq)]
pub struct RootSet {
    pub state_transitions_root: String,
    pub tool_graph_root: String,
}

#[derive(Debug, Clone, Serialize, Deserialize, PartialEq, Eq)]
pub struct ReplayBlock {
    pub canonicalization: String,
    pub requested_action: String,
}
