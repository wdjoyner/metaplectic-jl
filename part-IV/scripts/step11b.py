import sys; sys.path.insert(0, '.')
exec(open('./step11_endtoend.py').read().split("rng = random.Random(77)")[0])
import quat as Q, cmath
G3set = set(pickle.load(open('G3.pkl','rb'))['G3'])
rng = random.Random(123); z3 = cmath.exp(2j*cmath.pi/3)
def to_int(X):
    f = lambda g: (int(g[0]), int(g[1]))
    return ((f(X[0][0]), f(X[0][1])), (f(X[1][0]), f(X[1][1])))
def vclass(X):   # V-class of X in K^3 (integer coordinates required)
    Xi = to_int(X)
    return Q.V_vec(Q.coords_P3(Q.d_sub(Xi, Q.D1)))
t0 = time.time()
print("--- sigma(g) * ell(k) * (z,0) * zeta^m : expect 9 zeta^m ---")
for trial in range(5):
    while True:
        t = d_add(D1, (e_mul(EW, (gq(rng.randint(-2,2), rng.randint(-2,2)), gq(rng.randint(-2,2), rng.randint(-2,2)))), (gq(rng.randint(-2,2), rng.randint(-2,2)), gq(rng.randint(-2,2), rng.randint(-2,2)))))
        if d_val(d_sub(t, D1)) == 1: break
    k = d_add(D1, (e_mul(VARPI3, (gq(rng.randint(-2,2), rng.randint(-2,2)), gq())), e_mul(VARPI3, (gq(rng.randint(-2,2), rng.randint(-2,2)), gq()))))
    z = e_add(E1, e_mul(EW, (gq(rng.randint(0,2)), gq(rng.randint(0,2)))))   # in U_F^{(1)}
    m = rng.randint(0, 2)
    x = cmul(cmul(cmul((d_pow(t,3), 0), (k, kappa(k))), ((z, E0), 0)), (D1, m))
    val = induced_char(x)
    print("  m =", m, " Theta_Ind =", round(val.real, 4), round(val.imag, 4), " expected", round((9*z3**m).real, 4), round((9*z3**m).imag, 4))
print("--- depth-3 elements with V-class not in G3 : expect 0 ---")
n = 0
while n < 5:
    X = d_add(D1, (e_mul(e_mul(EW, EW), (gq(rng.randint(-1,1), rng.randint(-1,1)), gq())), e_mul(EW, (gq(rng.randint(-1,1), rng.randint(-1,1)), gq(rng.randint(-1,1), rng.randint(-1,1))))))
    if d_val(d_sub(X, D1)) != 3 or vclass(X) in G3set: continue
    val = induced_char((X, rng.randint(0,2)))
    print("  Theta_Ind =", round(val.real, 4), round(val.imag, 4)); n += 1
print("--- depth-3 elements with V-class in G3 : expect |value| = 9 ---")
n = 0
while n < 3:
    X = d_add(D1, (e_mul(e_mul(EW, EW), (gq(rng.randint(-1,1), rng.randint(-1,1)), gq())), e_mul(EW, (gq(rng.randint(-1,1), rng.randint(-1,1)), gq(rng.randint(-1,1), rng.randint(-1,1))))))
    if d_val(d_sub(X, D1)) != 3 or vclass(X) not in G3set: continue
    val = induced_char((X, 0))
    print("  |Theta_Ind| =", round(abs(val), 4)); n += 1
print("elapsed %.0fs" % (time.time()-t0))
