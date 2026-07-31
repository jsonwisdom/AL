# Moot court framework v0.1-θ (sandbox-only)

## 0. Preamble

**Label:** Purpose  
This framework defines a **fictional moot court** structure for pedagogical use inside `agent/pony-express-v0-1`. It is:
- **Fictional:** All “cases” are invented.
- **Non-binding:** No decisions have any real-world effect.
- **Sandbox-scoped:** Operates only within the draft PR and simulation environment.

Gate posture: `GATE_1 = BLOCKED` for real-world scenario admission.  
Moot court operates on **FICTIONAL_CASE** objects only.

## 1. Role model

**Label:** Roles  
1. **Presiding Facilitator (PF):**  
   - Interprets rules, keeps time, and enforces boundaries.  
   - Cannot issue real-world judgments; only simulation outcomes.

2. **Advocate A (AA):**  
   - Presents arguments in favor of a position defined by the fictional case.

3. **Advocate B (AB):**  
   - Presents arguments against or alternative to AA’s position.

4. **Rule Scribe (RS):**  
   - Logs which rules were invoked, how, and when.  
   - Maintains a neutral record of the session.

**Label:** Optional roles  
- **Observer (OB):** Reflects on process, not outcome.  
- **Designer (DG):** Proposes rule tweaks for future iterations.

## 2. Case objects

**Label:** FICTIONAL_CASE definition  
Each moot court exercise uses a `FICTIONAL_CASE` object with:

1. **Case ID:** `CASE-θ-<short-name>-v0.1`.  
2. **Case summary:** 3–5 sentences describing the fictional dispute.  
3. **Issue list:** 2–4 questions framed as “Should X be allowed under rule Y?”  
4. **Evidence tokens:**  
   - Drawn only from game schemas, navigation artifacts, or bespoke fictional text.  
   - No real-world documents, names, or events.

5. **Boundary disclaimer:**  
   - Explicit statement that the case is fictional and non-authoritative.

## 3. Session phases

**Label:** Phase 0 – Setup  
- PF selects a `FICTIONAL_CASE`.  
- RS loads the relevant rule set (e.g., from `CIVIC_WAR_GAME_SCHEMA`).  
- PF reads the boundary disclaimer aloud or displays it prominently.

**Label:** Phase 1 – Opening statements  
- AA and AB each get a fixed time window (e.g., 3–5 minutes) to present:  
  - Their interpretation of the case issues.  
  - Which rules they expect to rely on.

**Label:** Phase 2 – Evidence and rule application  
- AA and AB may reference only allowed evidence tokens.  
- PF may ask clarifying questions about rule interpretation, not about “truth” of the fictional facts.  
- RS logs each rule citation with:  
  - Rule ID  
  - Who invoked it  
  - Context (issue number)

**Label:** Phase 3 – Deliberation (procedural only)  
- PF summarizes the competing rule interpretations.  
- Group discusses which interpretation best fits the written rules, not which outcome is “morally right”.  
- OB (if present) notes any confusion or ambiguity in the rules.

**Label:** Phase 4 – Simulation outcome  
- PF declares a **simulation outcome**:  
  - Example: “Under these rules, AA’s interpretation is adopted for Issue 1; AB’s for Issue 2.”  
- RS records the outcome as a **session artifact**, tagged as:  
  - `SIMULATION_ONLY`  
  - `NON_PRECEDENTIAL`  
  - `NON_AUTHORITY`

## 4. Logging and replay

**Label:** Session log structure  
Each session produces a log with:

1. **Header:** Case ID, date/time, participants, version tags.  
2. **Rule set reference:** File names and version IDs used.  
3. **Issue-by-issue record:**  
   - Opening positions (AA, AB).  
   - Rules cited.  
   - Simulation outcome.

4. **Reflection section:**  
   - At least two prompts answered by participants.

**Label:** Replayability  
- Logs must be sufficient to replay the session with the same rules and case.  
- Any change to rules or case requires a new Case ID or version tag.

## 5. Boundary and safety constraints

**Label:** Hard constraints  
1. **No real cases:**  
   - PF must reject any attempt to import real-world disputes, names, or documents.  
2. **No normative claims:**  
   - Participants may discuss “what the rules say”, not “what should happen in reality”.  
3. **No authority leakage:**  
   - Outcomes cannot be described as “judgments”, “verdicts”, or “precedent” outside the sandbox.

**Label:** Language constraints  
- Preferred terms: “simulation outcome”, “exercise”, “session”, “artifact”.  
- Avoid: “ruling”, “binding decision”, “legal precedent”.

## 6. Integration with pedagogical schema

**Label:** Linkage  
- Modules from `PONY_EXPRESS_PEDAGOGICAL_SCHEMA_v0.1-θ` can use moot court sessions as:  
  - **Module 2:** Argument construction exercises.  
  - **Module 3:** Gate posture awareness (e.g., what changes if certain evidence tokens are disallowed).

**Label:** Assessment hooks  
- Reflection prompts from the pedagogical schema can be attached to session logs.  
- Designers can propose rule clarifications based on observed confusion.

## 7. Versioning

**Label:** Version tag  
- Current: `MOOT_COURT_FRAMEWORK_v0.1-θ`.

**Label:** Change rules  
- Text clarifications: `v0.1-θ.x`.  
- Structural changes (roles, phases, constraints): bump to `v0.2-θ`.  
- Any change that touches gate posture or docket behavior must be defined in a separate governance artifact and is **out of scope** for this file.
