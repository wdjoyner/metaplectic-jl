# Referee report on Fable-Claude's Draft 4

Manuscript: Wild-place metaplectic character transfer in degree two: Toral positivity and the nonabelian gluing problem

Materials: `mjl_rank2_wild_draft4.tex` and its Draft 3–4 revision log, dated November 8, 2026.

## 1. Assessment of the six requested corrections

The six corrections identified in my Draft 3 referee report have been incorporated. I find that the principal algebraic repairs are sound.

| Draft 3 issue                                                 | Draft 4 assessment                     |
| ------------------------------------------------------------- | -------------------------------------- |
| Incorrect central character in the \\(SD\_{16}\\) calculation | Repaired                               |
| Incorrect Brauer case split                                   | Repaired for the cases actually needed |
| Incorrect general-\\(p\\) exponent                            | Repaired                               |
| Incomplete ramified/unramified depth lemma                    | Repaired                               |
| Incorrect norm identity in the depth-three calculation        | Repaired                               |
| Summation-by-parts exposition and cocycle citation            | Repaired                               |

### The \\(SD\_{16}\\) argument

The corrected proof in lines 1747–1801 now uses the untwisted \\(\rho^\vee\\), together with the genuine order-three character \\(\psi_P\\). This eliminates the central-character discrepancy I found in Draft 3.

In the odd-central-character case, the resulting formula is

\\[ \phi\_\rho|\_{\Gamma\_{P_0}} = \psi_P\otimes \left( 3f\Theta\_{\rho^\vee|\_{SD\_{16}}} + 3\dim(\rho)(2\chi_1+2\chi_2) \right). \\]

The requisite identities

\\[ f\chi_1=\chi_2,\qquad f\chi_2=\chi_1 \\]

give a genuine representation character. The even-central-character case is handled correctly as well.

I accept the corrected finite-group character calculation.

### The Brauer reduction

The proof now separates cases according to the image of \\(B_2\\) in \\(D_8\\), rather than whether \\(B_2\\) itself is cyclic.

This addresses the counterexample involving \\(\langle a^4,b\rangle\\). In particular, the proof no longer makes the false assertion that every noncyclic \\(B_2\\) has centralizer equal to \\(T\\).

The three cases—trivial image, nontrivial cyclic image, and noncyclic image—provide the right structure for applying Brauer's characterization.

There is one technical qualification to the centralizer lemma that I discuss below.

### The depth lemma and general-\\(p\\) summation

The ramified proof correctly uses the isomorphism of leading unit quotients followed by the deep-unit \\(p\\)-th-power bijection.

The unramified proof correctly identifies the boundary map as a scaled Artin–Schreier map. The scalar residue direction supplies the missing codimension-one component.

The summation-by-parts calculation is also correct, including the four endpoint corrections. It establishes the claimed congruence for every odd prime \\(p\\), rather than only the primes used in computational checks.

The corrected exponent

\\[ \theta_0(\operatorname{Nrd}X)^{(p+1)/2} \\]

is the appropriate one, since \\((p+1)/2\\) is the inverse of \\(2\\) modulo \\(p\\).

These repairs are substantive and successful.

## 2. Two further points requiring clarification

During this review I found two issues in supporting arguments that were not among the six Draft 3 corrections. Neither appears to require changing the principal results, but both should be addressed.

### A. The centralizer lemma needs a qualification

Lines 918–948 and 1744–1745

Lemma `lem:centralizers(a)` was originally proved in the situation where \\(\Gamma_0\\) is a \\(3\\)-group. Its assertion is

\\[ C\_{\Gamma_0}(y)\subset T\_{E_y} \\]

for a nontrivial \\(2\\)-element \\(y\\).

In the odd-central-character case of Theorem `thm:reduction-all`, however, \\(\Gamma_0\\) contains the central subgroup \\(\mu_2\\).

A nonidentity element \\(y\\) of that central \\(\mu_2\\) satisfies

\\[ C\_{\Gamma_0}(y)=\Gamma_0, \\]

and its projection to \\(D_8\\) is trivial. There is no associated quadratic field \\(E_y=F(\eta)\\) in this case.

Thus the lemma cannot be extended unchanged to all nontrivial \\(2\\)-elements.

Recommended correction: In the extended version, require that the image of \\(y\\) in \\(\Gamma/\Gamma_0\simeq D_8\\) be nontrivial.

This restriction is already satisfied in the nontrivial cyclic-image case of the revised Brauer proof. Consequently, I do not regard this as a counterexample to Theorem `thm:reduction-all`; it is an imprecision in the supporting lemma's scope.

### B. The splitting of \\(\widetilde V\\) needs one additional justification

Lemma `lem:H1consequences(c)`, lines 1095–1106

After proving that the commutator form \\(\omega\\) vanishes, the manuscript concludes

\\[ \widetilde V\simeq\mu_3\times V, \\]

with the explanation that an abelian \\(\widetilde V\\) has genuine characters.

That explanation is insufficient in general. For example, the nonsplit central extension

\\[ 1\longrightarrow C_3 \longrightarrow C_9 \longrightarrow C_3 \longrightarrow1 \\]

is abelian and admits characters nontrivial on its central \\(C_3\\), yet it does not split.

Fortunately, the manuscript has the ingredients for a direct repair.

For \\(v\in K^3\\), the cube identity gives

\\[ (v,0)^3=(v^3,0), \\]

where \\(v^3\in K^7\subset K^6\\). This is a canonical star lift on which \\(\psi_6\\) takes value \\(1\\).

Similarly, central scalars have trivial third powers modulo \\(N_6\\), because \\(\theta_0^3=1\\).

Therefore every element of \\(\widetilde V=\widetilde U_3/N_6\\) has order dividing \\(3\\). Once \\(\omega=0\\) has been established, \\(\widetilde V\\) is an elementary abelian \\(3\\)-group, and the central extension necessarily splits.

I recommend inserting this argument immediately before the final sentence of Lemma `lem:H1consequences(c)`.

This appears to repair the step without changing anything downstream.

## 3. Results that depend on finite computations

The manuscript is careful to distinguish hand proofs, exhaustive finite calculations, and sampled checks. That is good mathematical practice.

However, I have not independently certified the exhaustive finite computations supporting the following assertions:

- Proposition `prop:design`, including the classification of the defect functions \\(e=\pm e\_\*\\).
- The \\(D_8\\)-orbit and Fourier calculations on the 72 good vectors in \\(\mathbb F_3^5\\).
- The exact character comparison and induced-model assertions in the proof of Target A.

The stated counting results are internally consistent with the character formulas, and nothing in this review has produced a contradiction.

For formal referee acceptance of Target A, I would want to run and inspect the load-bearing scripts identified in Remark `rem:dependencies`: principally scripts 1–4, 6, and 7. Scripts 8–12 are described as corroborative rather than essential.

This qualification concerns independent verification of the computational part of the proof, not a discovered mathematical error.

## 4. Assessment of the principal theorems

| Result                             | Referee assessment                                                              |
| ---------------------------------- | ------------------------------------------------------------------------------- |
| Quadratic toral positivity theorem | No new error identified in the valuation and permutation-character arguments    |
| Proposition `prop:H1`              | Accept the revised exhaustive Hilbert-symbol proof                              |
| Theorem `thm:pthpower`             | Accept                                                                          |
| Theorem `thm:H1-gen`               | Accept the principal argument, subject to the stated cocycle normalization      |
| Theorem `thm:reduction-all`        | Accept after clarifying the centralizer lemma                                   |
| Theorem `thm:levelone`             | Algebraic argument checks; dependent on Target A                                |
| Theorem `thm:main-targetA`         | Proof architecture is coherent; computational certification remains outstanding |

The \\(GL_2\\) cocycle cited in Draft 4 is algebraically equivalent to the published Kazhdan–Patterson formula, using antisymmetry of the Hilbert symbol.&#x20;

[image](https://www.google.com/s2/favicons?domain=https://uva.theopenscholar.com\&sz=32)

Get Started with OpenScholar



The manuscript also compiles successfully under `pdflatex`, producing a 33-page paper. Cross-references resolve after repeated compilation. The remaining `hyperref` warnings concern mathematical material in PDF bookmarks and are cosmetic.

## 5. Final referee recommendation

Minor revision

Draft 3 errors repaired

I find no new counterexample to the principal transfer results in Draft 4. The two remaining proof clarifications appear straightforward.

My recommendation to Fable-Claude is to prepare a narrowly focused Draft 5 that qualifies the centralizer lemma in the odd-central-character case and supplies the exponent-three argument establishing the splitting of \\(\widetilde V\\). The principal \\(SD\_{16}\\), Brauer, depth, and summation-by-parts arguments need not be rewritten.

This would be a favorable mathematical assessment of the manuscript, but not yet an unconditional certification of the full proof of Target A: that stronger conclusion requires independently reproducing the finite computations and confirming the imported statements from Parts I and III.

For the next verification, the most useful additional materials would be the Python modules for scripts 1–4, 6, and 7, together with the exact versions of Parts I and III on which Draft 4 relies.

Overall: Draft 4 is a significant improvement over Draft 3. I would regard the outstanding issues as limited and potentially resolvable without altering the main claims.