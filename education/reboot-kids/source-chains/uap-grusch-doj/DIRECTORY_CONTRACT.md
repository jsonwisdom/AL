# uap-grusch-doj — Directory Contract

Purpose: narrow provenance-routing lane for public-source UAP claims associated with David Grusch, including the limited DOJ/FBI/FOIA edge, without promoting the alleged Cheney/detainment event as fact.

## Semantic class

`SOURCE_CHAIN_ROUTING`

## Intended routing labels

`PRIMARY_NEW_CLAIM = GRUSCH / DR. PHIL`
`PRESS_RELAY = NY POST`
`SWORN_RECORD = HOUSE OVERSIGHT`
`WHISTLEBLOWER_GATE = ICIG`
`UAP_PROGRAM_GATE = AARO / DOD`
`ARCHIVAL_GATE = NARA RG-615`
`DOJ_COMPONENT_EDGE = FBI`
`DOJ_LEGAL_RECORD_EDGE = OIP / FOIA`
`DOJ_VALIDATION = NOT_FOUND`
`CHENEY_EVENT_PROOF = NOT_BOUND`

## Verified public-record anchors — 2026-08-17

- House Oversight repository: July 26, 2023 UAP hearing; David Grusch listed as former National Reconnaissance Officer Representative to the UAP Task Force, Department of Defense.
- Grusch submitted statement: states a PPD-19 Urgent Concern filing with the Intelligence Community Inspector General (ICIG) and reporting to multiple Inspectors General.
- NARA Record Group 615: lists UAP transfers including ODNI, OSD, NSA, State, FAA, NRC, and FBI; FBI National Archives Identifier 580705010.
- FBI Vault: maintains historical UFO records as a FOIA/public-record collection; record existence does not validate a separate modern allegation.
- AARO FY2025 Consolidated Annual Report, information cutoff May 30, 2025: states that no evidence suggests a USG or private entity has ever captured or exploited UAP-derived materials. This is preserved as an official conflict-state record, not treated as proof of universal nonexistence.
- DOJ Office of Information Policy: Slaughter v. Department of the Air Force, No. 24-862, 2026 WL 571249 (D.D.C. Mar. 2, 2026), documents litigation over Air Force UAP/UFO records and deficiencies in parts of the agency's FOIA search explanation. It provides a legal-record/FOIA edge only.

## First-party Dr. Phil surface — 2026-08-17

The official Dr. Phil Podcast website currently lists a 55:39 video titled **David Grusch: The Whistleblower Who Told Congress We're Not Alone**.

`FIRST_PARTY_DRPHIL_SURFACE = FOUND`
`FIRST_PARTY_DRPHIL_VIDEO_TITLE_BOUND = TRUE`
`FIRST_PARTY_DRPHIL_DURATION_BOUND = TRUE`
`PRIMARY_MEDIA_DIRECT_CAPTURE = PENDING`
`DIRECT_PROVIDER_TRANSCRIPT_CAPTURE = PENDING`

The first-party surface establishes that the interview/video exists on the official host site. It does not validate Grusch's underlying allegations, and no provider media bytes or transcript have been captured into this repository by this contract.

## Fail-closed membranes

`RECORD_EXISTS != CLAIM_TRUE`
`FBI_RECORDS_EDGE != DOJ_VALIDATION`
`FOIA_LITIGATION != EVENT_PROOF`
`HOUSE_TESTIMONY != UNDERLYING_EVENT_VERIFIED`
`ICIG_ROUTE != CLAIM_VALIDATED`
`AARO_ASSESSMENT != UNIVERSAL_NEGATIVE_PROOF`
`PRESS_RELAY != PRIMARY_EVENT_EVIDENCE`
`CHENEY_IDENTIFICATION != CHENEY_EVENT_PROOF`
`FIRST_PARTY_SURFACE != UNDERLYING_CLAIM_VERIFIED`
`SOURCE_SURFACE_FOUND != SOURCE_BYTES_CAPTURED`

## Current topology state

`ROUTING_METADATA_ONLY = TRUE`
`LESSON_CONTENT_CREATED = FALSE`
`SOURCE_BYTES_CAPTURED = FALSE`
`CLAIM_PROMOTION = FALSE`
`AUTHORITY_CREATED = FALSE`
`PRODUCTION_GREEN = FALSE`
`NO_FAKE_GREEN = TRUE`
