import pandas as pd 
import matplotlib.pyplot as plt 
import numpy as np 
from datetime import datetime

# read csv
def read_csv(filepath):
    data=pd.read_csv(filepath)
    data['last-update-time'] = data['last-update-time'].map(lambda s:s[:-4])  #删掉秒
    data['last-update-time'] = pd.to_datetime(data['last-update-time'])       #转换成时间戳的格式
    return data

# 可视化show
def show(data,filename='uname.jpg',colname='speed'):
    plt.plot(data[colname])
    plt.show()
    #filename=filename+'.jpg'
    #plt.savefig(filename)

# 计算某一列的数据缺失率
def miss_rate(data,colname='speed'):
    df = pd.isnull(data[colname])
    df_list = df.tolist()
    miss_rate = sum(df_list)/float(len(df_list))
    print ("col : ",colname,", miss rate is : ",miss_rate)

# 合并数据
def merge_data(data,colname='speed'):
    arr=np.array(data['speed'])
    speed_list = arr.tolist()
    merge_step = 5
    merge_length = len(speed_list) / merge_step 
    merge_list=[]
    for i in range(int(merge_length)):
        begin_index=i*merge_step
        merge_list.append(sum(speed_list[begin_index:begin_index+merge_step])/merge_step)
    return merge_list

# 简单的填充数据，将缺失的数据np.nan的数据 填充
def fillnan(data):
    #以一个默认的数值 填充
    #val=1.0
    #filldata=data.fillna(val)
    #前置值填充
    #filldata=data.fillna(method='ffill')
    #后置值填充
    filldata=data.fillna(method='bfill')
    return filldata


#pandas 取一个时间段的数据
def select_time_period(data,begin_day=14,end_day=15):
    data1 =data[data['last-update-time']>datetime(2012,11,begin_day,0,0)]
    data2 =data1[data1['last-update-time']<datetime(2012,11,end_day,0,0)]
    print ("select data shape is : ",data2.shape)
    return data2

#绘制热力图
def heatmap(data):
    data_to_arr = list(np.array(data['speed']))
    width = len(data_to_arr)
    height= 100
    arr = np.zeros((height, width))
    for i in range(height):
        for j in range(width):
            arr[i,j]= data_to_arr[j]
    plt.matshow(arr, cmap='hot')
    plt.colorbar()
    plt.show()


if __name__ =="__main__":
    filepath='52_csv.csv'
    data = read_csv(filepath)
    #miss_rate(data)
    #show(data)
    filldata=fillnan(data)
    print (filldata.head())

    selectdata = select_time_period(data)
    print (selectdata.head())
    #show(selectdata)
    heatmap(selectdata)