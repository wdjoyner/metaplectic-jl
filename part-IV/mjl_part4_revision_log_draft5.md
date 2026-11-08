# Part IV — Draft 5 revision log

Date: November 7, 2026.  Base: `mjl_part4_draft4.tex` (not overwritten).

## Scope and status

This revision adds a worked wild-place example and develops it into a general *necessary* character-restriction test. It does **not** prove wild-place irreducible-character integrality, a local metaplectic Jacquet–Langlands bijection, or the complete global trace comparison. Existing Section 8 conditions remain conditional.

## New and expanded material

1. **Section 6.3 — all quadratic maximal tori in the smallest wild example.** Take `F=Q_3(zeta_3)`, `r=2`, `n=3`, quaternion division `D`, and the scalar-central cover determined by [JC] and Part I. Recheck the cocycle relabeling `c=1 -> c_v=2`; the covered torus commutator, index 9, Stone–von Neumann degree 3, and local transform coefficients `b_D=3`, `c_D=27`.
2. **Toral Fourier lemma.** For a maximal field torus `E×/F×`, expand `R_E(t)=Delta(t)/Delta(t^n)` in finite Fourier characters. Show explicitly how its coefficients become multiplicities in the restriction of the transformed ordinary character to the genuine covered-torus dual. This step uses the full preimage of `F× E×n` as the center and the compatible central-character normalization.
3. **Unramified quadratic subfield.** For `E=F(i)`, `i²=-1`, derive `R(a+bi)=|a²+b²|/|3a²-b²|`, its two valuations `9` and `1`, and the exact Fourier identity `R=1+2 Reg(C4)=3 chi_0+2 chi_1+2 chi_2+2 chi_3`. The three-dimensional genuine covered-torus irreducibles therefore occur with multiplicities `(3,2,2,2)`, giving total dimension 27.
4. **Both ramified quadratic field types.** For `E_d=F(j_d)`, `j_d²=u*(zeta_3-1)` with `u` a unit, derive `R(a+bj_d)=|a²-d b²|/|3a²+d b²|`. Its three valuation strata yield `R(j_d)=1`, `R(1+j_d)=3`, `R(1+varpi j_d)=9`. On a finite `C2 x C3` quotient the exact expansion is `R=1+Reg(C2)+Reg(C2 x C3)`, with covered-torus multiplicities `(3,2,1,1,1,1)` and total dimension 27. The formula works for both ramified quadratic squareclasses.
5. **Proposition on all three field types.** `Q_3(zeta_3)` has three quadratic extension classes, all embedding in the quaternion division algebra. Hence *every* maximal field torus passes the positive integral Fourier test. The multiplicities also obey the natural Galois symmetry. This is not full-group integrality.
6. **Section 6.4 — program for the general case.** Divide the missing theorem into Step T (toral Fourier positivity, potentially via permutation characters of finite unit-filtration quotients) and Step G (nonabelian gluing of genuine torus modules into representations of the full covered division algebra). Add the determinant formula `R_E=|det(sum_{j=0}^{n-1} Ad(t)^j | D/E)|^{-1/2}`, and an exact twisted finite-quotient computation roadmap retaining the genuine central character.
7. **Abstract, mathematical-status table, glossary, and closing research program** updated to reflect the proved torus-level statements and the still-open full-group theorem.
8. **Bibliography** now includes the supplied corrected [JC] manuscript explicitly, alongside previously cited Parts I Draft 8, II Draft 8, III Draft 9, original Flicker–Kazhdan and Zou's corrections.

## Independent checks

- `pdflatex`/`latexmk`: successful; 22 US-letter pages. No undefined references, missing citations, or overfull-box warnings found in the final LaTeX log.
- The PDF pages containing the new computations were rendered and visually inspected.
- Exact finite character multiplicities were separately recalculated by discrete Fourier sums; the small reproducibility script `mjl_part4_toral_fourier_check_draft5.py` outputs the two coefficient tables and dimension checks.

## Important limitations

- Existence of a global genuine irreducible of degree 27, and the integrality of the *full* character matrix `a_{rho,tau}`, are not proved. Even positive integral branching to every maximal covered field torus need not glue to a full-group character.
- The finite twisted character table of a congruence quotient of the specified cover of `D×` has not been computed here. The cocycle calculation, compatible splittings, and actual full-group coefficient computation remain work to do.
- The general Fourier-positivity criterion is sufficient for **torus restrictions**, not a theorem that all `R_E` are positive characters for arbitrary wild fields, ranks and covering degrees.
- The global trace formula comparison remains subject to the hypotheses of Draft 4.
