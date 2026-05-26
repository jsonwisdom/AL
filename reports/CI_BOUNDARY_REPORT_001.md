# CI_BOUNDARY_REPORT_001
Classification: BOUNDARY_MEMBRANE_ATTESTATION  
Authority: NONE  
Doctrine: replay-only, no governance, no semantic authority  
Operator: Jason  
Status: CLEAN

## 1. Truth Surfaces

- Exposure Audit #922: PASS  
  Commit: de624bddc6b148e9969588b267ff7cb96b94ed5f  
  First run under corrected Scorecard gating.

- Historical Failure #921: PRESERVED  
  Commit: 8a3d3b0dff994676117f62bb80c936a41dff322e  
  Failure due to Scorecard running on a non-default branch.  
  Retained as pre-patch evidence.

- v0.2 Skeleton Commit: 87d80c53  
- v0.1 Freeze Commit: ae12a64a

## 2. Boundary Condition Change

Applied guard:

    if: github.ref == 'refs/heads/main' || github.ref == 'refs/heads/master'

Purpose:
- Default-branch gating for OpenSSF Scorecard  
- Prevents Scorecard from executing on ALMS research branches  
- Eliminates false failures unrelated to research-branch intent  
- Preserves mainline governance enforcement

Effect:
- Establishes #921 → #922 correction trail  
- Maintains research-branch sovereignty  
- Keeps exposure-audit CI separate from vector-pack CI

## 3. Membrane Integrity Assessment

- Gitleaks: PASS  
- Scorecard: GUARDED  
- ALMS Branch Membrane: CLEAN  
- Cross-branch contamination: NONE  
- Semantic drift: NONE  
- Replay determinism: PRESERVED

## 4. Rationale for Preserving #921

- Historical evidence is part of the audit chain  
- Pre-patch failure surfaces document system state before correction  
- Supersession semantics: #922 supersedes #921 as authoritative  
- No remediation appropriate or allowed

## 5. Boundary Rationale (for future operators)

This report documents:
- Why Scorecard is default-branch only  
- Why research branches must not inherit mainline governance checks  
- Why #921 is preserved  
- How #922 establishes the corrected truth surface  
- How ALMS vector-pack CI remains isolated from exposure-audit CI

## 6. Next Action

None required.  
Boundary is stable.  
Membrane is clean.  
Lineage is preserved.
