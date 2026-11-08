import sys; sys.path.insert(0, '.')
from quat import *
from itertools import product

# --- sanity checks ---
zeta = e_add(E1, EW)                     # zeta_3 = 1 + varpi
assert e_mul(e_mul(zeta, zeta), zeta) == E1 and zeta != E1
assert e_mul(EI, EI) == e_neg(E1)
three = e_int(3)
assert e_mul(EW, EW) == e_neg(e_add(three, e_mul(three, EW)))   # varpi^2 = -3 - 3 varpi
assert d_mul(DJ, DJ) == DW                                     # j^2 = varpi
assert d_mul(DJ, DI) == d_neg(d_mul(DI, DJ))                   # j i = -i j
assert d_val(d_mul(DJ, DJ)) == 2 and d_val(DJ) == 1 and d_val(DI) == 0
assert e_val(e_int(3)) == 2 and d_val((e_int(3), E0)) == 4
print("arithmetic sanity OK")

# --- lifts of F_9 to Z[i] ---
def lift9(a): return ((a[0], a[1]), G0)   # as element of O_{E_0}

# depth-1 representatives t = 1 + (u0 + u1 varpi) j + varpi v0, u0 != 0
reps = []
for u0 in F9x:
    for u1 in F9:
        for v0 in F9:
            u = (lift9(u0)[0], lift9(u1)[0])      # u0 + u1 varpi  as (gauss, gauss)
            y = u
            x = e_add(E1, e_mul(EW, lift9(v0)))
            reps.append((x, y))
print("number of depth-1 representatives:", len(reps))

G3 = {}
for t in reps:
    assert d_val(d_sub(t, D1)) == 1
    t3 = d_pow(t, 3)
    X = d_sub(t3, D1)
    assert d_val(X) == 3, d_val(X)
    v = V_vec(coords_P3(X))
    G3.setdefault(v, 0); G3[v] += 1
print("distinct images in V of cubes of depth-1 elements:", len(G3))
print("fiber sizes:", sorted(set(G3.values())))

# compare with the closed formula
def formula_G3():
    S = set()
    for a in F9x:
        for x4 in [(0,0),(0,1),(0,2)]:
            for y in F9:
                tr = f9_tr(f9_mul(a, f9_conj(y)))
                coef = (tr + f9_mul(x4, x4)[0] - 1) % 3
                Na = f9_norm(a)
                third = f9_add(y, f9_mul(((Na*coef) % 3, 0), a))
                S.add((a[0], a[1], x4[1], third[0], third[1]))
    return S
Sf = formula_G3()
print("formula set size:", len(Sf), " equal to computed:", Sf == set(G3.keys()))

# leading coefficients and depth-4 coordinates distribution
from collections import Counter
print("A-coordinates (level 3) present:", sorted(set((v[0], v[1]) for v in G3)))
print("count by x4:", Counter(v[2] for v in G3))
# lines
lines = set()
for v in G3:
    nv = tuple((-c) % 3 for c in v)
    assert nv in G3
    lines.add(frozenset([v, nv]))
print("number of good lines:", len(lines))

import pickle
pickle.dump({'G3': sorted(G3.keys()), 'lines': [sorted(l) for l in lines]}, open('./G3.pkl', 'wb'))
