package main

import (
	"bytes"
	"encoding/json"
	"errors"
	"fmt"
	"os"

	validator "cleansing-gate/merkle-validator"
)

func main() {
	if len(os.Args) != 3 {
		fmt.Fprintln(os.Stderr, "usage: merkle-validator <proof.json> <branch-context>")
		os.Exit(1)
	}

	proofBytes, err := os.ReadFile(os.Args[1])
	if err != nil {
		fmt.Fprintf(os.Stderr, "SYSTEM_OR_IO_ERROR: %v\n", err)
		os.Exit(1)
	}

	var proof validator.MerkleProof
	decoder := json.NewDecoder(bytes.NewReader(proofBytes))
	decoder.DisallowUnknownFields()
	if err := decoder.Decode(&proof); err != nil {
		fmt.Fprintf(os.Stderr, "SYSTEM_OR_IO_ERROR: decode proof: %v\n", err)
		os.Exit(1)
	}

	if err := validator.ValidateMerkleProof(proof, os.Args[2]); err != nil {
		if errors.Is(err, validator.ErrMerkleMismatch) {
			fmt.Fprintln(os.Stderr, "MERKLE_MISMATCH")
			os.Exit(validator.MerkleMismatchExitCode)
		}
		fmt.Fprintf(os.Stderr, "SYSTEM_OR_IO_ERROR: %v\n", err)
		os.Exit(1)
	}
}
