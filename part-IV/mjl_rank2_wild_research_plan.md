# Research plan — wild-place metaplectic character transfer in degree two

**Project:** `part-IV/mjl_rank2_wild_draft0.tex` (standalone companion paper)
**Date:** November 8, 2026
**Sources:** Parts I Draft 8, II Draft 8, III Draft 9, Part IV Draft 5; corrected [JC] revised12; Flicker–Kazhdan (1986) read with Zou's December 2024 corrections; Claude's Part IV Draft 5 report; the separate quadratic toral-positivity proof note.

## Proposed paper structure

1. State the wild quaternionic problem precisely and separate the imported unitarity theorem from the unproved integrality conjecture.
2. Fix the cocycle and genuine central character, including the relabeling `c=1` in [JC] to `c_v=2` in the Part I convention for `n=3`.
3. Prove the **uniform quadratic toral permutation-character theorem** for every quadratic `E/F` when `p` and `n` are odd and `mu_n` lies in `F` (wild cases included).
4. Give fully worked `F=Q_3(zeta_3)`, `n=3` calculations for the unramified and both ramified quadratic maximal tori. Explain the covered torus degree-three constituents and the two degree-27 branching tables.
5. State and prove the all-row **integrality ⇔ positivity** lemma for the unitary transfer matrix. Explicitly note that a *single* positive-definite row need not be integral.
6. Develop a separate nonabelian gluing program with exact proof checkpoints; do **not** promote torus-level positivity to a full-group theorem without additional evidence.

## Milestones

| Stage | Technical deliverable | Acceptance criterion |
|---|---|---|
| 1. Local multiplier | Explicit cocycle on `D×`, derived from [JC] and checked against Part I commutators; compatible genuine central character | Direct checks on all quadratic torus types, not merely an abstract extension isomorphism |
| 2. Finite-level model | Identify a congruence level at which `L_D 1` genuinely factors as a twisted finite-group class function | Prove factorization and preservation of the faithful central `mu_3` action |
| 3. Exact integrality test | Exact character table or coefficient integrals in cyclotomic arithmetic | Exhibit integer coefficients for a *capturing* quotient, or a verifiable noninteger counterexample |
| 4. Representation construction | Candidate 27-dimensional genuine module from Heisenberg/Clifford/compact induction | Prove irreducibility and match the full character, not just restrictions to maximal tori |
| 5. All irreducibles | Generalize from the trivial ordinary character to arbitrary `rho` | Establish a uniform argument yielding all-row positivity or all-row integrality |
| 6. Uniform rank two | Extend from `Q_3(zeta_3)` to arbitrary allowed `F,n` | State sharp hypotheses, address congruence-depth changes, verify every character family |

## Mathematical tests that prevent premature claims

- **Toral positivity is necessary, not sufficient:** the scalar class function on `C_2 x C_2` with value 2 at the identity and 0 elsewhere restricts to a character on every cyclic subgroup but is half the sum of the group's four characters.
- **A single positive row is not sufficient:** an orthonormal row can have positive nonintegral coefficients. Positivity of **every** row forces permutation by orthogonality; for one row use a virtual-character proof or exact integer coefficient calculation.
- **Finite quotients require justification:** a computed quotient must faithfully encode the genuine central character and the selected transferred class function. An arbitrary cutoff is only exploratory evidence.
- **At a wild prime, `n` is not a unit:** any Kirillov/orbit-method rescaling must account for the failure of multiplication by `n` to be a lattice automorphism.
- **No inference to global transfer:** the companion paper addresses local character integrality. The Part IV conditional global comparison still needs exceptional split-place matching, archimedean and Haar conventions, and geometric/spectral justification.

## Proposed draft sequence

- **Draft 0 (current):** theorem, complete cubic torus example, positivity lemma, and precise research program.
- **Draft 1:** rigorous cocycle finite-level model plus character/Gram calculations; update the statement of the conjecture if a counterexample appears.
- **Draft 2:** induced-representation or Clifford-theoretic proof for the first row, or a documented obstruction.
- **Draft 3+:** all-character or general-field theorem only if independently proved.

**Publication boundary:** Part IV Draft 6 can conclude with its conditional global statement and the proved general quadratic toral theorem. The detailed rank-two computations, experiments, and unproved gluing conjecture belong in this independent paper under `part-IV/`.
