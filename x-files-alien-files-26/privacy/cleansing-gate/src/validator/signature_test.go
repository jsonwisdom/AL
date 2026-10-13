package validator

import (
	"crypto/ed25519"
	"crypto/sha256"
	"encoding/hex"
	"errors"
	"testing"
)

func signedManifest(t *testing.T) (Manifest, ed25519.PublicKey) {
	t.Helper()
	seed := sha256.Sum256([]byte("cleansing-gate-signature-test-seed-v0.1"))
	privateKey := ed25519.NewKeyFromSeed(seed[:])
	publicKey := privateKey.Public().(ed25519.PublicKey)
	keyID := sha256.Sum256(publicKey)

	m := Manifest{
		Version: "0.1",
		AssetID: "gray-baby-memory-blossom-001",
		BranchContext: "reston/memory-blossom/main",
		Lineage: []string{"reston", "memory-blossom", "main"},
		SessionID: "018f4f0c-7f93-7c13-9e42-0f4f44fc7482",
		Nonce: "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
		IssuedAt: "2026-07-12T01:40:00Z",
		ExpiresAt: "2026-07-12T01:45:00Z",
		PipelineVersion: "CLEANSING_GATE_V0_1",
		InputSHA256: "bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb",
		OutputSHA256: "cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc",
		PreviewSHA256: "dddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddd",
		ExportTarget: ExportTarget{Mode: "local-only", Destination: nil, BranchID: "reston/memory-blossom/main"},
		Merkle: MerkleProof{
			LeafHash: "2a18af40425f9232914f2a39bb86d657e6e565840a96d8419ce89f3789da3cc0",
			Siblings: []MerkleSibling{{Position: "right", Hash: "48178dbc3645aba3865d00a384a53a58bcedbb3cd840b21d06ebb4d00756888d"}},
			Root: "26100e348b15e808ec4a2f54ae3995afc5e8adee297d51298c5d287ebc85ed89",
			BranchID: "reston/memory-blossom/main",
			Depth: 1,
		},
		NormalizedFilename: "20260712T014000Z_bbbbbbbbbbbbbbbb.png",
		StegoPolicy: "REJECT_IF_DETECTED_OR_UNSUPPORTED",
		SigningKeyID: hex.EncodeToString(keyID[:]),
		SignatureAlgorithm: "Ed25519",
		CleansingRequired: true,
	}
	payload, err := canonicalPayload(m)
	if err != nil {
		t.Fatalf("canonical payload: %v", err)
	}
	m.ParentSignature = ed25519.Sign(privateKey, payload)
	return m, publicKey
}

func TestVerifySignatureAcceptsValidSignatureAndKeyBinding(t *testing.T) {
	m, publicKey := signedManifest(t)
	if err := verifySignature(m, publicKey); err != nil {
		t.Fatalf("expected signature acceptance, got %v", err)
	}
}

func TestVerifySignatureRejectsMutatedPayload(t *testing.T) {
	m, publicKey := signedManifest(t)
	m.AssetID = "mutated-asset"
	if err := verifySignature(m, publicKey); !errors.Is(err, ErrInvalidSignature) {
		t.Fatalf("expected ErrInvalidSignature, got %v", err)
	}
}

func TestVerifySignatureRejectsWrongKeyBinding(t *testing.T) {
	m, publicKey := signedManifest(t)
	m.SigningKeyID = "eeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee"
	if err := verifySignature(m, publicKey); !errors.Is(err, ErrKeyBinding) {
		t.Fatalf("expected ErrKeyBinding, got %v", err)
	}
}

func TestCanonicalPayloadExcludesParentSignature(t *testing.T) {
	m, _ := signedManifest(t)
	first, err := canonicalPayload(m)
	if err != nil {
		t.Fatal(err)
	}
	m.ParentSignature = make([]byte, ed25519.SignatureSize)
	second, err := canonicalPayload(m)
	if err != nil {
		t.Fatal(err)
	}
	if string(first) != string(second) {
		t.Fatal("parent_signature affected canonical payload")
	}
}
