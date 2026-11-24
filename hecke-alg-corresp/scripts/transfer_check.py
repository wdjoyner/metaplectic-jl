"""For gamma~=(t0^{n'k},1), compare genuine F(fbar_{(w,1)}) with F'(Theta(fbar_{(w,1)})) at mu^k.
Theta(fbar_{(w,1)}) = zeta_w^{-1} a_n^{#r} f'_{Psi(w)}, where (alternating product of X,Y) = zeta_w fbar_{(w,1)}.
F' from the linear formulas (SL2 for n odd, PGL2 for n even)."""
import sys, os, cmath, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import savin_check as S
import orbital2 as O
from fractions import Fraction as Fr

def word(kind, j, npr):
    # returns list of letters ('s','r') with alternating product = +- w, w = t0^{n'j} or t0^{n'j} s1
    if kind == 't':
        return ['s', 'r'] * j if j >= 0 else ['r', 's'] * (-j)
    else:
        return (['s', 'r'] * j + ['s']) if j >= 0 else (['r', 's'] * (-j - 1) + ['r'])

def zeta_w(kind, j, npr):
    r = S.mul(S.t0(-npr), S.S1)
    L = (S.ONE, 1)
    for c in word(kind, j, npr):
        L = S.cmul(L, ((S.S1 if c == 's' else r), 1))
    w = S.t0(npr * j) if kind == 't' else S.mul(S.t0(npr * j), S.S1)
    g, z = L
    if g == w:
        sign = 1
    else:
        assert g == tuple(tuple(-e for e in row) for row in w)
        # (-w,1) = beta(-1,w)^{-1} (-1,1)(w,1); fbar_{(-w,1)} = beta(-1,w) fbar_{(w,1)}
        sign = S.beta(S.hh(-1), w)
    # alt product = fbar_L = fbar_{(+-w, z)} = z^{-1} fbar_{(+-w,1)} = z^{-1} sign fbar_{(w,1)}
    return (pow(z, -1, S.P) * sign) % S.P

def lin_F(nodd, q, kind, j, k):
    # F' of f'_{Psi(w)} at mu^k, k>=1
    if nodd:  # SL2, Psi(w) = t0^j or t0^j s1, gamma'=t0^k
        if kind == 't': return q ** k if abs(j) == k else 0
        ell = abs(2 * j + 1)
        return (q - 1) * q ** ((ell - 1) // 2) if ell >= 2 * k + 1 else 0
    else:     # PGL2, Psi(w) = lambda^j or lambda^j s1, gamma' = lambda^k
        if kind == 't': return q ** (k / 2) if abs(j) == k else 0
        ellp = j + 1 if j >= 0 else -j - 1
        return (q - 1) * q ** ((ellp - 1) / 2) if (ellp >= k + 1 and (j - k) % 2 == 0) else 0

if __name__ == '__main__':
    p, n, k = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3])
    S.setup(p, n)
    npr = n // math.gcd(n, 2); nodd = n % 2 == 1
    m = npr * k
    eps = (-1) ** ((p - 1) // 2)
    a = p ** (n - 1) if nodd else (1 if eps == 1 else 1j) * p ** ((n - 1) / 2)
    zprim = cmath.exp(2j * cmath.pi / n)
    js = eval(sys.argv[4])
    for kind, j in js:
        lab = (kind, npr * j)
        gen = O.orbital(lab, m)
        G = sum(complex(float(c)) * zprim ** e for e, c in gen.items())
        nr = word(kind, j, npr).count('r')
        zw = S.zeta_name(zeta_w(kind, j, npr))
        Lval = lin_F(nodd, p, kind, j, k) * a ** nr * zprim ** (-zw)
        ratio = (G / Lval) if abs(Lval) > 1e-9 else None
        print(f"q={p} n={n} k={k} w=({kind},{npr*j}): genuine={G:.4g} Savin-side={complex(Lval):.4g} ratio={ratio if ratio is None else complex(round(ratio.real,6), round(ratio.imag,6))}", flush=True)
