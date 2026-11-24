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
