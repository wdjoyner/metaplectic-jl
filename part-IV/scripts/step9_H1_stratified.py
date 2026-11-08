"""Stratified exact test of (H1) using the closed form ell(X) = (X, h_E(z_X, y_X)),
   z_X = (1+varpi^3)^{c(X)}, c(X) = real part of the level-6 digit of X.
   (H1) <=> kappa(XX') = kappa(X) + kappa(X') + beta(X,X') for all X, X' in K^6."""
import sys; sys.path.insert(0, '.')
from cover import *
import random, time, pickle, collections
import numpy as np

S = pickle.load(open('./symbols.pkl', 'rb'))
sym = Symbols(S['AE'], S['AF'])
cov = Cover(sym, cv=2, relabel=False)
VARPI3 = e_pow(EW, 3)
ONE_P_W3 = e_add(E1, VARPI3)

def digit6(X):
    x = e_sub(X[0], E1)
    for _ in range(3): x = e_div_varpi(x)
    return e_red(x)
def kappa(X):
    c = digit6(X)[0]
    if c == 0 or e_zero(X[1]): return 0
    z = e_pow(ONE_P_W3, c)
    return sym.hE(z, X[1])
def check_pair(X, Xp):
    lhs = kappa(d_mul(X, Xp))
    rhs = (kappa(X) + kappa(Xp) + cov.betaD(X, Xp)) % 3
    return lhs == rhs, lhs, rhs

def rand_O(rng, R=4):
    return (gq(rng.randint(-R, R), rng.randint(-R, R)), gq(rng.randint(-R, R), rng.randint(-R, R)))
def rand_unit(rng, R=4):
    while True:
        u = rand_O(rng, R)
        if e_val(u) == 0: return u
def make_X(a, b):
    """X = 1 + varpi^3 (a + b j)"""
    return d_add(D1, (e_mul(VARPI3, a), e_mul(VARPI3, b)))

rng = random.Random(31)
t0 = time.time()
stats = collections.Counter(); fails = []
def run(case, X, Xp):
    ok, l, r = check_pair(X, Xp)
    stats[(case, ok)] += 1
    if not ok: fails.append((case, X, Xp, l, r))

# Case 0: generic random
for _ in range(1500):
    X = make_X(rand_O(rng), rand_O(rng)); Xp = make_X(rand_O(rng), rand_O(rng))
    run('generic', X, Xp)
# Case 1: controlled valuations of b, b'
for vb in range(0, 5):
    for vbp in range(0, 5):
        for _ in range(60):
            b = e_mul(e_pow(EW, vb), rand_unit(rng)); bp = e_mul(e_pow(EW, vbp), rand_unit(rng))
            X = make_X(rand_O(rng), b); Xp = make_X(rand_O(rng), bp)
            run('val(%d,%d)' % (vb, vbp), X, Xp)
# Case 2: t = sigma(b'/b) == -1 mod varpi^m  (b' = -b (1 + varpi^m s0))
for m in range(1, 6):
    for _ in range(300):
        b = e_mul(e_pow(EW, rng.randint(0, 2)), rand_unit(rng))
        s0 = rand_unit(rng)
        bp = e_neg(e_mul(b, e_add(E1, e_mul(e_pow(EW, m), s0))))
        X = make_X(rand_O(rng), b); Xp = make_X(rand_O(rng), bp)
        run('tminus1_m%d' % m, X, Xp)
# Case 3: elements of E_0 (b = 0) on either side
for _ in range(300):
    X = make_X(rand_O(rng), E0); Xp = make_X(rand_O(rng), rand_O(rng)); run('E0,gen', X, Xp)
    X = make_X(rand_O(rng), rand_O(rng)); Xp = make_X(rand_O(rng), E0); run('gen,E0', X, Xp)
    X = make_X(rand_O(rng), E0); Xp = make_X(rand_O(rng), E0); run('E0,E0', X, Xp)
# Case 4: deeper elements (K^7, K^8, K^9) mixed with K^6
for k in range(1, 4):
    for _ in range(300):
        X = make_X(rand_O(rng), rand_O(rng))
        Xp = make_X(e_mul(e_pow(EW, k), rand_O(rng)), e_mul(e_pow(EW, k), rand_O(rng)))
        run('K6xK%d' % (6 + k), X, Xp); run('K%dxK6' % (6 + k), Xp, X)
# Case 5: scalars
for _ in range(200):
    c = rng.randint(0, 2); z = (e_pow(ONE_P_W3, c), E0)
    X = make_X(rand_O(rng), rand_O(rng))
    run('scalar', z, X); run('scalar2', X, z)
# Case 6: triple associativity-type check: ell multiplicative on random triples (consistency)
print("elapsed %.0fs" % (time.time() - t0))
tot_ok = sum(v for (c, ok), v in stats.items() if ok); tot = sum(stats.values())
print("TOTAL pairs tested:", tot, " passed:", tot_ok, " failed:", tot - tot_ok)
for key in sorted(stats):
    if not key[1]: print("  FAILURES in case", key[0], ":", stats[key])
print("per-case counts:", {c: n for (c, ok), n in sorted(stats.items()) if ok})
# distribution of kappa and beta values (non-vacuity)
cnt = collections.Counter()
for _ in range(500):
    X = make_X(rand_O(rng), e_mul(e_pow(EW, rng.randint(0, 3)), rand_unit(rng))); Xp = make_X(rand_O(rng), e_mul(e_pow(EW, rng.randint(0, 3)), rand_unit(rng)))
    cnt[(kappa(X), cov.betaD(X, Xp))] += 1
print("distribution of (kappa(X), beta(X,X')):", dict(cnt))
if fails:
    print("first failure:", fails[0])
