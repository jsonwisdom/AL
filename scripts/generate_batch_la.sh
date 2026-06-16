#!/usr/bin/env bash
set -e

BASE=data

# --- Leaf 004 Eigenvector ---
mkdir -p $BASE/la_004
cat > $BASE/la_004/claims.json <<'JSON'
{
  "leaf_id": "la_004",
  "model": "linear_algebra_eigen_v1",
  "fields": [{
    "id": "eigenvector_check",
    "canonical_claim": "A=[[2,0],[0,3]], v=[1,0], lambda=2 satisfies Av=lambda v",
    "tests": [
      {"id":"exact_match","claim_text":"A=[[2,0],[0,3]], v=[1,0], lambda=2 satisfies Av=lambda v"},
      {"id":"wrong_lambda","claim_text":"A=[[2,0],[0,3]], v=[1,0], lambda=3 satisfies Av=lambda v"},
      {"id":"wrong_vector","claim_text":"A=[[2,0],[0,3]], v=[0,1], lambda=2 satisfies Av=lambda v"}
    ]
  }]
}
JSON

# --- Leaf 005 Orthogonality ---
mkdir -p $BASE/la_005
cat > $BASE/la_005/claims.json <<'JSON'
{
  "leaf_id": "la_005",
  "model": "linear_algebra_orthogonal_v1",
  "fields": [{
    "id": "dot_product_zero",
    "canonical_claim": "v=[1,0], w=[0,1] are orthogonal",
    "tests": [
      {"id":"exact_match","claim_text":"v=[1,0], w=[0,1] are orthogonal"},
      {"id":"wrong_not_orthogonal","claim_text":"v=[1,0], w=[0,1] are not orthogonal"},
      {"id":"wrong_vectors","claim_text":"v=[1,1], w=[1,1] are orthogonal"}
    ]
  }]
}
JSON

# --- Leaf 006 Determinant ---
mkdir -p $BASE/la_006
cat > $BASE/la_006/claims.json <<'JSON'
{
  "leaf_id": "la_006",
  "model": "linear_algebra_determinant_v1",
  "fields": [{
    "id": "determinant_zero",
    "canonical_claim": "A=[[1,2],[2,4]] has determinant 0",
    "tests": [
      {"id":"exact_match","claim_text":"A=[[1,2],[2,4]] has determinant 0"},
      {"id":"wrong_nonzero","claim_text":"A=[[1,2],[2,4]] has determinant 2"},
      {"id":"wrong_matrix","claim_text":"A=[[1,2],[3,4]] has determinant 0"}
    ]
  }]
}
JSON

echo "Batch claims generated."
