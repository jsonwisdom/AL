package validator

import (
	"encoding/json"
	"errors"
	"os"
	"path/filepath"
	"testing"
)

type fixtureExpectation struct {
	ExpectedResult      string `json:"expected_result"`
	ExpectedError       string `json:"expected_error"`
	ExpectedCLIExitCode int    `json:"expected_cli_exit_code"`
	BranchContext       string `json:"branch_context"`
}

func TestNegativeMerkleFixtures(t *testing.T) {
	fixtures := []string{
		"fixture-006-merkle-mutated-leaf",
		"fixture-007-cross-branch-proof-forgery",
	}

	for _, fixture := range fixtures {
		fixture := fixture
		t.Run(fixture, func(t *testing.T) {
			base := filepath.Join("..", "..", "tests", "cleansing_gate", "fixtures", "negative", fixture)

			proofBytes, err := os.ReadFile(filepath.Join(base, "proof.json"))
			if err != nil {
				t.Fatalf("read proof: %v", err)
			}
			var proof MerkleProof
			if err := json.Unmarshal(proofBytes, &proof); err != nil {
				t.Fatalf("decode proof: %v", err)
			}

			expectationBytes, err := os.ReadFile(filepath.Join(base, "expected.json"))
			if err != nil {
				t.Fatalf("read expectation: %v", err)
			}
			var expectation fixtureExpectation
			if err := json.Unmarshal(expectationBytes, &expectation); err != nil {
				t.Fatalf("decode expectation: %v", err)
			}

			if expectation.ExpectedResult != "REJECT" || expectation.ExpectedError != "MERKLE_MISMATCH" || expectation.ExpectedCLIExitCode != MerkleMismatchExitCode {
				t.Fatalf("invalid fixture expectation: %+v", expectation)
			}

			err = ValidateMerkleProof(proof, expectation.BranchContext)
			if !errors.Is(err, ErrMerkleMismatch) {
				t.Fatalf("expected ErrMerkleMismatch, got %v", err)
			}
		})
	}
}
