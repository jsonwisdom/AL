# MODEL JUDICIAL OPINION

## Memorandum and Order Granting Summary Judgment in Automated Benefits Denial Case

**Draft model opinion. This is not an actual court order. It is a judicial-style template applying existing procedural due process doctrine to machine-mediated benefits adjudication.**

---

# UNITED STATES DISTRICT COURT
# DISTRICT OF COLUMBIA

## JANE DOE,
Plaintiff,

v.

## UNITED STATES DEPARTMENT OF HEALTH AND HUMAN SERVICES,
Defendant.

Civil Action No. 26-cv-____

# MEMORANDUM OPINION AND ORDER

Plaintiff Jane Doe challenges the termination of her Medicaid long-term care benefits after an automated eligibility system determined that she no longer qualified. The agency produced the application data and the denial notice, but it did not produce any replayable record of the computational process that transformed the former into the latter. It concedes that no replayable manifest was generated at the time of decision.

The question before the Court is not whether federal agencies may use automated systems. They may. The question is whether the government may use an automated system to make a materially consequential benefits decision while preserving no reviewable record of how the system reached that result. It may not.

For the reasons below, Plaintiff's motion for summary judgment is granted.

## I. Background

Plaintiff is a disabled adult who received Medicaid long-term care benefits. On March 12, 2026, the agency issued a notice stating that her benefits would terminate because an automated eligibility review determined that she no longer met program requirements.

The notice stated a conclusion. It did not identify the model or ruleset used, the policy version applied, the input provenance relied upon, the transformation chain from submitted information to denial, the output integrity record, or any replay path by which Plaintiff, a hearing officer, or this Court could verify the computational basis of the decision.

Plaintiff appealed and requested the administrative record. The record contains her application information, certain database screenshots, and the denial letter. It does not contain the computation that transformed inputs into output. The agency concedes that no replayable manifest or equivalent computational record was generated when the denial issued.

## II. Standard of Review

Procedural due process claims are reviewed de novo. Agency factual findings may be reviewed under the applicable substantial-evidence or administrative-record standards, but the question of what process is constitutionally due is a legal question for the Court.

This is not a case about deference to an agency's policy judgment or technical expertise. It is a case about the minimum procedure required before the government may deprive a person of a protected interest. Constitutional procedure is for courts to determine.

Under the Administrative Procedure Act, agency action must be set aside if it is arbitrary, capricious, an abuse of discretion, contrary to law, or undertaken without observance of procedure required by law. Judicial review also requires an administrative record adequate to show the basis for the agency's action.

## III. Analysis

### A. The Administrative Record of a Machine-Mediated Decision Includes the Computational Process.

The agency argues that the administrative record consists of the materials it compiled: Plaintiff's data, database screenshots, and the denial letter. That position is insufficient where the operative decision was made or materially shaped by an automated system.

When a human adjudicator acts, the record must reveal enough of the materials and reasoning to permit meaningful review. When a machine performs the operative analysis, the computational process is part of the decisional path. The output letter is not the record of the decision. It is the summary of the result.

Under Citizens to Preserve Overton Park v. Volpe, courts review agency action on the whole record. The whole record of a machine-mediated decision must include enough information to determine what rule or model version was applied, what policy version governed, what information or input categories mattered, how the transformation from inputs to output occurred, and whether the result can be tested against the agency's own stated process.

The agency need not disclose source code in every case. Nor must it publish sensitive fraud thresholds to the world. But it must preserve and produce a reviewable computational record sufficient for meaningful administrative and judicial review. Here it did not.

Judicial review of an incomplete record is not deference. It is review of nothing material to the disputed decision. The agency's failure to preserve the computational basis of the denial renders the record incomplete.

### B. Mathews Requires More Process Where Automated Error Can Replicate at Scale.

The Court applies the familiar Mathews v. Eldridge balancing test: the private interest affected; the risk of erroneous deprivation and probable value of additional safeguards; and the government's interest, including administrative burdens.

The first factor favors Plaintiff. Termination of medical and long-term care benefits affects property interests and practical access to basic care. The injury is concrete, immediate, and serious.

The second factor strongly favors Plaintiff. The risk of erroneous deprivation is structural, not marginal. A single defect in model versioning, policy mapping, input ingestion, threshold selection, or system drift can replicate across thousands of cases before any human official notices. Without a replayable record, neither the affected person nor the agency nor the Court can determine whether the system applied the correct policy to the correct facts.

The value of the requested safeguard is substantial. A replayable manifest or equivalent record would identify the decision system, policy version, input provenance, transformation chain, output integrity record, and path for independent review. Such a record does not decide whether the agency's policy is lawful. It establishes what the system did so that ordinary review can proceed.

The third factor does not justify the agency's position. The government has a legitimate interest in efficient administration. But efficiency gained by eliminating verifiability is not a countervailing constitutional interest. It is the mechanism of the due process violation. The agency chose machine-speed adjudication. Having done so, it must preserve a record adequate to review machine-speed action.

The Court does not hold that agencies must implement any particular technology. It holds only that when a materially consequential automated decision affects protected interests, the record must be sufficient to verify the decision's computational basis. That is the minimum condition for meaningful notice and review.

### C. Goldberg Confirms That Review Must Be Meaningful Before Serious Benefits Harm Becomes Irreparable.

Goldberg v. Kelly teaches that termination of subsistence benefits requires procedures adequate to protect against erroneous deprivation. A hearing is meaningful only if the recipient can understand and contest the basis for the action.

Plaintiff could not do so here. She received a conclusion, not an explanation tied to the actual decisional process. She could challenge the result, but not the process that produced it. She could submit evidence, but she could not know what information the system considered decisive or whether the correct policy version was applied.

Due process does not require perfect transparency. But it does require a meaningful opportunity to be heard. That opportunity is hollow when the operative basis of the denial is unavailable.

### D. The Court Adopts a Two-Track Review Structure as the Logical Form of Meaningful Review.

The parties' briefing distinguishes between two forms of challenge. The Court adopts that distinction as a remedial structure, not as a new constitutional test.

The first track is execution fidelity. It asks whether the automated system did what the record says it did. That inquiry requires a replayable manifest or equivalent computational record.

The second track is substantive legitimacy. It asks whether the system was permitted to do what it did. That inquiry includes the lawfulness of the governing rule, policy threshold, feature selection, drift tolerance, explanation, and human-review pathway.

The tracks are distinct because a system may execute perfectly and still apply an unlawful rule. Conversely, a lawful rule cannot be meaningfully reviewed if the agency cannot show how the system applied it.

Plaintiff need not know which track applies when she challenges a denial. A person whose benefits are terminated may say, in ordinary language, that the computer said no and she believes that is wrong. The institution must route the challenge correctly and preserve both forms of review.

### E. Delay That Functions as Denial Is a Due Process Problem.

The agency argues that Plaintiff may appeal through ordinary channels. But review delayed beyond the point of meaningful relief may function as denial. Where a routing or triage system determines whether a person receives review in days or years, queue design itself may become materially consequential.

The Court does not hold that every delay is unconstitutional. It holds that where delay effectively deprives an affected person of meaningful review before serious benefits harm occurs, the delay must be treated as part of the process due. A backlog cannot substitute for a hearing.

## IV. Holding

The Court holds as follows:

1. A materially consequential decision produced by an automated or semi-automated system without a replayable manifest or equivalent computational record creates a rebuttable presumption of procedural inadequacy.

2. The administrative record of a machine-mediated decision includes the computational basis of the decision, not merely the inputs and output.

3. When the agency cannot produce a reviewable computational record, the agency bears the burden of proving that the process was lawful and correctly applied, rather than requiring the citizen to prove an error hidden inside an uninspectable system.

4. Delay that functions as denial triggers the same due process concerns as a formal denial.

5. These holdings do not create new rights. They apply the existing procedural guarantees of the Fifth Amendment to machine-speed state action.

## V. Remedy

The appropriate remedy is remand.

On remand, the agency shall, within 90 days, either:

1. produce a replayable manifest or equivalent computational record sufficient to permit Plaintiff to challenge execution fidelity and substantive legitimacy; or

2. provide de novo human review of Plaintiff's eligibility without relying on the challenged automated denial as presumptively valid.

If the agency produces a computational record, Plaintiff must be given a meaningful opportunity to challenge both whether the system executed as recorded and whether the governing rule, threshold, or policy logic was lawful as applied.

If the agency cannot produce such a record, the denial may not be treated as carrying a presumption of regularity. The agency must make a new determination through human review on a record sufficient for administrative and judicial review.

The Court retains jurisdiction to ensure compliance with this order.

## VI. Conclusion

The Constitution does not require perfection. It requires due process. When the state acts at machine speed, due process requires that the affected person may trigger verification of the state's action at machine speed. No manifest, no authority. No replay, no automated power. No plain-language explanation, no automated authority. A delay that functions as a denial is a decision.

These are not new principles. They are what notice, hearing, and meaningful review have always required.

Plaintiff's motion for summary judgment is GRANTED. The matter is REMANDED to the agency for proceedings consistent with this opinion. The Court retains jurisdiction.

SO ORDERED.

Date: _____________

__________________________________
United States District Judge
