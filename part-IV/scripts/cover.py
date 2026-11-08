"""
Exact arithmetic in Q(zeta_12) = Q(i)(varpi), varpi^2 = -3 - 3 varpi, with Fractions;
the quaternion algebra D = E_0 + E_0 j (j^2 = varpi, j x = sigma(x) j), E_0 = Q_3(zeta_3)(i);
cubic Hilbert symbols of F = Q_3(zeta_3) and E_0 via the Steinberg relations (Moore's theorem);
the Kazhdan--Patterson cocycle on GL_2(E_0) and its restriction to D^x.
"""
from fractions import Fraction as Fr
import random, itertools
import numpy as np

# ---------------- Q(i) ----------------
def gq(a=0, b=0): return (Fr(a), Fr(b))
def g_add(a, b): return (a[0]+b[0], a[1]+b[1])
def g_sub(a, b): return (a[0]-b[0], a[1]-b[1])
def g_mul(a, b): return (a[0]*b[0]-a[1]*b[1], a[0]*b[1]+a[1]*b[0])
def g_neg(a): return (-a[0], -a[1])
def g_conj(a): return (a[0], -a[1])
def g_scal(k, a): return (k*a[0], k*a[1])
def g_zero(a): return a[0] == 0 and a[1] == 0
def g_inv(a):
    n = a[0]*a[0] + a[1]*a[1]
    return (a[0]/n, -a[1]/n)
def v3_frac(x):
    if x == 0: return 10**9
    n, d = x.numerator, x.denominator; v = 0
    while n % 3 == 0: n //= 3; v += 1
    while d % 3 == 0: d //= 3; v -= 1
    return v
def g_v3(a):
    return min(v3_frac(a[0]), v3_frac(a[1]))

# ---------------- O_{E_0} / E_0 : a + b varpi ----------------
def e_add(x, y): return (g_add(x[0], y[0]), g_add(x[1], y[1]))
def e_sub(x, y): return (g_sub(x[0], y[0]), g_sub(x[1], y[1]))
def e_neg(x): return (g_neg(x[0]), g_neg(x[1]))
def e_mul(x, y):
    a, b = x; c, d = y
    ac = g_mul(a, c); bd = g_mul(b, d); ad = g_mul(a, d); bc = g_mul(b, c)
    return (g_sub(ac, g_scal(3, bd)), g_sub(g_add(ad, bc), g_scal(3, bd)))
def e_sigma(x): return (g_conj(x[0]), g_conj(x[1]))
def e_zero(x): return g_zero(x[0]) and g_zero(x[1])
def e_norm_to_F(x): return e_mul(x, e_sigma(x))          # N_{E_0/F}
def e_inv(x):
    # (a + b w)^{-1}: use the conjugate over Q(i): (a + b w')... simpler: solve via norm to Q(i)-coeffs:
    # w and w' = -3 - w are the two roots; (a+bw)(a+bw') = a^2 + ab(w+w') + b^2 ww' = a^2 - 3ab + 3b^2
    a, b = x
    n = g_add(g_sub(g_mul(a, a), g_scal(3, g_mul(a, b))), g_scal(3, g_mul(b, b)))
    ninv = g_inv(n)
    # a + b w' = a + b(-3 - w) = (a - 3b) - b w
    conj = (g_sub(a, g_scal(3, b)), g_neg(b))
    return (g_mul(conj[0], ninv), g_mul(conj[1], ninv))
def e_val(x):
    if e_zero(x): return 10**9
    return min(2*g_v3(x[0]), 2*g_v3(x[1]) + 1)
def e_int(k): return (gq(k), gq())
E0 = (gq(), gq()); E1 = (gq(1), gq()); EI = (gq(0, 1), gq()); EW = (gq(), gq(1))
ZETA = e_add(E1, EW)
ZETAINV = e_mul(ZETA, ZETA)
THREE = e_int(3)
assert e_mul(EW, EW) == e_neg(e_add(THREE, e_mul(THREE, EW)))
def e_pow(x, n):
    r = E1
    for _ in range(n): r = e_mul(r, x)
    return r
def e_div_varpi(x):
    a, b = x
    return (g_sub(b, a), g_scal(Fr(-1, 3), a))
def e_mul_varpi(x): return e_mul(x, EW)
def e_red(x):
    """reduction of an element of O_{E_0} mod varpi, as (re mod 3, im mod 3)"""
    a = x[0]
    assert a[0].denominator % 3 != 0 and a[1].denominator % 3 != 0
    r = (a[0].numerator * pow(a[0].denominator, -1, 3)) % 3
    s = (a[1].numerator * pow(a[1].denominator, -1, 3)) % 3
    return (r, s)
def is_in_F(x): return x[0][1] == 0 and x[1][1] == 0

# ---------------- D = E_0 + E_0 j ----------------
def d_add(X, Y): return (e_add(X[0], Y[0]), e_add(X[1], Y[1]))
def d_sub(X, Y): return (e_sub(X[0], Y[0]), e_sub(X[1], Y[1]))
def d_mul(X, Y):
    x, y = X; u, v = Y
    return (e_add(e_mul(x, u), e_mul(e_mul(y, e_sigma(v)), EW)), e_add(e_mul(x, v), e_mul(y, e_sigma(u))))
def d_val(X): return min(2*e_val(X[0]), 2*e_val(X[1]) + 1)
def d_pow(X, n):
    R = D1
    for _ in range(n): R = d_mul(R, X)
    return R
def d_nrd(X):
    x, y = X
    return e_sub(e_mul(x, e_sigma(x)), e_mul(e_mul(y, e_sigma(y)), EW))
def d_trd(X): return e_add(X[0], e_sigma(X[0]))
def d_scal(c, X): return (e_mul(c, X[0]), e_mul(c, X[1]))   # c in E_0 acting on the left
def d_inv(X):
    # X^{-1} = conj(X)/Nrd(X), conj(x + yj) = sigma(x) - y j
    n = d_nrd(X); ninv = e_inv(n)
    conj = (e_sigma(X[0]), e_neg(X[1]))
    return (e_mul(ninv, conj[0]), e_mul(ninv, conj[1]))
D0 = (E0, E0); D1 = (E1, E0); DJ = (E0, E1); DI = (EI, E0); DW = (EW, E0)

# ---------------- classes modulo cubes ----------------
GENS_E = [e_add(E1, EW), e_add(E1, e_mul(EW, EI)), e_add(E1, e_mul(EW, EW)), e_add(E1, e_mul(e_mul(EW, EW), EI)),
          e_add(E1, e_pow(EW, 3))]
def cls_E_unit1(u):
    """u in U^{(1)}_{E_0}: coordinates in F_3^5 w.r.t. 1+w, 1+wi, 1+w^2, 1+w^2 i, 1+w^3 (mod cubes)"""
    coords = []
    r = u
    for level in (1, 2):
        d = e_red(e_div_varpi(e_sub(r, E1)) if level == 1 else e_div_varpi(e_div_varpi(e_sub(r, E1))))
        a, b = d
        coords += [a, b]
        g1, g2 = GENS_E[2*(level-1)], GENS_E[2*(level-1)+1]
        r = e_mul(r, e_inv(e_mul(e_pow(g1, a), e_pow(g2, b))))
        assert e_val(e_sub(r, E1)) >= level + 1
    d = e_red(e_div_varpi(e_div_varpi(e_div_varpi(e_sub(r, E1)))))
    coords.append(d[0])      # real part at level 3; imaginary part is a cube
    return coords
def cls_E(x):
    """class of x in E_0^x / E_0^{x3} as a vector in F_3^6: (v mod 3, 5 unit coordinates)"""
    v = e_val(x)
    u = x
    # divide by varpi^v (multiply by varpi^{-v} if v < 0)
    if v >= 0:
        for _ in range(v): u = e_div_varpi(u)
    else:
        for _ in range(-v): u = e_mul_varpi(u)
    assert e_val(u) == 0
    # u is a unit; u^8 in U^{(1)}, cls(u) = -cls(u^8)
    u8 = e_pow(u, 8)
    c = cls_E_unit1(u8)
    return np.array([v % 3] + [(-t) % 3 for t in c]) % 3
GENS_F = [e_add(E1, EW), e_add(E1, e_mul(EW, EW)), e_add(E1, e_pow(EW, 3))]
def cls_F_unit1(u):
    coords = []; r = u
    for level in (1, 2, 3):
        d = e_sub(r, E1)
        for _ in range(level): d = e_div_varpi(d)
        a = e_red(d)[0]
        coords.append(a)
        r = e_mul(r, e_inv(e_pow(GENS_F[level-1], a)))
        assert e_val(e_sub(r, E1)) >= level + 1
    return coords
def cls_F(x):
    assert is_in_F(x)
    v = e_val(x); u = x
    if v >= 0:
        for _ in range(v): u = e_div_varpi(u)
    else:
        for _ in range(-v): u = e_mul_varpi(u)
    assert e_val(u) == 0
    u2 = e_pow(u, 2)          # u^2 in U^{(1)}_F ; cls(u) = -cls(u^2)
    c = cls_F_unit1(u2)
    return np.array([v % 3] + [(-t) % 3 for t in c]) % 3

# ---------------- F_3 linear algebra ----------------
def nullspace_mod3(M):
    M = np.array(M, dtype=int) % 3
    rows, cols = M.shape; r = 0; piv = []
    for c in range(cols):
        p = None
        for i in range(r, rows):
            if M[i, c]: p = i; break
        if p is None: continue
        M[[r, p]] = M[[p, r]]
        M[r] = (M[r] * (1 if M[r, c] == 1 else 2)) % 3
        for i in range(rows):
            if i != r and M[i, c]: M[i] = (M[i] - M[i, c] * M[r]) % 3
        piv.append(c); r += 1
        if r == rows: break
    R = M[:r]; free = [c for c in range(cols) if c not in piv]; basis = []
    for f in free:
        v = np.zeros(cols, dtype=int); v[f] = 1
        for i, p in enumerate(piv): v[p] = (-R[i, f]) % 3
        basis.append(v)
    return basis

def solve_steinberg(cls, dim, samples):
    pairs = [(a, b) for a in range(dim) for b in range(a+1, dim)]
    rows = []
    for a in samples:
        one_minus = e_sub(E1, a)
        if e_zero(one_minus) or e_zero(a): continue
        x, y = cls(a), cls(one_minus)
        rows.append([(x[p]*y[q] - x[q]*y[p]) % 3 for (p, q) in pairs])
    sols = nullspace_mod3(np.array(rows))
    return sols, pairs
def form_from(sol, pairs, dim):
    A = np.zeros((dim, dim), dtype=int)
    for s, (p, q) in zip(sol, pairs):
        A[p, q] = s % 3; A[q, p] = (-s) % 3
    return A

def random_E_element(rng, maxv=2):
    """random element of E_0^x with coefficients small, valuation in [0, maxv]"""
    while True:
        a = (gq(rng.randint(-13, 13), rng.randint(-13, 13)), gq(rng.randint(-13, 13), rng.randint(-13, 13)))
        if not e_zero(a) and e_val(a) <= maxv: return a
def random_F_element(rng, maxv=2):
    while True:
        a = (gq(rng.randint(-40, 40), 0), gq(rng.randint(-40, 40), 0))
        if not e_zero(a) and e_val(a) <= maxv: return a

def build_symbols(seed=1, nE=4000, nF=2500):
    rng = random.Random(seed)
    sE = [random_E_element(rng) for _ in range(nE)]
    # also add elements 1 - u for units u etc. are covered; add varpi-multiples
    solsE, pairsE = solve_steinberg(cls_E, 6, sE)
    sF = [random_F_element(rng) for _ in range(nF)]
    solsF, pairsF = solve_steinberg(cls_F, 4, sF)
    return solsE, pairsE, solsF, pairsF

class Symbols:
    def __init__(self, AE, AF):
        self.AE = AE % 3; self.AF = AF % 3
    def hE(self, x, y):   # exponent of the cubic Hilbert symbol (x,y)_{E_0}
        return int(cls_E(x) @ self.AE @ cls_E(y)) % 3
    def hF(self, x, y):
        return int(cls_F(x) @ self.AF @ cls_F(y)) % 3
    def hE_cls(self, cx, cy): return int(cx @ self.AE @ cy) % 3

# ---------------- GL_2(E_0) and the KP cocycle ----------------
def m_mul(A, B):
    return ((e_add(e_mul(A[0][0], B[0][0]), e_mul(A[0][1], B[1][0])), e_add(e_mul(A[0][0], B[0][1]), e_mul(A[0][1], B[1][1]))),
            (e_add(e_mul(A[1][0], B[0][0]), e_mul(A[1][1], B[1][0])), e_add(e_mul(A[1][0], B[0][1]), e_mul(A[1][1], B[1][1]))))
def m_det(A): return e_sub(e_mul(A[0][0], A[1][1]), e_mul(A[0][1], A[1][0]))
def xfun(A):
    c = A[1][0]
    return c if not e_zero(c) else A[1][1]
def iota(X):
    x, y = X
    return ((x, e_mul(EW, y)), (e_sigma(y), e_sigma(x)))

class Cover:
    """exponent-valued cocycle beta(g,h) in F_3 for the (parameter c_v=2) KP cover of GL_2(E_0),
       convention sigma(g,h) = (x(gh)/x(g), x(gh)/(x(h) det g)); relabel = multiply by r' = 2."""
    def __init__(self, sym, cv=2, relabel=True):
        self.sym = sym; self.cv = cv; self.relabel = relabel
    def sigma(self, g, h):
        gh = m_mul(g, h)
        cx_g, cx_h, cx_gh = cls_E(xfun(g)), cls_E(xfun(h)), cls_E(xfun(gh))
        cdet_g = cls_E(m_det(g))
        a = (cx_gh - cx_g) % 3
        b = (cx_gh - cx_h - cdet_g) % 3
        return self.sym.hE_cls(a, b)
    def beta(self, g, h):
        s = self.sigma(g, h) + self.cv * self.sym.hE(m_det(g), m_det(h))
        if self.relabel: s = 2*s
        return s % 3
    def betaD(self, X, Y):
        return self.beta(iota(X), iota(Y))
    # cover elements: (X, e) with X in D^x, e in F_3
    def mul(self, A, B):
        X, e = A; Y, f = B
        return (d_mul(X, Y), (e + f + self.betaD(X, Y)) % 3)
    def power(self, A, n):
        R = (D1, 0)
        for _ in range(n): R = self.mul(R, A)
        return R
    def commutator_exp(self, X, Y):
        """exponent of [X~, Y~] for commuting X, Y:  beta(X,Y) - beta(Y,X)"""
        return (self.betaD(X, Y) - self.betaD(Y, X)) % 3
