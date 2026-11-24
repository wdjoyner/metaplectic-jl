"""N_k(x,z) = coefficient of the double coset B_k xz B_k in f_x * f_z at level k (vol(B_k)=1),
i.e. #{cosets x'B_k in B_k x B_k : x'^{-1} x z in B_k z B_k}, for x,z in +-W_a."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import savin_check as S
from fractions import Fraction as Fr

def in_Bk(g, k):
    (a, b), (c, d) = g
    P = S.P
    def ok(e, v): return e == 0 or S.val(e) >= v
    return ok(a - 1, k) and ok(d - 1, k) and ok(b, k) and ok(c, k + 1)

def reps_k(lab, k):
    kind, m = lab
    P = S.P
    if kind == 't': i, j = 2 * m, 1 - 2 * m
    else: i, j = 1 + 2 * m, -2 * m
    # B_k = U+_k T_k U-_{k+1}; x B_k x^{-1} has U+_{k+i}, U-_{k+j}
    up = max(k, k + i); lo = max(k + 1, k + j)
    out = []
    for x in range(P ** (up - k)):
        for y in range(P ** (lo - k - 1)):
            out.append(S.mul(S.up(Fr(x) * Fr(P) ** k), S.lo(Fr(y) * Fr(P) ** (k + 1))))
    return out

def N(labx, labz, k):
    x = S.wlab_elem(labx); z = S.wlab_elem(labz)
    xz = S.mul(x, z)
    Rz = reps_k(labz, k)
    cnt = 0
    for b in reps_k(labx, k):
        xp = S.mul(b, x)
        y = S.mul(S.inv(xp), xz)       # need y in B_k z B_k = U_{b'} b' z B_k
        if any(in_Bk(S.mul(S.inv(S.mul(bp, z)), y), k) for bp in Rz):
            cnt += 1
    return cnt

if __name__ == '__main__':
    p = int(sys.argv[1]); S.setup(p, 1)
    pairs = eval(sys.argv[2])
    for labx, labz in pairs:
        print(labx, labz, [N(labx, labz, k) for k in (1, 2, 3)], flush=True)
