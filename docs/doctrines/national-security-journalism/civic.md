# CIVIC RECORD — National-Security Journalism Doctrine

**Doctrine ID:** `NSJ-001`  
**Version:** `1.0.0`  
**Role:** Operational guidance derived from the sovereign doctrine

## CIVIC RECORD

### Investigative Workflow

A newsroom applying this doctrine SHOULD:

1. Identify the claim and the authority asserting it.
2. Record provenance, custody, release channel, and document version.
3. Separate document authenticity from statement reliability.
4. Map the sovereign-record and civic-record boundary.
5. Record known redactions, withheld attachments, substitutions, docket gaps, and revision history.
6. Seek corroboration independent of the originating institution.
7. Test contradictions and alternative explanations.
8. conduct victim-risk and public-interest review before publication.
9. Hash the final reviewed artifact and retain the receipt.

### Corpus Audit Checklist

For large document releases, record:

- source systems and custodians;
- collection scope and date ranges;
- search terms and collection rules, when public;
- exact-duplicate and near-duplicate treatment;
- parent-message and attachment relationships;
- OCR failures and unreadable files;
- removed, restored, or replaced files;
- stable public identifiers and release URLs;
- redaction categories and stated legal authority;
- unresolved completeness limitations.

### Negative-Space Ledger

A negative-space observation SHOULD include:

- expected artifact;
- observed artifact;
- missing or altered element;
- basis for expecting it;
- government or custodian explanation;
- related docket or metadata evidence;
- confidence level;
- alternative explanations;
- revision trigger.

A missing item alone MUST NOT be labeled misconduct.

### Verification Envelope

```yaml
claim:
classification:
source_type:
source_identity_status:
document_id:
document_date:
custodian:
release_channel:
original_or_copy:
redactions_present:
classification_status:
corroborating_sources: []
contradictory_sources: []
victim_risk_review:
government_response:
confidence:
unknowns: []
revision_trigger:
artifact_hash:
```

### Publication Language

Use bounded language:

- `The document records the allegation that…`
- `The agency states…`
- `The released corpus does not independently establish…`
- `Completeness could not be verified from the civic record.`
- `This remains contested.`

Avoid converting presence in a file, contact list, interview memorandum, intelligence report, or docket into proof of criminal conduct.

### Gate Map

For each major investigation, map control across:

Collector → Investigator → Classifier → Prosecutor → Records custodian → Redaction reviewer → Publishing authority → Search index → Journalist → Public narrative.

At each gate, assess whether context was preserved, delayed, protected, altered, omitted, or made independently reviewable.

### Replay Requirement

A replay is complete only when another reviewer can identify the same inputs, apply the same rules, reproduce the recorded hashes, and distinguish verified facts from unknown, inferred, and contested claims.
