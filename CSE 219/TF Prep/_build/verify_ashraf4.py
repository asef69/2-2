import sympy as sp
s,t=sp.symbols('s t',positive=True)
def il(F): return sp.simplify(sp.inverse_laplace_transform(F,s,t))
def pf(F): return sp.apart(sp.together(F),s)
print("6a",pf((s+2)/(s*(s+3)*(s+4))), il((s+2)/(s*(s+3)*(s+4))))
print("2b",pf((s+2)/((s+3)*(s+4))))
# 2023-24 EEE 4a
V=(4*s**2+4*s+1)/(s*(4*s**2+2*s+1)); print("4a V",pf(V)); print(il(V))
# 8b EEE: y''+5y'+6y=x'+x, y(0)=2,y'(0)=1, x=e^-4t u  (x(0-)=0)
X=1/(s+4); Y=((s+1)*X+(s+5)*2+1)/(s**2+5*s+6); print("8b Y",pf(Y)); print(il(Y)); 
Yzi=((s+5)*2+1)/(s**2+5*s+6); Yzs=(s+1)*X/(s**2+5*s+6); print("ZIR",pf(Yzi),"ZSR",pf(Yzs))
# 6(a)'s 2022-23 EEE etc
print("3b",pf((s**2-3*s+2)/(s**3+6*s**2+11*s+6)), il((s**2-3*s+2)/(s**3+6*s**2+11*s+6)))
# 21-22 7c: y'+2y=e^-3t u, y(0)=1
Y=(1+1/(s+3))/(s+2); print("7c",pf(Y),il(Y))
# 21-22 7b 1/(s-a)^3
a=sp.symbols('a',real=True); print(il(1/(s+2)**3))
# 2013-14 6a  y''+4y'+3y=u, y(0)=2,y'(0)=1
Y=(1/s+2*s+8+1)/(s**2+4*s+3); print("6a13",pf(Y),il(Y))
# 2014-15 7a: y''+4y'+3y=e^-3t, y(0)=0,y'(0)=1
Y=(1/(s+3)+1)/(s**2+4*s+3); print("7a14",pf(Y),il(Y))
# 2015-16 7b: y''+5y'+6y=2e^-t, y'(0)=-2,y(0)=3
Y=(2/(s+1)+3*s+15-2)/(s**2+5*s+6); print("7b15",pf(Y),il(Y))
# 2011-12 8a h of y''+5y'+6y=x''+5x'+5x
H=(s**2+5*s+5)/(s**2+5*s+6); print("8a",pf(H),il(H))
# 2012-13 7c: x=e^-2t u, y=(e^-t-3e^-2t)u
H=(1/(s+1)-3/(s+2))*(s+2); print("7c12",sp.simplify(H),pf(H),il(H))
# 2017-18 4b
H=(2*s+1)/(s**2+3*s+2); print("4b",pf(H),il(H))
# 2010-11 3a
Y=(3*s+10)/(s**2+3*s+2); print("3a10",pf(Y),il(Y), "final", sp.limit(s*(Y),s,0))
# 2018-19 8a: y''+3y'+Ky=x'', K for stability, ZIR K=2
Y=(s*0+ (s+3)*0+1)/1
print("ZIR K2", il((0*s+1)/(s**2+3*s+2)))  # y(0+)=0,y'(0+)=1 -> Y=1/(s^2+3s+2)
# 3b 17-18 / 20-21 3a / 17-18: closed-loop H=H1/(1+H1H2)
b=sp.symbols('b'); print("20-21 3a", sp.simplify((1/(s**2+b*s+b-3))/(1+(1/(s**2+b*s+b-3))*(-2))))
print("17-18 3b", sp.simplify((1/(s**2+b*s+b-2))/(1+(1/(s**2+b*s+b-2))*(-1))))
# 2020-21 4a  H1=1/(s+2), H2=s/(s+3), K=2 : assume y feeding structure unknown -> skip
# 2023-24 5b feedback: plant 1/(s+2), controller (s+1)/s
G=(s+1)/(s*(s+2)); T=G/(1+G); print("5b",sp.simplify(T), sp.limit(s*T/s,s,0))
G2=1/((s-2)*(s+2)); T2=G2/(1+G2); print("5b2",sp.simplify(T2),sp.limit(s*T2/s,s,0))
# 2016-17 7b: X=(s^3+2s^2+3s+2)/(s^4+2s^3+2s^2+2s+2) -> LT of t x + x' + int_0^t x
X=(s**3+2*s**2+3*s+2)/(s**4+2*s**3+2*s**2+2*s+2); Y=-sp.diff(X,s)+s*X+X/s; print("7b16",sp.simplify(Y))
# 2016-17 8b
H=1/(4*s**2+2*s+1); print("8b16",il(H))
# 2011-12 3a: poles -2,4, h(0+)=4, H(0)=0 -> H=(a s^2+...)
