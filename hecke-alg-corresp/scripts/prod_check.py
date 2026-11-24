import sys, time
sys.path.insert(0, __import__('os').path.dirname(__import__('os').path.abspath(__file__)))
import savin_check as S
p, n = int(sys.argv[1]), int(sys.argv[2])
labs = [eval(a) for a in sys.argv[3:]]
S.setup(p, n)
for lab in labs:
    t = time.time()
    res = S.product(lab, lab)
    # drop non-admissible supports but report if nonzero
    print(f"p={p} n={n}: fbar_{lab}^2 =", flush=True)
    print(S.show(res), flush=True)
    for y in res:
        if not S.admissible(y, 30):
            print("  WARNING nonadmissible support", y)
    print(f"  ({time.time()-t:.1f}s)", flush=True)
