"""tau(1), tau(X), tau(Y) for elliptic orbital integrals (vol T_gamma = 1), genuine and linear,
for both SL2-classes in the stable class of gamma=[[0,-1],[1,t]] (second class: conjugate by g2)."""
import sys, os, math, cmath
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import savin_check as S
import elliptic as E
from fractions import Fraction as Fr

def taus(gamma, L, npr):
    r_lab = ('ts', -npr)
    targets = {('t', 0): 'one', ('ts', 0): 'X', r_lab: 'Y'}
    out = {'one': 0, 'X': 0, 'Y': 0}
    lin = {'one': 0, 'X': 0, 'Y': 0}
    z = cmath.exp(2j * cmath.pi / S.N)
    gt = (gamma, 1)
    for lab0, x in E.edges(L):
        xt = (x, 1)
        Y = S.cmul(S.cmul(S.cinv(xt), gt), xt)
        _, _, _, lab = S.iwahori_decomp(Y[0])
        if lab in targets:
            v = S.fbar(lab, Y)
            out[targets[lab]] += z ** S.zeta_name(v)
            lin[targets[lab]] += 1
    return out, lin

if __name__ == '__main__':
    p, n, L = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3])
    t = Fr(eval(sys.argv[4])); kind2 = sys.argv[5]
    S.setup(p, n); npr = n // math.gcd(n, 2)
    g = S.M(0, -1, 1, t)
    if kind2 == 'unit':
        u = next(x for x in range(2, p) if pow(x, (p - 1) // 2, p) == p - 1)
        h = S.M(u, 0, 0, 1)
    else:
        h = S.M(0, -1, p, 0)
    hi = ((h[1][1] / (h[0][0]*h[1][1]-h[0][1]*h[1][0]), -h[0][1] / (h[0][0]*h[1][1]-h[0][1]*h[1][0])),
          (-h[1][0] / (h[0][0]*h[1][1]-h[0][1]*h[1][0]), h[0][0] / (h[0][0]*h[1][1]-h[0][1]*h[1][0])))
    g2 = S.mul(S.mul(hi, g), h)
    for name, gg in (('class1', g), ('class2', g2)):
        tau, lin = taus(gg, L, npr)
        f = lambda c: complex(round(c.real, 6), round(c.imag, 6))
        print(f"q={p} n={n} t={t} {name}: genuine tau(1),tau(X),tau(Y) = {f(tau['one'])}, {f(tau['X'])}, {f(tau['Y'])}; linear counts = {lin['one']}, {lin['X']}, {lin['Y']}", flush=True)
