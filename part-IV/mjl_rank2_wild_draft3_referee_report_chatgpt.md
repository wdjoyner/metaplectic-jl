# Referee report — Draft 3

Manuscript: Wild-place metaplectic character transfer in degree two: Toral positivity and the nonabelian gluing problem

Materials examined: Draft 3 and its revision log, November 8, 2026.

## Overall assessment

Draft 3 contains substantial mathematical progress. Of the four issues singled out by Fable-Claude, I find that the \\(SD\_{16}\\) character calculation and summation by parts are correct. However, the \\(SD\_{16}\\) proof has a separate central-character error that must be repaired, and the general-\\(p\\) theorem contains an incorrect formula for its character.

My preliminary disposition is revision required, rather than acceptance as written.

| Referee checkpoint                                    | Finding                                                  |
| ----------------------------------------------------- | -------------------------------------------------------- |
| \\(SD\_{16}\\) identification and character swap      | Correct calculation; faulty representation normalization |
| Depth-three digit \\(w=\pm\pi_3(g)\\)                 | Correct conclusion; one algebraic typo                   |
| General-\\(p\\) summation by parts                    | Correct                                                  |
| Ramified-torus depth lemma                            | Correct approach; proof should be expanded               |
| Additional finding: general-\\(p\\) character formula | Incorrect for \\(p\ge5\\)                                |

## 1. The \\(SD\_{16}\\) argument

Theorem `thm:reduction-all`, lines 1743–1787

### 1.1 The group identification is correct

Let \\(a,b\\) be the images of \\(1+i,j\\), respectively, after passing to the relevant quotient.

Using

\\[ (1+i)^4=-4,\qquad j^2=\varpi,\qquad j(1+i)j^{-1}=2(1+i)^{-1}, \\]

and

\\[ \operatorname{sgn}(-4)=\operatorname{sgn}(2)=-1, \\]

one obtains

\\[ a^8=1,\qquad b^2=1,\qquad bab^{-1}=a^3. \\]

These are the defining relations of the semidihedral group of order \\(16\\):

\\[ SD\_{16}=\langle a,b\mid a^8=b^2=1,\ bab^{-1}=a^3\rangle. \\]

The central involution is \\(a^4\\), corresponding to \\(-1\\).

I also verified the asserted character identity. If

\\[ f(a^k)=(-1)^k,\qquad f(a^kb)=1, \\]

then the two faithful, irreducible two-dimensional characters satisfy

\\[ f\chi_1=\chi_2,\qquad f\chi_2=\chi_1. \\]

The identity

\\[ 8\delta^{\mathrm{sgn}}=2\chi_1+2\chi_2 \\]

is correct as well. Thus the finite-group calculation that Fable-Claude identified as potentially troublesome is valid.

### 1.2 A central-character error remains

At lines 1762–1775 the manuscript introduces

\\[ \rho'=\rho^\vee\otimes(\theta_1^2\circ\operatorname{Nrd}) \\]

and asserts that \\(\rho'\\) has central character \\(\mathrm{sgn}\\), so that its restriction factors through \\(SD\_{16}\\).

This is not correct for a nontrivial character \\(\theta_1\\) of order \\(3\\).

Indeed, on a scalar \\(z\in F^\times\\),

\\[ (\theta_1^2\circ\operatorname{Nrd})(z) =\theta_1(z^2)^2 =\theta_1(z)^4 =\theta_1(z). \\]

Consequently,

\\[ \boxed{\omega\_{\rho'}=\mathrm{sgn}\cdot\theta_1,} \\]

not simply \\(\mathrm{sgn}\\).

In particular, \\(\rho'\\) need not be trivial on \\(\ker\mathrm{sgn}\\), and the claimed factorization through \\(SD\_{16}\\) is not justified.

The same normalization problem appears in the preceding even-central-character case, where \\(\rho^\vee\otimes(\theta_1^2\circ\operatorname{Nrd})\\) is said to be trivial on \\(F^\times\\).

This is a genuine error in the proof, although the character calculation needed to repair it remains available.

### 1.3 Recommended repair

The character calculation can be salvaged cleanly by separating the cubic central character from the \\(2\\)-group representation.

Let \\(\psi_P\\) be the genuine order-three character of \\(\Gamma\_{P_0}\\), trivial on its \\(2\\)-Sylow subgroup and satisfying

\\[ \psi_P(z,0)=\theta_1(z) \qquad(z\in F^\times). \\]

Since

\\[ x\_\eta=\widetilde{\eta^4}(\tilde\eta^{-1})^3, \\]

and \\(\psi_P^3=1\\), we have

\\[ \psi_P(x\_\eta)=\theta_1(\eta^4). \\]

Consequently, away from the center,

\\[ \frac{\phi\_\rho(x\_\eta)}{\psi_P(x\_\eta)} = 3\operatorname{sgn}(\eta^4)\Theta\_{\rho^\vee}(\eta) \\]

in the odd-central-character case.

Now \\(\rho^\vee\\) itself, without the extra \\(\theta_1^2\circ\operatorname{Nrd}\\) twist, has central character \\(\operatorname{sgn}\\) and descends to the appropriate \\(SD\_{16}\\) quotient.

Thus the desired formula becomes

\\[ \boxed{ \phi\_\rho|\_{\Gamma\_{P_0}} = \psi_P\otimes \left( 3f\\,\Theta\_{\rho^\vee|\_{SD\_{16}}} + 3\dim\rho\\,(2\chi_1+2\chi_2) \right). } \\]

This is a character because multiplication by \\(f\\) interchanges \\(\chi_1\\) and \\(\chi_2\\).

The analogous repair in the even-central-character case uses \\(\rho^\vee|\_{D_8}\\), rather than the incorrectly asserted scalar-trivial twist.

Recommendation: Replace the relevant two-group paragraph with a proof organized around \\(\psi_P\\) and \\(\rho^\vee\\). The substantive \\(SD\_{16}\\) computation survives.

### 1.4 An additional gap in the Brauer reduction

There is another issue in lines 1782–1785, where the proof asserts that every noncyclic \\(2\\)-subgroup \\(B_2\\) has

\\[ C\_{\Gamma_0}(B_2)=T. \\]

This is false when \\(B_2\\) is noncyclic but its image in \\(D_8\\) is cyclic.

For example, in \\(SD\_{16}\\), consider

\\[ B_2=\langle a^4,b\rangle\cong C_2\times C_2. \\]

Its image in \\(D_8\\) is cyclic because \\(a^4\\) is central and maps to the identity. The centralizer of \\(B_2\\) can contain noncentral elements from the \\(j\\)-torus.

More concretely, the cube of \\(1+j\\) is a noncentral depth-three element, and its lift commutes with the lift of \\(j\\): commutators in the covered torus are central of order dividing three, so cubing kills them. This element survives the quotient used in the proof.

The repair is to divide Brauer's argument according to the image of \\(B_2\\) in \\(D_8\\), rather than according to whether \\(B_2\\) itself is cyclic.

- If its image is trivial, \\(B\subset\Gamma_0\\), and the assumed virtual-character property applies.
- If its image is nontrivial cyclic, \\(B\\) lies in the appropriate covered torus, so toral descent applies.
- If its image is noncyclic, the centralizer argument reduces \\(B_3\\) to the center, and the corrected \\(SD\_{16}\\) calculation applies.

This is a straightforward but necessary correction to the claimed all-row reduction theorem.

## 2. The depth-three digit calculation

Theorem `thm:levelone`, lines 1889–1902

Verdict: Correct, with a minor algebraic correction.

Let \\(w\in\mathbb F_9^\times\\) be the leading coefficient of \\(t\\). Lemma `lem:cube(c)` gives

\\[ \pi_3(t^3)=w^5. \\]

Since \\(w\in\mathbb F_9^\times\\),

\\[ w^4=\operatorname{Nm}\_{\mathbb F_9/\mathbb F_3}(w) \in\mathbb F_3^\times=\\{\pm1\\}. \\]

Therefore

\\[ w^5=\pm w. \\]

Conjugation by \\(i\\) sends \\(w\\) to \\(-w\\) in \\(K^1/K^2\\). Consequently, the restriction of any character of \\(D^\times\\) to \\(K^1/K^2\\) is invariant under \\(w\mapsto-w\\).

The desired equality follows:

\\[ \Theta\_\rho(t) = \Theta\_{\rho|K^1}(\pi_3(g)). \\]

The manuscript writes \\(w^4=\operatorname{Nm}(w)^2=\pm1\\). The middle equality is incorrect. It should read

\\[ \boxed{w^4=\operatorname{Nm}(w)=\pm1.} \\]

The conclusion and subsequent proof remain valid.

The construction of the invariant character \\(\Psi\\) is also correct. Thus I find no independent obstruction in this step, although Theorem `thm:levelone` remains dependent on the corrected all-row reduction theorem and the earlier Target A result.

## 3. The summation-by-parts argument

Theorem `thm:pthpower`, lines 2011–2053

Verdict: Correct.

This is one of the strongest additions in Draft 3. I verified the algebra independently, including the endpoint terms.

Define

\\[ a_k=(S\_{k+1},S_k)\_E,\qquad b_k=(S_k,n)\_E \\]

with additive Hilbert-symbol notation.

Cassini's identity and the Steinberg relation give

\\[ 2(a_k-a\_{k-1}) =(k-1)(b\_{k+1}-2b_k+b\_{k-1}). \\]

This identity is correct.

Set

\\[ c_j=\frac{(j-1)(p-j)}2. \\]

The proof then needs

\\[ \sum\_{j=2}^{p-1}c_j\Delta^2b_j \equiv-\sum\_{j=1}^{p}b_j\pmod p. \\]

To establish this rigorously, extend \\(c_j\\) using its quadratic formula. Direct calculation yields

\\[ c\_{j-1}-2c_j+c\_{j+1}=-1 \\]

for every integer \\(j\\), while

\\[ c_1=c_p=0,\qquad c_0=c\_{p+1}=-\frac p2\equiv0\pmod p. \\]

Discrete summation by parts therefore gives precisely the required congruence, including both endpoints.

Since \\(b_1=(1,n)\_E=0\\),

\\[ \sum\_{k=1}^{p-1}a_k+ \sum\_{k=2}^{p}b_k=0\pmod p. \\]

This proves the claimed vanishing of the accumulated cocycle exponent.

The argument is algebraic and valid for every odd prime \\(p\\). Testing \\(p\le13\\) was useful corroboration but is not logically necessary.

### 3.1 Is the general-\\(p\\) Kubota formula legitimate?

Yes, subject to the stated cocycle normalization.

The Kubota formula for the \\(n\\)-fold cover of \\(\mathrm{GL}\_2\\) is not restricted to \\(n=3\\). Patterson explicitly gives the formula using the \\(n\\)-th Hilbert symbol, and the Kazhdan–Patterson family is obtained by the determinant-symbol twist used here.&#x20;

[image](https://www.google.com/s2/favicons?domain=https://intlpress.com\&sz=32)

Intl Press+1



I recommend adding a precise citation to the particular cocycle representative, rather than relying only on the general Kazhdan–Patterson reference.

I find no defect in the summation-by-parts argument itself. The proof of Theorem `thm:pthpower` is acceptable, once the cocycle convention is specified explicitly.

## 4. The generalized depth lemma, including ramified tori

Lemma `lem:depth-gen(c)`, lines 1984–2009

Verdict: The proposed proof is sound in its essential idea, but the ramified case deserves a complete argument.

Write

\\[ k_0=\frac{2e}{p-1},\qquad d=\frac{pe}{p-1}. \\]

The assertion is

\\[ K^{2d}=U_F^{(1)}(K^{k_0})^p. \\]

Here is how I recommend filling in the ramified case.

Let \\(E/F\\) be a ramified quadratic maximal subfield, and let

\\[ X\in E^\times\cap K^{2d}=U_E^{(2d)}. \\]

Because \\(E/F\\) is totally ramified and \\(k_E=k_F\\), the natural map

\\[ U_F^{(d)}/U_F^{(d+1)} \longrightarrow U_E^{(2d)}/U_E^{(2d+1)} \\]

is an isomorphism of additive residue groups.

Consequently, we can choose \\(z\in U_F^{(d)}\\) so that

\\[ z^{-1}X\in U_E^{(2d+1)}. \\]

Now \\(e(E/\mathbb Q_p)=2e\\), so the standard deep-unit power-map theorem gives a bijection

\\[ (\cdot)^p: U_E^{(k_0+1)} \xrightarrow{\ \sim\ } U_E^{(k_0+1+2e)} =U_E^{(2d+1)}. \\]

Thus \\(z^{-1}X=v^p\\) for some \\(v\in U_E^{(k_0+1)}\subset K^{k_0}\\), establishing the desired decomposition.

This fills the ramified gap without any finite computation.

The unramified argument also works: its boundary map is a scaled Artin–Schreier operator on \\(k_E\\). Its image has codimension one over \\(\mathbb F_p\\), and the image of \\(k_F\\) supplies the missing direction because

\\[ \operatorname{Tr}\_{k_E/\mathbb F_p}(u) =2\operatorname{Tr}\_{k_F/\mathbb F_p}(u) \qquad(u\in k_F), \\]

and \\(p\\) is odd.

I recommend including these arguments explicitly. They are important because the generalized (H1) theorem depends on this lemma.

## 5. An additional error in the general-\\(p\\) theorem

Theorem `thm:H1-gen`, lines 2055–2092

The construction of the star section is persuasive, and its multiplicativity computation appears to generalize the cubic argument correctly. However, the stated formula for \\(\psi\_{2d}\\) is wrong for \\(p\ge5\\).

The theorem currently gives

\\[ \psi\_{2d}(X,e) = \zeta^{e-\kappa(X)} \theta_0(\operatorname{Nrd}X)^{-1}. \\]

But Lemma `lem:depth-gen(c)` establishes

\\[ z\equiv\operatorname{Nrd}(X)^{(p+1)/2} \pmod{F^{\times p}}. \\]

Since the character is supposed to take the value \\(\theta_0(z)\\) on the canonical star lift, the correct formula, assuming \\(\theta_0^p=1\\), is

\\[ \boxed{ \psi\_{2d}(X,e) = \zeta^{e-\kappa(X)} \theta_0(\operatorname{Nrd}X)^{(p+1)/2}. } \\]

For \\(p=3\\), the exponent \\(2\\) is congruent to \\(-1\\), explaining why the old formula works in the running example.

For \\(p=5\\), it does not. Indeed, take a scalar \\(X=z\\) for which \\(\theta_0(z)\\) has order five. The canonical lift is \\((z,0)\\), so its prescribed character value is \\(\theta_0(z)\\). The printed formula instead gives

\\[ \theta_0(z^2)^{-1}=\theta_0(z)^{-2}, \\]

which is generally different.

This is a definite error, not merely a missing justification. Fortunately, it concerns the formula for the character, not the Hilbert-symbol proof that the star section is multiplicative.

I recommend correcting the exponent and making the condition \\(\theta_0^p=1\\) explicit.

## 6. Final referee recommendations

I would send Fable-Claude the following set of required changes.

| Priority | Required change                                                                                                       | Consequence                                    |
| -------- | --------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------- |
| High     | Correct the \\(\rho'\\) central character and rewrite the \\(SD\_{16}\\) proof using \\(\psi_P\\) and \\(\rho^\vee\\) | Repairs a genuine gap in the all-row reduction |
| High     | In the Brauer argument, classify \\(B_2\\) by its image in \\(D_8\\)                                                  | Repairs the false centralizer assertion        |
| High     | Replace the general-\\(p\\) exponent \\(-1\\) by \\((p+1)/2\\)                                                        | Corrects Theorem `thm:H1-gen`                  |
| Medium   | Expand the ramified and unramified cases of `lem:depth-gen(c)`                                                        | Makes the depth argument self-contained        |
| Low      | Correct \\(w^4=\operatorname{Nm}(w)^2\\) to \\(w^4=\operatorname{Nm}(w)\\)                                            | Editorial/algebraic correction                 |
| Low      | Add a precise Kubota cocycle citation and an explicit summation-by-parts calculation                                  | Improves verifiability                         |

### Status of the principal results

Theorem `thm:pthpower`

Accept

The general odd-prime summation identity is valid, assuming the standard Kubota cocycle normalization.

Theorem `thm:levelone`

Conditional

The depth-three digit calculation is correct. The theorem still relies on the all-row reduction and the earlier computationally supported Target A theorem.

Theorem `thm:reduction-all`

Requires revision. The semidihedral representation theory is correct, but the proof contains both the central-character error and the centralizer gap.

Theorem `thm:H1-gen`

The multiplicativity calculation is promising and appears correct under the stated depth hypotheses. The explicit character formula must be corrected, and the depth lemma should be fully justified before accepting the theorem as stated.

### Conclusion

I would not reject Draft 3. The four flagged calculations largely survive independent examination, including the difficult summation-by-parts identity and the faithful-character swap in \\(SD\_{16}\\). The problems I found appear repairable without changing the central mathematical strategy.

Nevertheless, I would not yet label the new all-row reduction theorem `[P]` without the repairs above. Nor would I retain the current general-\\(p\\) character formula.

My recommendation is for Fable-Claude to prepare Draft 4 with these six corrections, keeping the mathematical scope unchanged. That would allow the next referee pass to concentrate on verifying the corrected all-row reduction and generalized (H1), rather than reopening calculations that have already checked out.