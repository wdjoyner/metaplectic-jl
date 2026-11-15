#!/usr/bin/env python3
"""
Independent Level 1 exact verification of the finite-design and adjoint-action
tables in Appendix A (chapters/appA_scripts.tex) for Chapter 8 (Target A).

License: MIT
"""
from collections import Counter
from itertools import product


def mat_mul_mod3(A, B):
    n = len(A)
    return tuple(
        tuple(sum(A[i][k] * B[k][j] for k in range(n)) % 3 for j in range(n))
        for i in range(n)
    )


def mat_vec_mod3(M, v):
    return tuple(sum(M[i][k] * v[k] for k in range(5)) % 3 for i in range(5))


def generate_group(gens):
    ident = tuple(tuple(1 if i == j else 0 for j in range(5)) for i in range(5))
    seen = {ident}
    queue = [ident]
    while queue:
        cur = queue.pop()
        for g in gens:
            nxt = mat_mul_mod3(cur, g)
            if nxt not in seen:
                seen.add(nxt)
                queue.append(nxt)
    return seen


def main():
    Ad_1pj = (
        (1, 0, 0, 0, 0),
        (0, 1, 0, 0, 0),
        (0, 1, 1, 0, 0),
        (0, 0, 0, 1, 0),
        (0, 2, 1, 0, 1),
    )
    Ad_1pij = (
        (1, 0, 0, 0, 0),
        (0, 1, 0, 0, 0),
        (2, 0, 1, 0, 0),
        (2, 0, 2, 1, 0),
        (0, 0, 0, 0, 1),
    )
    Ad_1pi = (
        (0, 2, 0, 0, 0),
        (1, 0, 0, 0, 0),
        (0, 0, 1, 0, 0),
        (0, 0, 0, 0, 2),
        (0, 0, 0, 1, 0),
    )
    Ad_j = (
        (1, 0, 0, 0, 0),
        (0, 2, 0, 0, 0),
        (0, 0, 2, 0, 0),
        (0, 0, 0, 1, 0),
        (0, 0, 0, 0, 2),
    )

    G_heis = generate_group([Ad_1pj, Ad_1pij])
    G_d8 = generate_group([Ad_1pi, Ad_j])
    G_full = generate_group([Ad_1pj, Ad_1pij, Ad_1pi, Ad_j])
    assert len(G_heis) == 27, f"Expected 27, got {len(G_heis)}"
    assert len(G_d8) == 8, f"Expected 8, got {len(G_d8)}"
    assert len(G_full) == 216, f"Expected 216, got {len(G_full)}"

    raw_entries = """
    01002:0 01012:0 01022:0 01101:0 01111:1 01121:2
    01201:0 01211:2 01221:1 10020:0 10021:0 10022:0
    10110:0 10111:2 10112:1 10210:0 10211:1 10212:2
    11002:0 11011:0 11020:0 11101:1 11110:2 11122:0
    11201:2 11210:1 11222:0 12001:0 12012:0 12020:0
    12102:2 12110:1 12121:0 12202:1 12210:2 12221:0
    """.split()

    lines_36 = []
    e_star = {}
    for item in raw_entries:
        vec_s, val_s = item.split(":")
        v = tuple(int(c) for c in vec_s)
        val = int(val_s) % 3
        lines_36.append(v)
        e_star[v] = val
        e_star[tuple((-x) % 3 for x in v)] = (-val) % 3

    assert len(lines_36) == 36 and len(e_star) == 72
    bar_G3 = set(e_star.keys())
    assert all(mat_vec_mod3(M, v) in bar_G3 for M in G_full for v in bar_G3)

    coplanar = 0
    for l1 in lines_36:
        for l2 in lines_36:
            if l1 == l2:
                continue
            for l3 in lines_36:
                if l3 == l1 or l3 == l2:
                    continue
                in_plane = False
                for c1 in (1, 2):
                    for c2 in (1, 2):
                        comb = tuple((c1 * l1[k] + c2 * l2[k]) % 3 for k in range(5))
                        if comb == l3 or comb == tuple((-x) % 3 for x in l3):
                            in_plane = True
                            u1 = tuple((c1 * l1[k]) % 3 for k in range(5))
                            u2 = tuple((c2 * l2[k]) % 3 for k in range(5))
                            u3 = tuple((-comb[k]) % 3 for k in range(5))
                            assert (e_star[u1] + e_star[u2] + e_star[u3]) % 3 == 0
                if in_plane:
                    coplanar += 1
    assert coplanar == 720, f"Expected B=720, got {coplanar}"

    listed_lambda = """
    00000 00100 00200 01001 01121 01211 02002 02112 02222
    10010 10111 10212 11022 11110 11201 12021 12102 12210
    20020 20122 20221 21012 21101 21220 22011 22120 22202
    """.split()

    hits_20 = []
    counts = Counter()
    for h in product(range(3), repeat=5):
        n_h = sum(
            1
            for v in lines_36
            if (sum(h[k] * v[k] for k in range(5)) + e_star[v]) % 3 == 0
        )
        counts[n_h] += 1
        if n_h == 20:
            hits_20.append("".join(map(str, h)))

    assert dict(counts) == {11: 216, 20: 27}
    assert sorted(hits_20) == sorted(listed_lambda)

    beta_1pj = (1, 0, 0, 1, 0)
    beta_1pij = (0, 1, 0, 0, 1)
    for M, beta in [(Ad_1pj, beta_1pj), (Ad_1pij, beta_1pij)]:
        for v in bar_G3:
            mv = mat_vec_mod3(M, v)
            lhs = (e_star[mv] - e_star[v]) % 3
            rhs = sum(beta[k] * v[k] for k in range(5)) % 3
            assert lhs == rhs

    print("ALL APPENDIX A TABLE CHECKS PASSED:")
    print("  |Heis| = 27, |D8| = 8, |G_sym| = 216")
    print("  |bar G_3| = 72 (36 lines), G_sym-invariant")
    print("  B = 720 ordered coplanar triples, all defect-free")
    print("  N_{e_*}(h) distribution = {11: 216, 20: 27}; Lambda_+ matches table")
    print("  Heisenberg cocycle vectors beta_{Ad(1+j)}, beta_{Ad(1+ij)} verified")


if __name__ == "__main__":
    main()
