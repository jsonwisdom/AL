# AGENT SCHOOL REPUBLIC EXTENSION MAP V0.1

**status:** CANDIDATE  
**role:** LEARNING_REPLAY_EXTENSION_MAP  
**binding_effect:** ZERO  
**operative_authority:** NONE  
**activation:** PROHIBITED  
**authority:** false  

---

## 1. Purpose

This document maps **Agent School Republic** as a candidate extension into existing surfaces of the Glass-Box Republic / ALMS repository.

**This document introduces:**
- ❌ No new schema
- ❌ No new authority
- ❌ No new governance surface
- ❌ No ALMS_v3 activation

**This document only does:**
- ✅ Identify extension candidacy
- ✅ Map learning primitives to existing surfaces
- ✅ Declare transcript output role
- ✅ Route disputes to existing systems

---

## 2. Candidate Identity

| Field | Value |
|-------|-------|
| Name | Agent School Republic |
| Type | Learning transcript extension |
| Relationship | Plugs into existing surfaces |
| Authority | None (explicitly zero) |
| Activation | Prohibited without governance review |

---

## 3. Primitive Mapping

| Agent School Primitive | Existing Repo Surface | File Reference |
|------------------------|----------------------|----------------|
| Learning session transcript | Codex workflow receipt | `docs/codex_workflow_receipts_v0_1.md`<br>`schemas/codex_workflow_receipt.v0_1.schema.json` |
| Student/agent action trace | Witness replay input | `tools/public-replay-witness.html`<br>`witness_court_pilot_v4.py` |
| Refusal / out-of-scope boundary | ALMS agent constraints | `docs/ALMS-v2-SUBSYSTEM-AGENT-CONSTRAINTS.md`<br>`docs/ALMS-v2-SUBSYSTEM-AGENT-OPERATIONS.md` |
| Learning receipt validation | Codex receipt validator | `scripts/validate_codex_workflow_receipt.py` |
| Transcript replay verification | Witness replay CI gate | `constitutional-replay-v1/docs/CI_WITNESS_GATE.md`<br>`constitutional-replay-v1/src/replay.ts` |
| Disputed learning outcome | Replay Court challenge | `replay-court/BOOTSTRAP-REPLAY.md`<br>`replay-court/WITNESS-ANCHOR.md`<br>`schemas/eas/lapis_replay_court_v1.eas.txt` |
| Public archive of verified transcripts | Replay registry | `replay_registry/archive/PUBLIC_REPLAY_WITNESS_V1.sha256.txt`<br>`replay_registry/archive/PUBLIC_REPLAY_WITNESS_TOOL_V1.json` |
| Agent operational bounds | ALMS operations | `docs/ALMS-v2-SUBSYSTEM-AGENT-OPERATIONS.md`<br>`docs/ALMS-v2-SUBSYSTEM-AGENT-OPERATIONS-EXTENSIONS.md` |

---

## 4. Transcript Output Rules

When Agent School Republic produces a learning transcript:

1. **It is a replay input** – not a witness output, not a final judgment
2. **It must be validatable** – using Codex workflow receipt validator patterns
3. **It carries no authority** – transcripts are evidence, not rulings
4. **It respects agent constraints** – refusals and out-of-scope actions preserved

---

## 5. Dispute Routing

| Scenario | Route To |
|----------|----------|
| Learning outcome challenged | Replay Court (`replay-court/`) |
| Transcript replay fails | Witness replay CI gate |
| Receipt validation fails | Codex validator failure path |
| Agent boundary violation | ALMS constraint violation surface |

**No new dispute system is created.**

---

## 6. Authority Declaration

```json
{
  "agent_school_republic": "CANDIDATE_EXTENSION",
  "integration_mode": "MAP_TO_EXISTING_SURFACES",
  "binding_effect": "ZERO",
  "operative_authority": "NONE",
  "activation": "PROHIBITED",
  "authority": false
}
```

---

## 7. Repository State at Mapping

```json
{
  "repo": "jsonwisdom/AL",
  "target_branch": "master",
  "write_posture": "PAUSED_UNTIL_SINGLE_MAP_APPROVED",
  "authority": false
}
```

---

## 8. Next Actions

This document does not authorize:

· Schema creation
· Code writing
· Workflow implementation
· ALMS amendment

Next step: Review this map. No commit until approved.

---

End of map – no authority created, no activation implied.
