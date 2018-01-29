import pandas as pd 
import matplotlib.pyplot as plt 
import numpy as np 



# 计算某一列的数据缺失率
def miss_rate(data,colname='speed'):
    df = pd.isnull(data[colname])
    df_list = df.tolist()
    miss_rate = sum(df_list)/float(len(df_list))
    print (colname," miss rate is : ",miss_rate)


data=pd.read_csv('test_csv.csv')

#print (data)
#print (type(data))

print (data['speed'])

arr = np.array(data['speed'])

speed_list=arr.tolist()

print (speed_list)


print (miss_rate(data))

"""
data2 = pd.isnull(data['speed'])

print ( data2[data2[0]==True] )
#print ( pd.isnull(data['speed'])==True )
"""