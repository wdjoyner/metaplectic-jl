# Check the note's telescoping coefficients c_k for R_E on E^1, E/F quadratic.
# F/Q_p with ramification e_F, residue degree f_F, mu_{p^a} in F.
# For zeta of exact order p^j: v_F(1-zeta) = e_F/(p^(j-1)(p-1)) (must be an integer).
from fractions import Fraction as Fr
from math import gcd
def phi(m):
    return sum(1 for k in range(1,m+1) if gcd(k,m)==1)
bad=0; cases=0
for p in [3,5,7]:
  for a in [1,2]:
    for mult in [1,2,3]:
      eF = (p-1)*p**(a-1)*mult          # minimal ramification for mu_{p^a}, times mult
      for fF in [1,2]:
        q = p**fF
        for kind in ['unram','ram']:
          eE = 1 if kind=='unram' else 2
          qE = q**2 if kind=='unram' else q
          # t_zeta = v_E(1-zeta) for each nontrivial zeta in mu_{p^a}
          ts=[]
          for j in range(1,a+1):
            vF = Fr(eF, p**(j-1)*(p-1)); assert vF.denominator==1
            ts += [int(vF)*eE]*phi(p**j)
          T=max(ts)
          def M(k):  # q_E^{(1/2) sum min(k,t)}
            s=sum(min(k,t) for t in ts); assert s%2==0
            return qE**(s//2)
          if kind=='unram':
            idx=lambda k: (q+1)*q**(k-1)
            total=1; ok=True
            for k in range(1,T+1):
              num=M(k)-M(k-1); c=Fr(num, idx(k))
              ok &= (c.denominator==1 and c>=0); total+= num
          else:
            ok=True; c1=Fr(M(1)-1,2); ok&=(c1.denominator==1); total=1+(M(1)-1)
            for j in range(1,T//2+1):
              num=M(2*j+1)-M(2*j-1); c=Fr(num,2*q**j)
              ok&=(c.denominator==1 and c>=0); total+=num
          # R(1) should equal |n|_F^{-1} = |p^a|_F^{-1} = q^{a*eF}
          ok &= (total == q**(a*eF))
          cases+=1
          if not ok: bad+=1; print("FAIL",p,a,eF,fF,kind)
print(cases,"cases checked;",bad,"failures")
