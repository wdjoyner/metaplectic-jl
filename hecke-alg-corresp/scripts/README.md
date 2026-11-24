# Computer checks for the genuine Iwahori–Hecke algebra

These scripts check Proposition 9.7 and Remark 2026.5 of
`hecke-algebras-SL2bar.tex` (Draft 9) numerically. They work with the n-fold Kubota cover of SL(2,Q_p)
for p odd and n | p-1, using exact rational arithmetic and exact tame Hilbert symbols.

- `savin_check.py p n` checks the following:
  - Kubota's formula for the splitting of SL(2,Z_p) satisfies the cocycle identity on random elements.
  - Which double cosets B t0^m B and B t0^m s1 B are admissible, for |m| <= 3.
- `prod_check.py p n "('ts',m)" ...` expands the square of the genuine function on B t0^m s1 B in the
  basis of genuine double-coset functions.
  - Labels are `('t',m)` for t0^m and `('ts',m)` for t0^m s1.
  - Each coefficient is printed as counts of powers of a primitive n-th root of unity zeta.
  - Non-admissible supports are flagged. Their coefficients should be vanishing sums of roots of unity.

Example: `python3 prod_check.py 7 3 "('ts',-3)"` prints the relation Y^2 = 294 Y + 16807. It takes about 45 seconds.

## Orbital integrals (Draft 10, Section 9.4)

- `orbital.py p n "[m,...]" "[labels]"`: brute-force split orbital integrals |D|^{1/2} O at h(p^m) of
  Iwahori-level basis functions, using the reduction formula of Lemma 9.15. Use n=1 for SL(2) itself.
  This is slow for large m.
- `orbital2.py p n m "[labels]"`: the same, restricted to the regions that contribute (Proposition 9.16).
- `transfer_check.py p n k "[('t',j),('ts',j),...]"`: compares the genuine orbital integral at (t0^{n'k},1)
  with the orbital integral of its image under Savin's isomorphism at mu^k. The labels use j with w = t0^{n'j}
  or t0^{n'j} s1. It prints the ratio, which should be the constant Delta_k of Theorem 9.20.
  Example: `python3 transfer_check.py 3 2 1 "[('t',1),('ts',1),('ts',-3)]"` gives ratio -i each time.
