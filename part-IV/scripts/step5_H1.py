"""(a) Lazard form on K^4/K^8 = O_D/3O_D : invariant alternating forms vanishing on torus subspaces.
   (b) odd functions on Q_6/Q_8 with equivariant non-additivity, modulo linear functions."""
import sys; sys.path.insert(0, '.')
from quat import *
import numpy as np, itertools

# ---------- F_3 linear algebra helpers ----------
def rref_mod3(M):
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
    return M[:r], piv
def nullspace_mod3(M):
    M = np.array(M, dtype=int) % 3
    R, piv = rref_mod3(M)
    cols = M.shape[1]; free = [c for c in range(cols) if c not in piv]
    basis = []
    for f in free:
        v = np.zeros(cols, dtype=int); v[f] = 1
        for i, p in enumerate(piv):
            v[p] = (-R[i, f]) % 3
        basis.append(v)
    return basis

# ---------- (a) W = O_D/3 O_D, basis: pi^k, i pi^k (k=0..3) ----------
# represent an element of O_D by exact arithmetic; reduce mod 3 to coordinates in F_3^8.
def pi_pow(k): return d_pow(DJ, k)
Wbasis = []
for k in range(4):
    Wbasis.append(pi_pow(k)); Wbasis.append(d_mul(DI, pi_pow(k)))
def coords_mod3(X):
    """coordinates of X in O_D/3O_D w.r.t. Wbasis.  O_D = O_{E0} + O_{E0} j, O_{E0}/3 = F_9 + F_9 varpi,
       and pi^2 = varpi, pi^3 = varpi j.  So X = x + y j, x = a + b varpi, y = c + d varpi:
       x -> a*1 + b*pi^2 ; y j -> c*pi + d*pi^3  (c,d in F_9 = F_3 + F_3 i)."""
    x, y = X
    a, b = x; c, d = y
    a = g_red3(a); b = g_red3(b); c = g_red3(c); d = g_red3(d)
    # basis order: [1, i, pi, i pi, pi^2, i pi^2, pi^3, i pi^3]
    return np.array([a[0], a[1], c[0], c[1], b[0], b[1], d[0], d[1]]) % 3
# sanity: coordinates of basis elements
for k, b in enumerate(Wbasis):
    v = coords_mod3(b); assert v[k] == 1 and v.sum() == 1, (k, v)

# alternating forms: unknowns w_{ab} for a<b (28); omega(u,v) = sum_{a<b} w_ab (u_a v_b - u_b v_a)
pairs = [(a, b) for a in range(8) for b in range(a+1, 8)]
def form_row(u, v):
    return np.array([(u[a]*v[b] - u[b]*v[a]) % 3 for (a, b) in pairs])

constraints = []
# torus subspaces: O_F[x]/3 = span{1, varpi, x, varpi x} for pure x of valuation 0 or 1 (mod 3)
def lift9(a): return ((a[0], a[1]), G0)
pure_list = []
for a0 in F9:                      # x = (a) + (b) j with a in i O_F : a = i*(s + t varpi)
    pass
for s in range(3):
    for t in range(3):
        a = ((0, s), (0, t))       # i*s + i*t*varpi
        for c in F9:
            for d in F9:
                y = (lift9(c)[0], lift9(d)[0])
                X = (a, y)
                if d_val(X) in (0, 1): pure_list.append(X)
print("pure quaternions mod 3 of valuation 0 or 1:", len(pure_list))
vp = (EW, E0)
for X in pure_list:
    T = [D1, vp, X, d_mul(vp, X)]
    T = [coords_mod3(t) for t in T]
    for u, v in itertools.combinations(T, 2):
        constraints.append(form_row(u, v))
# invariance under conjugation: Ad(g) for g in generators
def ad_mod3(g, ginv):
    cols = [coords_mod3(d_mul(d_mul(g, b), ginv)) for b in Wbasis]
    return np.array(cols).T % 3
def inv_series(s, terms=9):
    n = d_sub(s, D1); R = D1; P = D1
    for k in range(1, terms):
        P = d_mul(P, d_neg(n)); R = d_add(R, P)
    return R
gens = []
for k in range(1, 4):
    for a in [D1, DI]:
        g = d_add(D1, d_mul(a, pi_pow(k))); gens.append(ad_mod3(g, inv_series(g)))
gens.append(ad_mod3(DI, d_neg(DI)))                       # Ad(i)
# Ad(1+i): inverse (1-i)/2 ; use 2*(...) trick: Ad(xi) X = xi X (1-i) * 2^{-1}, 2^{-1} = 2 mod 3
cols = [ (2*coords_mod3(d_mul(d_mul(d_add(D1, DI), b), d_sub(D1, DI)))) % 3 for b in Wbasis]
gens.append(np.array(cols).T % 3)
cols = [coords_mod3(d_sigma_conj_j(b)) for b in Wbasis]; gens.append(np.array(cols).T % 3)   # Ad(j)
# also Ad(1 + varpi) acts trivially (central); fine.
# invariance constraint: omega(gu, gv) = omega(u,v) for basis u,v
for M in gens:
    for (a, b) in pairs:
        u = np.zeros(8, dtype=int); u[a] = 1; v = np.zeros(8, dtype=int); v[b] = 1
        gu = (M @ u) % 3; gv = (M @ v) % 3
        constraints.append((form_row(gu, gv) - form_row(u, v)) % 3)
sol = nullspace_mod3(np.array(constraints))
print("(a) dimension of invariant alternating forms on K^4/K^8 vanishing on torus subspaces:", len(sol))
# for information: without invariance
sol_t = nullspace_mod3(np.array(constraints[:len(constraints) - len(gens)*len(pairs)]))
print("    (torus-vanishing alone, no invariance):", len(sol_t))

# ---------- (b) odd functions on Q_6/Q_8 = F_3^3 with equivariant defects ----------
# Q_6/Q_8 = (F_9/F_3) (level 6, coordinate alpha with a = alpha i) + F_9 (level 7, b = b1 + b2 i)
# generators (derived above): Ad(1+j): (al,b) -> (al, b + al i); Ad(1+ij): (al,b) -> (al, b - al);
# Ad(1+i): b -> i b ; Ad(j): (al,b) -> (-al, sigma b); Ad(i): b -> -b.
# We recompute these numerically from O_D to be safe.
def coords_Q68(X):
    """X in P^6: X = varpi^3 (a + b j) mod P^8, a mod varpi (F_9), b mod varpi (F_9); return (a, b)"""
    assert d_val(X) >= 6
    x, y = X
    a = e_red(e_div_varpi(e_div_varpi(e_div_varpi(x))))
    b = e_red(e_div_varpi(e_div_varpi(e_div_varpi(y))))
    return a, b
W3 = e_mul(e_mul(EW, EW), EW)
B68 = [ (e_mul(W3, EI), E0), (E0, W3), (E0, e_mul(W3, EI)) ]   # alpha-direction (varpi^3 i), b=1, b=i
def vec68(X):
    a, b = coords_Q68(X)
    return np.array([a[1], b[0], b[1]]) % 3     # drop a[0] (scalar line)
for k, bb in enumerate(B68):
    v = vec68(bb); assert v[k] == 1 and v.sum() == 1
def act68(g, ginv=None, half=False, isj=False):
    cols = []
    for bb in B68:
        Y = d_sigma_conj_j(bb) if isj else d_mul(d_mul(g, bb), ginv)
        v = vec68(Y)
        if half: v = (2*v) % 3
        cols.append(v)
    return np.array(cols).T % 3
gens68 = []
for k in range(1, 3):
    for a in [D1, DI]:
        g = d_add(D1, d_mul(a, pi_pow(k))); gens68.append(act68(g, inv_series(g)))
gens68.append(act68(DI, d_neg(DI)))
gens68.append(act68(d_add(D1, DI), d_sub(D1, DI), half=True))
gens68.append(act68(None, isj=True))
for M in gens68: print(M.tolist())
pts = list(itertools.product(range(3), repeat=3))
idx = {p: n for n, p in enumerate(pts)}
# unknowns: f(p) for p != 0 (26 unknowns), f(0)=0; plus for each generator a linear functional l_g (3 unknowns) with
# f(gp) - f(p) = l_g . p  for all p.  Odd: f(-p) = -f(p).
nvar = 26 + 3*len(gens68)
rows = []
def var_f(p):
    if p == (0,0,0): return None
    return idx[p] - 1 if idx[p] > idx[(0,0,0)] else idx[p]
# simpler: index f-variables by position in pts excluding origin
f_index = {}
cnt = 0
for p in pts:
    if p != (0,0,0): f_index[p] = cnt; cnt += 1
for p in pts:
    if p == (0,0,0): continue
    q = tuple((-c) % 3 for c in p)
    row = np.zeros(nvar, dtype=int); row[f_index[p]] += 1; row[f_index[q]] += 1; rows.append(row % 3)
for gi, M in enumerate(gens68):
    for p in pts:
        if p == (0,0,0): continue
        gp = tuple(int(t) for t in (M @ np.array(p)) % 3)
        row = np.zeros(nvar, dtype=int)
        if gp != (0,0,0): row[f_index[gp]] += 1
        row[f_index[p]] -= 1
        for c in range(3): row[26 + 3*gi + c] -= p[c]
        rows.append(row % 3)
sol68 = nullspace_mod3(np.array(rows))
# project to f-part and quotient by linear functions
fsols = [s[:26] for s in sol68]
lin = []
for l in itertools.product(range(3), repeat=3):
    v = np.zeros(26, dtype=int)
    for p in pts:
        if p != (0,0,0): v[f_index[p]] = sum(a*b for a, b in zip(l, p)) % 3
    lin.append(v)
allv = np.array(fsols + lin) if fsols else np.array(lin)
rk_all = len(rref_mod3(allv)[0]); rk_lin = len(rref_mod3(np.array(lin))[0])
print("(b) odd functions on Q_6/Q_8 with equivariant defects: solution dim", len(fsols),
      "; modulo linear functions:", rk_all - rk_lin)
