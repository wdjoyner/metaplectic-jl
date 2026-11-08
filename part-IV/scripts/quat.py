"""
Exact arithmetic in the maximal order O_D of the quaternion division algebra
D = (-1, varpi) over F = Q_3(zeta_3), with E_0 = F(i) unramified, j^2 = varpi,
j x = sigma(x) j.  Everything is done in Z[i][varpi] (exact integers), where
varpi = zeta_3 - 1 satisfies varpi^2 = -3 - 3*varpi.

Elements of O_{E_0}: pairs (a, b) of Gaussian integers meaning a + b*varpi,
Gaussian integers: pairs of Python ints (re, im).
Elements of O_D: pairs (x, y) of O_{E_0} elements meaning x + y*j.
"""

# ---------- Gaussian integers ----------
def g_add(a, b): return (a[0] + b[0], a[1] + b[1])
def g_sub(a, b): return (a[0] - b[0], a[1] - b[1])
def g_mul(a, b): return (a[0]*b[0] - a[1]*b[1], a[0]*b[1] + a[1]*b[0])
def g_neg(a): return (-a[0], -a[1])
def g_conj(a): return (a[0], -a[1])
def g_scal(k, a): return (k*a[0], k*a[1])
def g_is_zero(a): return a == (0, 0)
def g_div3(a):
    assert a[0] % 3 == 0 and a[1] % 3 == 0, a
    return (a[0]//3, a[1]//3)
def g_red3(a):  # reduction to F_9 = F_3[i], as (re mod 3, im mod 3)
    return (a[0] % 3, a[1] % 3)
def g_v3(a):
    if g_is_zero(a): return 10**9
    v = 0
    while a[0] % 3 == 0 and a[1] % 3 == 0:
        a = g_div3(a); v += 1
    return v

G0 = (0, 0); G1 = (1, 0); GI = (0, 1)

# ---------- O_{E_0} = Z[i][varpi], varpi^2 = -3 - 3 varpi ----------
def e_add(x, y): return (g_add(x[0], y[0]), g_add(x[1], y[1]))
def e_sub(x, y): return (g_sub(x[0], y[0]), g_sub(x[1], y[1]))
def e_neg(x): return (g_neg(x[0]), g_neg(x[1]))
def e_mul(x, y):
    a, b = x; c, d = y
    ac = g_mul(a, c); bd = g_mul(b, d); ad = g_mul(a, d); bc = g_mul(b, c)
    # (a + b w)(c + d w) = ac + (ad+bc) w + bd w^2 = (ac - 3bd) + (ad + bc - 3bd) w
    return (g_sub(ac, g_scal(3, bd)), g_sub(g_add(ad, bc), g_scal(3, bd)))
def e_sigma(x): return (g_conj(x[0]), g_conj(x[1]))
def e_is_zero(x): return g_is_zero(x[0]) and g_is_zero(x[1])
def e_val(x):
    """valuation v_{E_0} (normalized, v(varpi)=1)"""
    if e_is_zero(x): return 10**9
    return min(2*g_v3(x[0]), 2*g_v3(x[1]) + 1)
def e_div_varpi(x):
    """(a + b w)/w = (b - a) + (-a/3) w ; requires 3 | a"""
    a, b = x
    a3 = g_div3(a)
    return (g_sub(b, a), g_neg(a3))
def e_red(x):
    """reduction mod varpi to F_9 = F_3[i]"""
    return g_red3(x[0])

E0 = (G0, G0); E1 = (G1, G0); EI = (GI, G0); EW = (G0, G1)   # 0, 1, i, varpi
def e_int(k): return ((k, 0), G0)
def e_gauss(g): return (g, G0)

# ---------- O_D = O_{E_0} + O_{E_0} j ----------
def d_add(X, Y): return (e_add(X[0], Y[0]), e_add(X[1], Y[1]))
def d_sub(X, Y): return (e_sub(X[0], Y[0]), e_sub(X[1], Y[1]))
def d_neg(X): return (e_neg(X[0]), e_neg(X[1]))
def d_mul(X, Y):
    x, y = X; u, v = Y
    # (x + y j)(u + v j) = x u + y sigma(v) j^2 + (x v + y sigma(u)) j, j^2 = varpi
    return (e_add(e_mul(x, u), e_mul(e_mul(y, e_sigma(v)), EW)),
            e_add(e_mul(x, v), e_mul(y, e_sigma(u))))
def d_val(X):
    """v_D with v_D(j) = 1, v_D(varpi) = 2"""
    return min(2*e_val(X[0]), 2*e_val(X[1]) + 1)
def d_pow(X, n):
    R = D1
    for _ in range(n): R = d_mul(R, X)
    return R
def d_sigma_conj_j(X):
    """ j X j^{-1} = sigma(x) + sigma(y) j """
    return (e_sigma(X[0]), e_sigma(X[1]))

D0 = (E0, E0); D1 = (E1, E0); DJ = (E0, E1); DI = (EI, E0); DW = (EW, E0)

# ---------- reduced norm / trace ----------
def d_nrd(X):
    x, y = X
    return e_sub(e_mul(x, e_sigma(x)), e_mul(e_mul(y, e_sigma(y)), EW))
def d_trd(X):
    x, y = X
    return e_add(x, e_sigma(x))

# ---------- coordinates on P^3/P^6 ----------
def coords_P3(X):
    """X = x + y j in P_D^3.  Returns (A, B, C) in F_9^3 with
       X = varpi (A + B varpi) j + varpi^2 C   mod P^6."""
    x, y = X
    assert d_val(X) >= 3, d_val(X)
    y1 = e_div_varpi(y)
    A = e_red(y1)
    liftA = e_gauss(A)
    y2 = e_div_varpi(e_sub(y1, liftA))
    B = e_red(y2)
    x2 = e_div_varpi(e_div_varpi(x))
    C = e_red(x2)
    return (A, B, C)

# F_9 helpers (elements as pairs mod 3)
def f9_add(a, b): return ((a[0]+b[0]) % 3, (a[1]+b[1]) % 3)
def f9_neg(a): return ((-a[0]) % 3, (-a[1]) % 3)
def f9_mul(a, b): return ((a[0]*b[0] - a[1]*b[1]) % 3, (a[0]*b[1] + a[1]*b[0]) % 3)
def f9_conj(a): return (a[0], (-a[1]) % 3)
def f9_norm(a): return f9_mul(a, f9_conj(a))[0]
def f9_tr(a): return (2*a[0]) % 3
F9 = [(a, b) for a in range(3) for b in range(3)]
F9x = [a for a in F9 if a != (0, 0)]

def V_vec(ABC):
    """element of V = F_9 (A) + F_9/F_3 (C) + F_9 (B) as an F_3^5 tuple
       (A_re, A_im, C_im, B_re, B_im)"""
    A, B, C = ABC
    return (A[0], A[1], C[1], B[0], B[1])
