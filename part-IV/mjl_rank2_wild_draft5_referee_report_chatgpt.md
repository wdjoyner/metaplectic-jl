# Referee report — Draft 5

Manuscript: Wild-place metaplectic character transfer in degree two: Toral positivity and the nonabelian gluing problem

Materials examined: Draft 5 and Fable-Claude's Draft 4–5 revision log, November 8, 2026.

## 1. Overall assessment

Draft 5 makes a significant advance on Target B. Its new level-two argument is mathematically promising, and part of the central character identity can be proved directly, without relying on the reported computer calculation.

There is, however, an important distinction:

- The newly asserted decomposition of the restriction to \\(\widetilde U_3\\) can be justified by ordinary finite-group character theory.
- The final irreducibility argument depends on an exact orbit computation that I have not independently certified.
- The proposed extension to higher levels contains errors in its formulation, although these do not by themselves invalidate the level-two theorem.

My recommendation is revision before unconditional acceptance of the new Target B theorem. I see a plausible route to strengthening the manuscript considerably.

## 2. The corrections from Draft 4

Both requested corrections are present and address the defects identified previously.

The centralizer lemma: Its formulation now excludes central \\(2\\)-elements whose image in \\(D_8\\) is trivial. This removes the counterexample involving the central \\(\mu_2\\).

The splitting of \\(\widetilde V\\): The proof now establishes both

\\[ [\widetilde V,\widetilde V]=1 \quad\text{and}\quad x^3=1\quad(x\in\widetilde V). \\]

Thus \\(\widetilde V\\) is an elementary abelian \\(3\\)-group, and its central subgroup \\(\mu_3\\) admits a complement. This supplies the missing argument.

I find both corrections satisfactory.

## 3. Target B at level two: the principal new result

Theorem `thm:leveltwo`, lines 1979–2092

The new theorem concerns irreducible representations \\(\rho\\) of \\(D^\times\\) that are trivial on \\(K^3\\), with compatible central character.

For the genuinely new case, where the restriction to \\(K^2\\) is nonscalar, the manuscript establishes the following representation-theoretic structure:

\\[ \rho|\_{K^1}=\chi_3\oplus\chi_3', \qquad \dim\rho=6, \\]

where \\(\chi_3,\chi_3'\\) are the two irreducible degree-three characters of

\\[ \mathrm{Heis}=Q_1/Q_3. \\]

This is consistent with Clifford theory: the two characters are exchanged by the relevant order-two action, and their stabilizer has index two. The extension argument using the cyclic stabilizer is appropriate.

The predicted metaplectic transfer has dimension

\\[ 27\cdot6=162 \\]

and its restriction to \\(\widetilde U_1\\) is claimed to be the direct sum of two distinct irreducible representations of dimension \\(81\\).

That dimension count is consistent with the character theory. More importantly, the key restriction identity has a direct proof.

### 3.1 Independent verification of the character identity

Let

\\[ H=Q_3/Q_7,\qquad |H|=3^6=729. \\]

The manuscript gives \\(243\\) linear characters and \\(54\\) irreducible characters of degree \\(3\\). These numbers satisfy the character-degree sum:

\\[ 243+54\cdot 3^2=729. \\]

The group has commutator subgroup

\\[ H'=Q_6/Q_7\cong C_3. \\]

Consequently, the sum of its linear characters is

\\[ \sum\_{\lambda\in\operatorname{Irr}\_1(H)}\lambda(h) = \begin{cases} 243,&h\in H',\\\ 0,&h\notin H'. \end{cases} \\]

The regular character identity gives

\\[ \operatorname{Reg}\_H = \sum\_{\lambda\in\operatorname{Irr}\_1(H)}\lambda + 3\sum\_{\substack{\chi\in\operatorname{Irr}(H)\\\\\chi(1)=3}}\chi. \\]

Therefore

\\[ \boxed{ \sum\_{\chi(1)=3}\chi(h)= \begin{cases} 162,&h=1,\\\ -81,&h\in H'\setminus\\{1\\},\\\ 0,&h\notin H'. \end{cases}} \\]

This follows from standard character theory, not numerical computation.

Now consider the function

\\[ \bigl((\chi_3+\chi_3')\circ r\bigr)D \\]

in Step 2 of the new proof.

On elements of depth three, the cube root has noncentral image in the Heisenberg group. Both degree-three Heisenberg characters vanish there. The product is therefore zero.

On the subgroup \\(H'=Q_6/Q_7\\), the function \\(D\\) takes the value \\(27\\). At the identity, \\(\chi_3+\chi_3'=6\\), giving \\(162\\). At the two nonidentity elements of \\(H'\\), the cube root has nontrivial central image in \\(\mathrm{Heis}\\), so

\\[ \chi_3+\chi_3' =3\zeta+3\zeta^2=-3. \\]

The product is therefore \\(-81\\). Outside the good set, \\(D\\) vanishes.

Thus the manuscript's identity

\\[ \boxed{ \bigl((\chi_3+\chi_3')\circ r\bigr)D = \sum\_{\substack{\chi'\in\operatorname{Irr}(H)\\\\\chi'(1)=3}}\chi' } \\]

is correct, using the stated congruence-group structure.

I recommend replacing the computational assertion in Step 2 by this proof. It is shorter, more transparent, and eliminates a substantial computational dependency from Theorem `thm:leveltwo`.

### 3.2 The Clifford-theory argument

Lines 2066–2091

Let

\\[ \widehat\Gamma=\widetilde U_1/N,\qquad \widehat H=\widetilde U_3/N,\qquad [\widehat\Gamma:\widehat H]=27 \\]

for the finite normal subgroup \\(N\\) specified in the manuscript.

After Step 2, the restriction of \\(\Phi\_\rho\\) to \\(\widehat H\\) is a multiplicity-free sum of \\(54\\) genuine degree-three irreducible characters.

The remaining question is how \\(\widehat\Gamma\\) permutes those characters.

For an orbit \\(O\\), if

\\[ \operatorname{Stab}\_{\widehat\Gamma}(\mu)=\widehat H, \\]

then Clifford theory gives

\\[ \operatorname{Ind}\_{\widehat H}^{\widehat\Gamma}\mu \\]

irreducible, of degree \\(27\cdot3=81\\).

If all \\(54\\) characters form two orbits of length \\(27\\), their induced characters give precisely the desired \\(162\\)-dimensional restriction.

Fable-Claude reports that script 15 obtains exactly

\\[ 54=27+27 \\]

under the twisted conjugation action. This is the correct action to use:

\\[ \mu^t=\lambda_0\\,c_t\\,(\chi'\circ\operatorname{Ad}t), \qquad c_t=\lambda_0^t/\lambda_0. \\]

The distinction between this action and ordinary conjugation on \\(\operatorname{Irr}(H)\\) is essential. It is entirely possible for the untwisted action to have stabilizers while the twisted action is free.

My finding: The Clifford-theoretic deduction is correct provided the two free orbits reported by script 15 are verified. The dimension counts and the proposed induction mechanism contain no apparent error.

However, the scripts and their machine-readable outputs were not included with Draft 5. I therefore cannot certify the free-orbit assertion merely from its description in the revision log.

This is the principal remaining verification dependency for the new level-two theorem.

### 3.3 A normalization inconsistency

There is also a minor but real inconsistency in Step 1.

At lines 1714–1729, the notation fixes a nontrivial cubic character \\(\theta_1\\) for the trivial row and chooses \\(\theta_0=\theta_1\\) in the even-central-character case.

But line 2039 says:

> Here \\(\theta_0=1\\); the general case is a twist.

The argument then uses \\(\lambda_0\\), defined for the fixed trivial-row central character \\(\widetilde\theta_1\\).

These conventions need to be made consistent. If one works with \\(\theta_0=1\\), the baseline character \\(\lambda_0\\) must also be taken in the corresponding normalization, or explicitly twisted to it.

I do not think this is an obstruction: the manuscript already proves independence of the compatible central character. Nevertheless, the finite quotient and the character \\(\lambda_0\\) must be defined in the same normalization.

## 4. The higher-level cube-root correspondence

Section 12.5, lines 2114–2160

Here I find substantive problems that should be corrected before publication, even though this section is labeled as an outline/conjecture.

### 4.1 The claimed bijection is false

The text states that the cube root induces a bijection from the good classes of

\\[ H_m=Q_3/Q\_{3m+1} \\]

onto

\\[ \mathrm{Heis}\_m=Q_1/Q\_{m+1}. \\]

For \\(m=2\\), the manuscript itself supplies a counterexample by counting:

\\[ \\#\operatorname{Good}(Q_3/Q_7)=219, \qquad \\#(Q_1/Q_3)=27. \\]

There cannot be a bijection between sets of those sizes.

The correct statement is that the cube-root construction gives a surjective, generally many-to-one map from the good residue classes to the appropriate root classes.

This matters because the fibers are precisely where some of the higher-level character theory becomes nontrivial.

### 4.2 The \\(m=1\\) quotient is too shallow

The proposed definition

\\[ \widehat H_m = \widetilde U_3/ \ell(K^{3m+1})\ker\widetilde\theta \\]

is problematic for \\(m=1\\).

The canonical star splitting \\(\ell\\) is established on \\(K^6\\), not on all of \\(K^4\\). Thus \\(\ell(K^4)\\) has not been defined as the required subgroup, and \\(\lambda_0\\) has not been shown to descend through that quotient.

There is also a counting obstruction. At \\(m=1\\),

\\[ H_1=Q_3/Q_4 \\]

has order \\(9\\). Even if its covering extension admitted the proposed splitting, it would have only nine genuine linear characters for the fixed central character. A group of order \\(27\\) cannot act freely on that nine-element set.

Consequently, the assertion that the freeness condition holds for \\(m\le2\\) is false under the definitions as printed.

A more appropriate finite model must retain at least the depth-six information used in the construction of \\(\lambda_0\\).

### 4.3 A counterexample to the \\(m=1\\) correspondence as stated

There is a second, more substantive problem with the assertion at lines 2136–2138 that the conjecture holds for \\(m=1\\) with

\\[ \chi'=\chi\circ\pi_3. \\]

Consider the residue field

\\[ \mathbb F_9=\mathbb F_3(i),\qquad i^2=-1, \\]

and choose the nontrivial additive character

\\[ \chi(a+bi)=\zeta^a. \\]

Take

\\[ w=1+i. \\]

Since \\(\operatorname{Nm}(w)=-1\\),

\\[ w^5=\operatorname{Nm}(w)w=-w. \\]

For \\(t=1+wj\\) and \\(g=t^3\\), the cube-root transform gives

\\[ (\chi\circ r)(g)=\chi(w)=\zeta, \\]

whereas the depth-three digit gives

\\[ (\chi\circ\pi_3)(g)=\chi(w^5)=\zeta^{-1}. \\]

The two values differ, and \\(\Phi_1(g)\ne0\\). Thus the proposed character identity cannot hold with the stated choice of \\(\chi'\\).

In fact, no alternative linear character of \\(Q_3/Q_4\\) repairs this particular example for all \\(g\\). Such a character would have to satisfy

\\[ \chi'(a)=\chi(a^5) \\]

for every \\(a\in\mathbb F_9\\). But the right-hand side is not additive: it takes the values \\(\zeta,1,\zeta^{-1}\\) at \\(1,i,1+i\\), respectively, contradicting \\(\chi'(1+i)=\chi'(1)\chi'(i)\\).

Therefore the constituent-wise cube-root conjecture is false for \\(m=1\\) as formulated.

This does not contradict Theorem `thm:levelone`. That theorem applies to restrictions of actual \\(D^\times\\)-representations, whose characters are invariant under the additional \\(D_8\\)-action. The offending individual additive character is not \\(D_8\\)-invariant.

A potentially useful replacement conjecture would operate on \\(D_8\\)-stable orbit sums of characters, rather than requiring a correspondence for every individual irreducible character.

This distinction is worth developing; it could reveal the correct higher-level formulation of Target B.

## 5. Computational certification and presentation

There are three smaller issues I recommend addressing.

First, script 15 is essential. The reported orbit calculation should be accompanied by a certificate showing the action of generators of \\(Q_1/Q_3\\) on the \\(54\\) degree-three characters, with exact verification that every stabilizer is trivial. An orbit table or explicit stabilizer test would be more useful than sampled checks of cocycle compatibility.

Second, the computational provenance needs clarification. The appendix says that the scripts use no floating-point arithmetic except in script 11. But the revision log and line 2108 describe a numerical Burnside computation followed by reconstruction of characters in \\(\mathbb Z[\zeta_3]\\).

This is not intrinsically objectionable—numerical discovery followed by exact certification is perfectly legitimate—but the description should be consistent. Orthogonality alone should not be presented as a complete certificate that the reconstructed rows are the irreducible characters. The analytic argument in §3.1 of this report offers a cleaner alternative for the character identity.

Third, the abstract and introduction overstate the admissible scope slightly. The new result is for representations with compatible central character, requiring

\\[ \theta\_\rho|\_{\mu_3}=1. \\]

Not every irreducible representation trivial on \\(K^3\\) satisfies that condition. The abstract should therefore include this qualification. Also, the introduction's statement that Drafts 1–3 settled the new level-two result should be updated to include Draft 5.

## 6. Referee verdict by result

| Result                                          | Assessment                                          |
| ----------------------------------------------- | --------------------------------------------------- |
| Two Draft 4 proof corrections                   | Accept                                              |
| Level-two Clifford classification of \\(\rho\\) | Accept                                              |
| Level-two restriction identity, Step 2          | Accept; direct proof available                      |
| Level-two twisted orbit computation, Step 3     | Requires independent certification                  |
| General all-row reduction theorem               | No new error identified                             |
| General-\\(p\\) summation and (H1)              | Previous favorable assessment stands                |
| Higher-level cube-root conjecture               | Must be reformulated; false at \\(m=1\\) as printed |
| Full Target B                                   | Still open beyond the classes treated               |

### What Draft 5 has established, subject to computational verification

The emerging representation-theoretic picture is particularly interesting:

### Progress toward Target B

Level zero and one

Proved

Representations trivial on \\(K^2\\), with compatible central character, and the specified norm twists.

Level two

Computational verification needed

New \\(162\\)-dimensional transfer, with a proposed \\(81+81\\) restriction decomposition.

Level three and beyond

Open

The constituent-wise conjecture needs revision before it can serve as a general approach.

## 7. Recommendations for Draft 6

I recommend five specific changes, in this order:

1. Retain the level-two theorem, but make its acceptance conditional on certification of the twisted orbit calculation in script 15. The representation-theoretic derivation is otherwise coherent.
2. Replace the numerical character decomposition in Step 2 with the regular-character proof given in §3.1 above. The same approach should establish the decomposition into the two groups of \\(27\\) degree-three characters.
3. Make the central-character normalization consistent throughout the level-two argument.
4. Rewrite Section 12.5. Correct the many-to-one cube-root map, fix the finite-quotient definitions, and replace the false \\(m=1\\) constituent-wise conjecture with a formulation appropriate to \\(D_8\\)-stable character sums.
5. Specify the exact computational certificates, and correct the descriptions of numerical versus exact calculations.

### Overall recommendation: Revision required, with a favorable assessment of the new level-two strategy

I agree that the paper is becoming mathematically stronger. Draft 5 does more than extend a list of examples: it identifies a mechanism by which transfer integrality can survive even when the earlier sufficient criterion fails.

That is a valuable observation. It shows why studying the induced representation and its Clifford orbits can be more effective than insisting that the cube-root transform itself be an invariant virtual character.

The new character decomposition admits an elegant proof. The remaining load-bearing question is whether the twisted action really has the two free orbits claimed. If script 15 is correct and reproducible, the level-two part of Target B has a strong case for acceptance, after the normalization correction.

The higher-level conjecture is another matter: the explicit \\(m=1\\) counterexample means it needs genuine mathematical revision, not merely editorial clarification.

For the next referee pass, the most useful files would be `step15_level2_clifford.py`, its dependencies (including `cover.py` and the data used to construct \\(\lambda_0\\)), and `step13_level2.py` and `step14_level2_restriction.py` if Fable-Claude wishes to retain the computational character-table proof. They would allow me to test the decisive orbit assertion independently rather than relying on its reported output.

My bottom line: Draft 5 contains credible and substantial progress on Target B, but I would not yet approve the new theorem unconditionally. The strongest next step is to certify the \\(54=27+27\\) orbit calculation and separate the proved level-two theorem from the conjectural—and currently incorrect—generalization.