"""End-to-end check: Theta(Ind_{U3~}^{U1~} lambda_0)(x) == Phi(x) at sample points of U1~,
   with lambda_0(y) = (prod_{d in D8} d y d^{-1})^{-1} evaluated through psi_6."""
import sys; sys.path.insert(0, '.')
from cover import *
import quat as Q
import random, time, pickle, collections, cmath
import numpy as np

S = pickle.load(open('./symbols.pkl', 'rb'))
sym = Symbols(S['AE'], S['AF'])
cov = Cover(sym, cv=2, relabel=False)
VARPI3 = e_pow(EW, 3); ONE_P_W3 = e_add(E1, VARPI3)

def digit6(X):
    x = e_sub(X[0], E1)
    for _ in range(3): x = e_div_varpi(x)
    return e_red(x)
def kappa(X):
    c = digit6(X)[0]
    if c == 0 or e_zero(X[1]): return 0
    return sym.hE(e_pow(ONE_P_W3, c), X[1])
def split_scalar(P):
    """P in U_F^{(1)} K^6 (projection of an element of U6~): return (z, X) with P = z X, z in O_F, X in K^6"""
    a, b = P[0]
    z = ((a[0], Fr(0)), (b[0], Fr(0)))
    X = d_mul(d_inv((z, E0)), P)
    return z, X
def psi6(A):
    P, E = A
    z, X = split_scalar(P)
    assert d_val(d_sub(X, D1)) >= 6, d_val(d_sub(X, D1))
    return (E - cov.betaD((z, E0), X) - kappa(X)) % 3
def cmul(A, B): return cov.mul(A, B)
def cinv(A):
    X, e = A; Xi = d_inv(X)
    return (Xi, (-e - cov.betaD(X, Xi)) % 3)
def conj(A, B):  # A B A^{-1}
    return cmul(cmul(A, B), cinv(A))

# D8 lifts: (1+i)^k j^l
XI = d_add(D1, DI)
D8_lifts = []
for l in range(2):
    for k in range(4):
        g = D1
        for _ in range(k): g = d_mul(g, XI)
        if l: g = d_mul(g, DJ)
        D8_lifts.append((g, 0))
assert len(D8_lifts) == 8

def lambda0(y):
    """y in U3~ ; returns exponent of lambda_0(y) in F_3"""
    N = (D1, 0)
    for d in D8_lifts:
        N = cmul(N, conj(d, y))
    return (-psi6(N)) % 3

# coset representatives of U1~/U3~ : t = 1 + a j + b varpi, a in F_9, b in {0, i, 2i}
reps = []
for a0 in range(3):
    for a1 in range(3):
        for b1 in range(3):
            t = d_add(D1, (e_mul(EW, (gq(0, b1), gq())), (gq(a0, a1), gq())))
            reps.append((t, 0))
assert len(reps) == 27

def induced_char(x):
    """character of Ind lambda_0 at x in U3~ (exponent sum as complex number)"""
    z3 = cmath.exp(2j*cmath.pi/3)
    tot = 0
    for s in reps:
        y = conj(cinv(s), x)          # s^{-1} x s
        tot += z3**lambda0(y)
    return tot

def Phi(x):
    """Phi = L_D 1 on U1~: 27 zeta^{e-ell} on star lifts over Q_6, 9 zeta^{e-ell} on star lifts over G_3, 0 else.
       Uses: for X a cube of a depth-1 element, sigma(X) = (X,0); for X in U_F K^6, ell = (z,0)(X', kappa(X'))."""
    X, e = x
    z3 = cmath.exp(2j*cmath.pi/3)
    v = d_val(d_sub(X, D1))
    # try to see X as scalar * K^6 element
    a, b = X[0]
    zs = ((a[0], Fr(0)), (b[0], Fr(0)))
    Xp = d_mul(d_inv((zs, E0)), X)
    if d_val(d_sub(Xp, D1)) >= 6:
        return 27 * z3**((e - cov.betaD((zs, E0), Xp) - kappa(Xp)) % 3)
    return None   # handled by the caller (depth-3 cube or non-good)

rng = random.Random(77)
t0 = time.time()
print("--- star lifts of cubes of depth-1 elements (Phi = 9) ---")
for trial in range(6):
    while True:
        t = d_add(D1, (e_mul(EW, (gq(rng.randint(-2,2), rng.randint(-2,2)), gq(rng.randint(-2,2), rng.randint(-2,2)))),
                       (gq(rng.randint(-2,2), rng.randint(-2,2)), gq(rng.randint(-2,2), rng.randint(-2,2)))))
        if d_val(d_sub(t, D1)) == 1: break
    g = d_pow(t, 3)
    x = cov.power((t, 0), 3)          # = (g, 0)
    val = induced_char(x)
    print("  Theta_Ind(sigma(g)) =", round(val.real, 6), round(val.imag, 6), "  expected 9;   at zeta*sigma(g):", round((induced_char((g, 1))/cmath.exp(2j*cmath.pi/3)).real, 6))
print("--- elements of U6~ (Phi = 27 psi_6) ---")
for trial in range(4):
    X = d_add(D1, (e_mul(VARPI3, (gq(rng.randint(-2,2), rng.randint(-2,2)), gq(rng.randint(-2,2), rng.randint(-2,2)))),
                   e_mul(VARPI3, (gq(rng.randint(-2,2), rng.randint(-2,2)), gq(rng.randint(-2,2), rng.randint(-2,2))))))
    e = rng.randint(0, 2)
    val = induced_char((X, e)); ph = Phi((X, e))
    print("  Theta_Ind =", round(val.real, 6), round(val.imag, 6), "  Phi =", round(ph.real, 6), round(ph.imag, 6))
print("--- non-good elements of depth 3 and depth 4, 5 (Phi = 0) ---")
cnt = 0
for trial in range(8):
    k = rng.choice([3, 3, 3, 4, 5])
    # element of exact depth k not a cube: random; check it is not a star lift over G_3 by testing depth/cube status roughly
    if k == 3:
        X = d_add(D1, (e_mul(e_mul(EW, EW), (gq(rng.randint(-2,2), rng.randint(-2,2)), gq())), e_mul(EW, (gq(rng.randint(-2,2), rng.randint(-2,2)), gq(rng.randint(-2,2), rng.randint(-2,2))))))
    elif k == 4:
        X = d_add(D1, (e_mul(e_mul(EW, EW), (gq(rng.randint(-2,2), rng.randint(1,2)), gq())), e_mul(e_mul(EW, EW), (gq(rng.randint(-2,2), rng.randint(-2,2)), gq()))))
    else:
        X = d_add(D1, (e_mul(VARPI3, (gq(rng.randint(-2,2), rng.randint(-2,2)), gq())), e_mul(e_mul(EW, EW), (gq(rng.randint(-2,2), rng.randint(-2,2)), gq(1, 0)))))
    if d_val(d_sub(X, D1)) != k: continue
    # is X (mod U_F K^6) in the image of cubing? use the integer finite model: coordinates in V and membership in G3 (depth 3 only)
    val = induced_char((X, 0))
    print("  depth", k, " Theta_Ind =", round(val.real, 6), round(val.imag, 6))
    cnt += 1
print("elapsed %.0fs" % (time.time() - t0))
