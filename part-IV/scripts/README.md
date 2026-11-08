# Verification scripts for the rank-two wild companion paper

Scripts for *Wild-place metaplectic character transfer in degree two* (`part-IV/mjl_rank2_wild_draftK.tex`),
current draft 7 (scripts tagged `draft7-scripts`). Pure Python 3; exact arithmetic throughout (`fractions.Fraction`, integers mod 3^k),
except where stated below. Tested with Python 3.12, numpy 2.5, sympy 1.14 (sympy is used only by
`step13_level2.py` for a rank computation; the integer solving is done by `zsolve.py`).

Run every script **from this directory** (`python3 stepN_....py`); the scripts import `quat.py`/`cover.py`
from `.` and read/write their data files here. A fresh checkout regenerates all data files: the three
committed pickles are byte-identical to what the scripts produce.

## Which statement in the paper uses which script

| Script | Produces | Used for | Status in the paper |
|---|---|---|---|
| `quat.py` | — | exact arithmetic in Z[i][varpi], O_D, coordinates on V | library |
| `cover.py` | — | exact Q(zeta_12) arithmetic, Hilbert-symbol classes, Kubota–KP cocycle, cover group law | library |
| `step1_G3.py` | `G3.pkl` | the 72 elements / 36 lines of G_3 in V (Prop. 8.2) | load-bearing [P^c] (also proved by hand) |
| `step2_finite.py` | `finite.pkl` | the group Q/Q_7, cube map, depths, Cubes(Q_2)=Q_6, Q_6-invariance of G_3 | load-bearing [P^c] (corroborates Lemma 8.1) |
| `step3_actions.py` | `actions.pkl` | actions of Ad(1+j), Ad(1+ij), Ad(1+i), Ad(j) on V; orbits; B=720 | load-bearing [P^c] |
| `step4_design.py`, `step6_orbit.py` | `design.pkl`, `design_0011020002.pkl`, `design_0022010001.pkl` | the design search, Heisenberg cocycle extension, Lambda, Fourier identities (Prop. 10.5) | load-bearing [P^c] |
| `step7_symbols.py` | `symbols.pkl` | cubic Hilbert symbols of F and E_0 from the Steinberg relations; cocycle checks | load-bearing [P^c] (symbol tables, App. A) |
| `step5_H1.py` | — | Lazard form on K^4/K^8; equivariant defects on Q_6/Q_8 | corroboration |
| `step8_H1test.py`, `step8b.py`, `step9_H1_stratified.py` | — | (H1) through cube roots and on a stratified sample | corroboration (Prop. 11.4 is proved by hand) |
| `step10_defects.py` | — | defects of 3- and 4-term relations; omega = 0; kappa_{1,5} | corroboration |
| `step11_endtoend.py`, `step11b.py` | — | character of Ind lambda_0 against L_D 1 | corroboration |
| `step12_H1_proof_check.py` | — | referee's example; closed form of kappa; symbol facts; the (H1) identity on 12,000 structured instances | corroboration |
| `step13_level2.py`, `zsolve.py` | — | group H = Q_3/Q_7, character table (Burnside, then exact verification), Ad(Q_1)-orbits, good classes, cube root; the criterion of Prop. 13.4 by exact integer linear algebra | corroboration (Thm. 13.8 is proved by hand since Draft 6) |
| `step14_level2_restriction.py` | — | decomposition of (chi o r)·D into irreducibles of H (eq. (chi3D)) | corroboration |
| `step15_level2_clifford.py` | `level2_orbit_certificate.txt` | lambda_0 on H^ (certified as a character on all generator x element pairs), twisted Ad(Q_1)-action on genuine characters, stabilizer test, orbit table, Heis multiplication table | corroboration of Prop. 13.9 (certificate) |
| `verify_certificate.py` | — | independent check of the certificate without the cover: Heis table is a group, the action tables define an action, no fixed points, orbits as listed | verifier |
| `dump_appendix.py` | — | prints the tables of Appendix A | utility |

Load-bearing means: listed in Remark 12.2 (dependencies of Target A) as an exhaustive finite computation
on which a [P^c] statement rests. Everything else is corroboration of a statement proved by hand.

## Dependencies between scripts (data files)

```
step7_symbols.py  -> symbols.pkl   (needed by cover-based scripts: 8, 9, 10, 11, 12, 15)
step1_G3.py       -> G3.pkl        (needed by 3, 6, 10, 11b)
step2_finite.py   -> finite.pkl    (needed by 13, 14, 15)
step3_actions.py  -> actions.pkl   (needed by 4, 5, 6, 10)
step4_design.py   -> design.pkl    (needed by 6)
step6_orbit.py    -> design_0011020002.pkl, design_0022010001.pkl   (needed by 10, 11, 14, 15)
step13_level2.py  -> H_multtable.npy (cache, ~50 s to rebuild; not committed)
```
`step14` and `step15` re-execute the setup part of `step13` (so they need `finite.pkl` and, for 15,
`symbols.pkl` and `design_0011020002.pkl`). Committed data files: `symbols.pkl`, `finite.pkl`,
`design_0011020002.pkl`, so that 12–15 run without regenerating the design layer.

## Suggested order for an independent check

```
python3 step7_symbols.py          # ~10 s   symbols; cocycle identity; torus commutator vs Part I
python3 step12_H1_proof_check.py  # ~1 min  (H1): referee's example, closed form of kappa, identity
python3 step1_G3.py; python3 step2_finite.py; python3 step3_actions.py   # ~2 min  design layer
python3 step4_design.py; python3 step6_orbit.py                          # ~1 min
python3 step13_level2.py          # ~1 min  (+50 s first time)  level two: criterion fails for chi_3+chi_3'
python3 step14_level2_restriction.py  # ~1 min  (chi o r)D = sum of the 54 degree-3 characters
python3 step15_level2_clifford.py     # ~10 min freeness certificate -> level2_orbit_certificate.txt
python3 verify_certificate.py         # ~5 s    independent check of the certificate
```

## Deterministic certification (Draft 7)

`step13` certifies the group law of H by checking associativity on all 729^3 triples (vectorized), identity and
inverses, and certifies the character table exactly: every rounded row is a common eigenvector of all 297
class-sum matrices (computed in Z[zeta_3] with integer arithmetic) and has norm |H|, which characterizes the
irreducible characters. `step15` certifies that lambda_0 is a character of H^ on all (generator, element)
pairs. `verify_certificate.py` re-reads `level2_orbit_certificate.txt` and checks it independently.
There are no sampled checks left in scripts 13-15.

## Numerical steps

Only two places use floating point: `step11*` to display complex character values, and `step13`/`step14`
to find the character table of Q_3/Q_7 by Burnside's algorithm (numpy eigenvectors). In the latter the
values are rounded to Z[zeta_3] (maximal rounding error about 2e-13) and all orthogonality relations
are then re-verified exactly; this is numerical discovery followed by exact verification, and since
Draft 6 these two scripts are corroboration only.

## The certificate `level2_orbit_certificate.txt`

For Proposition 13.9 (freeness) / Step 3 of Theorem 13.8: the 27 coset representatives t_k of U_1/U_3
(listed with their Heisenberg classes), the full action table mu -> mu^{t_k} on the 54 genuine
degree-3 characters and on the 243 genuine linear characters of H^ (central character zeta on mu_3,
theta_0 = 1), the count of fixed pairs (mu, t != 1) — zero in both cases — the orbit lists
(2 x 27 and 9 x 27), and the values of the 54 degree-3 characters on the class representatives.
