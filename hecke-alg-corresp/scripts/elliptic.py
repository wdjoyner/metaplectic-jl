"""Elliptic orbital integrals at Iwahori level by counting edges of the Bruhat-Tits tree.
O_gamma(fbar_{(w,1)}) = sum over edges D=xB (vol(T_gamma)=1) of fbar_{(w,1)}(x~^{-1} gamma~ x~),
for the edges D within gallery distance L of the standard edge. Linear case: n=1."""
import sys, os, itertools
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import savin_check as S
from fractions import Fraction as Fr

def all_labels(L):
    out = []
    for m in range(-L, L + 1):
        for kind in ('t', 'ts'):
            if S.length((kind, m)) <= L: out.append((kind, m))
    return out

def edges(L):
    """coset representatives x of G/B with gallery distance <= L from the standard edge"""
    for lab in all_labels(L):
        w = S.wlab_elem(lab)
        for v in S.reps(lab):
            yield lab, S.mul(v, w)

ADM = {}
def elliptic_orbital(gamma, L):
    gt = (gamma, 1)
    res = {}
    for lab0, x in edges(L):
        xt = (x, 1); xi = S.cinv(xt)
        Y = S.cmul(S.cmul(xi, gt), xt)
        b1, w, b2, lab = S.iwahori_decomp(Y[0])
        if lab not in ADM: ADM[lab] = S.admissible(lab, 20)
        val = S.fbar(lab, Y) if ADM[lab] else None
        d = res.setdefault(lab, {})
        key = 'NA' if val is None else S.zeta_name(val)
        d[key] = d.get(key, 0) + 1
    return res

if __name__ == '__main__':
    p, n, L = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3])
    t = Fr(eval(sys.argv[4]))
    S.setup(p, n)
    gamma = S.M(0, -1, 1, t)
    res = elliptic_orbital(gamma, L)
    for lab in sorted(res, key=lambda l: (S.length(l), l)):
        print(f"  w={lab} len={S.length(lab)}: {res[lab]}")
