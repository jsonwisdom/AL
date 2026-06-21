# MN Fiscal Replay — Primary User Groups v0.1

**Artifact:** `MN_FISCAL_REPLAY_PRIMARY_USER_GROUPS_V0_1`  
**Lane:** `MN_FISCAL_REPLAY`  
**Status:** `RECORDED_FOR_PUBLIC_SITE_INTEGRATION`  
**NO_FAKE_GREEN:** `ACTIVE`

---

## Purpose

This architecture serves user groups requiring deterministic, zero-trust verification of public records.

The public site should explain these groups in plain language without implying unsupported allegations, fraud, or confirmed document tampering.

---

## Primary User Groups

### 1. Independent Forensic Auditors & Civic Watchdogs

Individuals tracking state-level budget adjustments who require a decentralized, mathematical baseline to detect possible institutional document revisions without relying on trust alone.

### 2. Legislative Researchers & Policy Analysts

Staffers and analysts managing multi-hundred-page fiscal forecasts, including Minnesota Management and Budget releases, who need automated regression testing to isolate textual or numerical drift between official revisions.

### 3. Investigative & Data Journalists

Newsroom teams requiring a reproducible chain of evidence that can convert claims about document changes into verifiable, reviewable, git-diff-style facts.

### 4. Public Records & MGDPA Litigators

Legal professionals who need strict document provenance and chain-of-custody records for public evidence, including proof that state-submitted PDFs match historical public hashes or identifying when they do not.

### 5. Civic Tech Developers & Sovereign Archive Builders

Systems architects looking for an open-source, reproducible pattern for public-records compliance workflows, including PDF-to-text extraction, chunk comparison, receipt generation, and optional ledger anchoring.

---

## Public-Safe Language Boundary

Allowed public framing:

```text
verification
baseline tracking
provenance
chain of custody
public records integrity
formatting drift
substantive content change
no public discrepancy claim issued
```

Blocked public framing unless evidence proves it:

```text
fraud
tampering
cover-up
silent alteration
institutional misconduct
confirmed discrepancy
```

---

## Site Integration Target

Recommended public page section title:

```text
Who this register is for
```

Recommended placement:

```text
After: What is being monitored?
Before: Audited document streams
```

---

## Loop Status

```text
ENTRY_TRIGGER = PUBLIC_VALUE_CONTEXT_ADDED
ACTION = RECORD_USER_GROUPS_FOR_SITE_INTEGRATION
EXIT_STATUS = PASS_WITH_LIMITS
LIMITATION = Website HTML not yet updated in this receipt.
```
