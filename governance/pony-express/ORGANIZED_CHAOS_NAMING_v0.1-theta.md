# Organized Chaos — Scholarly Naming Conventions v0.1-θ

**For:** a tokenized universe inside the pedagogical substrate  
**Parent:** `CHAOS_ORDER_VERTICAL_SCALING_v0.1-theta`, `PONY_EXPRESS_v0.1`, `CIVIC_WAR_BOARD_GAME_v0.1`  
**Materiality control:** `MATERIALITY_RULE_v1.0`  
**Classification:** Naming taxonomy & token grammar (simulation only)  
**Authority:** false  
**Gate 1:** BLOCKED  
**Core docket:** EMPTY  
**Vessel status:** EMPTY_VESSEL  
**Simulation only:** true  
**Promotion:** blocked

## 1. Purpose

Provide a consistent, scholarly-flavored naming system for objects in a **tokenized universe** used for teaching, cold cases, reenactments, and RePlay. All nuclear / atomic vocabulary is **metaphor only**. Nothing here describes, enables, or relates to real nuclear materials, weapons, or energy systems.

```text
NAMING                    = ORGANIZED_CHAOS
TOKEN                     = ADDRESSABLE_SIMULATION_OBJECT
METAPHOR                  ≠ PHYSICAL_CLAIM
FUSION / FISSION / ATOMIC ≠ REAL_NUCLEAR_PROCESS
```

## 2. Core Token Classes

| Class | Symbol (optional) | Meaning in simulation |
|-------|-------------------|------------------------|
| **Atomic idea** | `⚛` / `ATM-` | Smallest coherent claim or concept unit; not further split without a Fission Statement |
| **Fission statement** | `✂` / `FIS-` | Explicit split of one Atomic idea into named daughter claims; preserves lineage |
| **Fusion entry** | `⊕` / `FUS-` | Join of two or more Atomic ideas (or prior fusions) into a compound claim; must list parents |
| **Nuclear fuel** | `⛽` / `NFL-` | Bounded energy/attention budget for a session, gate, or magnitude band — **game resource only** |
| **Isotope variant** | `ISO-` | Same Atomic core, different pedagogical framing or difficulty |
| **Half-life note** | `HL-` | Optional decay/relevance timer for entertainment or teaching packs (not legal expiry) |
| **Containment vessel** | `CV-` | Packet or schema instance that holds tokens without admitting them as mass-bearing sources |
| **Chain reaction log** | `CRX-` | Receipt sequence showing successive Fission/Fusion steps |

## 3. Identifier Grammar

```text
TOKEN://<CLASS>/<ERA_OR_SCOPE>/<SHORT_SLUG>@<VERSION>
```

Examples (informative):

```text
TOKEN://ATM/SANDBOX/byte-equality-only@v1
TOKEN://FIS/SANDBOX/split-claim-vs-evidence@v1
TOKEN://FUS/SANDBOX/integrity-plus-custody@v1
TOKEN://NFL/REPLAY/session-attention-budget@v1
TOKEN://CV/GSR/empty-vessel@v0.1
```

Rules:

- `CLASS` ∈ { `ATM`, `FIS`, `FUS`, `NFL`, `ISO`, `HL`, `CV`, `CRX`, … }
- `ERA_OR_SCOPE` may use Civic War era labels or `SANDBOX` / `REPLAY` / `TEACH`
- `SHORT_SLUG` is lowercase kebab-case
- `@VERSION` is required for any token cited in a receipt

## 4. Relationship Rules

1. **Fission** of an Atomic idea MUST emit a Fission Statement listing parent id and daughter ids.
2. **Fusion** MUST list all parent token ids; fusion does not erase parents (forks may remain).
3. **Nuclear fuel** is spent only inside session rules; it never buys Gate 1 or mass.
4. Tokens may sit inside a **Containment vessel** (`GOVERNOR_SOURCE_RECORD` EMPTY_VESSEL or session packet) without becoming primary sources.
5. Every material Fission/Fusion MUST append a receipt under `RECEIPT_CHAIN_PROTOCOL_v0.1-theta` (RFC 8785 JCS).
6. Materiality defaults to `MUST`; a `MAY` classification must be explicit and receipted.
7. Fusion and Fission inherit materiality under `STRICTEST_PARENT_WINS`; any `MUST` or unknown parent makes the child `MUST`.

## 5. Materiality Binding

```text
DEFAULT_MATERIALITY = MUST
INHERITANCE_RULE    = STRICTEST_PARENT_WINS
UNRECEIPTED_EDIT    = MATERIAL
```

Token creation, deletion, renaming, lineage edits, scoring changes, stage changes, custody changes, and replay-state changes are material. Decorative classification is permitted only through the explicit `MAY` path defined by `MATERIALITY_RULE_v1.0`.

```text
MATERIALITY ≠ EPISTEMIC_MASS
MATERIALITY ≠ ADMISSION
MATERIALITY ≠ AUTHORITY
```

## 6. Mapping to Existing Layers

| Token idea | Maps toward |
|------------|-------------|
| Atomic idea | Claim / Z-layer assertion |
| Fission statement | Fork / gap disclosure |
| Fusion entry | Evidence chain composition |
| Nuclear fuel | Movement points, review budget, dual-axis effort |
| Containment vessel | EMPTY_VESSEL / packet / schema instance |
| Chain reaction log | Receipt chain |
| Magnitude (M0–M5) | How many tokens interact in one reading |

## 7. Organized Chaos Principle

```text
CHAOS   = unrestricted split/join without lineage
ORDER   = every split/join named, linked, receipted
ORGANIZED_CHAOS = Chaos allowed only inside Order’s naming and custody rules
```

Vertical scaling magnitude (`CHAOS_ORDER_VERTICAL_SCALING_v0.1-theta`) may report how organized a token graph is; it does not rank real institutions.

## 8. Hard Boundaries

```text
NO_REAL_NUCLEAR_OR_WEAPON_CONTENT     = ENFORCED
NO_TOKEN_OPENS_GATE_1                 = ENFORCED
NO_TOKEN_ASSIGNS_MASS                 = ENFORCED
NO_TOKEN_CREATES_PUBLIC_OFFICE        = ENFORCED
NO_METAPHOR_AS_PHYSICAL_INSTRUCTION   = ENFORCED
SEPARATION_OF_DUTIES                  = FROZEN
```

## 9. Media & RePlay

- Learning videos may animate Fission/Fusion as graph edits
- Teaching props: cards labeled ATM / FIS / FUS / NFL
- 80s RePlay: optional “reactor” aesthetic for session energy bars (fuel = attention only)
- JSON movie streams may include `token_events[]` frames

## 10. Current State

```text
ARTIFACT              = ORGANIZED_CHAOS_NAMING_v0.1-theta
UNIVERSE              = TOKENIZED_SIMULATION
TAXONOMY              = FUSION | FISSION | ATOMIC | NUCLEAR_FUEL | …
DEFAULT_MATERIALITY   = MUST
INHERITANCE_RULE      = STRICTEST_PARENT_WINS
GATE_1                = BLOCKED
VESSEL_STATUS         = EMPTY_VESSEL
AUTHORITY             = FALSE
CORE_DOCKET           = EMPTY
PROMOTION             = BLOCKED
```

## 11. Promotion Boundary

Scholarly nicknames for sandbox tokens are not a theory of matter and not a source-admission path. Real-source work still requires Entrenched Admissions, epistemic_class declaration, and Gate 1 after explicit operator action.

🧐
