# CLASS LITERATURE V0.1  
## Product-Class Literature: Mathematical Formula Specific to Air University and USAF Reported Numbers

**Node:** `AL/MAXWELL/AU/CLASS/MATH/Gambit`  
**Status:** provisional product literature  
**creates_truth:** false  
**Discipline:** replay — receipts over narrative; observe ≠ assume

---

### 1. Framing (Maxwell's Demon / information accounting)

Maxwell's Demon sorts molecules by measuring a single bit of state. Landauer's principle and the Szilard engine give the thermodynamic cost of that bit:

\[
E_{\text{bit}} \ge k_B T \ln 2
\]

where \(k_B\) is Boltzmann's constant and \(T\) is temperature. In the educational domain we treat a completed learning event (degree, PME graduation, leader-development course) as an information event that reduces uncertainty about the readiness state of the Total Force. The literature does **not** claim that AU or USAF measures energy this way; it only offers a formal scaffold that can be replayed against public counts.

---

### 2. Observed public counts (provisional)

Primary source: Air University Fact Sheet, September 2024 (AU Office of Academic Affairs).

| Category | In-Resident (IR) | Distance Learning (DL) | Total |
|---|---:|---:|---:|
| Officer PME | 4,140 | 5,412 | 9,552 |
| Enlisted PME | 4,040 | 7,502 | 11,542 |
| Leader Development | 4,884 | 21,795 | 26,679 |
| Professional Continuing Education | 12,642 | 12,376 | 25,018 |
| **Completions sum** | **25,706** | **47,085** | **72,791** |

Academic degrees conferred (same sheet):

| Level | Count |
|---|---:|
| Associates (CCAF 10,060 + Eaker 56) | 10,116 |
| Master's | 1,484 |
| Doctoral | 49 |
| **Total degrees** | **11,649** |

Cross-check (AETC Snapshot as of 19 Sep 2025, FY24 production):

- Academic Degrees Awarded: 11,480  
- Professional Military Education: 24,177 (Resident 9,012 / Non-Resident 15,165)

Numbers differ by reporting window and inclusion rules. All figures are treated as provisional observations, not canonical totals.

CCAF context (public): ~270k registered students; historically largest multi-campus community college system serving the enlisted force.

---

### 3. Product formulae (interpretive)

Define:

- \(N_{\text{comp}}\) = reported completions (IR + DL) in a reporting window  
- \(N_{\text{deg}}\) = reported degrees conferred  
- \(N_{\text{PME}}\) = reported PME completions  
- \(b\) = bits of uncertainty resolved per event (model parameter; default 1 for a binary ready/not-ready distinction)

**Information events**

\[
I_{\text{window}} = b \cdot N_{\text{comp}}
\]

**Landauer lower bound (theoretical energy cost of erasure / measurement)**

\[
E_{\text{min}} \ge N_{\text{comp}} \cdot k_B T \ln 2
\]

At room temperature (\(T = 300\,\text{K}\)):

\[
k_B T \ln 2 \approx 2.87 \times 10^{-21}\,\text{J/bit}
\]

so for the AU Fact Sheet completion total:

\[
E_{\text{min}}(72{,}791) \gtrsim 2.09 \times 10^{-16}\,\text{J}
\]

(orders of magnitude below any real institutional energy budget; the formula is a lower-bound identity, not an operational claim).

**Degree share**

\[
r_{\text{deg}} = \frac{N_{\text{deg}}}{N_{\text{comp}}} \approx \frac{11{,}649}{72{,}791} \approx 0.160
\]

**PME fraction of completions**

\[
r_{\text{PME}} = \frac{N_{\text{PME}}}{N_{\text{comp}}}
\]

(using AETC PME 24,177 against AU completions yields a different ratio; both are provisional).

**IR / DL split**

\[
r_{\text{IR}} = \frac{N_{\text{IR}}}{N_{\text{comp}}} \approx \frac{25{,}706}{72{,}791} \approx 0.353
\]

**CCAF dominance of associates**

\[
r_{\text{CCAF}} = \frac{10{,}060}{10{,}116} \approx 0.994
\]

---

### 4. Replay instruction

1. Re-fetch the cited public fact sheets.  
2. Recompute the ratios and Landauer bounds from the raw counts.  
3. If numbers diverge, record the divergence as a new receipt; do not overwrite.  
4. Do not promote any formula to institutional authority.

---

### 5. Boundary restatement

This document is product-class literature inside the AL Maxwell educational canon path. It observes public numbers and overlays information-theoretic identities. It does not speak for Air University, AETC, or the Department of the Air Force. `creates_truth: false`.
