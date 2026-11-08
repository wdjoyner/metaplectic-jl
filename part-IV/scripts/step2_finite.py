"""Finite model Q/Q_7 = K^1/(K^7 U_F^{(1)}) : check the depth/goodness structure."""
import sys; sys.path.insert(0, '.')
from quat import *
from itertools import product
import pickle, time

def g_mod(a, m): return (a[0] % m, a[1] % m)

def reduce_P7(X):
    """canonical form of X in O_D / P^7 : x mod varpi^4 (=9), y mod varpi^3 (a mod 9, b mod 3)"""
    x, y = X
    x = (g_mod(x[0], 9), g_mod(x[1], 9))
    y = (g_mod(y[0], 9), g_mod(y[1], 3))
    return (x, y)

# O_F elements c mod varpi^3: c = k + m varpi with k mod 3? varpi^3 O_F = {a+b varpi: 9|a, 3|b}
OF_mod3 = [((k, 0), (m, 0)) for k in range(9) for m in range(3)]   # 27 elements of O_F/varpi^3

def F_part_zero(x):
    """is the O_F-part of x (in O_{E_0}, mod varpi^4 = 9) zero ?"""
    return x[0][0] % 9 == 0 and x[1][0] % 9 == 0

def normalize(X):
    """multiply 1+X on the right by (1 + varpi c), c in O_F/varpi^3, to kill the F-part of x; return canonical X"""
    g = d_add(D1, X)
    for c in OF_mod3:
        u = (e_add(E1, e_mul(EW, c)), E0)           # 1 + varpi c  (scalar)
        h = d_mul(g, u)
        Y = reduce_P7(d_sub(h, D1))
        if F_part_zero(Y[0]):
            return Y
    raise RuntimeError("no normalization found")

# enumerate canonical representatives of Q/Q_7:
# x = i*(3k + m varpi) with k mod 3, m mod 9 ; y = a + b varpi, a mod 9 gaussian, b mod 3 gaussian
elements = []
for k in range(3):
    for m in range(9):
        x = ((0, 3*k), (0, m))            # i*3k + i*m*varpi  -> gauss parts (0,3k) and (0,m)
        for a0 in range(9):
            for a1 in range(9):
                for b0 in range(3):
                    for b1 in range(3):
                        y = ((a0, a1), (b0, b1))
                        elements.append((x, y))
print("elements of Q/Q_7:", len(elements))
assert len(elements) == 3**9
elem_set = set(elements)

def depth(X):
    v = d_val(X)
    return min(v, 7)

t0 = time.time()
cube_of = {}
for X in elements:
    g = d_add(D1, X)
    g3 = d_mul(d_mul(g, g), g)
    Y = normalize(reduce_P7(d_sub(g3, D1)))
    assert Y in elem_set
    cube_of[X] = Y
print("cubing done in %.1fs" % (time.time() - t0))

cubes = set(cube_of.values())
print("number of distinct cubes (image of cubing in Q/Q_7):", len(cubes))
from collections import Counter
print("depth distribution of all elements:", sorted(Counter(depth(X) for X in elements).items()))
print("depth distribution of cubes:", sorted(Counter(depth(X) for X in cubes).items()))
print("injectivity (fiber sizes) of cubing:", Counter(Counter(cube_of.values()).values()))
# cubes of depth-1 elements vs depth >=2
c1 = set(cube_of[X] for X in elements if depth(X) == 1)
c2 = set(cube_of[X] for X in elements if depth(X) >= 2)
print("cubes of depth-1: %d (depths %s); cubes of depth>=2: %d (depths %s)" % (
    len(c1), sorted(Counter(depth(X) for X in c1).items()), len(c2), sorted(Counter(depth(X) for X in c2).items())))
Q6 = set(X for X in elements if depth(X) >= 6)
print("|Q_6/Q_7| =", len(Q6), "; Q_6 subset of cubes of Q_2:", Q6 <= c2, "; equal:", Q6 == c2)
# Q_6-invariance of G_3 (mod Q_7): multiply depth-3 cubes by Q_6/Q_7 elements
def mult(X, Y):
    return normalize(reduce_P7(d_sub(d_mul(d_add(D1, X), d_add(D1, Y)), D1)))
ok = True
for X in c1:
    for q in Q6:
        if mult(X, q) not in c1: ok = False
print("G_3 (mod Q_7) is invariant under Q_6/Q_7:", ok)
print("|G_3 mod Q_7| =", len(c1), " = 72 * |Q_6/Q_7| =", 72*len(Q6))
pickle.dump({'elements': elements, 'cube_of': cube_of}, open('./finite.pkl', 'wb'))
