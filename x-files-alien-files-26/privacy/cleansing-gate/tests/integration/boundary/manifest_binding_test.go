package boundary

import (
	"encoding/json"
	"errors"
	"os"
	"testing"

	validator "cleansing-gate/merkle-validator"
)

type manifest struct {
	Version       string   `json:"version"`
	AssetID       string   `json:"asset_id"`
	BranchContext string   `json:"branch_context"`
	Lineage       []string `json:"lineage"`
	ExportTarget  struct {
		Mode        string  `json:"mode"`
		Destination *string `json:"destination"`
		BranchID    string  `json:"branch_id"`
	} `json:"export_target"`
	Merkle validator.MerkleProof `json:"merkle"`
}

func loadManifest(t *testing.T, path string) manifest {
	t.Helper()
	data, err := os.ReadFile(path)
	if err != nil {
		t.Fatalf("read manifest: %v", err)
	}
	var m manifest
	if err := json.Unmarshal(data, &m); err != nil {
		t.Fatalf("decode manifest: %v", err)
	}
	return m
}

func validateBoundary(m manifest) error {
	if m.BranchContext == "" || m.ExportTarget.BranchID == "" || m.Merkle.BranchID == "" {
		return validator.ErrMerkleMismatch
	}
	if m.BranchContext != m.ExportTarget.BranchID {
		return validator.ErrMerkleMismatch
	}
	if m.BranchContext != m.Merkle.BranchID {
		return validator.ErrMerkleMismatch
	}
	return validator.ValidateMerkleProof(m.Merkle, m.BranchContext)
}

func TestManifestMerkleBindingAcceptsConsistentManifest(t *testing.T) {
	m := loadManifest(t, "valid-binding.json")
	if err := validateBoundary(m); err != nil {
		t.Fatalf("expected valid manifest boundary, got %v", err)
	}
}

func TestManifestMerkleBindingRejectsExportTargetDivergence(t *testing.T) {
	m := loadManifest(t, "valid-binding.json")
	m.ExportTarget.BranchID = "reston/memory-blossom/alternate"
	if err := validateBoundary(m); !errors.Is(err, validator.ErrMerkleMismatch) {
		t.Fatalf("expected ErrMerkleMismatch, got %v", err)
	}
}

func TestManifestMerkleBindingRejectsMerkleBranchDivergence(t *testing.T) {
	m := loadManifest(t, "valid-binding.json")
	m.Merkle.BranchID = "reston/emergent-sovereignty/alternate"
	if err := validateBoundary(m); !errors.Is(err, validator.ErrMerkleMismatch) {
		t.Fatalf("expected ErrMerkleMismatch, got %v", err)
	}
}
