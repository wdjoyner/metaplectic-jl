"""Independent check of the defect function e_* against the explicit cover, and omega = 0."""
import sys; sys.path.insert(0, '.')
from cover import *
import quat as Q   # integer model for V-coordinates
import random, time, pickle, collections, itertools
import numpy as np

S = pickle.load(open('./symbols.pkl', 'rb'))
sym = Symbols(S['AE'], S['AF'])
cov = Cover(sym, cv=2, relabel=False)
VARPI3 = e_pow(EW, 3); ONE_P_W3 = e_add(E1, VARPI3)
G3data = pickle.load(open('./G3.pkl', 'rb'))
des = pickle.load(open('./design_0011020002.pkl', 'rb'))   # e_* (one of the two signs)
e_star = des['e']

def digit6(X):
    x = e_sub(X[0], E1)
    for _ in range(3): x = e_div_varpi(x)
    return e_red(x)
def kappa(X):
    c = digit6(X)[0]
    if c == 0 or e_zero(X[1]): return 0
    return sym.hE(e_pow(ONE_P_W3, c), X[1])
def psi6(A):
    """psi_6 on an element A = (P, E) of the cover with P in U_F^{(1)} K^6; returns exponent in F_3"""
    P, E = A
    # F-part of x_P as scalar z
    a, b = P[0]
    z = ((a[0], Fr(0)), (b[0], Fr(0)))        # real parts: element of O_F
    X = d_mul(d_inv((z, E0)), P)
    assert d_val(d_sub(X, D1)) >= 6, d_val(d_sub(X, D1))
    return (E - cov.betaD((z, E0), X) - kappa(X)) % 3
def cmul(A, B): return cov.mul(A, B)
def cinv(A):
    X, e = A; Xi = d_inv(X)
    return (Xi, (-e - cov.betaD(X, Xi)) % 3)

# depth-1 representatives with their V-vectors (reuse the integer model to get coordinates)
def to_frac(Xint):
    (x, y) = Xint
    return (((Fr(x[0][0]), Fr(x[0][1])), (Fr(x[1][0]), Fr(x[1][1]))), ((Fr(y[0][0]), Fr(y[0][1])), (Fr(y[1][0]), Fr(y[1][1]))))
reps_by_v = collections.defaultdict(list)
for u0 in Q.F9x:
    for u1 in Q.F9:
        for v0 in Q.F9:
            y = ((u0, (0, 0)) if False else None)
            t_int = ( Q.e_add(Q.E1, Q.e_mul(Q.EW, ((v0[0], v0[1]), (0, 0)))), ((u0[0], u0[1]), (u1[0], u1[1])) )
            t3 = Q.d_pow(t_int, 3)
            v = Q.V_vec(Q.coords_P3(Q.d_sub(t3, Q.D1)))
            reps_by_v[v].append(to_frac(t_int))
assert len(reps_by_v) == 72
G3 = list(reps_by_v.keys())
def neg(v): return tuple((-c) % 3 for c in v)
def addv(*vs): return tuple(sum(c) % 3 for c in zip(*vs))

rng = random.Random(5)
def sigma_of(t):
    """sigma(t^3) = (t,0)^3 ; verify it equals (t^3, 0)"""
    A = cov.power((t, 0), 3)
    assert A[1] == 0
    return A
# ---- defects of relations sum v_i = 0 among good vectors ----
def defect(ts):
    A = (D1, 0)
    for t in ts: A = cmul(A, sigma_of(t))
    return psi6(A)
results = collections.Counter(); t0 = time.time()
# coplanar triples (predicted defect 0) and general 3-term relations
n3 = 0
for _ in range(400):
    v1, v2 = rng.choice(G3), rng.choice(G3)
    v3 = neg(addv(v1, v2))
    if v3 not in reps_by_v or v3 in (v1, v2) or v1 == v2: continue
    ts = [rng.choice(reps_by_v[v]) for v in (v1, v2, v3)]
    d = defect(ts); pred = (e_star[v1] + e_star[v2] + e_star[v3]) % 3
    results[('triple', d, pred)] += 1; n3 += 1
# 4-term relations
n4 = 0; match_plus = 0; match_minus = 0
for _ in range(600):
    v1, v2, v3 = rng.choice(G3), rng.choice(G3), rng.choice(G3)
    v4 = neg(addv(v1, v2, v3))
    if v4 not in reps_by_v: continue
    ts = [rng.choice(reps_by_v[v]) for v in (v1, v2, v3, v4)]
    d = defect(ts); pred = (e_star[v1] + e_star[v2] + e_star[v3] + e_star[v4]) % 3
    results[('quad', d, pred)] += 1; n4 += 1
    if d == pred: match_plus += 1
    if d == (-pred) % 3: match_minus += 1
print("elapsed %.0fs ; triples %d, quads %d" % (time.time() - t0, n3, n4))
print("triple (defect, predicted) counts:", {k[1:]: v for k, v in results.items() if k[0] == 'triple'})
print("quad   (defect, predicted) counts:", {k[1:]: v for k, v in results.items() if k[0] == 'quad'})
print("quads: defect == +e_* sum:", match_plus, " defect == -e_* sum:", match_minus, " of", n4)
# also: does the defect depend only on the V-classes (NC3-type consistency)? test with different representatives
incons = 0
for _ in range(100):
    v1, v2, v3 = rng.choice(G3), rng.choice(G3), rng.choice(G3)
    v4 = neg(addv(v1, v2, v3))
    if v4 not in reps_by_v: continue
    d1 = defect([rng.choice(reps_by_v[v]) for v in (v1, v2, v3, v4)])
    d2 = defect([rng.choice(reps_by_v[v]) for v in (v1, v2, v3, v4)])
    if d1 != d2: incons += 1
print("representative-independence failures (NC3 consistency):", incons)

# ---- omega = 0: psi_6([x~,y~]) for x, y in K^3 ----
def rand_K3(rng):
    a = (gq(rng.randint(-3, 3), rng.randint(-3, 3)), gq(rng.randint(-3, 3), rng.randint(-3, 3)))
    b = (gq(rng.randint(-3, 3), rng.randint(-3, 3)), gq(rng.randint(-3, 3), rng.randint(-3, 3)))
    return d_add(D1, (e_mul(e_mul(EW, EW), a), e_mul(EW, b)))     # 1 + varpi^2 a + varpi b j  in K^3
bad = 0; nz = 0
for _ in range(300):
    x = rand_K3(rng); y = rand_K3(rng)
    A = (x, 0); B = (y, 0)
    C = cmul(cmul(A, B), cmul(cinv(A), cinv(B)))
    if d_val(d_sub(C[0], D1)) < 6: continue
    val = psi6(C)
    if val != 0: bad += 1
    nz += 1
print("omega(x,y) = psi_6([x~,y~]) nonzero count:", bad, "of", nz)
# ---- kappa_{1,5}: psi_6([t~, v~]) for t depth 1 (level-1 coefficient a) and v in K^5 (level-5 coefficient b): compare with beta*Tr(a sigma(b))
def rand_K5(rng):
    a = (gq(rng.randint(-3, 3), rng.randint(-3, 3)), gq(rng.randint(-3, 3), rng.randint(-3, 3)))
    b = (gq(rng.randint(-3, 3), rng.randint(-3, 3)), gq(rng.randint(-3, 3), rng.randint(-3, 3)))
    return d_add(D1, (e_mul(e_pow(EW, 3), a), e_mul(e_mul(EW, EW), b)))  # 1 + varpi^3 a + varpi^2 b j in K^5
def red_coeff_level(X, lev):
    # leading coefficient at odd level lev = 2k+1: y-part / varpi^k mod varpi
    y = X[1]
    for _ in range((lev - 1)//2): y = e_div_varpi(y)
    return e_red(y)
cnt = collections.Counter()
for _ in range(300):
    t = d_add(D1, (e_mul(EW, (gq(rng.randint(-3,3), rng.randint(-3,3)), gq(rng.randint(-3,3), rng.randint(-3,3)))),
                   (gq(rng.randint(-3,3), rng.randint(-3,3)), gq(rng.randint(-3,3), rng.randint(-3,3)))))
    if d_val(d_sub(t, D1)) != 1: continue
    v = rand_K5(rng)
    if d_val(d_sub(v, D1)) != 5: continue
    A = (t, 0); B = (v, 0)
    C = cmul(cmul(A, B), cmul(cinv(A), cinv(B)))
    val = psi6(C)
    a = red_coeff_level(d_sub(t, D1), 1); b = red_coeff_level(d_sub(v, D1), 5)
    # Tr(a sigma(b)) in F_3
    prod = ((a[0]*b[0] + a[1]*b[1]) % 3, (a[1]*b[0] - a[0]*b[1]) % 3)   # a * conj(b)
    tr = (2*prod[0]) % 3
    cnt[(val, tr)] += 1
print("kappa_{1,5} vs Tr(a sigma(b)): (psi, Tr) counts:", dict(cnt))
