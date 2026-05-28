# Jay's Syllabus v0.1

Status: Draft Teaching Path  
Builder: Jason Wisdom / jaywisdom.base.eth  
Origin: Alabama, USA  
Scope: Jay's AL learning environment  
Authority: false  
Politics: excluded  
State lines: false

## One-Sentence Purpose

Jay's AL teaches kids, parents, teachers, builders, and agents how to check reality, protect privacy, use receipts, and move through ideas at machine speed.

## Rule 1

```txt
If you cannot explain it to a six-year-old, you do not understand it yet.
```

## Kid Translation

```txt
Do not guess. Check.
```

## Root Lesson

```txt
Reality is not what is loud.
Reality is what can be checked.
```

## Course Frame

```json
{
  "course": "Jay's Syllabus",
  "environment": "Jay's AL",
  "builder": "jaywisdom.base.eth",
  "mode": "repo_parkour",
  "goal": "enter_reality_at_machine_speed",
  "politics": false,
  "authority": false,
  "state_lines": false
}
```

## Learners

This syllabus is for:

- kids
- parents
- teachers
- builders
- agents
- verifiers
- guardians
- curious people starting from zero

## Learning Outcomes

By the end, a learner should be able to:

1. Ask where a claim came from.
2. Find or request a source.
3. Understand that private information must be protected.
4. Know what a receipt means.
5. Understand that computers can check things quickly.
6. See why payment proofs matter for machine-speed work.
7. Understand that replay checks what happened without touching real systems.
8. Move through a repo like a map instead of a filing cabinet.
9. Refuse loud claims that cannot be checked.
10. Start from zero again tomorrow.

## Module 0: Start From Zero

### Big Idea

Every day is a new chance to learn.

### Kid Rule

```txt
Today I can choose one good mission.
```

### Activity

Pick one question:

- What do I want to learn today?
- What do I want to check today?
- What do I want to build today?
- What should I protect today?

### Receipt

```json
{
  "module": "start_from_zero",
  "mission_chosen": true,
  "receipt_required": false
}
```

## Module 1: Sources

### Big Idea

A claim needs a source before it can become trusted.

### Kid Rule

```txt
Ask: where did this come from?
```

### Activity

Show three cards:

1. A claim with a source.
2. A claim with no source.
3. A claim that is only someone yelling.

Learners sort them into:

- checkable
- needs source
- not ready

### Receipt

```json
{
  "module": "sources",
  "skill": "claim_classification",
  "win_condition": "learner_can_separate_checkable_from_unchecked"
}
```

## Module 2: Privacy

### Big Idea

Some information should be protected.

### Kid Rule

```txt
Before you share, ask your guardian.
```

### Activity

Sort information into:

- safe to share
- ask first
- keep private

Examples:

- favorite color
- home address
- school name
- password
- drawing
- parent phone number

### Receipt

```json
{
  "module": "privacy",
  "skill": "safe_sharing",
  "guardian_review": true
}
```

## Module 3: Receipts

### Big Idea

A receipt helps us remember what happened.

### Kid Rule

```txt
Keep the proof.
```

### Activity

Learners compare:

- a story with no proof
- a picture
- a timestamp
- a signed receipt

They learn that better proof makes checking easier.

### Receipt

```json
{
  "module": "receipts",
  "skill": "proof_memory",
  "phrase": "keep_the_proof"
}
```

## Module 4: Hashes

### Big Idea

A hash is a tiny fingerprint for data.

### Kid Rule

```txt
If the thing changes, the fingerprint changes.
```

### Activity

Change one letter in a sentence and show that the computer fingerprint changes.

### Receipt

```json
{
  "module": "hashes",
  "skill": "change_detection",
  "kid_translation": "data_fingerprint"
}
```

## Module 5: Verifiers

### Big Idea

A verifier checks whether the rule was followed.

### Kid Rule

```txt
The checker checks the rule.
```

### Activity

Run a simple checklist:

- source present?
- private info protected?
- receipt present?
- hash matched?

### Receipt

```json
{
  "module": "verifiers",
  "skill": "rule_checking",
  "verifier_result": "pass_or_fail_closed"
}
```

## Module 6: Payment Proofs

### Big Idea

Machine-speed work needs clear permission and payment before work starts.

### Kid Rule

```txt
No work button without a proof ticket.
```

### Activity

A game machine has three buttons:

- free demo
- paid fix
- blocked request

Learners see that some actions require a proof ticket first.

### Receipt

```json
{
  "module": "payment_proofs",
  "skill": "bounded_execution",
  "rule": "payment_proof_gates_execution"
}
```

## Module 7: Replay

### Big Idea

Replay checks what happened without doing it again in the real world.

### Kid Rule

```txt
Watch the recording. Do not break the machine again.
```

### Activity

Compare two paths:

- live action
- safe replay

Learners see why replay uses recorded fixtures and never calls real APIs.

### Receipt

```json
{
  "module": "replay",
  "skill": "safe_checking",
  "invariant": "replay_never_calls_real_apis"
}
```

## Module 8: Repo Parkour

### Big Idea

A repo can be a map.

### Kid Rule

```txt
Move room by room.
```

### Activity

Learners follow a route:

```txt
Zero Room -> Source Room -> Receipt Room -> Verifier Room -> Replay Room
```

### Receipt

```json
{
  "module": "repo_parkour",
  "skill": "route_following",
  "win_condition": "learner_can_complete_a_safe_learning_path"
}
```

## Module 9: Family Wisdom

### Big Idea

Children enter reality with guardians, not fear.

### Kid Rule

```txt
Ask. Check. Protect. Learn.
```

### Compass

```txt
          Parent
             ↑
Mrs  ←     Neo     →  Mr
             ↓
          Child
```

### Receipt

```json
{
  "module": "family_wisdom",
  "skill": "guardian_supported_learning",
  "fear_training": false
}
```

## Module 10: Build One Good Thing

### Big Idea

Learning becomes real when you build one small useful thing.

### Kid Rule

```txt
Make one thing better.
```

### Activity

Choose one:

- explain a claim clearly
- protect one private detail
- make a receipt card
- check a source
- design a route
- teach someone Rule 1

### Final Receipt

```json
{
  "module": "build_one_good_thing",
  "completion": true,
  "learner_status": "ready_to_start_from_zero_again"
}
```

## Teacher Rules

```json
{
  "teacher_rules": [
    "explain_in_plain_language",
    "avoid_fear_training",
    "exclude_political_bullshit",
    "protect_children_private_data",
    "never_collect_unneeded_personal_information",
    "treat_failure_as_learning",
    "make_every_step_checkable"
  ]
}
```

## Parent Rules

```json
{
  "parent_rules": [
    "teach_consent",
    "review_privacy_choices",
    "help_children_check_sources",
    "explain_monitoring_before_using_it",
    "never_turn_learning_into_shame",
    "celebrate_receipts_not_loudness"
  ]
}
```

## Builder Rules

```json
{
  "builder_rules": [
    "no_state_lines",
    "no_authority_cosplay",
    "no_live_harm",
    "no_unverified_accusation_promotion",
    "no_execution_without_scope",
    "no_status_without_receipt"
  ]
}
```

## Final Syllabus Line

```txt
Jay's Syllabus teaches people to move through a fast world with sources, privacy, receipts, verifiers, replay, and courage.
```

By Jason Wisdom  
jaywisdom.base.eth