import sys; sys.path.insert(0, '.')
from cover import *
import random, time, pickle
import numpy as np

t0 = time.time()
solsE, pairsE, solsF, pairsF = build_symbols(seed=7, nE=3000, nF=1500)
print("Steinberg solution space dims: E_0:", len(solsE), " F:", len(solsF), " (%.1fs)" % (time.time()-t0))
assert len(solsE) == 1 and len(solsF) == 1
AE = form_from(solsE[0], pairsE, 6); AF = form_from(solsF[0], pairsF, 4)
print("A_E =\n", AE); print("A_F =\n", AF)
# nondegeneracy
def rank3(M):
    M = np.array(M) % 3; M = M.copy(); r = 0; rows, cols = M.shape
    for c in range(cols):
        piv = None
        for i in range(r, rows):
            if M[i, c]: piv = i; break
        if piv is None: continue
        M[[r, piv]] = M[[piv, r]]; M[r] = (M[r]*(1 if M[r, c] == 1 else 2)) % 3
        for i in range(rows):
            if i != r and M[i, c]: M[i] = (M[i] - M[i, c]*M[r]) % 3
        r += 1
    return r
print("rank A_E =", rank3(AE), " rank A_F =", rank3(AF))

rng = random.Random(11)
# Galois invariance of the E symbol
ok = all(int(cls_E(a) @ AE @ cls_E(b)) % 3 == int(cls_E(e_sigma(a)) @ AE @ cls_E(e_sigma(b))) % 3
         for a, b in [(random_E_element(rng), random_E_element(rng)) for _ in range(300)])
print("Galois invariance of (,)_E:", ok)
# norm compatibility: (a,b)_E = (a, N b)_F for a in F, fixes relative sign
signs = set()
for _ in range(300):
    a = random_F_element(rng); b = random_E_element(rng)
    lhs = int(cls_E(a) @ AE @ cls_E(b)) % 3
    rhs = int(cls_F(a) @ AF @ cls_F(e_norm_to_F(b))) % 3
    if lhs == rhs: signs.add(+1)
    elif lhs == (-rhs) % 3: signs.add(-1)
    else: signs.add(0)
print("norm compatibility sign set:", signs)
if signs == {-1}:
    AF = (-AF) % 3; print("flipped sign of A_F")
sym = Symbols(AE, AF)
# (a,b)_E = (a,b)_F^2 for a,b in F
ok = all(sym.hE(a, b) == (2*sym.hF(a, b)) % 3 for a, b in [(random_F_element(rng), random_F_element(rng)) for _ in range(200)])
print("(a,b)_E = (a,b)_F^2 on F x F:", ok)
# known values: (zeta, zeta)=1 (alternating), (varpi, zeta)? , (varpi,varpi)=(varpi,-1)=1
print("h_F(varpi,varpi) =", sym.hF(EW, EW), " h_F(varpi, zeta) =", sym.hF(EW, ZETA), " h_F(zeta, 1+varpi^2)=", sym.hF(ZETA, e_add(E1, e_mul(EW, EW))))
print("h_F(1+varpi, 1+varpi^2) =", sym.hF(e_add(E1, EW), e_add(E1, e_mul(EW, EW))), " h_F(varpi, 1+varpi^3) =", sym.hF(EW, e_add(E1, e_pow(EW, 3))))

# ---- KP cocycle: cocycle identity on random matrices ----
cov = Cover(sym, cv=2, relabel=False)
def rand_mat(rng):
    while True:
        A = ((random_E_element(rng, 3), random_E_element(rng, 3)), (random_E_element(rng, 3), random_E_element(rng, 3)))
        if rng.random() < 0.3: A = ((A[0][0], A[0][1]), (E0, A[1][1]))      # sometimes c = 0
        if not e_zero(m_det(A)): return A
bad = 0; t0 = time.time()
for _ in range(150):
    g, h, k = rand_mat(rng), rand_mat(rng), rand_mat(rng)
    lhs = (cov.sigma(g, h) + cov.sigma(m_mul(g, h), k)) % 3
    rhs = (cov.sigma(g, m_mul(h, k)) + cov.sigma(h, k)) % 3
    if lhs != rhs: bad += 1
print("KP cocycle identity failures (sigma, parameter 0):", bad, "/150  (%.1fs)" % (time.time()-t0))
bad = 0
for _ in range(100):
    g, h, k = rand_mat(rng), rand_mat(rng), rand_mat(rng)
    lhs = (cov.beta(g, h) + cov.beta(m_mul(g, h), k)) % 3
    rhs = (cov.beta(g, m_mul(h, k)) + cov.beta(h, k)) % 3
    if lhs != rhs: bad += 1
print("twisted cocycle identity failures:", bad, "/100")
# diagonal check: sigma(diag(a1,a2), diag(b1,b2)) = (a1, b2)
bad = 0
for _ in range(100):
    a1, a2, b1, b2 = [random_E_element(rng) for _ in range(4)]
    g = ((a1, E0), (E0, a2)); h = ((b1, E0), (E0, b2))
    if cov.sigma(g, h) != sym.hE(a1, b2): bad += 1
print("diagonal formula failures:", bad, "/100")
# scalar cocycle trivial (with twist, before relabel)
bad = 0
for _ in range(100):
    a = random_F_element(rng); b = random_F_element(rng)
    g = ((a, E0), (E0, a)); h = ((b, E0), (E0, b))
    if cov.beta(g, h) != 0: bad += 1
print("scalar cocycle nontrivial count:", bad, "/100")
# torus commutators on E_0 embedded in D: [x,y] = (Nx,Ny)_F^{r+2c} (x,y)_E^{-r} = (Nx,Ny)_F (x,y)_E  (exponents, before relabeling)
bad = 0; mism = []
for _ in range(200):
    x = random_E_element(rng); y = random_E_element(rng)
    X = (x, E0); Y = (y, E0)
    lhs = cov.commutator_exp(X, Y)
    rhs = (sym.hF(e_norm_to_F(x), e_norm_to_F(y)) + sym.hE(x, y)) % 3
    if lhs != rhs: bad += 1; mism.append((lhs, rhs))
print("E_0 torus commutator mismatches vs Part I formula:", bad, "/200", mism[:5])
# good elements of E_0: center = preimage of F^x E_0^{x3}: check index 9 pairing nondegeneracy on U^{(1)}/(U_F U^{(1)3})
pickle.dump({'AE': AE, 'AF': AF}, open('./symbols.pkl', 'wb'))
