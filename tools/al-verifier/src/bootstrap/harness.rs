use crate::error::InternalError;
use crate::io::resolver::AnchorResolver;
use crate::model::receipt::ReceiptV1;
use crate::model::verdict::RootSet;
use std::io::{Read, Write};

pub fn run_verifier<R: Read, W: Write, Res: AnchorResolver>(
    mut input: R,
    mut output: W,
    _resolver: Res,
) -> Result<(), Box<dyn std::error::Error>> {
    let receipt: ReceiptV1 = serde_json::from_reader(&mut input)?;

    let expected_roots = RootSet {
        state_transitions_root: receipt
            .observed_roots
            .state_transitions_root
            .clone(),
        tool_graph_root: receipt.observed_roots.tool_graph_root.clone(),
    };

    let verdict = InternalError::ReplayUnavailable.into_verdict(
        receipt.receipt_id,
        expected_roots,
        receipt.execution.verifier_env_hash,
    );

    serde_json::to_writer_pretty(&mut output, &verdict)?;

    Ok(())
}
