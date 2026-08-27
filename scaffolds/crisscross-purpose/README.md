# AL CrissCross Purpose Scaffold v0.1

Status: DRAFT  
Source purpose head: `jsonwisdom/COMPUTERWISDOM#527`  
Authority created: false

## Locality

Jason declares Alabama as a locality connected to family, civic responsibility, and taxes.

This scaffold records the declaration without publishing an address, county, tax record, family location, or residency proof. Those details remain private unless Jason separately approves a bounded public record.

```json
{
  "locality": "Alabama",
  "declared_by": "Jason Wisdom",
  "tax_connection": "OPERATOR_DECLARED_UNVERIFIED",
  "family_connection": "OPERATOR_DECLARED_PRIVATE_BOUNDARY",
  "address_public": false,
  "authority_created": false
}
```

## Existing lineage

This scaffold appends to:

- `LIFE_WORK_CONTINUITY_LEDGER.md`
- `PAY_JAYWISDOM_BASE_ETH.md`
- `GOVERNANCE_BOUNDARY.md`
- `jurisdiction/`
- `projects/`
- `receipts/`

The existing continuity ledger already requires agents to search Jason's lineage before adding, renaming, summarizing, or changing a build surface.

## AL purpose

AL is the locality-facing lane for:

- Alabama public-record and civic work;
- life-work continuity;
- family-safe local projects;
- evidence and receipts;
- jurisdiction-aware research;
- paths that help people understand documents and systems without pretending to provide legal authority.

## Placement contract

```text
purpose/
  locality/
  family-boundaries/
  civic-work/
projects/
  <project-id>/
    purpose/
    people/
    evidence/
    receipts/
    public/
    private-index/
    gaps/
```

No new project file should enter the root before its project directory and purpose manifest exist.

## CrissCross link

```text
COMPUTERWISDOM
  purpose and cross-project doctrine
        ↕
AL
  Alabama locality, continuity, jurisdiction, and civic evidence
        ↕
JOY
  family-facing choice, culture, welcome, and personal boundaries
```

Cross-repo links are references, not authority transfer.

## Identity anchor

`jaywisdom.base.eth` is recorded as Jason's declared identity/payment anchor because existing AL and JOY documents use it.

It does not prove:

- current control;
- wallet custody;
- ENS resolution;
- payment completion;
- family consent;
- authority over another person.

Live claims require separate technical readback.

## Personal boundary precedence

```text
PERSONAL SAFETY
> PERSONAL BOUNDARY
> CONSENT
> FAMILY PURPOSE
> LOCALITY PURPOSE
> PROJECT
> AUTOMATION
> PLACEMENT
> FILE
```

## Invariants

```json
{
  "locality_declared": "Alabama",
  "private_location_published": false,
  "family_details_inferred": false,
  "lineage_preserved": true,
  "directories_first": true,
  "cross_repo_authority_transfer": false,
  "identity_anchor_control_verified": false,
  "authority_created": false
}
```
