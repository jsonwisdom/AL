import { hashPair, merkleRoot, normalizeLeaf } from "./batch.js";

export class ProofError extends Error {
  readonly code: ProofFailureCode;

  constructor(code: ProofFailureCode, message?: string) {
    super(message ?? code);
    this.name = "ProofError";
    this.code = code;
  }
}

export type ProofFailureCode =
  | "EMPTY_BATCH"
  | "INVALID_PROOF_SCHEMA"
  | "PAIRING_UNSUPPORTED"
  | "PROOF_INDEX_INVALID"
  | "PROOF_ROOT_MISMATCH"
  | "LEAF_NOT_IN_BATCH"
  | "RECEIPT_HASH_MISSING";

export const PROOF_VERSION = "merkle-proof.v1" as const;
export const PAIRING_ID = "sha256-utf8-hex" as const;

export interface MerkleProofV1 {
  proof_version: typeof PROOF_VERSION;
  pairing: typeof PAIRING_ID;
  leaf: string;
  index: number;
  siblings: string[];
  root: string;
}

export interface MerkleProofResult {
  merkle_status: "INCLUDED";
  pairing: typeof PAIRING_ID;
  leaf: string;
  index: number;
  root: string;
  semantic_authority: "NOT_CLAIMED";
}

export function generateProof(leaves: string[], index: number): MerkleProofV1 {
  if (!Array.isArray(leaves) || leaves.length === 0) {
    throw new ProofError("EMPTY_BATCH");
  }

  if (!Number.isInteger(index) || index < 0 || index >= leaves.length) {
    throw new ProofError("PROOF_INDEX_INVALID", String(index));
  }

  let current = leaves.map(normalizeLeaf);
  const leaf = current[index] as string;
  const siblings: string[] = [];
  let idx = index;

  while (current.length > 1) {
    const isRight = idx % 2 === 1;
    const pairIndex = isRight ? idx - 1 : idx + 1;
    const sibling = pairIndex < current.length ? current[pairIndex] : current[idx];
    if (sibling === undefined) {
      throw new ProofError("RECEIPT_HASH_MISSING", `index=${idx}`);
    }
    siblings.push(sibling);

    const next: string[] = [];
    for (let i = 0; i < current.length; i += 2) {
      const left = current[i];
      if (left === undefined) {
        throw new ProofError("RECEIPT_HASH_MISSING", `index=${i}`);
      }
      const right = current[i + 1] ?? left;
      next.push(hashPair(left, right));
    }
    current = next;
    idx = Math.floor(idx / 2);
  }

  const root = current[0];
  if (root === undefined) {
    throw new ProofError("EMPTY_BATCH");
  }

  return {
    proof_version: PROOF_VERSION,
    pairing: PAIRING_ID,
    leaf,
    index,
    siblings,
    root
  };
}

export function verifyProof(proof: MerkleProofV1 | unknown): MerkleProofResult {
  if (typeof proof !== "object" || proof === null || Array.isArray(proof)) {
    throw new ProofError("INVALID_PROOF_SCHEMA", "proof must be an object");
  }

  const p = proof as Record<string, unknown>;

  if (p.proof_version !== PROOF_VERSION) {
    throw new ProofError("INVALID_PROOF_SCHEMA", "proof_version");
  }

  if (p.pairing !== undefined && p.pairing !== PAIRING_ID) {
    throw new ProofError("PAIRING_UNSUPPORTED", String(p.pairing));
  }

  if (!Number.isInteger(p.index) || (p.index as number) < 0) {
    throw new ProofError("PROOF_INDEX_INVALID", String(p.index));
  }

  if (!Array.isArray(p.siblings)) {
    throw new ProofError("INVALID_PROOF_SCHEMA", "siblings");
  }

  let node = normalizeLeaf(p.leaf);
  const expectedRoot = normalizeLeaf(p.root);
  let idx = p.index as number;

  for (const sibling of p.siblings) {
    if (typeof sibling !== "string") {
      throw new ProofError("RECEIPT_HASH_MISSING", String(sibling));
    }
    node = idx % 2 === 1 ? hashPair(sibling, node) : hashPair(node, sibling);
    idx = Math.floor(idx / 2);
  }

  if (node !== expectedRoot) {
    throw new ProofError(
      "PROOF_ROOT_MISMATCH",
      `PROOF_ROOT_MISMATCH expected=${expectedRoot} actual=${node}`
    );
  }

  return {
    merkle_status: "INCLUDED",
    pairing: PAIRING_ID,
    leaf: p.leaf as string,
    index: p.index as number,
    root: expectedRoot,
    semantic_authority: "NOT_CLAIMED"
  };
}

export function verifyLeafAgainstRoot(leaf: string, leaves: string[]): MerkleProofResult {
  const normalized = normalizeLeaf(leaf);
  const index = leaves.map(normalizeLeaf).indexOf(normalized);

  if (index < 0) {
    throw new ProofError("LEAF_NOT_IN_BATCH", normalized);
  }

  const proof = generateProof(leaves, index);
  const result = verifyProof(proof);
  const root = merkleRoot(leaves);

  if (result.root !== root) {
    throw new ProofError("PROOF_ROOT_MISMATCH", "generated proof root != merkleRoot(leaves)");
  }

  return result;
}
