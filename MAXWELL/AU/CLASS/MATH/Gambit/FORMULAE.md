# FORMULAE — pure mathematical identities used in Gambit literature

**Status:** theoretical identities only. No claim of institutional measurement.

## Landauer / Szilard bit cost

\[
E_{\text{bit}} \ge k_B T \ln 2
\]

\[
k_B = 1.380649 \times 10^{-23}\,\text{J/K}
\]

At \(T = 300\,\text{K}\):

\[
k_B T \ln 2 \approx 2.870 \times 10^{-21}\,\text{J}
\]

## Aggregate information events

\[
I = b \cdot N
\]

where \(N\) is a reported count of completions or degrees and \(b\) is bits resolved per event (model parameter).

## Minimum theoretical energy for a count

\[
E_{\text{min}}(N) \ge N \cdot k_B T \ln 2
\]

## Ratio identities

\[
r = \frac{N_{\text{subset}}}{N_{\text{total}}}
\]

Applied in the literature to:

- degree share of completions  
- IR share of completions  
- CCAF share of associates  
- PME share of completions (when consistent reporting windows are available)

## Entropy of a binary readiness partition (Shannon)

For a force of size \(M\) with ready fraction \(p\):

\[
H = -p \log_2 p - (1-p)\log_2(1-p) \quad \text{(bits per member)}
\]

Total uncertainty before measurement:

\[
H_{\text{total}} = M \cdot H
\]

A completion that resolves one member's readiness state reduces the ensemble uncertainty by up to 1 bit (when the prior was maximally uncertain). This is a formal upper bound on information gain, not an empirical measurement of institutional learning.
