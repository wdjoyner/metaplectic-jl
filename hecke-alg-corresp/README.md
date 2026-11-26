# hecke-alg-corresp

Two revisions of D. Joyner, *A correspondence for the generalized Hecke algebra of the metaplectic cover SL(2,F)-bar, F p-adic*, New York J. Math. **4** (1998), 223–235. Both start from the 1998 paper and are kept side by side.

## Summaries

**A correspondence for the generalized Hecke algebra of the metaplectic cover SL(2,F)-bar, F p-adic** (`hecke-alg-corresp-for-metapletic-SL2-revised.tex`; David Joyner; Draft 1 of the corrected and expanded version, November 2026). This revision stays close to the 1998 paper. Using a technique of Howe and Moy for GL(n), it proves a bijection between the generalized Hecke algebras of G = SL(2, F), F p-adic, and those of its n-fold metaplectic cover. The consequence is a canonical correspondence between irreducible admissible representations of G and genuine irreducible admissible representations of the cover of sufficiently large level (depending on n and p).

**On Hecke algebras of the p-adic metaplectic cover SL(2)-bar** (`hecke-algebras-SL2bar.tex`; David Joyner and Claude; Draft 14). A substantial rewrite that asks why a comparison of the cover with SL(2) fails at the level of Hecke algebras, and how far it is from being correct. The genuine representation theory of the cover is known to resemble that of PGL(2), not SL(2).

- For filtration subgroups B_k of an Iwahori subgroup that lift canonically to the cover, the relations among characteristic functions of double cosets transfer to genuine functions with suitable lifts. When p ∤ n, the part of the algebra supported on SL(2, 𝒪) transfers exactly; for n = 2 the remaining signs are computed.
- For every n ≥ 2, no algebra homomorphism sends each characteristic function to a unimodular multiple of the corresponding genuine function. The reason is that the cover does not split.
- For n ≥ 3 the obstruction is local: certain lifted torus elements commute only up to a Hilbert symbol, so no support-preserving homomorphism exists for any choice of constants, and the corresponding Hecke operators have trace zero in every admissible genuine representation.
- At Iwahori level the paper presents the genuine Iwahori–Hecke algebra and gives a direct proof of Savin's theorem for SL(2): the algebra is isomorphic to the Iwahori–Hecke algebra of SL(2) for odd n and of PGL(2) for even n. It computes the split orbital integrals of all basis functions and shows that Savin's isomorphism transfers them with an explicit transfer factor. The elliptic orbital integrals are computed on the linear side, and numerical values on the genuine side imply an elliptic transfer, of endoscopic shape for even n.

## Files

| File | What it is |
|---|---|
| `hecke-alg-corresp-for-metapletic-SL2_1998.pdf`, `hecke-alg-corresp-for-metapletic-SL2-1998-amsart.tex`, `howe6.tex` | The 1998 paper and its sources |
| `hecke-alg-corresp-for-metapletic-SL2-revised.tex`, `.pdf` | The close revision (Draft 1) |
| `hecke-alg-corresp-for-metapletic-SL2-revision-log.tex`, `.pdf` | Its revision log |
| `hecke-algebras-SL2bar.tex`, `.pdf` | The rewrite (Draft 14) |
| `hecke-algebras-SL2bar-revision-log.tex`, `.pdf` | Its revision log, with the corrections to the 1998 paper |
| `scripts/` | Exact-arithmetic checks over ℚ_p for the rewrite (see `scripts/README.md`) |

## Status

AI-assisted working drafts, not independently refereed. The AI contributions are described in each paper's Acknowledgments and revision log.
