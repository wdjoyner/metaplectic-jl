"""Hyperbolic orbital integrals of Iwahori-level basis functions, linear (n=1) and genuine.
O_gamma(f) = |1-a^{-2}|^{-1} sum_{kappa in K/B} int_F f(s(kappa)^{-1} gamma~ u+(z)~ s(kappa)) dz,
Haar measure vol(B)=1, vol(T(O))=1. Prints F = |D|^{1/2} O as dict zeta-exponent -> coefficient."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import savin_check as S
from fractions import Fraction as Fr

def orbital(lab, m, u0=1, R=None):
    P = S.P
    a = Fr(P) ** m * u0
    gam = (S.hh(a), 1)
    if R is None:
        R = 2 * abs(m) + S.length(lab) + 3
    kappas = [S.lo(Fr(y)) for y in range(P)] + [S.S1]
    tally = {}
    for kap in kappas:
        sk = S.s(kap); ski = S.cinv(sk)
        # z in p^{-R} O / p O : z = x * p^{-R}, x in 0..p^{R+1}-1
        for x in range(P ** (R + 1)):
            z = Fr(x) / Fr(P) ** R
            Y = S.cmul(S.cmul(S.cmul(ski, gam), (S.up(z), 1)), sk)
            v = S.fbar(lab, Y)
            if v:
                tally[v] = tally.get(v, 0) + 1
    # each z-cell has measure q^{-1}; prefactor |1-a^{-2}|^{-1} = q^{-2|m|} ; |D|^{1/2} = q^{|m|}
    scale = Fr(1, P) * Fr(P) ** (-2 * abs(m)) * Fr(P) ** abs(m)
    return {S.zeta_name(v): c * scale for v, c in tally.items()}

if __name__ == '__main__':
    p, n = int(sys.argv[1]), int(sys.argv[2])
    S.setup(p, n)
    ms = eval(sys.argv[3]); labs = eval(sys.argv[4])
    for m in ms:
        for lab in labs:
            r = orbital(lab, m)
            print(f"q={p} n={n} m={m} w={lab}: F =", {e: str(c) for e, c in sorted(r.items())}, flush=True)
