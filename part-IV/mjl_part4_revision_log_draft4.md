# Part IV — Draft 4 revision log

**Date:** November 7, 2026  
**Revised manuscript:** `mjl_part4_draft4.tex`  
**Base:** attached `mjl_part4_draft3(2).tex`  
**Review incorporated:** attached `mjl_part4_draft3_referee_report_claude(2).tex`, plus independent check of the rank-two split-place case and the central-germ issue.  
**Scope:** Part IV alone. This revision makes no changes to Parts I–III.

## Main mathematical changes

1. **Conditional global comparison (Section 8; Proposition 8.3).** Replaced the former conclusion of equality subject to a product-normalization hypothesis by the more informative and formally stronger conditional identity
   
   \[
     I_{\widetilde H}(\widetilde f)=\Lambda I_H(f),\qquad
     \Lambda=\Bigl(\prod_{v\notin S}\lambda_v\Bigr)
             \Bigl(\prod_{v\in S}b_{D,v}\Bigr).
   \]
   
   Equality is the special case \(\Lambda=1\). Uniformity in the rational class and torus type is explicit. Rescaling can enforce \(\Lambda=1\) once matching functions exist, but cannot preserve a prescribed canonical spherical normalization.

2. **Additional nongood-rational-class hypothesis.** The ordinary geometric expansion can contain nongood rational classes absent from the genuine expansion; matching globally good summands alone does not imply equality of the complete expansions. The new proposition explicitly assumes these ordinary nongood contributions vanish on the selected support, in addition to suppressing the central identity term. This is a genuinely necessary extra assumption, not a theorem supplied by local FK-compatibility.

3. **Rational-lift and measure audit.** Added the identity \(\iota(s^n)=\iota(s)^n\) and explained why the local rational lift agrees with the star lift. Required corresponding quotient Haar, torus, normalizer, and central-phase conventions in the proposition. Replaced the inference “homeomorphic adelic quotients have equal volumes” by the correct statement that equality of volumes requires compatible measures. Preserved the trace-class and convergence qualifications rather than asserting unconditional absolute convergence for arbitrary functions.

4. **Nonscalar root-fibre invariance (Definition 8.1 and Lemma 8.2).** Distinguished the automatic scalar \(\mu_n\)-invariance from the substantive action of the nonscalar kernel \(\mu_n(E_v)/\mu_n(F)\simeq \mu_n^{k_v}/\mu_n\). Removed the redundant standalone assumption about central translates by working with a scalar-stable region and reciprocal central-character laws.

5. **Rank-two tame spherical place (new proposition and remark in Section 8).** Verified, for \(r=2\), \(p\nmid n\), the elementary normalized split-torus identity \(J(\operatorname{diag}(a,b),1_{K_0})=1\) for unit eigenvalues with compatible measures, hence ordinary root-fibre invariance. For quadratic field tori the quotient-torus root kernel is trivial. Cited Flicker–Kazhdan, Sections 11–12, for unramified spherical-unit matching under its published hypotheses and normalizations; for rank two, \(N_2=1\). Transport of the theorem to the *particular* ambient cover, compact splitting, central-character extension, and Haar measures used in Parts I–IV is **not** asserted without additional verification. The same FK theorem covers mixed tori in higher ranks when its stated hypotheses hold.

6. **Central identity term and Shalika germs (new subsection in Section 8).** Distinguished the valid discriminant ratio limit \(\Delta(x)/\Delta(x^n)\to |n|_v^{-r(r-1)/2}\) from the generally **invalid** inference that a split-group orbital-integral limit gives a test function's value at the identity. Shalika germs intervene. Thus the split-place identity-value formula is now an *explicit additional hypothesis* for the product-formula consistency check, not a proved lemma. Recorded the Part III division-place factor \(c_{D,v}=b_{D,v}|n|_v^{-r(r-1)/2}\) and the formal consequence \(\prod_v \widetilde f_v(1)/f_v(1)=\Lambda\) if the complementary split identities are independently verified. This does not match global identity coefficients without a matched quotient volume and a valid trace-formula test range.

7. **Concrete \(K=\mathbb Q(\zeta_3)\) example (Section 8).** For \(r=2,n=3\), a quaternion algebra ramified at the place above 3 and one further finite place yields \(b_{D,v}=3,c_{D,v}=27\) at the wild place. If all finite split constants equal 1 and \(\Lambda=1\), the unique complex-place constant would have to be \(1/3\), and its *hypothetical* identity-value factor \(1/27\). Marked this as a consistency constraint, not a constructed archimedean transfer.

8. **Other mathematical refinements.** Replaced the misleading sign argument for Zou's odd-\(n\) correction \(u(x)\) with the original odd-cover star convention. Extended the root-collision/germ warning to complex places. Distinguished suppression of the central identity class from the treatment of other hypothetical “singular” classes: for prime-degree division algebras, noncentral rational elements are regular elliptic.

## Editorial, cross-reference, and bibliography changes

- Set title to **Part IV, Draft 4**; preserved the Part IV subtitle and author order: David Joyner; ChatGPT (OpenAI); Claude (Anthropic).
- Updated Parts I and II bibliography entries from **Draft 7** to **Draft 8** and retained Part III at **Draft 9**, consistent with the most recent draft history supplied in the earlier series work. These draft numbers are also mentioned in the introduction. **Version-identification caveat:** the source files for Parts I and II Draft 8 were not available in this working directory for line-by-line verification of internal proposition numbering; their *numbers and titles* are taken from the completed-draft history. The Part III Draft 9 source was discoverable and its status terminology and central identity-factor citation were checked.
- Replaced the unverified “Part I Proposition 2.3 and its archimedean remark” reference for complex splitting by **Part I Appendix B, item (R4)**, as indicated by the earlier series revision record. This appendix location should be checked when Part I Draft 8 is next available.
- Removed undefined \(I_F\) in the wild example, explicitly writing \([E^\times:F^\times E^{\times3}]=9\).
- Dropped “new” from the local power-map section heading and eliminated the repeated display of the global torus coefficient \(c(\gamma)\).
- Clarified the established/proved/outlined/conjectural status table; identified FK unramified matching separately from the still-open exceptional-place and ambient-cover normalization tasks.
- Updated abstract, conclusion-oriented research agenda, and acknowledgments to include Claude's Draft 3 report and the conditional split-place result.

## Still open; not claimed in Draft 4

- Integrality of \(L_D\) on irreducible characters at places \(p\mid n\), including the model \((r,n,F)=(2,3,\mathbb Q_3(\zeta_3))\).
- Explicit exceptional split-place matching functions, including the complex places, with a *uniform* class-independent multiplier and all star, central, and Haar identifications.
- An unconditional global \(D^\times\)-to-cover trace comparison with canonical local normalizations, including treatment or elimination of nongood rational summands and any nonzero identity term.
- Removing the spectral/packet restrictions from Parts I–II.

## Build verification

- `pdflatex` via `latexmk -pdf -interaction=nonstopmode -halt-on-error -file-line-error`: **success**, 18 pages.
- No TeX errors or unresolved references were reported in the final build log.
- All pages were rendered for visual layout review. The final archive contains the editable source, compiled PDF, and this log.

**External source checked:** Y. Flicker and D. Kazhdan, *Metaplectic correspondence*, Publ. Math. IHÉS **64** (1986), §§11–12 (especially the unit-element corollary), https://www.numdam.org/articles/10.1007/BF02699192/.
