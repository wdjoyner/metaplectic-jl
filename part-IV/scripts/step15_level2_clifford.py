"""Level two, final step: Clifford analysis of Phi_rho on U~_1.

Phi_rho (rho trivial on K^3, rho|_{Q_2} nontrivial) is supported on U~_3 and its restriction is
lambda_0 times the sum of the 54 three-dimensional irreducible characters of H = Q_3/Q_7 (step 14),
each with multiplicity one.  Hence Phi_rho is a virtual character of U~_1 iff Ad(Q_1) acts freely
on these 54 genuine irreducible characters of H^ = U~_3/(s(K^7) ker theta~)  (orbits of size 27).
This script constructs H^ in the explicit cocycle model (theta_0 = 1), computes lambda_0 on it,
the Ad(Q_1)-action on the genuine irreducibles, and the orbit sizes.
"""
import sys; sys.path.insert(0, '.')
import pickle, time, numpy as np
from collections import Counter
import quat as Q
from cover import *
import cover as C

t00 = time.time()
exec(open('step13_level2.py').read().split("# ---------- the criterion")[0].replace("from quat import *", "from quat import *"))
# (the exec above runs with quat's names; re-import cover's names for exact arithmetic)
from cover import *
S = pickle.load(open('./symbols.pkl', 'rb'))
sym = Symbols(S['AE'], S['AF']); cov = Cover(sym, cv=2, relabel=False)

# ---- conversions quat (integer coords) -> cover (Fraction coords) ----
def to_cov(X):
    (x0, x1), (y0, y1) = X
    return ((gq(x0[0], x0[1]), gq(x1[0], x1[1])), (gq(y0[0], y0[1]), gq(y1[0], y1[1])))
Xh = [d_add(D1, to_cov(X)) for X in H]           # exact representatives 1+X_h of the classes h
Xt = {hc: d_add(D1, to_cov(T)) for hc, T in Q1reps.items()}   # exact representatives of Q_1/Q_3

# ---- lambda_0 and psi_6 (from step 11, theta_0 = 1) ----
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
    a, b = P[0]
    z = ((a[0], Fr(0)), (b[0], Fr(0)))
    return z, d_mul(d_inv((z, E0)), P)
def psi6(A):
    P, E = A
    z, X = split_scalar(P)
    assert d_val(d_sub(X, D1)) >= 6
    return (E - cov.betaD((z, E0), X) - kappa(X)) % 3
def cmul(A, B): return cov.mul(A, B)
def cinv(A):
    X, e = A; Xi = d_inv(X)
    return (Xi, (-e - cov.betaD(X, Xi)) % 3)
def conj(A, B): return cmul(cmul(A, B), cinv(A))
XI = d_add(D1, DI)
D8_lifts = []
for l in range(2):
    for kk in range(4):
        g = D1
        for _ in range(kk): g = d_mul(g, XI)
        if l: g = d_mul(g, DJ)
        D8_lifts.append((g, 0))
def lambda0(y):
    N = (D1, 0)
    for d in D8_lifts: N = cmul(N, conj(d, y))
    return (-psi6(N)) % 3

# ---- reduction of an exact element (Y, eps) of U~_3 to H^ = {(h, eps')} ----
def reduce_quat(Y):
    """exact Y in K^3 -> canonical quat element (integer coords mod P^7)"""
    (x0, x1), (y0, y1) = d_sub(Y, D1)
    def fm(fr, m): return (fr.numerator * pow(fr.denominator, -1, m)) % m
    def gi(g, m): return (fm(g[0], m), fm(g[1], m))
    Xq = ((gi(x0, 9), gi(x1, 9)), (gi(y0, 9), gi(y1, 3)))
    return normalize(Xq)
def to_Hhat(A):
    Y, eps = A
    hq = reduce_quat(Y); h = Hidx[hq]
    M = d_mul(d_inv(Xh[h]), Y)                 # = z n with z in U_F^(2), n in K^7
    a0, a1 = M[0]                                # x_M = a0 + a1 varpi, a_k Gaussian; F-part = Re a0 + Re a1 varpi
    z = ((a0[0], Fr(0)), (a1[0], Fr(0)))
    n = d_mul(d_inv((z, E0)), M)
    assert d_val(d_sub(n, D1)) >= 7, d_val(d_sub(n, D1))
    assert e_val(e_sub(z, E1)) >= 2
    corr = (cov.betaD(Xh[h], (z, E0)) + cov.betaD(d_mul(Xh[h], (z, E0)), n)) % 3
    return h, (eps - corr) % 3

# ---- lambda_0 on H^ : lambda_0(h, eps) = zeta^eps * zeta^{L[h]} ----
print("computing lambda_0 on the 729 representatives ...")
t0 = time.time()
L = [lambda0((Xh[h], 0)) for h in range(729)]
print("  done in %.0fs; value distribution %s" % (time.time() - t0, Counter(L)))
# consistency: lambda_0 is a character of H^ : check on random pairs via the cocycle of H^
import random
rng = random.Random(5)
for _ in range(300):
    a, b = rng.randrange(729), rng.randrange(729)
    prod = cmul((Xh[a], 0), (Xh[b], 0))
    h, eps = to_Hhat(prod)
    assert h == MT[a, b]
    assert (L[a] + L[b]) % 3 == (eps + L[h]) % 3, "lambda_0 does not descend to H^"
print("lambda_0 is a character of H^ (300 random pairs)")

# ---- genuine irreducibles of H^ with central character zeta: mu_chi = lambda_0 * chi, chi in Irr(H) ----
deg3 = [t for t in table if t[id_cls][0] == 3]
assert len(deg3) == 54
# ---- Ad(Q_1) action: (mu^t)(h,0) := mu(conj(t~, x_h)) = zeta^{eps'} zeta^{L[h']} chi(h'), and
#      mu^t = lambda_0 * chi''  with chi''(h) = zeta^{eps' + L[h'] - L[h]} chi(h')
ZZ = [(1, 0), (0, 1), (-1, -1)]   # zeta^0, zeta^1, zeta^2 in the (a,b) basis
def zpow(k): return ZZ[k % 3]
print("computing the conjugation action of the 27 representatives of Q_1/Q_3 on H^ ...")
t0 = time.time()
conj_data = {}   # (tkey, h) -> (h', eps')
for tkey, Tex in Xt.items():
    Tl = (Tex, 0)
    for h in range(729):
        conj_data[(tkey, h)] = to_Hhat(conj(Tl, (Xh[h], 0)))
print("  done in %.0fs" % (time.time() - t0))
# linear twist c_t = lambda_0^t / lambda_0 must be a class function (character of H trivial on mu_3)
tidx = {t: n for n, t in enumerate(table)}
def act(tkey, chi):
    vals = [None] * k
    for l in range(k):
        h = reps[l]
        hp, eps = conj_data[(tkey, h)]
        vals[l] = zz_mul(zpow(eps + L[hp] - L[h]), chi[cls_of[hp]])
    vals = tuple(vals)
    assert vals in tidx, "image not an irreducible character of H"
    return vals
# check: the action is well defined on classes (compute via two different class members)
for tkey in list(Xt)[:5]:
    for l in range(0, k, 37):
        if len(classes[l]) > 1:
            h1, h2 = classes[l][0], classes[l][1]
            a1 = conj_data[(tkey, h1)]; a2 = conj_data[(tkey, h2)]
            v1 = zz_mul(zpow(a1[1] + L[a1[0]] - L[h1]), deg3[0][cls_of[a1[0]]])
            v2 = zz_mul(zpow(a2[1] + L[a2[0]] - L[h2]), deg3[0][cls_of[a2[0]]])
            assert v1 == v2
orbits3 = []; seen = set()
for chi in deg3:
    if chi in seen: continue
    orb = {chi}; fr = [chi]
    while fr:
        u = fr.pop()
        for tkey in Xt:
            v = act(tkey, u)
            if v not in orb: orb.add(v); fr.append(v)
    seen |= orb; orbits3.append(orb)
print("Ad(Q_1)-orbits on the 54 genuine 3-dimensional irreducibles of H^:",
      sorted(len(o) for o in orbits3))
# for comparison: orbits of the untwisted action (chi -> chi o Ad) on the 54, and on the 243 linear ones
def act_untw(tkey, chi):
    return tuple(chi[cls_of[conj_data[(tkey, reps[l])][0]]] for l in range(k))
def orbs(chars, action):
    out = []; seen = set()
    for chi in chars:
        if chi in seen: continue
        orb = {chi}; fr = [chi]
        while fr:
            u = fr.pop()
            for tkey in Xt:
                v = action(tkey, u)
                if v not in orb: orb.add(v); fr.append(v)
        seen |= orb; out.append(orb)
    return out
print("  (untwisted action on the 54 three-dimensional characters of H: orbit sizes",
      sorted(len(o) for o in orbs(deg3, act_untw)), ")")
lin = [t for t in table if t[id_cls][0] == 1]
print("Ad(Q_1)-orbits on the 243 genuine linear characters lambda_0*chi:", Counter(len(o) for o in orbs(lin, act)))
pickle.dump({'L': L, 'orbits3': [sorted(o) for o in orbits3]}, open('level2_clifford.pkl', 'wb'))
print("total %.0fs" % (time.time() - t00))
