I’ll referee Draft 1 against its revision log and the mathematical goals of the rank-two project. I’ll check the new proofs and computations independently, especially anything claimed about nonabelian gluing or wild integrality. I’ll also identify which Python modules, if any, are needed to verify computational claims. I won’t edit the manuscript yet.

Checked the proof

Audited the argument

Identified proof gaps and refined validation

Reviewed mathematical draft, proofs, lemmas, revisions, and identified fatal flaws




I’ve found a material proof gap in Draft 1’s central claim. It labels Target A as proved with computational assistance, but Proposition (H1)—which the main theorem depends on—explicitly leaves boundary cases checked only by sampling. I also found a specific incorrect intermediate assertion in the written (H1) proof. I’ll check whether it is repairable and independently verify the finite design tables; the Python modules would be valuable for auditing those computations.

Planned a rigorous referee report

Consolidated review points

Flagged proof gaps







Referee report on Claude's rank-two wild Draft 1
Manuscripts: mjl_rank2_wild_draft1.tex and mjl_rank2_wild_revision_log_draft1.tex

Recommendation: Major revision.

This is a substantial and promising development of Draft 0. Claude has introduced a concrete finite-group strategy for resolving the wild-place integrality problem, and several of its combinatorial calculations survive independent verification.

However, I do not yet accept the central claim that Target A has been proved. The main theorem depends on Hypothesis (H1), whose proof contains an unverified infinite family of cases. The manuscript acknowledges this, but nevertheless labels the resulting theorem as proved with computational assistance.

The appropriate current description is:
Draft 1 reduces Target A to an explicit multiplicativity identity for a star-section character, and supplies substantial finite computational evidence for that identity. The final proof remains incomplete.

This is considerably stronger than where Draft 0 left us, but it is not yet a completed theorem.
1. Assessment of the main additions
Result	My assessment
Pro-\(3\) filtration and cube-map calculations (§7)	Promising; some arguments require fuller justification
Reduction to the Sylow \(3\)-subgroup (§8)	Substantial and potentially correct; minor gaps to repair
Construction of the \(72\) good elements in \(V\) (§7)	Main finite combinatorial data independently checked
Defect-function design (§9)	Important numerical identities independently confirmed
Explicit covering cocycle (§10)	Needs verification against [JC] and the supplied Python implementation
Multiplicativity hypothesis (H1) (§10)	Not proved; contains an incorrect intermediate assertion
Target A: irreducible character of dimension \(27\) (§11)	Conditional on H1 and the remaining finite-model checks
Level-zero extension of Target B (§11)	Conditional on Target A

2. An encouraging independent verification
I reconstructed the finite Fourier calculation using the coordinates and tables printed in Draft 1, without using Claude's Python modules.

For
\[
V=Q_3/Q_6\simeq\mathbb F_3^5,
\]

I confirmed that the displayed formula for the good set \(\overline G_3\) produces exactly 72 elements, organized into 36 antipodal lines.

I also checked the tabulated defect function \(e_*\) against all \(3^5=243\) linear functionals \(h\in V^\vee\).

The resulting distributions agree exactly with Draft 1:
Defect function	Distribution of \(N_e(h)\)
\(e=0\)	\(9^{80},12^{90},15^{72},36^1\)
\(e=e_*\)	\(11^{216},20^{27}\)
\(e=-e_*\)	\(11^{216},20^{27}\)

Here \(20^{27}\) means that exactly 27 linear functionals have \(N_e(h)=20\).

I additionally verified that the manuscript's list of those 27 functionals is correct, that \(e_*\) is invariant under the two stated \(D_8\) generators, and that their action has orbit sizes
\[
4,4,8,8,8,8,8,8,8,8.
\]

These are meaningful checks, not merely confirmation that the tables contain the expected number of entries.

They support the proposed finite design, although they do not yet verify the actual covering-group cocycle or the identification of the design with the genuine star-section defect.
3. A specific error in the proof of (H1)
The most urgent issue is Proposition prop:H1 in §10.

The manuscript writes an explicit cocycle
\[
\beta(X,X')=-h_E(r,t)-h_E(r,n)
\]

and attempts to prove that
\[
\boxed{\kappa(XX')=\kappa(X)+\kappa(X')+\beta(X,X')}
\tag{H1}
\]

for all \(X,X'\in K^6\).

In case (i), where \(v(t)>0\), the proof asserts that \(\beta(X,X')=0\). This assertion is not generally correct, even using the Hilbert-symbol table supplied in Draft 1.
A concrete example
Take
\[
X=1+\varpi^3j,\qquad
X'=1+\varpi^3+\varpi^4j,
\]

where \(\varpi=\zeta_3-1\). Both belong to \(K^6\).

In the notation of the manuscript,
\[
t=\varpi,\qquad
r=1+\varpi+\varpi^3,\qquad
n=1-\varpi^7.
\]

Using the cubic Hilbert-symbol values stated in Appendix A,
\[
h_E(r,\varpi)=1,\qquad h_E(r,n)=0,
\]

with exponents taken modulo 3. Thus
\[
\boxed{\beta(X,X')=2\ne0.}
\]

The claimed vanishing fails because the factor \(1+\varepsilon\) arising from \(r/(1+t)\) can have a nonzero level-three term; it need not lie in the deeper unit subgroup asserted in the proof.

Fortunately, this example is not a counterexample to (H1). Indeed, the same printed formulas give
\[
\kappa(X)=0,\qquad
\kappa(X')=1,\qquad
\kappa(XX')=0,
\]

so the required difference is \(0-0-1=2\), precisely matching \(\beta(X,X')\).

That is encouraging: the correction term appears to do exactly what it should. But the proof must retain and calculate it.
What this means
There are presently two distinct problems with Proposition (H1):
- The written proof of its supposedly established cases (i)–(iii) contains an incorrect calculation.
- Cases (iv)–(v) have been tested on 7,600 selected instances, not proved for all instances.
Consequently, the [Pᶜ] label is not adequate for Proposition (H1) as currently written. A finite exact computation can support a proof if it exhausts a rigorously defined finite reduction. Sampling—even with exact arithmetic—cannot establish an identity over an infinite \(p\)-adic group.

The appropriate next result to seek is a complete symbolic proof of (H1), or a rigorous finite-precision reduction followed by exhaustive enumeration of every remaining class.