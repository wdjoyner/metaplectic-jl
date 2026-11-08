"""Checks accompanying the symbolic proof of (H1) in Draft 2, Section 10.
 (1) The referee's example: beta(X,X') != 0 in a v(t)>0 case (Draft 1 case (i) was wrong).
 (2) New closed form kappa(k) = (b_k, Nrd k)_{E_0} (0 if b_k = 0) agrees with Draft 1's kappa.
 (3) Hilbert-symbol inputs used in the proof: (U^(1),U^(3)) = 0, mu_8 and -1 cubes,
     (x, m) = v(x) (varpi, m) for m in U^(3).
 (4) The identity (**) (R, tau) = v(tau)(a',varpi) - v(R)[(a',varpi)-(a,varpi)] and
     the full (H1) identity, on a large structured sample including every degenerate case.
"""
import sys; sys.path.insert(0, '.')
from cover import *
import random, pickle, collections, itertools
S = pickle.load(open('./symbols.pkl', 'rb'))
sym = Symbols(S['AE'], S['AF']); cov = Cover(sym, cv=2, relabel=False)
VARPI3 = e_pow(EW, 3); ONE_P_W3 = e_add(E1, VARPI3)
def digit6(X):
    x = e_sub(X[0], E1)
    for _ in range(3): x = e_div_varpi(x)
    return e_red(x)
def kappa_old(X):
    c = digit6(X)[0]
    if c == 0 or e_zero(X[1]): return 0
    return sym.hE(e_pow(ONE_P_W3, c), X[1])
def kappa_new(X):
    if e_zero(X[1]): return 0
    return sym.hE(X[1], d_nrd(X))
def make_X(a, b): return d_add(D1, (e_mul(VARPI3, a), e_mul(VARPI3, b)))
rng = random.Random(2026)
def rand_O(R=4): return (gq(rng.randint(-R, R), rng.randint(-R, R)), gq(rng.randint(-R, R), rng.randint(-R, R)))
def rand_unit():
    while True:
        u = rand_O()
        if e_val(u) == 0: return u

# (1) referee's example: X = 1 + varpi^3 j, X' = 1 + varpi^3 + varpi^4 j
X = (E1, VARPI3); Xp = (e_add(E1, VARPI3), e_pow(EW, 4))
print("referee example: beta =", cov.betaD(X, Xp), " kappa:", kappa_new(X), kappa_new(Xp), kappa_new(d_mul(X, Xp)))
# (2) old vs new kappa
bad = 0
for _ in range(3000):
    Y = make_X(rand_O(), rand_O() if rng.random() < 0.9 else (gq(), gq()))
    if kappa_old(Y) != kappa_new(Y): bad += 1
print("kappa_old == kappa_new failures:", bad)
# (3) symbol facts
def U(k): return e_add(E1, e_mul(e_pow(EW, k), rand_unit()))
f = collections.Counter()
for _ in range(500):
    f['U1,U3'] += sym.hE(U(1), U(3)) != 0
    f['U2,U2'] += sym.hE(U(2), U(2)) != 0
    f['-1'] += sym.hE(e_neg(E1), U(1)) != 0 or sym.hE(e_neg(E1), EW) != 0
    f['i'] += sym.hE(EI, U(1)) != 0 or sym.hE(EI, EW) != 0
    m = U(3); x = e_mul(e_pow(EW, rng.randint(-3, 3)), e_mul(rand_unit(), E1))
    f['(x,m)=v(x)(w,m)'] += sym.hE(x, m) != (e_val(x) * sym.hE(EW, m)) % 3
print("symbol-fact violations:", dict(f))
# (4) identity (**) and (H1)
def star2(a, ap, tau):
    R = e_add(ap, e_mul(e_sigma(a), tau))
    if e_zero(R): return True
    lhs = sym.hE(R, tau)
    rhs = (e_val(tau) * sym.hE(ap, EW) - e_val(R) * (sym.hE(ap, EW) - sym.hE(a, EW))) % 3
    return lhs == rhs
def H1(X, Xp):
    return kappa_new(d_mul(X, Xp)) == (kappa_new(X) + kappa_new(Xp) + cov.betaD(X, Xp)) % 3
cnt = collections.Counter(); fails = []
for case in range(12000):
    a = e_add(E1, e_mul(VARPI3, rand_O())); ap = e_add(E1, e_mul(VARPI3, rand_O()))
    kind = rng.choice(['gen', 'gen', 'gen', 'b0', 'bp0', 'both0', 'R0', 'tau-1', 'deep'])
    if kind == 'gen':
        b = e_mul(e_pow(EW, rng.randint(3, 7)), rand_unit()); bp = e_mul(e_pow(EW, rng.randint(3, 7)), rand_unit())
    elif kind == 'b0':
        b = (gq(), gq()); bp = e_mul(e_pow(EW, rng.randint(3, 6)), rand_unit())
    elif kind == 'bp0':
        bp = (gq(), gq()); b = e_mul(e_pow(EW, rng.randint(3, 6)), rand_unit())
    elif kind == 'both0':
        b = bp = (gq(), gq())
    elif kind == 'R0':   # b' chosen so that R = a' + sigma(a) tau = 0, tau = sigma(b'/b)
        b = e_mul(e_pow(EW, rng.randint(3, 6)), rand_unit())
        tau = e_neg(e_mul(ap, e_inv(e_sigma(a))))
        bp = e_mul(b, e_sigma(tau))
    elif kind == 'tau-1':  # tau = -1 + varpi^m u
        b = e_mul(e_pow(EW, rng.randint(3, 6)), rand_unit()); m = rng.randint(1, 5)
        tau = e_add(e_neg(E1), e_mul(e_pow(EW, m), rand_unit()))
        bp = e_mul(b, e_sigma(tau))
    else:  # deep: X' in K^8..K^12
        k = rng.randint(4, 6)
        ap = e_add(E1, e_mul(e_pow(EW, k), rand_O()))
        b = e_mul(e_pow(EW, rng.randint(3, 6)), rand_unit()); bp = e_mul(e_pow(EW, rng.randint(k, k + 3)), rand_unit())
    X = (a, b); Xp = (ap, bp)
    ok = H1(X, Xp); cnt[(kind, ok)] += 1
    if not ok: fails.append((kind, X, Xp))
    if not e_zero(b) and not e_zero(bp):
        tau = e_sigma(e_mul(bp, e_inv(b)))
        cnt[('**', star2(a, ap, tau))] += 1
print(sorted(cnt.items()))
print("failures:", len(fails))
# distribution of values of both sides (non-vacuity)
vals = collections.Counter()
for _ in range(2000):
    X = make_X(rand_O(), e_mul(e_pow(EW, rng.randint(0, 3)), rand_unit())); Xp = make_X(rand_O(), e_mul(e_pow(EW, rng.randint(0, 3)), rand_unit()))
    vals[(kappa_new(X), kappa_new(Xp), cov.betaD(X, Xp), kappa_new(d_mul(X, Xp)))] += 1
print("distinct value patterns:", len(vals), "; beta nonzero in", sum(v for k, v in vals.items() if k[2] != 0))
