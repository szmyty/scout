# PursuitEV Specification

**Version:** 1.0.0  
**Status:** Stable decision-aid model  
**Last updated:** 2026-08-21

## Purpose

PursuitEV is a practical prioritization model for choosing which job opportunities deserve limited application energy. It is designed for a sustainable search: favor a viable, stable bridge into meaningful work over prestige, volume, or generic employment.

It is not a scientific predictor, an automated hiring decision, or a guarantee of an offer. Its purpose is to make trade-offs visible, compare opportunities consistently, and identify what needs further research before applying.

## Operating sequence

Use the model in this order:

1. **Verify the posting.** Treat employer sources as authoritative for vacancy status, deadline, location, and eligibility.
2. **Apply hard gates.** If a must-have constraint fails, stop.
3. **Estimate outcome probability and sustainability.**
4. **Score the outcome value using the current weights.**
5. **Estimate pursuit cost.**
6. **Record confidence.** A high score built on weak evidence is a research task, not an automatic priority.
7. **Choose a next action:** pursue, research, watch, or skip.

## 1. Hard gate

\[
Eligible(J) =
\begin{cases}
1 & \text{if all hard constraints pass}\\
0 & \text{otherwise}
\end{cases}
\]

If \(Eligible(J)=0\), do not pursue the role. Its CareerEV and PursuitEV are zero.

Typical hard constraints include:

- Work authorization that cannot realistically be satisfied.
- Compensation that cannot support stability.
- Mandatory heavy on-call or clearly unsustainable hours.
- Extreme travel or otherwise incompatible work design.
- Outside-work or intellectual-property terms that conflict with maintaining independent work.

Hard gates protect attention. They are not a moral judgment of a role or employer.

## 2. Probability layer

\[
P(O \mid J) = P(\text{offer} \mid J)
\]

Estimated probability of receiving an offer after applying. Consider demonstrated experience, domain and technical overlap, seniority, evidence quality, visa friction, interview format, role clarity, and likely competition.

\[
P(S \mid O, J) = P(\text{sustainable} \mid \text{offer}, J)
\]

Estimated probability that the role remains sustainable after an offer. Consider workload, interruptions, meetings, on-call, autonomy, flexibility, manager and team signals, deep-work availability, health compatibility, and organizational stability.

Both probabilities are estimates in \([0,1]\). They should be revised as better evidence appears.

## 3. Outcome value

Each dimension is scored from 0 to 1, where 0 is poor fit and 1 is excellent fit.

\[
V(J)=w_FF(J)+w_SS(J)+w_MM(J)+w_AA(J)+w_GG(J)+w_PP(J)
\]

The weights must sum to 1.

| Symbol | Dimension | What it captures | Current stabilization weight |
| --- | --- | --- | ---: |
| \(F\) | Financial stability | Compensation, benefits, and practical security. | 0.25 |
| \(S\) | Sustainability quality | Health impact, workload, stability, culture, and manageable operating burden. | 0.30 |
| \(M\) | Mission and meaning | Values alignment and meaningful technical impact. | 0.10 |
| \(A\) | Autonomy | Independence, ownership, and decision latitude. | 0.10 |
| \(G\) | Growth | Learning, durable skill growth, and future optionality. | 0.05 |
| \(P\) | Personal-life compatibility | Location, lifestyle, flexibility, and room for independent work. | 0.20 |

Therefore, during the current stabilization phase:

\[
V(J)=0.25F+0.30S+0.10M+0.10A+0.05G+0.20P
\]

Because each dimension is normalized and the weights sum to 1, \(V(J)\in[0,1]\).

## 4. CareerEV

\[
CareerEV(J)=Eligible(J)\times P(O\mid J)\times P(S\mid O,J)\times V(J)
\]

CareerEV ranks the expected value of accepting a role if the application process were free.

## 5. Pursuit cost

\[
C_{pursuit}(J)=C_{time}+C_{cognitive}+C_{stress}+C_{opportunity}
\]

Use a practical 1–5 scale:

| Cost | Interpretation |
| ---: | --- |
| 1 | Cheap, clear, low-friction application. |
| 2 | Straightforward tailoring and portal work. |
| 3 | Moderate effort or ambiguity. |
| 4 | High cognitive, emotional, or logistical load. |
| 5 | Expensive multistage process, heavy uncertainty, or major opportunity cost. |

Cost is about the effort required to pursue the role, not the worth of the work itself.

## 6. PursuitEV

\[
\boxed{
PursuitEV(J)=
\frac{
Eligible(J)\times P(O\mid J)\times P(S\mid O,J)\times V(J)
}{
C_{pursuit}(J)
}
}
\]

Higher PursuitEV means higher expected return per unit of search energy. Use it to rank a manageable queue, not to maximize application count.

## Confidence and evidence

Record confidence independently for the major estimates:

- **High:** directly established by the posting, official policy, or reliable firsthand evidence.
- **Medium:** supported by multiple credible signals.
- **Low:** inferred from incomplete or ambiguous information.

A high PursuitEV with low confidence should become a verification task. A lower score with high confidence may still be the more actionable choice.

## Worked illustrative example

For a hypothetical research-software role:

- \(Eligible=1\)
- \(P(O\mid J)=0.45\)
- \(P(S\mid O,J)=0.85\)
- \(V=0.82\)
- \(C_{pursuit}=2\)

\[
PursuitEV=\frac{1\times0.45\times0.85\times0.82}{2}\approx0.157
\]

The result is useful only relative to other roles scored with the same assumptions and current weights.

## Change policy

This model is intentionally versioned because priorities can change.

- Keep the hard-gate-first sequence.
- Version every semantic formula, dimension, scale, or weight change.
- State why the revision occurred and its effective date.
- Do not retroactively imply that old decisions used a later version.
- Treat personal weighting and qualitative evidence as private decision context; Scout publishes only public-safe queue information.
