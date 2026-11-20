import sympy as sp, numpy as np
z=sp.symbols('z')
w=sp.symbols('w')
X=(1+2*w-w**2)/(1-sp.Rational(11,6)*w+w**2-w**3/6)
print(sp.apart(sp.together(X),w))
Xz=sp.simplify(X.subs(w,1/z)); print(Xz, sp.apart(Xz/z,z))
a=sp.Rational(1,2)
Xc=a/z/(1-a/z)**2+a*z/(1-a*z)**2; print(sp.factor(sp.simplify(Xc)))
# numeric check of 8(c) at z=1
print(float(Xc.subs(z,1)), sum(abs(n)*0.5**abs(n) for n in range(-200,201)))
# causal sequences for 8(a) ROC |z|>1: x[n]
num=[1,2,-1]; 
# apart in w: print coefficients
for n in range(0,6):
    pass
# log series check
av=0.4
ser=sum(((-1)**(n+1))*av**n/n*0.9**(-n) for n in range(1,400)); print(ser, np.log(1+av/0.9))
