import numpy
import scipy.linalg as lina
#系数组成的数组（等号左边自变量的系数）
#系数行列式
a = numpy.array([[2,1,-5],
                 [1,-3,0],
                 [1,4,-7]])
#等号右边的值
b= numpy.array([8,9,0])
#解方程组
x = lina.solve(a,b)
print(x)