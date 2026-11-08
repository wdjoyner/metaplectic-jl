"""Actions of generators of D^x/F^x K^3 on V = Q_3/Q_6, orbits on G_3, coplanar triples."""
import sys; sys.path.insert(0, '.')
from quat import *
import pickle, itertools
import numpy as np

G3 = pickle.load(open('./G3.pkl', 'rb'))['G3']
G3set = set(G3)

# basis elements of P^3/P^6 (mod the F_3-line in C)
W2 = e_mul(EW, EW)
basis = [ (E0, EW),                 # varpi j          -> A = 1
          (E0, e_mul(EW, EI)),      # varpi i j        -> A = i
          (e_mul(W2, EI), E0),      # varpi^2 i        -> C = i
          (E0, W2),                 # varpi^2 j        -> B = 1
          (E0, e_mul(W2, EI)) ]     # varpi^2 i j      -> B = i
for k, b in enumerate(basis):
    v = V_vec(coords_P3(b)); assert v == tuple(1 if t == k else 0 for t in range(5)), (k, v)

def inv_unit_series(s, terms=9):
    """inverse of s = 1 + n with n in P_D, via geometric series (exact enough mod P^9)"""
    n = d_sub(s, D1)
    assert d_val(n) >= 1
    R = D1; P = D1
    for k in range(1, terms):
        P = d_mul(P, d_neg(n))
        R = d_add(R, P)
    return R

def ad_matrix(s, sinv=None, half=False):
    """matrix (mod 3) of X -> s X s^{-1} on V, columns = images of basis"""
    cols = []
    for b in basis:
        if sinv is None:
            Y = d_sigma_conj_j(b)             # for s = j
        else:
            Y = d_mul(d_mul(s, b), sinv)
        v = list(V_vec(coords_P3(Y)))
        if half: v = [(2*t) % 3 for t in v]   # divide by 2
        cols.append(v)
    M = np.array(cols, dtype=int).T % 3
    return M

s1 = d_add(D1, DJ)                          # 1 + j
s2 = d_add(D1, d_mul(DI, DJ))               # 1 + i j
xi = d_add(D1, DI)                          # 1 + i  (unit, inverse (1 - i)/2)
xi_inv_times2 = d_sub(D1, DI)
Ms = {
 'Ad(1+j)': ad_matrix(s1, inv_unit_series(s1)),
 'Ad(1+ij)': ad_matrix(s2, inv_unit_series(s2)),
 'Ad(1+i)': ad_matrix(xi, xi_inv_times2, half=True),
 'Ad(j)': ad_matrix(None),
 'Ad(i)': ad_matrix(DI, d_neg(DI)),
}
def apply(M, v): return tuple(int(t) for t in (M @ np.array(v)) % 3)
for name, M in Ms.items():
    img = set(apply(M, v) for v in G3)
    print(name, "preserves G3:", img == G3set, "\n", M)
# check orders / relations
def mpow(M, k):
    R = np.eye(5, dtype=int)
    for _ in range(k): R = (R @ M) % 3
    return R
I5 = np.eye(5, dtype=int)
print("Ad(1+i)^2 == Ad(i):", np.array_equal(mpow(Ms['Ad(1+i)'], 2), Ms['Ad(i)']))
print("Ad(i)^2 = 1:", np.array_equal(mpow(Ms['Ad(i)'], 2), I5), " Ad(j)^2 = 1:", np.array_equal(mpow(Ms['Ad(j)'], 2), I5))
print("Ad(1+j)^3 = 1:", np.array_equal(mpow(Ms['Ad(1+j)'], 3), I5), " Ad(1+ij)^3 = 1:", np.array_equal(mpow(Ms['Ad(1+ij)'], 3), I5))

# generate the group G_sym acting on V
def gen_group(gens):
    gens = [tuple(map(tuple, g)) for g in gens]
    seen = {tuple(map(tuple, I5))}
    frontier = [tuple(map(tuple, I5))]
    while frontier:
        new = []
        for g in frontier:
            for h in gens:
                p = tuple(map(tuple, (np.array(g) @ np.array(h)) % 3))
                if p not in seen:
                    seen.add(p); new.append(p)
        frontier = new
    return [np.array(g) for g in seen]
Heis = gen_group([Ms['Ad(1+j)'], Ms['Ad(1+ij)']])
D8 = gen_group([Ms['Ad(1+i)'], Ms['Ad(j)']])
Gsym = gen_group([Ms['Ad(1+j)'], Ms['Ad(1+ij)'], Ms['Ad(1+i)'], Ms['Ad(j)']])
print("|image of Heis on V| =", len(Heis), " |image of D8| =", len(D8), " |image of G_sym| =", len(Gsym))

def orbits(group, pts):
    pts = set(pts); orbs = []
    while pts:
        p = pts.pop(); orb = {p}; fr = [p]
        while fr:
            q = fr.pop()
            for g in group:
                r = apply(g, q)
                if r not in orb: orb.add(r); fr.append(r)
        pts -= orb; orbs.append(sorted(orb))
    return orbs
for name, grp in [('Heis', Heis), ('D8', D8), ('Gsym', Gsym)]:
    orbs = orbits(grp, G3)
    print(name, "orbits on the 72 good vectors: sizes", sorted(len(o) for o in orbs))
    # orbits on lines
    lines = set(frozenset([v, tuple((-c) % 3 for c in v)]) for v in G3)
    lorbs = orbits([g for g in grp], [min(l) for l in lines])  # action on representatives not closed; do properly:
def line_orbits(grp):
    lines = set(frozenset([v, tuple((-c) % 3 for c in v)]) for v in G3)
    lines = set(lines); orbs = []
    while lines:
        l = lines.pop(); orb = {l}; fr = [l]
        while fr:
            q = fr.pop()
            for g in grp:
                r = frozenset(apply(g, v) for v in q)
                if r not in orb: orb.add(r); fr.append(r)
        lines -= orb; orbs.append(orb)
    return orbs
for name, grp in [('Heis', Heis), ('D8', D8), ('Gsym', Gsym)]:
    print(name, "orbits on the 36 lines: sizes", sorted(len(o) for o in line_orbits(grp)))

# D8-orbits on vectors: which contain -v ?
d8orbs = orbits(D8, G3)
n_selfneg = sum(1 for o in d8orbs if tuple((-c) % 3 for c in o[0]) in o)
print("D8 vector-orbits:", len(d8orbs), "; containing -v:", n_selfneg)

# coplanar ordered triples of distinct good lines
lines = sorted(set(frozenset([v, tuple((-c) % 3 for c in v)]) for v in G3), key=lambda l: sorted(l))
reps = [sorted(l)[0] for l in lines]
def rank3(vs):
    M = np.array(vs) % 3
    # gaussian elimination mod 3
    M = M.copy(); r = 0; rows, cols = M.shape
    for c in range(cols):
        piv = None
        for i in range(r, rows):
            if M[i, c] % 3: piv = i; break
        if piv is None: continue
        M[[r, piv]] = M[[piv, r]]
        inv = 1 if M[r, c] == 1 else 2
        M[r] = (M[r]*inv) % 3
        for i in range(rows):
            if i != r and M[i, c]: M[i] = (M[i] - M[i, c]*M[r]) % 3
        r += 1
    return r
B = 0
for a, b, c in itertools.permutations(range(36), 3):
    if rank3([reps[a], reps[b], reps[c]]) == 2: B += 1
print("ordered coplanar triples of distinct good lines, B =", B, "; unordered:", B // 6)
# how many planes spanned by pairs of good lines contain a third good line?
pickle.dump({'Ms': {k: v.tolist() for k, v in Ms.items()}, 'Heis': [g.tolist() for g in Heis],
             'D8': [g.tolist() for g in D8], 'Gsym': [g.tolist() for g in Gsym], 'B': B}, open('./actions.pkl', 'wb'))
