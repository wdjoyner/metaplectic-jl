# Part IV — concluding Draft 6 revision log

**Date:** November 8, 2026  
**Base:** `mjl_part4_draft5.tex` (preserved unchanged)  
**Companion:** `mjl_rank2_wild_draft0.tex` (new independent paper)

## Intended scope

This draft closes the present Part IV manuscript as a statement of what is **actually proved**, while clearly separating two goals that remain unresolved: (i) wild-place irreducible-character integrality of `L_D`, and (ii) the unconditional comparison of the ordinary and covered global trace distributions.

## Main revisions

1. **Reframed the title and abstract** around local power maps, toral positivity, and an explicit conditional comparison. Maintained the established title stem and the agreed Part IV author order.
2. **Kept the proved arithmetic reductions:** diagonal cocycle audit; regular good-element classification; local kernel, index, and Haar modulus of the nth-power map on étale tori; the almost-everywhere global Kummer/Hasse criterion.
3. **Inserted the full uniform quadratic toral theorem**, not just the cubic example. For odd residual characteristic and odd covering degree with `mu_n` in the field, the quadratic discriminant ratio is a permutation character of a finite quotient. Included the norm-one filtration proof, the unramified formula and the ramified formula. This is explicitly a theorem about toral class functions.
4. **Added the full-row positivity equivalence:** integrality, nonnegative character coefficients, all-row positive definiteness, and positive irreducible-character permutation are equivalent for the unitary character matrix. Stated that a positive single row alone is insufficient.
5. **Moved the detailed `r=2, n=3` wild computations to `mjl_rank2_wild_draft0.tex`** while retaining a short synopsis and the exact formulas in Part IV. The companion is independently compilable and includes a research plan.
6. **Corrected the conditional global comparison:** removed the extraneous requirement that an ordinary rational class `s` be good (or vanish if nongood). The comparison pairs the ordinary class `[s]` with the automatically good covered star class `[s^n]`. Other matching, measure, support, and convergence hypotheses remain explicit and conditional.
7. Preserved the warning that **regular-orbital matching does not by itself identify central test-function values** because of Shalika-germ issues.
8. Updated references to Parts I Draft 8, II Draft 8, III Draft 9 and to the new companion Draft 0. No other manuscript was overwritten.

## Mathematical limitations retained

- The new toral permutation theorem **does not establish** the existence of any irreducible genuine `D×`-cover representation associated with an ordinary irreducible at a wild place.
- No full coefficient matrix or finite quotient capturing all representations has been computed.
- The conditional global trace comparison does not establish existence of exceptional split or complex-place matching functions or canonical product normalization `Lambda=1`.
- The original FK paper is uncorrected; Part IV continues to rely on Zou for the corrected metaplectic character scalar and distinguishes this from FK's spherical-unit assertions.
- Draft 6 is an internally compiled and checked research manuscript, **not a claim of independent peer review** of its mathematical arguments.

## Build verification

- `pdflatex` compiled the two manuscripts successfully with cross-references resolved after multiple passes.
- `mjl_part4_draft6.pdf`: 20 pages (US letter).
- `mjl_rank2_wild_draft0.pdf`: 11 pages (US letter).
- PDF title and initial pages visually reviewed; no unresolved LaTeX citations/references or overfull-box warnings in final logs.

## Addendum (November 8, 2026): edits integrated by Claude before posting

These edits were made to `mjl_part4_draft6.tex` and `mjl_rank2_wild_draft0.tex` after ChatGPT delivered them. No theorem, section or equation numbers changed.

1. **Citation fix.** The identity-value result of Part III is Corollary 9.4 in Part III Draft 9 (it was 9.3 in an earlier draft). The reference in the identity-class subsection now says Corollary 9.4.
2. **Running example.** Added an unnumbered subsection, "The running example", at the end of §1 of Part IV and of §1 of the companion paper. It points to `notes/mjl_running_example.tex`: `K = Q(zeta_3)`, `n = 3`, `r = 2`, `D = (-1, 4 - zeta_3)_K`, ramified at `p_3 = (1 - zeta_3)` and `p_7 = (3 + zeta_3)`. Example "A possible global numerical ledger" now names this `D` as an instance.
3. **Correction to §6.4.** The `C_2 x C_2` example given for "positive on every covered torus does not imply positive definite" was actually positive definite: its coefficients are 1/2. It showed only that positivity does not force integrality. It is replaced by the function equal to 2 at the identity and -2 at the involutions. That function restricts to twice the sign character on every cyclic subgroup but equals `-chi_0 + chi_1 + chi_2 + chi_3`, so it is not positive definite. The original example is kept, with the conclusion it actually supports.
