## Referee report on Draft 2 — (H1) only

Scope: Proposition `prop:H1`, its supporting lemmas, and the specific deficiencies identified in Draft 1. Target A and the remaining results are excluded from this review.

### 1. The principal repair is mathematically substantive

Draft 2 replaces the defective valuation-dependent argument with a direct proof using the cubic Hilbert symbol.

In the main case, \\(b,b'\ne0\\) and \\(R\ne0\\), the authors reduce (H1) to

\\[ h_E(R,\tau) = v(\tau)\lambda(a') -v(R)\bigl(\lambda(a')-\lambda(a)\bigr), \\]

where

\\[ R=a'+\sigma(a)\tau,\qquad \tau=\sigma(b'/b). \\]

The crucial substitution

\\[ R=a'(1+\tau_2),\qquad \tau_2=\frac{\sigma(a)\tau}{a'} \\]

allows the left-hand side to be expanded into three Hilbert symbols. One vanishes by the Steinberg relation, and the other two give exactly the required expression.

I have checked these algebraic manipulations independently. The main-case argument is valid, assuming the standard Hilbert-symbol identities stated in the manuscript.

In particular, it does not invoke Draft 1's false assertion that \\(\beta(X,X')=0\\) when \\(v(\tau)>0\\). The old case (i) is therefore repaired at the level of the principal identity.

### 2. The former sampled cases are now handled by proof

I checked the remaining cases in Proposition `prop:H1`, including the boundary case \\(R=0\\).

| Case in Draft 2        | Assessment                                                              |
| ---------------------- | ----------------------------------------------------------------------- |
| \\(b,b'\ne0,\ R\ne0\\) | Valid general identity; covers all valuations of \\(\tau\\) and \\(R\\) |
| \\(b=0,\ b'\ne0\\)     | Correct reduction using the norm identity and Galois invariance         |
| \\(b\ne0,\ b'=0\\)     | Correct computation of \\(\beta\\) and \\(\kappa\\)                     |
| \\(b=b'=0\\)           | Correct; follows from the depth bound                                   |
| \\(b,b'\ne0,\ R=0\\)   | Correct, although the calculation could be shortened                    |

For the last case, the key identity is particularly simple:

\\[ \beta(X,X') =v(b)\bigl[h_E(\varpi,a)+h_E(\varpi,a')\bigr]. \\]

On the other hand,

\\[ \kappa(X)+\kappa(X') =2v(b)\bigl[h_E(\varpi,a)+h_E(\varpi,a')\bigr]. \\]

Their sum vanishes modulo \\(3\\), as required because \\(\kappa(XX')=0\\).

This is an exhaustive argument over the possible cases, not an exhaustive computer enumeration. That distinction is important. The manuscript's 12,000 sampled checks are now supplementary evidence, not a substitute for a proof.

### 3. The counterexample that invalidated Draft 1

The original pair was

\\[ X=1+\varpi^3j,\qquad X'=1+\varpi^3+\varpi^4j. \\]

Draft 2 acknowledges that its cocycle has

\\[ \beta(X,X')=2, \\]

rather than zero. The revised formulas yield

\\[ \kappa(X)=0,\qquad \kappa(X')=1,\qquad \kappa(XX')=0. \\]

Consequently,

\\[ 0=0+1+2\pmod3. \\]

I independently checked this calculation using the revised Hilbert-symbol formulas and the normalization given in the manuscript.

The earlier counterexample therefore no longer contradicts the proof. More importantly, the new reasoning explains why the identity remains true even though \\(\beta\\) is nonzero.

### 4. Two minor corrections are still needed

Although the central proof works, I found two technical points in its supporting argument that should be corrected before marking (H1) fully proved as written.

A. Scalar uniqueness in Corollary `cor:starK6(b)`.

The manuscript argues that

\\[ zv^3=z'v'^3 \quad\Longrightarrow\quad (v'/v)^3\in F^\times. \\]

That implication needs justification because \\(D^\times\\) is noncommutative. Fortunately, there is a simpler proof using reduced norms:

\\[ z^2\operatorname{Nrd}(v)^3 =z'^2\operatorname{Nrd}(v')^3. \\]

Thus \\((z/z')^2\\) is a cube in \\(F^\times\\). Since \\(F^\times/F^{\times3}\\) has exponent \\(3\\), it follows immediately that

\\[ z/z'\in F^{\times3}. \\]

This establishes the required uniqueness without a commutativity argument.

B. The dependence on the scalar character \\(\theta_0\\).

Corollary `cor:starK6(c)` explicitly assumes \\(\theta_0=1\\), but the subsequent equivalence and the final formula of Proposition `prop:H1` are stated without that restriction.

For a general compatible character \\(\theta_0\\), the formula on \\(\widetilde K^6\\) should be

\\[ \boxed{ \psi\_{6,\theta_0}(X,e) = \zeta^{e-\kappa(X)} \theta_0(\operatorname{Nrd}X)^{-1}. } \\]

The extra factor is itself a character, so it does not obstruct (H1). The authors can either explicitly work with \\(\theta_0=1\\) throughout the calculation and then twist, or insert this factor and adjust the converse argument in Corollary `cor:starK6(d)`.

These are readily repairable issues; neither recreates the substantive gap in Draft 1.

### 5. Referee verdict

(H1): Accept after minor corrections

Substantially repaired

| Incorrect vanishing in old case (i)   | Repaired                |
| ------------------------------------- | ----------------------- |
| Sampled checks in old cases (iv)–(v)  | Replaced by proof       |
| Supporting scalar-uniqueness argument | Minor correction needed |
| General \\(\theta_0\\) normalization  | Minor correction needed |

My assessment is that Draft 2 successfully repairs the two mathematical deficiencies that caused me to reject the (H1) proof in Draft 1. The resulting proof is genuinely analytic, does not require exhaustive computational verification, and introduces no new hypothesis.

I recommend that Fable-Claude make the two small corrections above. I would then be prepared to accept Proposition `prop:H1` as proved, relative to the stated cocycle model and standard Hilbert-symbol properties.

I have not independently executed Script 12, and the Python modules are not needed for this limited assessment. The standard Kubota cocycle formula used in the argument is also consistent with the published formula.&#x20;

[image](https://www.google.com/s2/favicons?domain=https://citeseerx.ist.psu.edu\&sz=32)

CiteSeerX



I have deliberately not examined Target A, the finite Fourier calculations, or the remaining results. Those should be assessed separately after the two corrections are incorporated.