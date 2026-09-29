import numpy as np
import matplotlib.pyplot as plt

def signal(t):
    x= np.zeros_like(t)
    m1 = (t>=-2) & (t<=-1)
    m2 = (t>=-1) & (t<=0)
    m3 = (t>=0) & (t<=1)
    m4 = (t>=1) & (t<=2)
    x[m1] = 1+t[m1]
    x[m2] = 1
    x[m3] = 2
    x[m4] = 2 - t[m4]
    return x

def main():
    t = np.linspace(-100,100,20000)
    x= np.zeros_like(t)
    m1 = (t>=-2) & (t<=-1)
    m2 = (t>=-1) & (t<=0)
    m3 = (t>=0) & (t<=1)
    m4 = (t>=1) & (t<=2)
    x[m1] = 1+t[m1]
    x[m2] = 1
    x[m3] = 2
    x[m4] = 2 - t[m4]
    xi = np.interp(-t,t,x,left=0.0,right=0.0)

    xo = 0.5 * (xi-x)
    xe = 0.5 * (x-xi)

    fig,ax = plt.subplots(2,3,figsize=(15,9))
    ax[0][0].plot(t,x,lw=2,color = 'blue')
    ax[0][0].grid(alpha=0.3)
    ax[0][0].set_xlim(-5,5)
    ax[0][0].set_title("x(t)")
    ax[0][1].plot(t,np.interp(t-1,t,x,left=0.0,right = 0.0),lw=2,color = 'blue')
    ax[0][1].grid(alpha=0.3)
    ax[0][1].set_xlim(-5,5)
    ax[0][1].set_title("x(t-1)")
    ax[0][2].plot(t,np.interp(2-t,t,x,left=0.0,right = 0.0),lw=2,color = 'blue')
    ax[0][2].grid(alpha=0.3)
    ax[0][2].set_xlim(-5,5)
    ax[0][2].set_title("x(2-t)")
    ax[1][0].plot(t,np.interp(2*t+1,t,x,left=0.0,right = 0.0),lw=2,color = 'blue')
    ax[1][0].grid(alpha=0.3)
    ax[1][0].set_xlim(-5,5)
    ax[1][0].set_title("x(2t+1)")
    ax[1][1].plot(t,np.interp(4-t/2,t,x,left=0.0,right = 0.0),lw=2,color = 'blue')
    ax[1][1].grid(alpha=0.3)
    ax[1][1].set_xlim(0,20)
    ax[1][1].set_title("x(4-t/2)")
    
    plt.show()

main() 