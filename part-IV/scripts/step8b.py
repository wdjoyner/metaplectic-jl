import sys; sys.path.insert(0, '.')
exec(open('./step8_H1test.py').read().split("rng = random.Random(2026)")[0])
import collections
rng = random.Random(99)
def rand_K2b(rng, R=6):
    x1 = (gq(rng.randint(-R, R), rng.randint(-R, R)), gq(rng.randint(-R, R), rng.randint(-R, R)))
    y1 = (gq(rng.randint(-R, R), rng.randint(-R, R)), gq(rng.randint(-R, R), rng.randint(-R, R)))
    return d_add(D1, (e_mul(EW, x1), e_mul(EW, y1)))
cnt = collections.Counter(cube_exp(rand_K2b(rng)) for _ in range(200))
print("distribution of e(w) for random w in K^2:", dict(cnt))
cnt = collections.Counter()
fails = 0; t0 = time.time()
for trial in range(300):
    w = rand_K2b(rng); wp = rand_K2b(rng)
    X = d_mul(d_pow(w, 3), d_pow(wp, 3))
    b = cov.betaD(d_pow(w, 3), d_pow(wp, 3))
    e_prod = (cube_exp(w) + cube_exp(wp) + b) % 3
    e_ell, errv = ell_exp(X)
    cnt[(cube_exp(w), cube_exp(wp), b, e_ell)] += 1
    if e_prod != e_ell: fails += 1
print("(H1) broad test: failures", fails, "/300  (%.0fs)" % (time.time()-t0))
print("joint distribution (e(w), e(w'), beta(w^3,w'^3), e_ell):", dict(cnt))
# commutator nontriviality sanity in K^2: pairs in U^{(1)}_{E_0}
cnt = collections.Counter()
for _ in range(100):
    x = e_add(E1, e_mul(EW, (gq(rng.randint(-5,5), rng.randint(-5,5)), gq(rng.randint(-5,5), rng.randint(-5,5)))))
    y = e_add(E1, e_mul(EW, (gq(rng.randint(-5,5), rng.randint(-5,5)), gq(rng.randint(-5,5), rng.randint(-5,5)))))
    cnt[cov.commutator_exp((x, E0), (y, E0))] += 1
print("commutator exponents on U^{(1)}_{E_0} pairs:", dict(cnt))
