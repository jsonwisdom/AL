import assert from "node:assert/strict";
import { createHash } from "node:crypto";
import test from "node:test";

import { merkleRoot } from "../dist/src/batch.js";
import { generateProof, verifyProof } from "../dist/src/proof.js";

function fakeLeaf(label) {
  return `sha256:${createHash("sha256").update(label, "utf8").digest("hex")}`;
}

function leaves(n) {
  return Array.from({ length: n }, (_, i) => fakeLeaf(`leaf-${i}`));
}

test("single-leaf-001", () => {
  const L = leaves(1);
  const proof = generateProof(L, 0);
  assert.equal(proof.siblings.length, 0);
  assert.equal(proof.root, L[0]);
  assert.equal(verifyProof(proof).merkle_status, "INCLUDED");
});

test("odd-leaf-duplication-001", () => {
  const L = leaves(3);
  const root = merkleRoot(L);
  const proof = generateProof(L, 2);
  assert.equal(proof.siblings[0], L[2]);
  assert.equal(verifyProof(proof).root, root);
});

test("all-indices-match-root-001", () => {
  const L = leaves(5);
  const root = merkleRoot(L);
  for (let i = 0; i < L.length; i++) {
    const proof = generateProof(L, i);
    assert.equal(verifyProof(proof).root, root);
  }
});

test("side-flip-rejected-001", () => {
  const L = leaves(2);
  const proof = generateProof(L, 0);
  assert.throws(() => verifyProof({ ...proof, index: 1 }), /PROOF_ROOT_MISMATCH/);
});
