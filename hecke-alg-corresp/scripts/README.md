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

## Elliptic orbital integrals (Draft 11, Section 9.5)

- `elliptic.py p n L t`: counts edges D within gallery distance L of the standard edge, sorted by the relative
  position of D and gamma D, for gamma = [[0,-1],[1,t]]. Each count carries its root-of-unity phases. Use n=1 for
  SL(2).
- `elliptic2.py p n L t unit|t`: tau(1), tau(X), tau(Y) for gamma and for the other SL(2)-class gamma^h in its
  stable class. Use `unit` for ramified tori, where h=diag(u,1) with u a non-square unit. Use `t` for unramified
  tori, where h=[[0,-1],[p,0]].
  Example: `python3 elliptic2.py 3 2 6 5 unit` gives (1,3,-3) and (1,3,3).

## Structure constants N_k(x,z) (Draft 14, Section 6.4)

- `Ncheck.py p "[(labx,labz),...]"`: for each pair, prints N_k(x,z) for k=1,2,3. This is the coefficient of
  the double coset of xz in f_x*f_z at level k, counted as the number of cosets x'B_k in B_k x B_k with
  x'^{-1}xz in B_k z B_k. Labels are ('t',m) for t0^m and ('ts',m) for t0^m s1, so s1=('ts',0) and
  s2=('ts',-1).
  Example: `python3 Ncheck.py 3 "[(('ts',0),('ts',0)),(('t',1),('t',-1)),(('t',1),('ts',0))]"` gives
  [3,3,3], [9,9,9] and [1,1,1] (Remark 2026.4).
