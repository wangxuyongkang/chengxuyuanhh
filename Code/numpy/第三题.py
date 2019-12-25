import numpy as np
A = np.mat([[1,2],
            [1,4],
            [0,1],
            [5,3]])
u,sigma,v = np.linalg.svd(A)
print("u=",u)
print("sigma=",sigma)
print("v=",v)