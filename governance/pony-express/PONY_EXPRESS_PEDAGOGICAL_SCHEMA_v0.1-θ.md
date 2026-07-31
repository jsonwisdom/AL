# PONY EXPRESS pedagogical schema v0.1-θ

## 0. Preamble

**Label:** Purpose  
This schema defines a teaching-oriented layer for the `agent/pony-express-v0-1` branch. It is strictly:
- **Non-normative:** No legal, ethical, or historical authority is claimed.
- **Non-equivalent:** No scenario is asserted to match real-world events or actors.
- **Sandbox-bound:** All activity is confined to the draft PR and simulation context.

Gate posture: `GATE_1 = BLOCKED`.  
Docket posture: `CORE_DOCKET = EMPTY`.

## 1. Scope and invariants

**Label:** Scope  
- **Target:** Introductory civic reasoning, procedural literacy, and structured argument practice.
- **Audience:** Learners interacting with simulated artifacts only.
- **Artifacts:** Board game schema, navigation schema, judicial engineering variants, and moot court framework.

**Label:** Invariants  
1. **No promotion:** Outputs cannot be treated as policy, law, or historical verdicts.  
2. **No source admission:** Real-world evidence, cases, or parties are not admitted into the core docket.  
3. **Scenario abstraction:** All scenarios are explicitly tagged as fictional, stylized, or pedagogical.  
4. **Replayability:** Every exercise is designed to be re-run with the same inputs and rules.  
5. **Hash-stability:** Text blocks intended for governance use are kept stable once committed, except under explicit version bumps.

## 2. Pedagogical axes

**Label:** Self axis (learner)  
- **Goal:** Practice structured reasoning, role separation, and rule-following.  
- **Activities:**  
  - Identify roles and constraints in a given scenario.  
  - Draft arguments within defined evidence rules.  
  - Reflect on how rule changes alter outcomes.

**Label:** Justice axis (system)  
- **Goal:** Expose learners to the idea of procedural fairness without simulating real courts.  
- **Activities:**  
  - Compare different rule sets (e.g., strict vs. permissive evidence filters).  
  - Observe how gate posture (`BLOCKED` vs. `OPEN_SIMULATION`) changes what can be considered.  
  - Map “what the system allows” vs. “what the learner wants to argue”.

## 3. Scenario layer (PENDING_SCENARIO)

**Label:** Scenario status  
- Default: `self_axis = PENDING_SCENARIO`, `justice_axis = PENDING_EVIDENCE`.  
- No scenario is active until explicitly instantiated as **FICTIONAL_CASE**.

**Label:** Scenario template  
Each pedagogical scenario must declare:

1. **Scenario ID:**  
   - Format: `SCN-θ-<short-name>-v0.1`.  
2. **Scenario type:**  
   - `FICTIONAL_CASE`, `BOARD_GAME_EPISODE`, or `NAVIGATION_EXERCISE`.  
3. **Fictional boundary statement:**  
   - A one-paragraph disclaimer that the scenario is invented and non-authoritative.  
4. **Roles:**  
   - Learner roles (e.g., “Advocate A”, “Advocate B”, “Rule Interpreter”).  
5. **Constraints:**  
   - What evidence types are allowed (e.g., only text cards from the game schema).  
6. **Win / completion conditions:**  
   - Clear, non-legal criteria (e.g., “All players agree on a rule interpretation” or “Board state reaches stable configuration”).

## 4. Learning modules

**Label:** Module 1 – Rule reading and mapping  
- **Objective:** Learn to parse a rule text and map it to actions.  
- **Inputs:** Excerpts from `CIVIC_WAR_GAME_SCHEMA_v0.1.json` and navigation schema.  
- **Tasks:**  
  - Highlight “must”, “may”, and “cannot” clauses.  
  - Draw a simple flowchart of allowed moves.  
  - Identify at least one ambiguity and propose a clarifying rewrite.

**Label:** Module 2 – Argument construction  
- **Objective:** Practice building arguments under constraints.  
- **Inputs:** A fictional scenario card + allowed evidence tokens.  
- **Tasks:**  
  - Write a short “opening statement” using only permitted tokens.  
  - List which tokens were excluded and why (rule citation).  
  - Reflect on how the constraints shaped the argument.

**Label:** Module 3 – Gate posture awareness  
- **Objective:** Understand how gate states affect what can happen.  
- **Inputs:** Same scenario under two gate states: `GATE_1 = BLOCKED` vs. `GATE_1 = OPEN_SIMULATION`.  
- **Tasks:**  
  - Describe what changes when the gate is blocked (e.g., no scenario admission).  
  - Describe what changes when the gate is open in simulation only (still non-authoritative).  
  - Compare learner experience under each posture.

## 5. Assessment and reflection

**Label:** Formative assessment  
- **Artifacts:**  
  - Short written reflections.  
  - Move logs from board game episodes.  
  - Argument drafts from moot court exercises.

**Label:** Reflection prompts  
- “Which rule constrained you the most, and how did you adapt?”  
- “Did you ever want to use information the system forbade? What did that feel like?”  
- “How would you redesign one rule to be clearer without changing its effect?”

## 6. Safety and boundary statements

**Label:** Non-authority statement  
This schema is a teaching tool only. It does not:
- Provide legal advice.  
- Represent real courts, cases, or persons.  
- Establish any normative or historical truth.

**Label:** Boundary enforcement  
- All scenarios must include a visible disclaimer.  
- Any attempt to import real-world cases or evidence into the core docket is rejected at `GATE_1`.  
- Historical verification remains `NOT_PERFORMED` unless a separate, explicitly scoped research artifact is created (outside this schema).

## 7. Versioning

**Label:** Version tag  
- Current: `PONY_EXPRESS_PEDAGOGICAL_SCHEMA_v0.1-θ`.  

**Label:** Change rules  
- Minor clarifications: `v0.1-θ.x` (text-only, no semantic change).  
- Semantic changes: bump to `v0.2-θ` with explicit changelog entry.  
- Gate posture changes: require separate governance artifact; not permitted inside this file.
