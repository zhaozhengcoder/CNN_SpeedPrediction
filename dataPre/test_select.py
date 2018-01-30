import numpy as np 
import pandas as pd 
from datetime import datetime

# read csv
def read_csv(filepath):
    data=pd.read_csv(filepath)
    data['last-update-time'] = pd.to_datetime(data['last-update-time'])
    return data

#pandas 取一个时间段的数据
def select_time_period(data):
    data1 =data[data['last-update-time']>datetime(2012,11,14,0,0)]
    data2 =data1[data1['last-update-time']<datetime(2012,11,15,0,0)]
    print ("select data shape is : ",data2.shape)
    return data2

if __name__=="__main__":
    filepath='52_csv.csv'
    data = read_csv(filepath)
    data2 = select_time_period(data)
    #data2.to_csv("ahahah.csv")