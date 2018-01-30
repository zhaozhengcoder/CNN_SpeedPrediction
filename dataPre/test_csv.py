import pandas as pd 
import matplotlib.pyplot as plt 
import numpy as np 



# 计算某一列的数据缺失率
def miss_rate(data,colname='speed'):
    df = pd.isnull(data[colname])
    df_list = df.tolist()
    miss_rate = sum(df_list)/float(len(df_list))
    print (colname," miss rate is : ",miss_rate)


if __name__ =="__main__":
    data=pd.read_csv('11-14.csv')
    miss_rate(data)

