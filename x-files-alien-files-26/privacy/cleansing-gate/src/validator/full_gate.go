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

// ExportTarget is the runtime export destination binding.
type ExportTarget struct {
	Mode        string  `json:"mode"`
	Destination *string `json:"destination"`
	BranchID    string  `json:"branch_id"`
}

// Manifest is the runtime contract consumed by ValidateFullCleansingGate.
// ParentSignature is excluded from the canonical signed payload.
type Manifest struct {
	Version            string       `json:"version"`
	AssetID            string       `json:"asset_id"`
	BranchContext      string       `json:"branch_context"`
	Lineage            []string     `json:"lineage"`
	ParentSignature    []byte       `json:"parent_signature"`
	SessionID          string       `json:"session_id"`
	Nonce              string       `json:"nonce"`
	IssuedAt           string       `json:"issued_at"`
	ExpiresAt          string       `json:"expires_at"`
	PipelineVersion    string       `json:"pipeline_version"`
	InputSHA256        string       `json:"input_sha256"`
	OutputSHA256       string       `json:"output_sha256"`
	PreviewSHA256      string       `json:"preview_sha256"`
	ExportTarget       ExportTarget `json:"export_target"`
	Merkle             MerkleProof  `json:"merkle"`
	NormalizedFilename string       `json:"normalized_filename"`
	StegoPolicy        string       `json:"stego_policy"`
	SigningKeyID       string       `json:"signing_key_id"`
	SignatureAlgorithm string       `json:"signature_algorithm"`
	CleansingRequired  bool         `json:"cleansing_required"`
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
func ValidateFullCleansingGate(
	ctx context.Context,
	manifest Manifest,
	publicKey ed25519.PublicKey,
	files FileSet,
	nonceStore NonceStore,
	now time.Time,
) error {
	if ctx == nil || nonceStore == nil || now.IsZero() {
		return ErrFullGateNotImplemented
	}
	if files.Input == nil || files.Output == nil || files.Preview == nil {
		return ErrFullGateNotImplemented
	}
	if err := verifySignature(manifest, publicKey); err != nil {
		return err
	}
	return ErrFullGateNotImplemented
}
