package validator

import (
	"crypto/ed25519"
	"crypto/sha256"
	"encoding/hex"
	"encoding/json"
	"errors"

	"github.com/cyberphone/json-canonicalization/go/src/webpki.org/jsoncanonicalizer"
)

var (
	ErrInvalidSignature = errors.New("INVALID_SIGNATURE")
	ErrKeyBinding       = errors.New("KEY_BINDING_MISMATCH")
	ErrCanonicalPayload = errors.New("CANONICAL_PAYLOAD_INVALID")
)

// verifySignature validates both the Ed25519 signature and the binding between
// the supplied public key and manifest.signing_key_id.
func verifySignature(manifest Manifest, publicKey ed25519.PublicKey) error {
	if len(publicKey) != ed25519.PublicKeySize {
		return ErrKeyBinding
	}

	digest := sha256.Sum256(publicKey)
	if manifest.SigningKeyID == "" || manifest.SigningKeyID != hex.EncodeToString(digest[:]) {
		return ErrKeyBinding
	}

	payload, err := canonicalPayload(manifest)
	if err != nil {
		return err
	}
	if len(manifest.ParentSignature) != ed25519.SignatureSize || !ed25519.Verify(publicKey, payload, manifest.ParentSignature) {
		return ErrInvalidSignature
	}
	return nil
}

// canonicalPayload returns RFC 8785 / JCS canonical JSON for the signed
// manifest payload. parent_signature is deliberately excluded.
func canonicalPayload(manifest Manifest) ([]byte, error) {
	payload := struct {
		Version           string      `json:"version"`
		AssetID           string      `json:"asset_id"`
		BranchContext     string      `json:"branch_context"`
		Lineage           []string    `json:"lineage"`
		SessionID         string      `json:"session_id"`
		Nonce             string      `json:"nonce"`
		IssuedAt          string      `json:"issued_at"`
		ExpiresAt         string      `json:"expires_at"`
		PipelineVersion   string      `json:"pipeline_version"`
		InputSHA256       string      `json:"input_sha256"`
		OutputSHA256      string      `json:"output_sha256"`
		PreviewSHA256     string      `json:"preview_sha256"`
		ExportTarget      ExportTarget `json:"export_target"`
		Merkle            MerkleProof `json:"merkle"`
		NormalizedFilename string     `json:"normalized_filename"`
		StegoPolicy       string      `json:"stego_policy"`
		SigningKeyID      string      `json:"signing_key_id"`
		SignatureAlgorithm string     `json:"signature_algorithm"`
		CleansingRequired bool        `json:"cleansing_required"`
	}{
		Version: manifest.Version,
		AssetID: manifest.AssetID,
		BranchContext: manifest.BranchContext,
		Lineage: manifest.Lineage,
		SessionID: manifest.SessionID,
		Nonce: manifest.Nonce,
		IssuedAt: manifest.IssuedAt,
		ExpiresAt: manifest.ExpiresAt,
		PipelineVersion: manifest.PipelineVersion,
		InputSHA256: manifest.InputSHA256,
		OutputSHA256: manifest.OutputSHA256,
		PreviewSHA256: manifest.PreviewSHA256,
		ExportTarget: manifest.ExportTarget,
		Merkle: manifest.Merkle,
		NormalizedFilename: manifest.NormalizedFilename,
		StegoPolicy: manifest.StegoPolicy,
		SigningKeyID: manifest.SigningKeyID,
		SignatureAlgorithm: manifest.SignatureAlgorithm,
		CleansingRequired: manifest.CleansingRequired,
	}

	raw, err := json.Marshal(payload)
	if err != nil {
		return nil, ErrCanonicalPayload
	}
	canonical, err := jsoncanonicalizer.Transform(raw)
	if err != nil {
		return nil, ErrCanonicalPayload
	}
	return canonical, nil
}
