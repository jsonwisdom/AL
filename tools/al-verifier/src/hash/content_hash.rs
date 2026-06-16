use serde::{Deserialize, Serialize};
use sha2::{Digest, Sha256};

#[derive(Debug, Clone, PartialEq, Eq, Hash, Serialize, Deserialize)]
pub struct ContentHash {
    pub algorithm: String,
    pub value: [u8; 32],
}

impl ContentHash {
    pub fn from_sha256_hex(input: &str) -> Result<Self, String> {
        let hex = input.strip_prefix("sha256:").unwrap_or(input);

        let bytes = hex::decode(hex)
            .map_err(|e| format!("hex decode failed: {}", e))?;

        if bytes.len() != 32 {
            return Err(format!("expected 32 bytes, got {}", bytes.len()));
        }

        let mut value = [0u8; 32];
        value.copy_from_slice(&bytes);

        Ok(Self {
            algorithm: "sha256".into(),
            value,
        })
    }

    pub fn to_string(&self) -> String {
        format!("sha256:{}", hex::encode(self.value))
    }
}

pub fn hash_bytes(bytes: &[u8]) -> ContentHash {
    let mut hasher = Sha256::new();
    hasher.update(bytes);
    let result = hasher.finalize();

    let mut value = [0u8; 32];
    value.copy_from_slice(&result);

    ContentHash {
        algorithm: "sha256".into(),
        value,
    }
}
