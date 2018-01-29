import pandas as pd 
import matplotlib.pyplot as plt 
import numpy as np 

data=pd.read_csv('test_csv.csv')

#print (data)
#print (type(data))

print (data['speed'])

arr = np.array(data['speed'])

speed_list=arr.tolist()

print (speed_list)