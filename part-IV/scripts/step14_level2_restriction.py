"""Necessary test for Target B at level two: is Phi_rho|_{U~_3} a virtual character of U~_3 ?
Since Phi_1|_{U~_3} = lambda_0 * D with D(v) = sum_{h in Lambda} zeta^{h.v} (supported on good classes),
Phi_rho|_{U~_3} = lambda_0 * (F_rho * D), and this is a virtual character iff F_rho*D is a virtual
character of H = Q_3/Q_7.  Uses the exact character table of H from step13 (level2.pkl)."""
import sys; sys.path.insert(0, '.')
from quat import *
import pickle, numpy as np
from collections import Counter
exec(open('step13_level2.py').read().split("# ---------- the criterion")[0])   # reuse all the setup (H, table, Heis, r, ...)

des = pickle.load(open('design_0011020002.pkl', 'rb'))
Lam = des['Lambda']
def vvec(X): return V_vec(coords_P3(X))
def Dval(X):
    v = vvec(X)
    s = [0, 0]  # in Z[zeta] as (a,b)
    acc = (0, 0)
    for h in Lam:
        ex = sum(hi*vi for hi, vi in zip(h, v)) % 3
        acc = zz_add(acc, [(1, 0), (0, 1), (-1, -1)][ex])
    return acc
Dcls = [Dval(H[reps[l]]) for l in range(k)]
print("D on classes: values", Counter(Dcls))
# check D vanishes off good classes and the class function property
for l in range(k):
    if l not in good_classes: assert Dcls[l] == (0, 0), (l, Dcls[l])
    for a in classes[l]: assert Dval(H[a]) == Dcls[l]
print("D is a class function supported on the good classes")

def test_orbit_sum(O, label):
    S = [(0, 0)] * kh
    for t in O: S = [zz_add(S[l], t[l]) for l in range(kh)]
    # f = F_O * D on classes
    f = []
    for l in range(k):
        if l in good_classes:
            h = root_class[H[reps[l]]]
            f.append(zz_mul(S[hcls_of[hidx[h]]], Dcls[l]))
        else: f.append((0, 0))
    # inner products with Irr(H): <f, chi> = (1/729) sum_l |C_l| f(l) conj(chi(l))
    bad = []; mults = []
    for t in table:
        acc = (0, 0)
        for l in range(k):
            acc = zz_add(acc, zz_scal(int(sizes[l]), zz_mul(f[l], zz_conj(t[l]))))
        a, b = acc
        if a % 729 == 0 and b % 729 == 0 and b // 729 == 0:
            mults.append(a // 729)
        else:
            bad.append((t[id_cls][0], (a / 729, b / 729)))
    print("%s: %d of %d inner products integral; non-integral ones (degree, value): %s" % (
        label, len(table) - len(bad), len(table), sorted(set(bad))[:8]))
    if not bad: print("   multiplicities:", Counter(mults))
    return bad

for O in d8orbits:
    deg = sum(t[hcls_of[hid]][0] for t in O)
    test_orbit_sum(O, "orbit sum of degree %d" % deg)
# also the two 3-dimensional characters separately (not D_8-invariant, but informative)
for t in htable:
    if t[hcls_of[hid]][0] == 3:
        test_orbit_sum([t], "single 3-dim character of Heis")
