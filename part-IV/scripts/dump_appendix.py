import pickle, itertools, numpy as np
G3 = pickle.load(open('G3.pkl','rb'))['G3']
des = pickle.load(open('design_0011020002.pkl','rb'))
e = des['e']; Lam = des['Lambda']
acts = pickle.load(open('actions.pkl','rb'))
def neg(v): return tuple((-c)%3 for c in v)
def fmt(v): return ''.join(str(c) for c in v)
# lines with e values
lines = {}
for v in G3:
    key = min(v, neg(v)); lines.setdefault(key, []).append(v)
print("36 good lines (representative v = (A_re,A_im,C_im,B_re,B_im); e_*(v)); e_*(-v) = -e_*(v)")
out = []
for k in sorted(lines):
    out.append("%s:%d" % (fmt(k), e[k]))
for i in range(0, 36, 6): print("  " + "  ".join(out[i:i+6]))
print("Lambda (27 covectors h in F_3^5, N(h)=20):")
L = sorted(Lam)
for i in range(0, 27, 9): print("  " + " ".join(fmt(h) for h in L[i:i+9]))
# which lines have e=0
print("lines with e_*=0:", sum(1 for k in lines if e[k]==0), "; with e_*=1:", sum(1 for k in lines if e[k]==1), "; with e_*=2:", sum(1 for k in lines if e[k]==2))
print("B (ordered coplanar triples) =", acts['B'])
# matrices
for k,v in acts['Ms'].items(): print(k, v)
