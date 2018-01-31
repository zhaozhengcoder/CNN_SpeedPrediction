import pandas as pd 
import matplotlib.pyplot as plt 
import numpy as np 


def read_csv(filepath):
    data=pd.read_csv(filepath)
    data['last-update-time'] = data['last-update-time'].map(lambda s:s[:-4])  #删掉秒
    data['last-update-time'] = pd.to_datetime(data['last-update-time'])       #转换成时间戳的格式
    return data


# 计算某一列的数据缺失率
def miss_rate(data,colname='speed'):
    df = pd.isnull(data[colname])
    df_list = df.tolist()
    miss_rate = sum(df_list)/float(len(df_list))
    print (colname," miss rate is : ",miss_rate)


if __name__ =="__main__":
    data=read_csv('test_csv.csv')
    miss_rate(data)

