"""Direct test of (H1): the star section ell(X) = (cube root)~^3 on K^6 is multiplicative.
   Also: independent check of the defect function e on good depth-3 elements."""
import sys; sys.path.insert(0, '.')
from cover import *
import random, time, pickle
import numpy as np
from fractions import Fraction as Fr

S = pickle.load(open('./symbols.pkl', 'rb'))
sym = Symbols(S['AE'], S['AF'])
cov = Cover(sym, cv=2, relabel=False)   # (H1) is invariant under relabeling
NPREC = 14

def reduce_fr(x, N=NPREC):
    """3-adic truncation of a Fraction keeping value mod 3^N (denominator a power of 3 allowed)"""
    p, q = x.numerator, x.denominator; k = 0
    while q % 3 == 0: q //= 3; k += 1
    m = 3**(N + k)
    p = (p * pow(q, -1, m)) % m
    return Fr(p, 3**k)
def reduce_g(a, N=NPREC): return (reduce_fr(a[0], N), reduce_fr(a[1], N))
def reduce_e(x, N=NPREC): return (reduce_g(x[0], N), reduce_g(x[1], N))
def reduce_d(X, N=NPREC): return (reduce_e(X[0], N), reduce_e(X[1], N))

def W3(): return e_pow(EW, 3)
VARPI3 = W3(); VARPI3_INV = e_inv(VARPI3)

def rand_K2(rng):
    """random element of K^2 = 1 + varpi O_D with small coordinates"""
    x1 = (gq(rng.randint(-2, 2), rng.randint(-2, 2)), gq(rng.randint(-2, 2), rng.randint(-2, 2)))
    y1 = (gq(rng.randint(-2, 2), rng.randint(-2, 2)), gq(rng.randint(-2, 2), rng.randint(-2, 2)))
    X = (e_mul(EW, x1), e_mul(EW, y1))
    return d_add(D1, X)
def rand_K1_depth1(rng):
    while True:
        x1 = (gq(rng.randint(-2, 2), rng.randint(-2, 2)), gq(rng.randint(-2, 2), rng.randint(-2, 2)))
        y = (gq(rng.randint(-2, 2), rng.randint(-2, 2)), gq(rng.randint(-2, 2), rng.randint(-2, 2)))
        X = (e_mul(EW, x1), y)
        if d_val(X) == 1: return d_add(D1, X)

def cube_exp(w):
    """exponent e(w) of (w,0)^3 = (w^3, e(w))"""
    return cov.power((w, 0), 3)[1]

# ----- level-6 digit (real part) and scalar normalization -----
def level6_digit(X):
    """X in K^6: digit in F_9 of (X-1)/varpi^3 (the E_0-component)"""
    Y = d_sub(X, D1)
    assert d_val(Y) >= 6
    x = Y[0]
    for _ in range(3): x = e_div_varpi(x)
    return e_red(x)

def cube_root_K2(Xp, N=NPREC):
    """Xp in Cubes(K^2): return v in K^2 (3-adic approx mod 3^N) with v^3 = Xp, via Hensel in F(Xp)."""
    Yd = d_sub(Xp, D1)                     # Y = Xp - 1 in P^6
    Yp = d_scal(VARPI3_INV, Yd)            # Y' = Y / varpi^3 (scalar multiplication, exact)
    assert d_val(Yp) >= 0
    T = d_trd(Yp); Nn = d_nrd(Yp)          # in F
    # field F(Y') with basis 1, Y' : (a,b) <-> a + b Y',  Y'^2 = T Y' - N
    def fmul(p, q):
        a, b = p; c, d = q
        bd = e_mul(b, d)
        return (e_sub(e_mul(a, c), e_mul(bd, Nn)), e_add(e_add(e_mul(a, d), e_mul(b, c)), e_mul(bd, T)))
    def fadd(p, q): return (e_add(p[0], q[0]), e_add(p[1], q[1]))
    def fsub(p, q): return (e_sub(p[0], q[0]), e_sub(p[1], q[1]))
    def fscal(c, p): return (e_mul(c, p[0]), e_mul(c, p[1]))
    def finv(p):
        a, b = p
        nrm = e_add(e_add(e_mul(a, a), e_mul(e_mul(a, b), T)), e_mul(e_mul(b, b), Nn))
        ninv = e_inv(nrm)
        return (e_mul(e_add(a, e_mul(b, T)), ninv), e_mul(e_neg(b), ninv))
    def fred(p): return (reduce_e(p[0], N), reduce_e(p[1], N))
    one = (E1, E0); zero = (E0, E0)
    Yf = (E0, E1)                           # Y' itself
    zi = ZETAINV; ziw = e_mul(ZETAINV, EW)
    def g(W):
        W2 = fmul(W, W); W3_ = fmul(W2, W)
        return fsub(fsub(fsub(W3_, fscal(zi, W)), fscal(ziw, W2)), Yf)
    def gp(W):
        W2 = fmul(W, W)
        return fsub(fsub(fscal(THREE, W2), (zi, E0)), fscal(e_mul(e_int(2), ziw), W))
    W = Yf
    for it in range(7):
        W = fred(fsub(W, fmul(g(W), finv(gp(W)))))
    # v = 1 + varpi W  as an element of D
    a, b = W
    Vd = d_add(D1, d_scal(EW, d_add((a, E0), d_scal(b, Yp))))
    return reduce_d(Vd, N)

def ell_exp(X, N=NPREC):
    """exponent e with ell(X) = (X, e) for X in K^6; theta_0 = 1 normalization (scalar lift (z,0))."""
    dig = level6_digit(X)
    c = dig[0]                             # real part in F_3
    z = e_pow(e_add(E1, VARPI3), c)        # z = (1+varpi^3)^c in U_F^{(3)}
    Xp = d_mul(d_inv((z, E0)), X)          # X' = X / z  (scalar)
    assert level6_digit(Xp)[0] == 0
    v = cube_root_K2(Xp, N)
    # check v^3 == Xp to precision
    v3 = d_pow(v, 3)
    err = d_sub(v3, Xp)
    ev = cube_exp(v)                       # (v,0)^3 = (v^3, ev)
    # ell(X) = (z,0)*(v^3, ev) = (z v^3, ev + beta(z, v^3))
    e_total = (ev + cov.betaD((z, E0), v3)) % 3
    return e_total, d_val(err) if not (e_zero(err[0]) and e_zero(err[1])) else 10**9

rng = random.Random(2026)
t0 = time.time()
# ---------- (H1) test ----------
fails = 0; tested = 0; minerr = 10**9
for trial in range(60):
    w = rand_K2(rng); wp = rand_K2(rng)
    X = d_mul(d_pow(w, 3), d_pow(wp, 3))
    e_prod = (cube_exp(w) + cube_exp(wp) + cov.betaD(d_pow(w, 3), d_pow(wp, 3))) % 3
    e_ell, errv = ell_exp(X)
    minerr = min(minerr, errv)
    tested += 1
    if e_prod != e_ell: fails += 1
    if trial % 10 == 0: print("  trial", trial, "e_prod", e_prod, "e_ell", e_ell, "cube-root residual valuation", errv, "(%.0fs)" % (time.time()-t0))
print("(H1) test: failures", fails, "/", tested, "; minimal cube-root residual v_D =", minerr)

# precision stability check on a few
for trial in range(5):
    w = rand_K2(rng); wp = rand_K2(rng)
    X = d_mul(d_pow(w, 3), d_pow(wp, 3))
    e1, _ = ell_exp(X, N=10); e2, _ = ell_exp(X, N=18)
    print("  precision check N=10 vs N=18:", e1, e2)

# ---------- also test multiplicativity ell(X) ell(X') = ell(XX') for X in K^6, X' in K^8 (W8) and random K^6 pairs ----------
fails = 0
for trial in range(20):
    w = rand_K2(rng); X = d_pow(w, 3)
    u = d_add(D1, d_scal(e_pow(EW, 2), d_sub(rand_K2(rng), D1)))    # element of K^6-ish (1 + varpi^3 * stuff)
    u = d_add(D1, d_scal(e_pow(EW, 3), d_sub(rand_K1_depth1(rng), D1)))   # 1 + varpi^3 P = K^7-ish
    eX, _ = ell_exp(X); eU, _ = ell_exp(u); eXU, _ = ell_exp(d_mul(X, u))
    if (eX + eU + cov.betaD(X, u) - eXU) % 3 != 0: fails += 1
print("multiplicativity ell(X)ell(u)=ell(Xu) with u in K^7: failures", fails, "/20")
