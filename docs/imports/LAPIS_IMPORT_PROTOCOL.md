# Lapis Import Protocol

**Status:** Canonical Import Rule  
**Root Identity:** `jaywisdom.eth`  
**Station:** St. Cloud  
**Doctrine:** If the Auditor cannot read the bytes, the Auditor cannot witness the truth.

---

## 1. Purpose

The Lapis Import Protocol defines how externally referenced material becomes admissible inside the Computer Wisdom archive.

It exists to prevent high-entropy pointers, inaccessible links, private chat URLs, expired share links, and platform-dependent references from being treated as root evidence.

A pointer is not a receipt.

A URL is not a witness.

Only replayable, hashable, inspectable bytes may enter the archive as evidence.

---

## 2. Evidence Is a Pipeline Status

Evidence is not a file type.

Evidence is a status granted by the Lapis pipeline after a claim satisfies admissibility, hashing, replay, attribution, and witness requirements.

Storage is custodial: it keeps a record.

Admissibility is jurisdictional: it decides what the record is allowed to say.

The archive is therefore not merely a warehouse. It is a verification court for imported claims.

A source may exist in storage while remaining non-canonical. A source becomes evidence only after it passes the pipeline.

---

## 3. Classification Rule

ChatGPT share links and similar conversation links are classified as:

```json
{
  "source_type": "chatgpt_share_link",
  "status": "non_canonical",
  "classification": "high_entropy_pointer",
  "reason": "Not guaranteed retrievable or replayable by external observers",
  "required_action": "Paste or export the contents into a repo-tracked artifact before citation, replay, or settlement."
}
```

They may be used as human navigation aids, but they must not be treated as root evidence.

---

## 4. Admissibility Standard

A source becomes admissible only when it has:

1. **Readable Bytes**  
   The content must be directly available to the auditor as text, file bytes, or another stable inspectable format.

2. **Hashability**  
   The content must be capable of deterministic hashing.

3. **Replay Path**  
   An independent observer must be able to reconstruct what was imported and why.

4. **Attribution**  
   The import must preserve source, context, timestamp, and responsible witness where available.

5. **Archive Placement**  
   The imported content must be placed into a repo-tracked path before being treated as canonical.

---

## 5. Recommended Import Path

Use the following pattern for imported conversation material:

```text
docs/imports/<topic>/<timestamp>_conversation_excerpt.md
```

Every imported artifact should include:

- source pointer if available,
- import timestamp,
- importing witness,
- reason for import,
- raw excerpt or full exported text,
- and any known limitations.

---

## 6. Lapis Pipeline

The import pipeline is:

1. Paste or export source contents.
2. Commit imported bytes to the repo.
3. Generate content hash.
4. Create replay sample.
5. Run verifier.
6. Emit `REPLAY_SUMMARY.json`.
7. Only then consider GCS or Base settlement.

No inaccessible link may bypass this pipeline.

---

## 7. Sovereignty Boundary

The Lapis pipeline controls the burden of proof.

Evidence is not “I saw it.” Evidence is:

- here are the bytes,
- here is the hash,
- here is the replay path,
- here is the verifier output,
- here is the witness,
- and here is the lineage.

Ephemeral conversation artifacts may remain as pointers, but only durable, machine-checkable artifacts may cross into settlement.

Anyone who wants GCS or Base finality must satisfy this definition of evidence.

---

## 8. Final Rule

If the Auditor cannot read the bytes, the Auditor cannot witness the truth.

If the Auditor cannot hash the bytes, the archive cannot replay the claim.

If the archive cannot replay the claim, the claim cannot settle.

**No inaccessible link as root evidence.**
