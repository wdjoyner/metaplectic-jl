"""Exact integer linear algebra: Smith normal form with transforms, and A n = b over Z."""
def smith(A):
    """A: list of lists of ints (m x n). Returns (U, D, V) with U A V = D, U,V unimodular, D diagonal
       (as list of lists), d_1 | d_2 | ... (divisibility not enforced; only diagonal form needed here)."""
    m, n = len(A), len(A[0])
    D = [row[:] for row in A]
    U = [[int(i == j) for j in range(m)] for i in range(m)]
    V = [[int(i == j) for j in range(n)] for i in range(n)]
    def swap_rows(M, i, j): M[i], M[j] = M[j], M[i]
    def swap_cols(M, i, j):
        for r in M: r[i], r[j] = r[j], r[i]
    def add_row(M, i, j, c):  # row_i += c*row_j
        M[i] = [a + c*b for a, b in zip(M[i], M[j])]
    def add_col(M, i, j, c):  # col_i += c*col_j
        for r in M: r[i] += c*r[j]
    t = 0
    while t < min(m, n):
        # find nonzero pivot with minimal abs value in submatrix
        piv = None
        for i in range(t, m):
            for j in range(t, n):
                if D[i][j] != 0 and (piv is None or abs(D[i][j]) < abs(D[piv[0]][piv[1]])):
                    piv = (i, j)
        if piv is None: break
        swap_rows(D, t, piv[0]); swap_rows(U, t, piv[0])
        swap_cols(D, t, piv[1]); swap_cols(V, t, piv[1])
        done = False
        while not done:
            done = True
            for i in range(t+1, m):
                if D[i][t] != 0:
                    q = D[i][t] // D[t][t]
                    add_row(D, i, t, -q); add_row(U, i, t, -q)
                    if D[i][t] != 0:   # remainder nonzero: swap to get smaller pivot
                        swap_rows(D, t, i); swap_rows(U, t, i); done = False; break
            if not done: continue
            for j in range(t+1, n):
                if D[t][j] != 0:
                    q = D[t][j] // D[t][t]
                    add_col(D, j, t, -q); add_col(V, j, t, -q)
                    if D[t][j] != 0:
                        swap_cols(D, t, j); swap_cols(V, t, j); done = False; break
        t += 1
    return U, D, V

def zsolve(A, b):
    """Return (status, n) where n is an integer solution of A n = b, or None.
       status in {'solution', 'inconsistent_Q', 'no_integer_solution'}."""
    m, n = len(A), len(A[0])
    U, D, V = smith(A)
    Ub = [sum(U[i][j]*b[j] for j in range(m)) for i in range(m)]
    r = min(m, n)
    y = [0]*n
    for i in range(m):
        d = D[i][i] if i < r else 0
        if d == 0:
            if Ub[i] != 0: return 'inconsistent_Q', None
        else:
            if Ub[i] % d != 0: return 'no_integer_solution', None
            y[i] = Ub[i] // d
    x = [sum(V[i][j]*y[j] for j in range(n)) for i in range(n)]
    # verify
    for i in range(m):
        assert sum(A[i][j]*x[j] for j in range(n)) == b[i]
    return 'solution', x

if __name__ == '__main__':
    import random
    for _ in range(200):
        m, n = random.randint(1, 6), random.randint(1, 6)
        A = [[random.randint(-3, 3) for _ in range(n)] for _ in range(m)]
        x = [random.randint(-4, 4) for _ in range(n)]
        b = [sum(A[i][j]*x[j] for j in range(n)) for i in range(m)]
        st, s = zsolve(A, b); assert st == 'solution'
    # a system with rational but no integer solution
    print(zsolve([[2, 0], [0, 2]], [1, 2]))
    print("zsolve self-test ok")
