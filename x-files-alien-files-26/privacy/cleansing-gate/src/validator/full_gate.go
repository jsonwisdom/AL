package validator

import (
	"context"
	"crypto/ed25519"
	"errors"
	"io"
	"time"
)

// ErrFullGateNotImplemented is returned until every dependency in the
// Cleansing Gate decision chain has a concrete fail-closed implementation.
var ErrFullGateNotImplemented = errors.New("FULL_GATE_NOT_IMPLEMENTED")

// Manifest is the runtime contract consumed by ValidateFullCleansingGate.
// It intentionally separates expected values from observed inputs supplied
// through FileSet and NonceStore.
type Manifest struct {
	BranchContext string
	Nonce         string
	Merkle        MerkleProof
}

// FileSet supplies the actual bytes whose SHA-256 digests must be recomputed.
type FileSet struct {
	Input   io.Reader
	Output  io.Reader
	Preview io.Reader
}

// NonceStore must atomically consume a nonce. Implementations must reject a
// nonce that has already been consumed in the applicable key/session scope.
type NonceStore interface {
	Consume(ctx context.Context, nonce string) error
}

// ValidateFullCleansingGate defines the complete fail-closed entrypoint.
//
// Required execution order:
//   1. Ed25519 signature and signing-key binding
//   2. Atomic nonce consumption / replay rejection
//   3. Branch binding
//   4. Merkle proof verification
//   5. Input/output/preview SHA-256 recomputation
//
// This contract scaffold never returns nil. Concrete dependency
// implementations must be introduced and tested before an ALLOW decision is
// possible.
func ValidateFullCleansingGate(
	ctx context.Context,
	manifest Manifest,
	publicKey ed25519.PublicKey,
	files FileSet,
	nonceStore NonceStore,
	now time.Time,
) error {
	if ctx == nil || len(publicKey) != ed25519.PublicKeySize || nonceStore == nil || now.IsZero() {
		return ErrFullGateNotImplemented
	}
	if manifest.BranchContext == "" || manifest.Nonce == "" {
		return ErrFullGateNotImplemented
	}
	if files.Input == nil || files.Output == nil || files.Preview == nil {
		return ErrFullGateNotImplemented
	}
	return ErrFullGateNotImplemented
}
