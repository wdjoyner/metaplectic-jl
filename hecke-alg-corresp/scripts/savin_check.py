"""Numerical checks of the genuine Iwahori-Hecke algebra of the n-fold
Kubota cover of SL(2,Q_p), p odd, p not dividing n, n | p-1.

Elements of the cover are pairs (g, z) with g in SL(2,Q) (exact rationals)
and z in mu_n, realized as an integer mod p of order dividing n.
Group law (g1,z1)(g2,z2) = (g1 g2, beta(g1,g2) z1 z2), Kubota's cocycle
beta(g1,g2) = (x(g1g2)/x(g1), x(g1g2)/x(g2))_n, x(g)=c if c!=0 else d.
"""
from fractions import Fraction as Fr
import random, sys, itertools

P = None
N = None


def setup(p, n):
    global P, N
    assert (p - 1) % n == 0 and p % 2 == 1
    P, N = p, n


def val(a):
    a = Fr(a)
    assert a != 0
    v = 0
    num, den = a.numerator, a.denominator
    while num % P == 0:
        num //= P
        v += 1
    while den % P == 0:
        den //= P
        v -= 1
    return v


def unit_res(a):
    """residue mod p of the unit part of a"""
    a = Fr(a)
    v = val(a)
    u = a / Fr(P) ** v
    return (u.numerator * pow(u.denominator, -1, P)) % P


def hilb(a, b):
    """tame n-th power Hilbert symbol, value in mu_n inside F_p^x"""
    al, be = val(a), val(b)
    t = (-1 if (al * be) % 2 else 1) * pow(unit_res(a), be, P) * pow(unit_res(b), -al, P)
    t %= P
    return pow(t, (P - 1) // N, P)


def mul(A, B):
    return ((A[0][0] * B[0][0] + A[0][1] * B[1][0], A[0][0] * B[0][1] + A[0][1] * B[1][1]),
            (A[1][0] * B[0][0] + A[1][1] * B[1][0], A[1][0] * B[0][1] + A[1][1] * B[1][1]))


def inv(A):
    (a, b), (c, d) = A
    return ((d, -b), (-c, a))


def M(a, b, c, d):
    return ((Fr(a), Fr(b)), (Fr(c), Fr(d)))


def xf(g):
    return g[1][0] if g[1][0] != 0 else g[1][1]


def beta(g1, g2):
    x12 = xf(mul(g1, g2))
    return hilb(x12 / xf(g1), x12 / xf(g2))


def cmul(X, Y):
    return (mul(X[0], Y[0]), (beta(X[0], Y[0]) * X[1] * Y[1]) % P)


def cinv(X):
    g, z = X
    gi = inv(g)
    b = beta(g, gi)
    # (g,z)(gi,w) = (1, b z w) = (1,1)  =>  w = (b z)^{-1}
    return (gi, pow(b * z, -1, P))


def kappa(k):
    """Kubota's splitting of SL(2,Z_p): kappa(k) = (c,d)_n if c in pZ_p-{0}, else 1."""
    c, d = k[1][0], k[1][1]
    if c != 0 and val(c) > 0:
        return hilb(c, d)
    return 1


def s(b):
    return (b, kappa(b))


ONE = M(1, 0, 0, 1)
PI = None


def t0(m):
    return M(Fr(P) ** m, 0, 0, Fr(P) ** (-m))


S1 = M(0, -1, 1, 0)


def up(x):
    return M(1, x, 0, 1)


def lo(y):
    return M(1, 0, y, 1)


def hh(a):
    return M(a, 0, 0, Fr(1) / Fr(a))


def nu(e, pos):
    if e == 0:
        return None
    v = val(e)
    return {0: v, 3: v, 1: v + Fr(1, 2), 2: v - Fr(1, 2)}[pos]


def iwahori_decomp(g):
    """Return (b1, w, b2, label) with g = b1 w b2, b1,b2 in B,
    w = t0^m or t0^m s1. label = ('t',m) or ('ts',m)."""
    (a, b), (c, d) = g
    ents = [a, b, c, d]
    nus = [nu(e, i) for i, e in enumerate(ents)]
    cands = [(nus[i], i) for i in range(4) if nus[i] is not None]
    mn = min(cands)[0]
    piv = min(i for (v, i) in cands if v == mn)
    L = ONE  # g = L^{-1} * g' * R^{-1}  where g' = L g R
    R = ONE
    if piv in (0, 3):
        if piv == 3:
            # make a the pivot equivalently: use d, clear b,c
            # R1 -= (b/d) R2 : left mult by up(-b/d), ord(b/d)>=0 needed
            Lm = up(-b / d)
            Rm = lo(-c / d)
            gp = mul(mul(Lm, g), Rm)
        else:
            Lm = lo(-c / a)
            Rm = up(-b / a)
            gp = mul(mul(Lm, g), Rm)
        assert gp[0][1] == 0 and gp[1][0] == 0, gp
        A = gp[0][0]
        m = val(A)
        u = A / Fr(P) ** m
        # gp = t0^m h(u)
        w = t0(m)
        b1 = inv(Lm)
        b2 = mul(hh(u), inv(Rm))
        lab = ('t', m)
    elif piv == 1:
        Rm = lo(-a / b)
        Lm = lo(-d / b)
        gp = mul(mul(Lm, g), Rm)
        assert gp[0][0] == 0 and gp[1][1] == 0, gp
        x = gp[0][1]
        # gp = w(x) = [[0,x],[-1/x,0]] = h(x) w(1) = -t0^j h(u) s1, x = p^j u
        j = val(x)
        u = x / Fr(P) ** j
        w = mul(t0(j), S1)
        # w(x) = t0^j s1 * (s1^{-1} (-h(u)) s1) = t0^j s1 * h(-1/u)
        b1 = inv(Lm)
        b2 = mul(hh(-1 / u), inv(Rm))
        lab = ('ts', j)
    else:
        Lm = up(-a / c)
        Rm = up(-d / c)
        gp = mul(mul(Lm, g), Rm)
        assert gp[0][0] == 0 and gp[1][1] == 0, gp
        x = gp[0][1]
        j = val(x)
        u = x / Fr(P) ** j
        w = mul(t0(j), S1)
        b1 = inv(Lm)
        b2 = mul(hh(-1 / u), inv(Rm))
        lab = ('ts', j)
    assert mul(mul(b1, w), b2) == g
    for bb in (b1, b2):
        assert in_B(bb), bb
    return b1, w, b2, lab


def in_B(b):
    (a, bb), (c, d) = b
    ok = (a != 0 and val(a) == 0) and (d != 0 and val(d) == 0)
    ok = ok and (bb == 0 or val(bb) >= 0) and (c == 0 or val(c) >= 1)
    return ok


def wlab_elem(lab):
    kind, m = lab
    return t0(m) if kind == 't' else mul(t0(m), S1)


def fbar(lab, X):
    """value at X of the genuine function fbar_{(w,1)} for w = wlab_elem(lab);
    zero off the double coset. Assumes w admissible."""
    g, z = X
    b1, w, b2, l2 = iwahori_decomp(g)
    if l2 != lab:
        return 0
    Y = cmul(cmul(s(b1), (w, 1)), s(b2))
    assert Y[0] == g
    # X = (z / Y[1]) * Y, f(Y) = 1
    return (z * pow(Y[1], -1, P)) % P


def reps(lab):
    """representatives v of B/(B cap wBw^{-1})"""
    kind, m = lab
    if kind == 't':
        i, j = max(2 * m, 0), max(1 - 2 * m, 1)
    else:
        i, j = max(1 + 2 * m, 0), max(-2 * m, 1)
    out = []
    assert i == 0 or j == 1
    if i > 0:
        for x in range(P ** i):
            out.append(up(Fr(x)))
    elif j > 1:
        for y in range(P ** (j - 1)):
            out.append(lo(Fr(P * y)))
    else:
        out.append(ONE)
    return out


def length(lab):
    kind, m = lab
    return 2 * abs(m) if kind == 't' else abs(2 * m + 1)


def conv_value(lab1, lab2, Y):
    """(fbar_{w1} * fbar_{w2})(Y) as a dict root-of-unity -> count"""
    w1 = (wlab_elem(lab1), 1)
    w1i = cinv(w1)
    tally = {}
    for v in reps(lab1):
        sv = s(v)
        Z = cmul(cmul(w1i, cinv(sv)), Y)
        val_ = fbar(lab2, Z)
        if val_ != 0:
            tally[val_] = tally.get(val_, 0) + 1
    return tally


def admissible(lab, trials=200):
    w = wlab_elem(lab)
    wt = (w, 1)
    wti = cinv(wt)
    kind, m = lab
    if kind == 't':
        I, J = max(0, -2 * m), max(1, 1 + 2 * m)
    else:
        I, J = max(0, 1 + 2 * m), max(1, -2 * m)
    rng = random.Random(1)
    for _ in range(trials):
        a = Fr(rng.randrange(1, P)) + P * Fr(rng.randrange(0, P ** 2))
        b = Fr(P) ** I * rng.randrange(0, P ** 2)
        c = Fr(P) ** J * rng.randrange(0, P ** 2)
        x = mul(mul(lo(c), hh(a)), up(b))
        y = mul(mul(w, x), inv(w))
        assert in_B(x) and in_B(y)
        if s(y) != cmul(cmul(wt, s(x)), wti):
            return False
    return True


def test_kappa(trials=300):
    rng = random.Random(0)

    def rk():
        while True:
            a = Fr(rng.randrange(-50, 50))
            c = Fr(rng.randrange(-50, 50))
            if a == 0 and c == 0:
                continue
            # find b,d integers-ish with ad-bc=1 over Z_(p): pick b, solve d if a unit
            b = Fr(rng.randrange(-50, 50))
            if a != 0 and val(a) == 0:
                d = (1 + b * c) / a
            elif c != 0 and val(c) == 0:
                d = Fr(rng.randrange(-50, 50))
                b = (a * d - 1) / c
            else:
                continue
            k = ((a, b), (c, d))
            if all(e == 0 or val(e) >= 0 for e in (a, b, c, d)):
                return k
    for _ in range(trials):
        k1, k2 = rk(), rk()
        if kappa(mul(k1, k2)) != (beta(k1, k2) * kappa(k1) * kappa(k2)) % P:
            return False
    return True


def candidates(maxlen):
    out = []
    for m in range(-maxlen, maxlen + 1):
        for kind in ('t', 'ts'):
            lab = (kind, m)
            if length(lab) <= maxlen:
                out.append(lab)
    return out


def product(lab1, lab2):
    """expand fbar_{w1} * fbar_{w2} = sum_y c_y fbar_{(y,1)}; returns dict"""
    res = {}
    for y in candidates(length(lab1) + length(lab2)):
        Y = (wlab_elem(y), 1)
        t = conv_value(lab1, lab2, Y)
        if t:
            res[y] = t
    return res


def zeta_name(z):
    # express z in mu_n as exponent of a fixed primitive n-th root
    g = next(h for h in range(2, P) if all(pow(h, (P - 1) // r, P) != 1
                                           for r in range(2, P) if (P - 1) % r == 0 and isprime(r)))
    zeta = pow(g, (P - 1) // N, P)
    for e in range(N):
        if pow(zeta, e, P) == z:
            return e
    raise ValueError


def isprime(r):
    return r > 1 and all(r % k for k in range(2, int(r ** 0.5) + 1))


def show(res):
    out = []
    for y, t in sorted(res.items()):
        tot = {zeta_name(z): c for z, c in t.items()}
        out.append(f"  {y}: " + ", ".join(f"{c}*zeta^{e}" for e, c in sorted(tot.items())))
    return "\n".join(out)


if __name__ == '__main__':
    p, n = int(sys.argv[1]), int(sys.argv[2])
    setup(p, n)
    print(f"p={p}, n={n}", flush=True)
    print("kappa is a splitting of K:", test_kappa(), flush=True)
    for lab in [('t', m) for m in range(-3, 4)] + [('ts', m) for m in range(-3, 3)]:
        print("admissible", lab, admissible(lab), flush=True)
