import numpy as np 
import pandas as pd 
from datetime import datetime

# read csv
def read_csv(filepath):
    data=pd.read_csv(filepath)
    data['last-update-time'] = data['last-update-time'].map(lambda s:s[:-4])  #删掉秒
    data['last-update-time'] = pd.to_datetime(data['last-update-time'])       #转换成时间戳的格式
    return data

#pandas 取一个时间段的数据
def select_time_period(data,begin_day=14,end_day=15):
    data1 =data[data['last-update-time']>datetime(2012,11,begin_day,0,0)]
    data2 =data1[data1['last-update-time']<datetime(2012,11,end_day,0,0)]
    print ("select data shape is : ",data2.shape)
    return data2

#生成时间
def generate_time_col(data='2012-11-14'):
    time=[]
    str1='23:59:26'
    str2='0:00:16'
    data=data+'  '
    for i in range(0,24):
        for j in range(0,60):
            if(j<10):
                time.append(data+str(i)+':'+'0'+str(j))
            else:
                time.append(data+str(i)+':'+str(j))
    return time

#不全时间数据
def build_datadict(orig_data):
    #格式 time:[speed,vol]
    datadict={}
    for i in range(orig_data.shape[0]):
        item=[]
        last_update_time=orig_data.iloc[i,3]
        time=last_update_time.strip()[:-3]
        item.append(orig_data.iloc[i,2])
        item.append(orig_data.iloc[i,1])
        datadict[time]=item
    return datadict

def fill_col(time_col,datadict):
    speed_col=[]
    vol_col=[]
    for i in time_col:
        if i in datadict:
            speed_col.append(datadict[i][0])
            vol_col.append(datadict[i][1])
        else:
            speed_col.append(np.nan)
            vol_col.append(np.nan)
    return speed_col,vol_col

def build_newdataframe(speed_col,vol_col,time_col):
    df =pd.DataFrame(
        {
            'road':'gongyuanzhonglu(renminglu-henanlu)',
            'vol':np.array(vol_col),
            'speed':np.array(speed_col),
            'last-update-time':np.array(time_col),
        }
    )
    return df 

def dataframe_to_csv(data):
    data.to_csv('new.csv')

if __name__=="__main__":

    filepath='52_csv.csv'
    data = read_csv(filepath)
    data2 = select_time_period(data)
    
    time_col = generate_time_col()
    datadict = build_datadict(data2)

    speed_col,vol_col = fill_col(time_col,datadict)

    newdf = build_newdataframe(speed_col,vol_col,time_col)

    dataframe_to_csv(newdf)

    end=1