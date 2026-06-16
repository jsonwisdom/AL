use al_verifier::bootstrap::harness::run_verifier;
use al_verifier::hash::content_hash::ContentHash;
use al_verifier::io::resolver::AnchorResolver;
use std::io;

struct NullResolver;

impl AnchorResolver for NullResolver {
    type Error = String;

    fn resolve(&self, _hash: &ContentHash) -> Result<Vec<u8>, Self::Error> {
        Err("resolver unavailable".into())
    }
}

fn main() -> Result<(), Box<dyn std::error::Error>> {
    let resolver = NullResolver;

    run_verifier(io::stdin(), io::stdout(), resolver)?;

    Ok(())
}
