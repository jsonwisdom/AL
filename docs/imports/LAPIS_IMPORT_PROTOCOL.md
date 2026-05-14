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

## 2. Classification Rule

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

## 3. Admissibility Standard

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

## 4. Recommended Import Path

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

## 5. Lapis Pipeline

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

## 6. Final Rule

If the Auditor cannot read the bytes, the Auditor cannot witness the truth.

If the Auditor cannot hash the bytes, the archive cannot replay the claim.

If the archive cannot replay the claim, the claim cannot settle.

**No inaccessible link as root evidence.**
