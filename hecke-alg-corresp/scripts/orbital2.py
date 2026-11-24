"""Genuine/linear split orbital integrals at gamma~=(t0^m,1), Iwahori level, restricted to the
z-regions that can contribute (derived in the paper). F = |D|^{1/2} O. Output: zeta-exponent -> coeff."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import savin_check as S
from fractions import Fraction as Fr

def zs_ball(e):      # z in p^e O / pO
    P = S.P
    return [Fr(x) * Fr(P) ** e for x in range(P ** (1 - e))]

def zs_ann(j):       # ord z = j, mod pO
    P = S.P
    return [Fr(x) * Fr(P) ** j for x in range(P ** (1 - j)) if x % P]

def regions(lab, m):
    kind, i = lab
    R = []
    if kind == 't':
        if i == m: R.append(('one', zs_ball(-2 * m)))
        if i == -m:
            R.append(('s1', zs_ball(1 - 2 * m))); R.append(('lo', zs_ann(-2 * m)))
    else:
        if i <= -m - 1: R.append(('one', zs_ann(i - m)))
        if i >= m: R.append(('s1', zs_ann(-m - i)))
        if i == m: R.append(('lo', zs_ball(-2 * m)))
        if i > m: R.append(('lo', zs_ann(-m - i)))
    return R

def orbital(lab, m, full=False):
    P = S.P
    gam = (S.t0(m), 1)
    tally = {}
    regs = regions(lab, m)
    if full:
        Rr = 2 * m + abs(lab[1]) + 2
        regs = [('one', zs_ball(-Rr)), ('s1', zs_ball(-Rr)), ('lo', zs_ball(-Rr))]
    for kind, zs in regs:
        kaps = {'one': [S.ONE], 's1': [S.S1], 'lo': [S.lo(Fr(y)) for y in range(1, P)]}[kind]
        for kap in kaps:
            sk = S.s(kap); ski = S.cinv(sk)
            for z in zs:
                Y = S.cmul(S.cmul(S.cmul(ski, gam), (S.up(z), 1)), sk)
                v = S.fbar(lab, Y)
                if v:
                    tally[v] = tally.get(v, 0) + 1
    scale = Fr(1, P) * Fr(P) ** (-m)
    return {S.zeta_name(v): c * scale for v, c in tally.items()}

if __name__ == '__main__':
    p, n = int(sys.argv[1]), int(sys.argv[2])
    S.setup(p, n)
    m = int(sys.argv[3]); labs = eval(sys.argv[4]); full = len(sys.argv) > 5
    for lab in labs:
        r = orbital(lab, m, full)
        tot = sum(r.values())
        print(f"q={p} n={n} m={m} w={lab}: F =", {e: str(c) for e, c in sorted(r.items())}, flush=True)
