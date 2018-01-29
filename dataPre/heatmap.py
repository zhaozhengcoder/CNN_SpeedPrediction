import pandas as pd 
import matplotlib.pyplot as plt 
import numpy as np 

x=[1,2,3,4,5]
y=[5,4,3,2,1]

v=[10,20,30,40,50]

height = np.max(y) + 1
width = np.max(x) + 1
arr = np.zeros((height, width))
for i in range(len(x)):
    arr[y[i], x[i]] = v[i]

plt.matshow(arr, cmap='hot')
plt.colorbar()
plt.show()


"""
https://segmentfault.com/q/1010000005721713

https://discuss.analyticsvidhya.com/t/how-to-plot-heat-map-in-python/1922/2
"""