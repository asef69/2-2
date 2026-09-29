import matplotlib.pyplot as plt 
import numpy as np #type:ignore
xs=np.array([1,2,3,7,10])
ys=np.array([12,32,12,32,12])

plt.plot(xs,ys,marker='o',linestyle='--',color='hotpink')

xs=np.array([1,2,3,7,10])
ys=np.array([12,32,12,32,12])
plt.subplot(2,1,2)

plt.show()