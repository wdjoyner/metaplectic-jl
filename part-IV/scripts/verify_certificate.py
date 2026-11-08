"""Independent check of level2_orbit_certificate.txt (does not use cover.py or quat.py).
Checks: (1) the Heis table is a group of order 27 with identity t_0;
(2) each action table row is a permutation of the character indices and the assignment
    t -> permutation is a group action of Heis (a right action: mu^{t_a t_b} = (mu^{t_a})^{t_b}, or left);
(3) no character is fixed by any t != t_0;  (4) the orbits are as listed."""
import re, sys
txt = open(sys.argv[1] if len(sys.argv) > 1 else 'level2_orbit_certificate.txt').read()
lines = txt.splitlines()
def block(header, n, width):
    i = next(k for k, l in enumerate(lines) if l.startswith(header)) + 1
    rows = []
    while len(rows) < n:
        l = lines[i]; i += 1
        if l.strip() == '' : continue
        nums = [int(x) for x in re.findall(r'-?\d+', l.split(':', 1)[1] if ':' in l else l)]
        rows.append(nums[-width:] if width else nums)
    return rows
HM = block("Multiplication table of Heis", 27, 27)
assert all(len(r) == 27 for r in HM)
# group axioms for Heis
for a in range(27):
    assert sorted(HM[a]) == list(range(27)) and sorted(HM[b][a] for b in range(27)) == list(range(27))
    assert HM[0][a] == a and HM[a][0] == a
for a in range(27):
    for b in range(27):
        for c in range(27):
            assert HM[HM[a][b]][c] == HM[a][HM[b][c]]
print("Heis table: group of order 27, identity t_0")
def check_action(header, n):
    rows = block(header, n, 27)
    perms = [[rows[m][kk] for m in range(n)] for kk in range(27)]     # perms[k][m] = index of mu_m^{t_k}
    for kk in range(27): assert sorted(perms[kk]) == list(range(n)), "not a permutation"
    assert perms[0] == list(range(n)), "t_0 must act trivially"
    # action property: either perms[HM[a][b]] == perms[b] o perms[a] (left) or perms[a] o perms[b] (right)
    left = all(perms[HM[a][b]][m] == perms[a][perms[b][m]] for a in range(27) for b in range(27) for m in range(n))
    right = all(perms[HM[a][b]][m] == perms[b][perms[a][m]] for a in range(27) for b in range(27) for m in range(n))
    assert left or right, "tables do not define an action of Heis"
    fixed = sum(1 for kk in range(1, 27) for m in range(n) if perms[kk][m] == m)
    assert fixed == 0, "fixed point found"
    seen = set(); orbits = []
    for m in range(n):
        if m in seen: continue
        orb = {perms[kk][m] for kk in range(27)}; seen |= orb; orbits.append(sorted(orb))
    print("%s: action of Heis (%s), no fixed points, orbit sizes %s" % (header[:40], 'left' if left else 'right', sorted(len(o) for o in orbits)))
    return orbits
o3 = check_action("Action on the 54 degree-3 genuine characters", 54)
assert sorted(len(o) for o in o3) == [27, 27]
listed = eval(next(l for l in lines if l.startswith("orbits on the degree-3 characters:")).split(':', 1)[1])
assert sorted(map(sorted, listed)) == sorted(o3), "listed orbits differ from recomputed ones"
ol = check_action("Action on the 243 genuine linear characters", 243)
assert sorted(len(o) for o in ol) == [27] * 9
print("certificate verified")
