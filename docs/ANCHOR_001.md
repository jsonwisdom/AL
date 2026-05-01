> **STATUS: SUPERSEDED**
>
> This document describes a legacy Anchor #1 state from the older AL VCLP flow.
> It is preserved for historical continuity only.
>
> Current canonical Anchor 001 state is recorded in `docs/ANCHOR_001_FINAL_STATE.md`.
>
> Current status: `DOUBLE-ANCHORED — VERIFICATION SURFACE COMPLETE`
> Current GitHub commit: `13004719dd0c34f765ca95dfe8566b6feb2bf6cf`
> Current EAS UID: `0x18b5b00c62c648df2ccf4a746645493fa2a0b0dcda6697052d8c3a3d1586c142`
> Current ENS status: `DEFERRED` — Basename text records were not editable for `jaywisdom.base.eth`.
>
> Rule: no ghost anchor. ENS is a convenience layer, not the trust layer.

# AL Anchor #1 — Minnesota Budget Core Claims

## Anchor Identity

| Field | Value |
|-------|-------|
| **ENS Domain** | `jaywisdom.eth` |
| **ENS Text Key** | `al.verified_claims` |
| **Root Hash** | `sha256:2296352053488d28c6517523e0392080d3cef10724db0e2142779572c6179d7a` |
| **Manifest Commit** | `d4de1ec` |
| **Manifest URL** | `https://raw.githubusercontent.com/jsonwisdom/AL/master/docs/verified-claims.json` |
| **Status** | **VERIFIED** |

## Included Claims (4)

| # | Label | Value |
|---|-------|-------|
| 001 | Health & Human Services | 25,808,265 |
| 002 | Public Safety & Judiciary | 3,640,627 |
| 003 | E-12 Education | 25,869,108 |
| 004 | Higher Education | 4,015,828 |

## Verification Command

```bash
bash scripts/verify_verified_claims_root.sh \
  https://raw.githubusercontent.com/jsonwisdom/AL/master/docs/verified-claims.json
```

Expected result:

```text
VERIFY_ROOT_OK root=sha256:2296352053488d28c6517523e0392080d3cef10724db0e2142779572c6179d7a
```

## ENS Record

```text
name: jaywisdom.eth
key: al.verified_claims
value: root=sha256:2296352053488d28c6517523e0392080d3cef10724db0e2142779572c6179d7a;commit=d4de1ec;manifest=https://raw.githubusercontent.com/jsonwisdom/AL/master/docs/verified-claims.json
```

## Scope Note

Anchor #1 represents the core Minnesota budget rows from the February 2026 Minnesota Management and Budget forecast.

Transportation and Environment rows are intentionally excluded from Anchor #1 and may be included in a future Anchor #2.

---

Document generated: 2026-04-28  
Verification system: AL VCLP
