"""Search for the character set Lambda: e on G_3 (D8-invariant, odd), N(h) in {11,20}?"""
import sys; sys.path.insert(0, '.')
import pickle, itertools
import numpy as np
from collections import Counter

G3 = pickle.load(open('./G3.pkl', 'rb'))['G3']
acts = pickle.load(open('./actions.pkl', 'rb'))
D8 = [np.array(g) for g in acts['D8']]; Heis = [np.array(g) for g in acts['Heis']]; Gsym = [np.array(g) for g in acts['Gsym']]
Ms = {k: np.array(v) for k, v in acts['Ms'].items()}
def apply(M, v): return tuple(int(t) for t in (M @ np.array(v)) % 3)
def neg(v): return tuple((-c) % 3 for c in v)
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

d8orbs = orbits(D8, G3)
free = []      # pairs (O, -O)
zero = []
used = set()
for o in d8orbs:
    if id(o) in used: continue
    if neg(o[0]) in o: zero.append(o); used.add(id(o))
    else:
        no = [p for p in d8orbs if neg(o[0]) in p][0]
        free.append((o, no)); used.add(id(o)); used.add(id(no))
print("D8-orbits forced e=0:", [len(o) for o in zero], "; free orbit pairs:", [(len(a), len(b)) for a, b in free])
print("x4-coordinate of vectors in forced-zero orbits:", Counter(v[2] for o in zero for v in o))
print("x4-coordinate of vectors in free orbits:", Counter(v[2] for a, b in free for v in a + b))

# all h in V^* as vectors h (h(v) = h.v mod 3)
H = list(itertools.product(range(3), repeat=5))
Vall = H
Gset = set(G3)
nongood = [v for v in Vall if v not in Gset and any(v)]
print("non-good nonzero vectors:", len(nongood))

def e_from_params(params):
    e = {}
    for o in zero:
        for v in o: e[v] = 0
    for (a, b), p in zip(free, params):
        for v in a: e[v] = p
        for v in b: e[v] = (-p) % 3
    return e

def hv(h, v): return sum(x*y for x, y in zip(h, v)) % 3

results = []
for params in itertools.product(range(3), repeat=len(free)):
    e = e_from_params(params)
    # F_e(h) = sum_{v in G3} zeta^{-(e(v)+h(v))}; equivalently count lines with h(v)= -e(v)
    Ns = []
    for h in H:
        n = sum(1 for v in G3 if hv(h, v) == (-e[v]) % 3)   # counts vectors (2 per line)
        Ns.append(n // 2)
    dist = Counter(Ns)
    ok = set(dist.keys()) <= {11, 20}
    results.append((params, dist, ok))
    print("params", params, "N(h) distribution:", sorted(dist.items()), " admissible:", ok)

# the configuration independent of e: for each h, the vector of residues h(v_l) - ?  Let us also test the
# "all defects trivial" e == 0 case explicitly and the Fourier side:  S(h) = 3*N(h) - 36.
print()
print("Check: does ANY e (not nec. D8-invariant) work?  Use the Heis-cocycle + D8 structure first:")
# Heis-constraint: for each generator s, v -> e(s v) - e(v) must be linear on G3 (extend to V^*)
def is_linear_on_G3(f):
    # solve for beta in V^* with beta(v) = f(v) for all v in G3
    for beta in H:
        if all(hv(beta, v) == f[v] % 3 for v in G3): return beta
    return None
for params, dist, ok in results:
    e = e_from_params(params)
    betas = {}
    for name in ['Ad(1+j)', 'Ad(1+ij)']:
        M = Ms[name]
        f = {v: (e[apply(M, v)] - e[v]) % 3 for v in G3}
        betas[name] = is_linear_on_G3(f)
    print("params", params, "Heis-cocycle extension exists:", betas)
pickle.dump({'results': results, 'zero': zero, 'free': free}, open('./design.pkl', 'wb'))
