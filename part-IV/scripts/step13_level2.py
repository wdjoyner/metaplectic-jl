"""Target B at level two: the finite criterion of Proposition prop:criterion on H = Q_3/Q_7.

For every D_8-invariant character O of Heis = Q_1/Q_3 (these are the possible restrictions
Theta_rho|_{Q_1} of representations rho trivial on K^3, after the normalization of the central
character), form F_O(g) := O(r(g)) on the good classes g of H, where r is the cube root
(well defined modulo Q_3), and decide whether F_O is the restriction to the good classes of an
Ad(Q_1)-invariant *virtual* character of H (integer combination of Ad(Q_1)-orbit sums of Irr(H)).

Everything is exact except the Burnside eigenvector step, whose output is rounded to Z[zeta_3]
and then verified exactly (orthogonality relations, integrality, degrees).
"""
import sys; sys.path.insert(0, '.')
from quat import *
import pickle, time, itertools, random
import numpy as np
from fractions import Fraction
import sympy
from sympy import Matrix, ZZ
from sympy.matrices.normalforms import hermite_normal_form

t00 = time.time()
fin = pickle.load(open('finite.pkl', 'rb'))
elements, cube_of = fin['elements'], fin['cube_of']
elem_index = {X: k for k, X in enumerate(elements)}

def g_mod(a, m): return (a[0] % m, a[1] % m)
def reduce_P7(X):
    x, y = X
    return ((g_mod(x[0], 9), g_mod(x[1], 9)), (g_mod(y[0], 9), g_mod(y[1], 3)))
def F_part_zero(x): return x[0][0] % 9 == 0 and x[1][0] % 9 == 0
OF_mod3 = [((k, 0), (m, 0)) for k in range(9) for m in range(3)]
def normalize(X):
    g = d_add(D1, X)
    for c in OF_mod3:
        u = (e_add(E1, e_mul(EW, c)), E0)
        Y = reduce_P7(d_sub(d_mul(g, u), D1))
        if F_part_zero(Y[0]): return Y
    raise RuntimeError
def mult(X, Y):
    return normalize(reduce_P7(d_sub(d_mul(d_add(D1, X), d_add(D1, Y)), D1)))
def depth(X): return min(d_val(X), 7)
def inverse(X):
    # (1+X)^{-1} = sum (-X)^k, k<7, since X^7 in P^7
    S = D1; P = D1; mX = d_neg(X)
    for _ in range(1, 7):
        P = d_mul(P, mX); S = d_add(S, P)
    return normalize(reduce_P7(d_sub(S, D1)))
def scale_int(X, s):
    (x0, x1), (y0, y1) = X
    f = lambda g: (g[0]*s, g[1]*s)
    return ((f(x0), f(x1)), (f(y0), f(y1)))
def Ad_1pi(X):
    # (1+i)(1+X)(1-i)/2 - 1 = (1+i) X (1-i) / 2 ;  1/2 = 5 mod 9
    opi = (e_add(E1, EI), E0); omi = (e_sub(E1, EI), E0)
    Y = d_mul(d_mul(opi, X), omi)
    return normalize(reduce_P7(scale_int(Y, 5)))
def Ad_j(X): return normalize(reduce_P7(d_sigma_conj_j(X)))

# ---------- H = Q_3/Q_7 ----------
H = [X for X in elements if depth(X) >= 3]
assert len(H) == 729
Hidx = {X: k for k, X in enumerate(H)}
import os
if os.path.exists('H_multtable.npy'):
    MT = np.load('H_multtable.npy')
else:
    print("building multiplication table of H (729 elements) ...")
    t0 = time.time()
    MT = np.zeros((729, 729), dtype=np.int16)
    for a, X in enumerate(H):
        for b, Y in enumerate(H):
            MT[a, b] = Hidx[mult(X, Y)]
    np.save('H_multtable.npy', MT)
    print("  done in %.0fs" % (time.time() - t0))
e_id = Hidx[(((0, 0), (0, 0)), ((0, 0), (0, 0)))]
INV = np.zeros(729, dtype=np.int16)
for a in range(729):
    INV[a] = int(np.where(MT[a] == e_id)[0][0])
# sanity: associativity on random triples
for _ in range(2000):
    a, b, c = [random.randrange(729) for _ in range(3)]
    assert MT[MT[a, b], c] == MT[a, MT[b, c]]
print("H is a group (assoc. sampled), identity index", e_id)

# ---------- conjugacy classes of H ----------
def conj_class_partition(conj_maps):
    """orbits of {0..728} under the given list of permutations"""
    seen = [-1] * 729; classes = []
    for a in range(729):
        if seen[a] >= 0: continue
        orb = [a]; seen[a] = len(classes); fr = [a]
        while fr:
            x = fr.pop()
            for pm in conj_maps:
                y = pm[x]
                if seen[y] < 0: seen[y] = len(classes); orb.append(y); fr.append(y)
        classes.append(orb)
    return classes, seen
# inner conjugation permutations by generators of H (use all elements for safety -- cheap)
inner_perms = []
for g in range(729):
    gi = INV[g]
    inner_perms.append([MT[MT[g, x], gi] for x in range(729)])
classes, cls_of = conj_class_partition(inner_perms)
k = len(classes)
print("number of conjugacy classes of H:", k, "; class sizes:", sorted(set(len(c) for c in classes)))

# ---------- Burnside: character table ----------
reps = [c[0] for c in classes]
sizes = np.array([len(c) for c in classes])
# class multiplication constants c[j][i][l] = #{(a in C_j, b in C_i): a b = rep_l}
print("class multiplication constants ...")
t0 = time.time()
Cmats = np.zeros((k, k, k))
for j in range(k):
    for a in classes[j]:
        # for each rep l, b = a^{-1} rep_l ; its class i
        ai = INV[a]
        for l in range(k):
            b = MT[ai, reps[l]]
            Cmats[j, cls_of[b], l] += 1
print("  done in %.0fs" % (time.time() - t0))
rng = np.random.default_rng(7)
Mrand = sum(rng.normal() * Cmats[j] for j in range(k))
w, Vv = np.linalg.eig(Mrand)
# eigenvectors v (columns) with v_l = omega(K_l); normalize v_{identity class} = 1
id_cls = cls_of[e_id]
chars = []
zeta = np.exp(2j * np.pi / 3)
def round_Zzeta(z):
    b = 2 * z.imag / np.sqrt(3); a = z.real + b / 2
    ar, br = int(round(a)), int(round(b))
    val = ar + br * zeta
    return (ar, br), abs(val - z)
for col in range(k):
    v = Vv[:, col] / Vv[id_cls, col]
    s2 = sum(abs(v[l]) ** 2 / sizes[l] for l in range(k))
    deg = np.sqrt(729 / s2)
    chi = [deg * v[l] / sizes[l] for l in range(k)]
    rounded = []; err = 0
    for z in chi:
        r, e = round_Zzeta(z); rounded.append(r); err = max(err, e)
    chars.append((rounded, err))
maxerr = max(e for _, e in chars)
print("max rounding error of character values:", "%.2e" % maxerr)
assert maxerr < 1e-6
# exact arithmetic in Z[zeta]: (a,b) <-> a + b zeta, zeta^2 = -1 - zeta
def zz_mul(u, v):
    a, b = u; c, d = v
    return (a*c - b*d, a*d + b*c - b*d)
def zz_add(u, v): return (u[0]+v[0], u[1]+v[1])
def zz_conj(u): a, b = u; return (a - b, -b)   # conj(zeta) = zeta^2 = -1 - zeta
def zz_scal(s, u): return (s*u[0], s*u[1])
table = [c for c, _ in chars]
# verify: distinct, degrees positive integers, orthogonality  sum_l |C_l| chi(l) conj(chi'(l)) = 729 delta
table = sorted(set(tuple(t) for t in table))
assert len(table) == k, (len(table), k)
for t in table:
    assert t[id_cls][1] == 0 and t[id_cls][0] > 0
for s in table:
    for t in table:
        acc = (0, 0)
        for l in range(k):
            acc = zz_add(acc, zz_scal(int(sizes[l]), zz_mul(s[l], zz_conj(t[l]))))
        assert acc == ((729, 0) if s == t else (0, 0)), (s[id_cls], t[id_cls], acc)
degs = sorted(t[id_cls][0] for t in table)
from collections import Counter
print("character table verified exactly; degrees:", dict(Counter(degs)), "; sum of squares:", sum(d*d for d in degs))

# ---------- Ad(Q_1) action on H and on Irr(H) ----------
# representatives of Q_1/Q_3: canonical elements of Q/Q_7 with (x mod varpi^2, y mod varpi) taking all 27 values
def heis_class(X):
    (x0, x1), (y0, y1) = X
    return (x1[1] % 3, (y0[0] % 3, y0[1] % 3))      # (m mod 3, a mod 3 in F_9)
Q1reps = {}
for X in elements:
    h = heis_class(X)
    if h not in Q1reps: Q1reps[h] = X
assert len(Q1reps) == 27
def conj_perm(T):
    Ti = inverse(T)
    return [Hidx[mult(mult(T, X), Ti)] for X in H]
Ad_perms = [conj_perm(T) for T in Q1reps.values()]
def char_perm(t, perm):
    """character chi^T(g) = chi(T^{-1} g T): class function values permuted"""
    out = [None] * k
    for l in range(k):
        g = reps[l]
        # chi^T(g) := chi(T g T^{-1}) ; perm sends x -> T x T^{-1}
        out[l] = t[cls_of[perm[g]]]
    return tuple(out)
tset = {t: n for n, t in enumerate(table)}
orbits = []; seen = set()
for t in table:
    if t in seen: continue
    orb = {t}; fr = [t]
    while fr:
        u = fr.pop()
        for pm in Ad_perms:
            v = char_perm(u, pm)
            assert v in tset
            if v not in orb: orb.add(v); fr.append(v)
    seen |= orb; orbits.append(sorted(orb))
print("Ad(Q_1)-orbits on Irr(H):", len(orbits), "; orbit sizes:", dict(Counter(len(o) for o in orbits)))
orbit_sums = []
for o in orbits:
    S = [(0, 0)] * k
    for t in o:
        S = [zz_add(S[l], t[l]) for l in range(k)]
    orbit_sums.append(S)

# ---------- good classes and the cube root ----------
good = sorted(set(cube_of[T] for T in elements))
good = [g for g in good if depth(g) >= 3]
assert len(good) == 219
root_class = {}
for T in elements:
    g = cube_of[T]
    h = heis_class(T)
    if g in root_class: assert root_class[g] == h, "cube root mod Q_3 not well defined!"
    else: root_class[g] = h
print("cube root modulo Q_3 is well defined on the %d good classes" % len(good))
# good classes are unions of H-conjugacy classes?  F_O is a class function on H only if so
good_set = set(Hidx[g] for g in good)
good_classes = [l for l in range(k) if reps[l] in good_set]
assert all(set(classes[l]) <= good_set for l in good_classes)
# and r is constant on H-classes (and Ad(Q_1)-invariant)
for l in good_classes:
    hs = set(root_class[H[a]] for a in classes[l]); assert len(hs) == 1
for T, pm in zip(Q1reps.values(), Ad_perms):
    Ti = inverse(T)
    for g in good:
        # equivariance: r(T g T^{-1}) = T r(g) T^{-1}  in Heis
        lhs = root_class[H[pm[Hidx[g]]]]
        rhs = heis_class(mult(mult(T, Q1reps[root_class[g]]), Ti))
        assert lhs == rhs
print("good set = union of %d H-classes; r is Ad(Q_1)-equivariant" % len(good_classes))

# ---------- Heis = Q_1/Q_3, its irreducible characters, D_8 action ----------
hreps = list(Q1reps.keys()); hidx = {h: n for n, h in enumerate(hreps)}
def hmul(a, b): return heis_class(mult(Q1reps[a], Q1reps[b]))
HM = [[hidx[hmul(a, b)] for b in hreps] for a in hreps]
hid = hidx[heis_class(elements[0] if heis_class(elements[0]) == (0, (0, 0)) else (((0,0),(0,0)),((0,0),(0,0))))]
hid = hidx[(0, (0, 0))]
HINV = [HM[a].index(hid) for a in range(27)]
hinner = [[HM[HM[g][x]][HINV[g]] for x in range(27)] for g in range(27)]
def partition27(perms):
    seen = [-1]*27; cls = []
    for a in range(27):
        if seen[a] >= 0: continue
        orb = [a]; seen[a] = len(cls); fr = [a]
        while fr:
            x = fr.pop()
            for pm in perms:
                y = pm[x]
                if seen[y] < 0: seen[y] = len(cls); orb.append(y); fr.append(y)
        cls.append(orb)
    return cls, seen
hcls, hcls_of = partition27(hinner)
kh = len(hcls); hr = [c[0] for c in hcls]; hsz = np.array([len(c) for c in hcls])
C2 = np.zeros((kh, kh, kh))
for j in range(kh):
    for a in hcls[j]:
        for l in range(kh):
            b = HM[HINV[a]][hr[l]]; C2[j, hcls_of[b], l] += 1
Mr = sum(rng.normal() * C2[j] for j in range(kh))
w2, V2 = np.linalg.eig(Mr)
htable = []
for col in range(kh):
    v = V2[:, col] / V2[hcls_of[hid], col]
    s2 = sum(abs(v[l])**2 / hsz[l] for l in range(kh)); deg = np.sqrt(27 / s2)
    chi = [deg * v[l] / hsz[l] for l in range(kh)]
    r = tuple(round_Zzeta(z)[0] for z in chi); htable.append(r)
htable = sorted(set(htable)); assert len(htable) == kh
print("Irr(Heis): %d characters, degrees %s" % (kh, sorted(t[hcls_of[hid]][0] for t in htable)))
# D_8 generators on Heis
def heis_perm(f):
    return [hidx[heis_class(f(Q1reps[h]))] for h in hreps]
P_i = heis_perm(Ad_1pi); P_j = heis_perm(Ad_j)
# check they are automorphisms of Heis
for a in range(27):
    for b in range(27):
        for P in (P_i, P_j):
            assert HM[P[a]][P[b]] == P[HM[a][b]]
def hchar_perm(t, P):
    return tuple(t[hcls_of[P[hr[l]]]] for l in range(kh))
hts = set(htable); d8orbits = []; seen = set()
for t in htable:
    if t in seen: continue
    orb = {t}; fr = [t]
    while fr:
        u = fr.pop()
        for P in (P_i, P_j):
            v = hchar_perm(u, P); assert v in hts
            if v not in orb: orb.add(v); fr.append(v)
    seen |= orb; d8orbits.append(sorted(orb))
print("D_8-orbits on Irr(Heis):", [(len(o), o[0][hcls_of[hid]][0]) for o in d8orbits])

# ---------- the criterion: solve  sum_k n_k Psi_k(g) = F_O(g)  on good classes, n_k in Z ----------
def to_int_rows(vals):
    """list of Z[zeta] values -> two integer rows (coefficient of 1, of zeta)"""
    return [v[0] for v in vals], [v[1] for v in vals]
# matrix A: rows = (good class, component), cols = orbit sums
rowsA = []
for l in good_classes:
    for comp in (0, 1):
        rowsA.append([S[l][comp] for S in orbit_sums])
A = Matrix(rowsA)
print("criterion matrix: %d equations, %d unknowns, rank %d" % (A.rows, A.cols, A.rank()))

from zsolve import zsolve
def integer_solve(A, b):
    Al = [[int(x) for x in A.row(i)] for i in range(A.rows)]
    bl = [int(x) for x in b]
    st, n = zsolve(Al, bl)
    if st == 'solution': return Matrix(n), 'integer solution'
    return None, st

results = []
for O in d8orbits:
    S = [(0, 0)] * kh
    for t in O: S = [zz_add(S[l], t[l]) for l in range(kh)]
    # F_O on good classes: O(r(g))
    bvec = []
    for l in good_classes:
        h = root_class[H[reps[l]]]
        val = S[hcls_of[hidx[h]]]
        bvec.extend([val[0], val[1]])
    b = Matrix(bvec)
    n, status = integer_solve(A, b)
    deg = S[hcls_of[hid]][0]
    results.append((deg, len(O), status, None if n is None else [int(x) for x in n]))
    print("orbit sum of degree %2d (|orbit|=%d): %s" % (deg, len(O), status if n is None else "integer solution; nonzero coefficients " + str([(i,int(x)) for i,x in enumerate(n) if x != 0])))

pickle.dump({'table': table, 'classes': classes, 'orbits': orbits, 'results': results,
             'good_classes': good_classes, 'root_class': root_class}, open('level2.pkl', 'wb'))
print("total time %.0fs" % (time.time() - t00))
