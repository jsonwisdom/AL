use crate::hash::content_hash::ContentHash;

pub trait AnchorResolver {
    type Error;

    fn resolve(&self, hash: &ContentHash) -> Result<Vec<u8>, Self::Error>;
}
