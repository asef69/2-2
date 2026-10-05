import numpy as np # type: ignore

print(np.__version__)

arr1=np.array(10)

arr2=np.array([0,1,2,3,4,5,6,7,8,9])

print(arr1)

print(arr2)

#n-dim array te sobar same amount element thaka lagbe
arr3=np.array([[1,2,3,4,5,6,7],[23,5,6,73,34,66,44]])

print(arr3)

arr4=np.array([[12,13,14],[15,16,17]],ndmin=3)

print(arr4)
print(arr4.shape)
print(arr4.ndim)
print(arr4[0][0][1])
print(arr4[0,0,1])

print(arr4[0,-1,-1])


print(arr2[3:8])

print(arr2[2:8:2])

print(arr4[:,:,1:3])

arr6=np.array([1,2,3],dtype='S')
print(arr6)

arr7=arr6.copy()

arr8=arr6.view()
#arr8 and arr6 same memory ke point kore ache, so arr8 e change korle both change hobe but arr7 e change korle arr6 e kono change hobe na


print(arr7)
print(arr8)

print(arr8.base)
print(arr7.base)#nijei nijer data own kore

arr9=arr2.reshape(1,2,5)
print(arr9)

arr10=arr9.flatten()
print(arr10)

ones=np.ones(10)
zeros=np.zeros(10)
empty=np.empty(10)

tr=np.transpose(arr10)
arr11=arr10.T 
arr12=arr10.transpose()

arr13=np.concatenate((arr11,arr12))
print(arr13)   

arr14=np.vstack((arr10,arr12))
print(arr14)

np.sort(arr13)

arr15=(arr13 >=4)

arr16=arr13[arr15]
print(arr16)