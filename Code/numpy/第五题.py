import numpy as np
X = [74,71,72,68,76,73,67,70,65,74]
y = [76,75,71,70,76,79,65,77,62,72]

# (1).数学期望
E_X=np.mean(X)
print(np.mean(X))
E_Y=np.mean(y)
print(np.mean(y))

# (2).方差
D_X=np.var(X)
print(np.var(X))
D_Y=np.var(y)
print(np.var(y))

# (3).标准差
S_X=np.std(X)
print(np.std(X))
S_Y=np.std(y)
print(np.std(y))

# 协方差
COV_XY = np.cov(X,y)
print(np.cov(X,y))

# (4).相关系数
R_XY = COV_XY / S_X * S_Y
print(R_XY)
