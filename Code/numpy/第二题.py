import numpy as np
from numpy.linalg import *

info = np.array([[1,3,9,0],
                 [14,15,20,1],
                 [1,1,3,6]])
info_A = np.mat(info)   #使用 mat 方法将 2 维数组转化为矩阵

key = np.array([[3,1,-1,2],
                [-5,1,3,-4],
                [2,0,1,-1],
                [1,-5,3,-3]])
key_A = np.mat(key)   #使用 mat 方法将 2 维数组转化为矩阵
print("密钥：",key_A)
after_A = info_A*key_A
print("加密后：",after_A)
print("#######################")
print("解密")
#print(det(key))
#key1 = np.array([[3,5,7],
#               [4,7,20],
#              [100,1,0]])
#key1_A = np.mat(key1)   #使用 mat 方法将 2 维数组转化为矩阵
print(after_A*key_A.I)
