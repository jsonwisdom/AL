# Due Process at Machine Speed

## The Constitutional Requirement for Replayable Administrative Records

### Abstract

The administrative state increasingly uses automated systems to determine or materially influence benefits, eligibility, enforcement, immigration, housing, healthcare, and other protected interests. Existing procedural due process doctrine assumes that the basis of a government decision can be reconstructed from a human decision-maker's file, reasoning, testimony, notes, or explanation. Machine-speed adjudication breaks that assumption when agencies preserve only inputs and outputs while omitting the computational path that transformed one into the other. This Article argues that the Fifth Amendment requires a replayable administrative record when government delegates materially consequential decisions to automated or semi-automated systems. This is not a new right and not a technology policy preference. It is the application of Mathews v. Eldridge, Goldberg v. Kelly, Citizens to Preserve Overton Park v. Volpe, Motor Vehicle Manufacturers Association v. State Farm, and the Administrative Procedure Act to machine-mediated public power. The core principle is speed parity: when the state acts at machine speed, the affected person must be able to trigger verification at machine speed. A valid record must preserve both execution fidelity and the ability to challenge substantive legitimacy. Replay proves what the system did; it does not prove that what it did was lawful.

## Introduction

A person receives a denial letter. The letter states that an agency system determined she is no longer eligible for benefits. She appeals. The agency produces her application data and the denial notice. It does not produce the model or ruleset version, the policy hash, the transformation chain, the output integrity record, a replay path, or a plain-language explanation tied to the actual computation. The agency insists that the administrative record is complete because it contains what the agency retained.

That position cannot satisfy constitutional procedure. When an agency delegates a decision to a computational process, the computation is part of the decisional record. A denial letter is not the record; it is the summary of a result. If the state cannot show how the result was produced, it has not provided meaningful notice, a meaningful opportunity to be heard, or a record adequate for judicial review.

This Article develops the constitutional requirement for replayable administrative records. The argument is intentionally modest. It does not ask courts to ban automated adjudication, require public source-code disclosure, or mandate a single technical architecture. It asks courts to recognize that existing due process guarantees require the record of the decision to include the machine-mediated path when the machine materially shaped the decision.

The claim is not about AI ethics. It is about constitutional procedure.

## Part I — The Problem Defined

### A. Administrative Law Assumes a Reviewable Decision Path

Procedural due process and administrative law rest on a basic assumption: the government can show the basis for what it did. Notice matters because it tells the person what to contest. A hearing matters because the person can contest the basis. Judicial review matters because the court can examine the record and determine whether the agency acted lawfully.

Automated adjudication threatens that chain. Agencies may retain the submitted data and the output but fail to preserve the computational path between them. The result is an administrative record that contains the before and after while omitting the decision itself.

A human file may be incomplete. But a machine-mediated decision can be structurally unreviewable if no trace of model version, policy version, data transformation, threshold, drift state, or output integrity is preserved. The defect is not merely bad documentation. It is the absence of the decisional path.

### B. Machine-Speed Adjudication Makes Error Structural

Traditional procedural doctrine often imagines error as case-specific: a clerk misreads a form, a hearing officer credits the wrong evidence, a notice omits a reason. Automated systems can make case-specific errors too, but their distinctive risk is structural. A defect in model versioning, policy mapping, data ingestion, threshold selection, or drift can replicate across thousands of people before any human detects it.

That scale changes the Mathews analysis. The risk of erroneous deprivation is not marginal when one invisible defect can become a population-level administrative event. A record that cannot be replayed prevents the individual from contesting the decision and prevents the agency from detecting systemic failure.

### C. The Question Is Not Whether Automation May Be Used

Automation is not constitutionally forbidden. Agencies may use computers, rules engines, statistical models, and AI systems. The constitutional question is what process is due when those systems materially influence protected interests.

The answer begins with a simple proposition: the more the state delegates decisional authority to a machine, the more the record must preserve what the machine did. If the agency chooses machine-speed action, it must preserve machine-resolution review.

## Part II — The Doctrinal Foundation

### A. Mathews v. Eldridge and the Risk of Erroneous Deprivation

Mathews v. Eldridge supplies the familiar balancing test: courts weigh the private interest affected, the risk of erroneous deprivation and probable value of additional safeguards, and the government's interest, including fiscal and administrative burdens.[^1]

In automated adjudication, the private interest may be substantial: benefits, medical care, housing, credit, employment, legal exposure, public eligibility, immigration processing, or other interests protected by statute and constitutional procedure. The risk of erroneous deprivation increases when the decision is opaque, fast, repeatable, and unreviewable. The value of a replayable record is direct: it allows the person, agency, and court to determine what happened.

The government's interest in efficiency remains relevant, but efficiency gained by eliminating verifiability should not receive constitutional weight. It is the mechanism of the violation, not a justification for it. Mathews does not permit the state to reduce process, increase opacity, and then cite the resulting speed as the reason review would be burdensome.

### B. Goldberg v. Kelly and Meaningful Pre-Deprivation Protection

Goldberg v. Kelly recognized that termination of welfare benefits can inflict immediate and severe harm and therefore requires procedures adequate to reduce erroneous deprivation.[^2] The principle is not limited to paper bureaucracy. A hearing is meaningful only if the affected person can understand and contest the basis for the decision.

Where an automated system denies or terminates benefits, a generic denial letter does not provide meaningful notice if it omits the actual decisional path. The recipient cannot contest what she cannot examine. A paper appeal process attached to an unreviewable computation is not adequate process.

### C. Overton Park and the Whole Administrative Record

Citizens to Preserve Overton Park v. Volpe requires courts to conduct review based on the full administrative record and rejects post hoc rationalizations for agency action.[^3] When the operative analysis is computational, the computational process is part of the full record. The agency cannot satisfy Overton Park by producing the input data and output letter while omitting the process that transformed one into the other.

The record of a machine-mediated decision must include enough information to identify the model or ruleset, policy version, input provenance, transformation chain, output integrity record, and replay path. That does not mean public disclosure of every sensitive detail. It means the record must be reviewable.

### D. State Farm and Reasoned Decisionmaking

Motor Vehicle Manufacturers Association v. State Farm requires agencies to engage in reasoned decisionmaking and to explain the basis of policy choices.[^4] Automated systems do not escape that requirement. If model logic, thresholds, features, or drift policies materially shape decisions, the agency must preserve a governance record sufficient to explain why those choices are lawful and reasonable.

A replayable output does not prove reasoned decisionmaking. It proves execution. State Farm remains necessary because a system may apply an arbitrary threshold perfectly. Execution fidelity and substantive legitimacy are distinct.

### E. The APA and Arbitrary-and-Capricious Review

The APA requires courts to set aside agency action that is arbitrary, capricious, an abuse of discretion, contrary to constitutional right, or undertaken without observance of procedure required by law.[^5] Agency action that cannot be explained or reviewed because the decisional process was not preserved frustrates judicial review. It is not enough for an agency to say that a system produced a result. The agency must provide a record sufficient to assess whether the result was produced lawfully.

## Part III — The Speed-Parity Principle and the Two-Track Framework

### A. The Speed-Parity Principle

The central doctrinal innovation is speed parity:

> When the state acts at machine speed, due process requires that the affected person may trigger verification at machine speed.

Speed parity does not mean every citizen personally reruns federal software. It means that the review path must be capable of verifying the decision at the same operational resolution at which the decision was made. The state cannot use machine speed for deprivation and paper-speed opacity for review.

### B. Replayable Computational Records

A replayable administrative record should preserve, at minimum:

1. model or ruleset identifier;
2. policy or version identifier;
3. timestamp;
4. input provenance classification;
5. transformation chain;
6. output receipt or integrity hash;
7. audit log or equivalent event history;
8. drift or model-change record; and
9. plain-language explanation tied to the actual decision.

These are procedural elements, not a mandated platform. The agency may choose how to implement them. But without them, review is not meaningful.

### C. ALMS as Minimum Viable Architecture

The Audit Ledger Manifest Store, or ALMS, is one implementation model for satisfying execution-fidelity review. ALMS requires a machine-readable manifest, content addressing, audit memory, and verification without operator permission. Its purpose is not to constitutionalize a product. Its purpose is to show that replayability is administratively concrete.

ALMS demonstrates that agencies can preserve machine-speed decisions as reviewable records: decision identifier, system identifier, policy hash, transformation-chain hash, output hash, audit status, and replay surface. A court need not order ALMS by name. It need only require a record that performs the same constitutional function.

### D. The Two-Track Framework

Machine-mediated decisions require two distinct review tracks.

Track One is execution fidelity. It asks: did the system do what the record says it did? This track requires the replayable computational record.

Track Two is substantive legitimacy. It asks: was the system allowed to do that at all? This track examines policy legality, threshold reasonableness, feature governance, disparate impact, drift tolerance, human review, and plain-language explainability.

The tracks must remain separate because a system can execute perfectly and still apply an unlawful rule. Conversely, a lawful rule cannot be reviewed if the agency cannot show how the system applied it.

### E. The Model Governance Challenge

The Model Governance Challenge protocol supplies the Track Two structure. It requires pre-deployment deliberation, a public governance record, plain-language explanation, and a pathway for affected persons to challenge model design even when replay succeeds.

Its core rule is simple: replay proves execution; it does not prove justice. A valid hash does not cure an invalid rule. A replayable denial does not become lawful merely because it replayed perfectly.

### F. Delay as Adjudication

Automated systems often do not merely decide cases; they route objections. If triage determines whether a person receives review in days or years, routing becomes materially consequential. A delay that functions as denial is a decision.

Queue latency and triage routing therefore require their own records, explanations, and public metrics. Otherwise, agencies can preserve formal appeal rights while denying meaningful review by backlog.

## Part IV — Implementation, Objections, and the Path Forward

### A. Burden and Feasibility

Agencies will argue that replayability is expensive. That is true. But constitutional procedure has never been cost-free. The relevant question is whether the safeguard's value justifies its burden under Mathews.

Replayability reduces long-term cost by preventing unreviewable denials, remands, class actions, emergency litigation, and systemic distrust. One reviewable system that survives judicial scrutiny is cheaper than a black box that generates population-scale errors.

The doctrine also need not apply retroactively in a destabilizing way. Existing systems may be migrated through inventory, classification, and cutover dates. Post-cutover materially consequential decisions should carry replayable records. Pre-cutover decisions still under appeal or active enforcement should receive human review or a reconstructed record sufficient for meaningful review.

### B. Security and Privacy

Agencies will argue that replayability creates attack surfaces. The answer is that verifiability does not require unrestricted public disclosure. Courts already handle classified information, trade secrets, medical records, confidential business information, and sealed materials. Protective orders, redactions, in camera review, secure expert access, and controlled disclosure are ordinary judicial tools.

A replayable manifest need not reveal fraud thresholds or source code to the public. It must preserve enough information for the affected person and reviewing authority to test the decision. Security through obscurity is not a constitutional defense. A process that can be defended only by hiding its basis from the person harmed is not secure; it is unaccountable.

### C. Major Questions and Separation of Powers

Agencies will argue that replayability is a legislative policy choice. But procedural due process is not a major question doctrine problem. It is the constitutional floor. Courts need not wait for Congress to reaffirm that notice, hearing, and meaningful review apply when the state changes the mechanism of deprivation.

A court adopting replayability does not need to mandate a national infrastructure. It need only hold that an agency choosing automated adjudication must preserve a record adequate for review. The Constitution sets the floor. Agencies choose the architecture.

### D. The Record That Exists

Agencies will argue that courts review the record that exists, not the record plaintiffs wish existed. But when the missing record is the decisional path itself, the absence is not neutral. The computation is part of the record. If the agency cannot produce it, the record is incomplete.

Courts should treat unreplayable automated decisions as presumptively procedurally defective when they affect protected interests. The presumption should be rebuttable. An agency may show that a different record is sufficient. But it may not rely on a conclusion letter as a substitute for the computation that produced it.

### E. Proposed Judicial Holding

A court can adopt the doctrine without becoming a systems architect:

> When an agency delegates materially consequential decisions to automated or semi-automated systems, due process requires (1) a replayable decisional record establishing what the system did; (2) the ability of the affected person to contest either execution fidelity or substantive legitimacy; and (3) recognition that delay functionally equivalent to denial triggers the same protections as denial itself.

These are not new rights. They are existing Fifth Amendment guarantees applied to machine-speed governance.

## Conclusion

The administrative state may use machines. It may not use machines to make protected-interest decisions beyond meaningful review. A denial that cannot be replayed cannot be tested. A record that omits the computation is incomplete. A hearing without the decisional path is not meaningful. And a queue that delays review until the harm is complete is not review.

The technology may change. The rights do not.

```txt
NO MANIFEST, NO AUTHORITY.
NO REPLAY, NO AUTOMATED POWER.
NO PLAIN-LANGUAGE EXPLANATION, NO AUTOMATED AUTHORITY.
A DELAY THAT FUNCTIONS AS A DENIAL IS A DECISION.
```

## Footnotes

[^1]: Mathews v. Eldridge, 424 U.S. 319, 335 (1976) (establishing the three-factor procedural due process balancing test).

[^2]: Goldberg v. Kelly, 397 U.S. 254 (1970) (holding that termination of welfare benefits required pre-termination procedural protections adequate to reduce erroneous deprivation).

[^3]: Citizens to Preserve Overton Park, Inc. v. Volpe, 401 U.S. 402 (1971) (requiring judicial review based on the full administrative record and rejecting reliance on post hoc rationalizations).

[^4]: Motor Vehicle Mfrs. Ass'n v. State Farm Mut. Auto. Ins. Co., 463 U.S. 29 (1983) (requiring reasoned decisionmaking and adequate explanation under arbitrary-and-capricious review).

[^5]: Administrative Procedure Act, 5 U.S.C. § 706(2)(A), (B), (D) (requiring courts to set aside agency action that is arbitrary, capricious, contrary to constitutional right, or undertaken without observance of required procedure).

[^6]: Cleveland Bd. of Educ. v. Loudermill, 470 U.S. 532 (1985) (recognizing that once a protected property interest exists, the Constitution determines what process is due).

[^7]: Vermont Yankee Nuclear Power Corp. v. Natural Resources Defense Council, Inc., 435 U.S. 519 (1978) (limiting courts' ability to impose additional procedural requirements beyond statute or Constitution, while preserving constitutional requirements).

[^8]: SEC v. Chenery Corp., 318 U.S. 80 (1943) (requiring agency action to be judged on the grounds invoked by the agency).

[^9]: Burlington Truck Lines, Inc. v. United States, 371 U.S. 156 (1962) (requiring agencies to articulate a rational connection between facts found and choices made).

[^10]: Londoner v. Denver, 210 U.S. 373 (1908) (recognizing due process hearing requirements for individualized determinations).

[^11]: Bi-Metallic Inv. Co. v. State Bd. of Equalization, 239 U.S. 441 (1915) (distinguishing broad policy rules from individualized adjudicative decisions).

[^12]: Califano v. Yamasaki, 442 U.S. 682 (1979) (recognizing procedural protections in benefits recoupment context).

[^13]: Heckler v. Campbell, 461 U.S. 458 (1983) (permitting use of medical-vocational guidelines in benefits adjudication while preserving need for individualized consideration where appropriate).

[^14]: Richardson v. Perales, 402 U.S. 389 (1971) (addressing evidentiary standards in Social Security administrative hearings).

[^15]: 5 U.S.C. § 555(e) (requiring prompt notice of denial and a brief statement of grounds for denial in agency proceedings).

[^16]: 5 U.S.C. § 706 (scope of judicial review under the APA).

[^17]: Universal Camera Corp. v. NLRB, 340 U.S. 474 (1951) (describing substantial evidence review on the record as a whole).

[^18]: Camp v. Pitts, 411 U.S. 138 (1973) (per curiam) (review should ordinarily be based on the administrative record already in existence, not new rationalizations).

[^19]: Department of Commerce v. New York, 588 U.S. ___ (2019) (reaffirming that agency explanations must be genuine and reviewable).

[^20]: Kisor v. Wilkie, 588 U.S. ___ (2019) (emphasizing limits on deference and the importance of independent judicial judgment on legal questions).
