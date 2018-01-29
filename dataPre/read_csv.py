import pandas as pd 
import matplotlib.pyplot as plt 
import numpy as np 

data=pd.read_csv('52_csv.csv')

#print (data)
#print (type(data))

print (data['speed'])
#plt.plot(data['speed'])
#plt.show()

arr=np.array(data['speed'])
speed_list = arr.tolist()

#print (len(speed_list))

#plt.plot(speed_list)

merge_step = 5
merge_length = len(speed_list) / merge_step 
merge_list=[]
for i in range(int(merge_length)):
    begin_index=i*merge_step
    merge_list.append(sum(speed_list[begin_index:begin_index+merge_step])/merge_step)

plt.plot(merge_list)
plt.show()