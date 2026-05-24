use crate::{Receipt, Verdict};

pub fn parse_receipt(input: &str) -> Result<Receipt, serde_json::Error> {
    serde_json::from_str(input)
}

pub fn parse_verdict(input: &str) -> Result<Verdict, serde_json::Error> {
    serde_json::from_str(input)
}
