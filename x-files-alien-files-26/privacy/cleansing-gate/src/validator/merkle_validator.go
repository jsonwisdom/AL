// Package validator implements the Cleansing Gate Merkle proof contract.
//
// Status: skeleton implementation. It is fail-closed and side-effect-free,
// but it is not yet promoted as production-ready because concrete fixtures,
// test vectors, and harness integration are still absent.
package validator

import (
	"crypto/sha256"
	"encoding/hex"
	"errors"
	"strings"
)

const (
	// MerkleMismatchExitCode is the future CLI mapping for every Merkle
	// validation failure defined by MERKLE_INTEGRATION_V0_1.md.
	MerkleMismatchExitCode = 8

	nodeDomain = "CG:NODE:V0.1"
)

var ErrMerkleMismatch = errors.New("MERKLE_MISMATCH")

// MerkleSibling preserves the explicit left/right ordering required by v0.1.
type MerkleSibling struct {
	Position string `json:"position"`
	Hash     string `json:"hash"`
}

// MerkleProof is the branch-scoped proof shape defined by the v0.1 spec.
type MerkleProof struct {
	LeafHash string          `json:"leaf_hash"`
	Siblings []MerkleSibling `json:"siblings"`
	Root     string          `json:"root"`
	BranchID string          `json:"branch_id"`
	Depth    int             `json:"depth"`
}

// ValidateMerkleProof performs pure, fail-closed validation.
//
// It returns ErrMerkleMismatch for malformed hashes, impossible paths,
// branch-binding violations, or a recomputed-root mismatch. A separate CLI
// wrapper must map ErrMerkleMismatch to exit code 8.
func ValidateMerkleProof(proof MerkleProof, branchContext string) error {
	if branchContext == "" || proof.BranchID == "" || proof.BranchID != branchContext {
		return ErrMerkleMismatch
	}
	if proof.Depth < 0 || proof.Depth != len(proof.Siblings) {
		return ErrMerkleMismatch
	}

	current, err := decodeHash(proof.LeafHash)
	if err != nil {
		return ErrMerkleMismatch
	}

	for _, sibling := range proof.Siblings {
		siblingHash, err := decodeHash(sibling.Hash)
		if err != nil {
			return ErrMerkleMismatch
		}

		switch sibling.Position {
		case "left":
			current = hashNode(siblingHash, current)
		case "right":
			current = hashNode(current, siblingHash)
		default:
			return ErrMerkleMismatch
		}
	}

	expectedRoot, err := decodeHash(proof.Root)
	if err != nil {
		return ErrMerkleMismatch
	}
	if !equalHash(current, expectedRoot) {
		return ErrMerkleMismatch
	}

	return nil
}

func hashNode(left, right []byte) []byte {
	payload := make([]byte, 0, len(nodeDomain)+len(left)+len(right))
	payload = append(payload, []byte(nodeDomain)...)
	payload = append(payload, left...)
	payload = append(payload, right...)
	digest := sha256.Sum256(payload)
	return digest[:]
}

func decodeHash(value string) ([]byte, error) {
	if len(value) != 64 || value != strings.ToLower(value) {
		return nil, ErrMerkleMismatch
	}
	decoded, err := hex.DecodeString(value)
	if err != nil || len(decoded) != sha256.Size {
		return nil, ErrMerkleMismatch
	}
	return decoded, nil
}

func equalHash(left, right []byte) bool {
	if len(left) != len(right) {
		return false
	}
	var difference byte
	for i := range left {
		difference |= left[i] ^ right[i]
	}
	return difference == 0
}
