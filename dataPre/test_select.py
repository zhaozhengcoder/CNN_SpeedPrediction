import numpy as np 
import pandas as pd 
from datetime import datetime

# read csv
def read_csv(filepath):
    data=pd.read_csv(filepath)
    data['last-update-time'] = data['last-update-time'].map(lambda s:s[:-4])  #删掉秒
    data['last-update-time'] = pd.to_datetime(data['last-update-time'])       #转换成时间戳的格式
    data.drop_duplicates('last-update-time','first',inplace=True)
    #data2 = data.set_index(['last-update-time'])
    data.set_index(['last-update-time'],inplace=True)
    return data

#pandas 取一个时间段的数据
def select_time_period(data,begin_day=14,end_day=15):
    data1 =data[data['last-update-time']>datetime(2012,11,begin_day,0,0)]
    data2 =data1[data1['last-update-time']<datetime(2012,11,end_day,0,0)]
    print ("select data shape is : ",data2.shape)
    return data2


# time
def fill_time_col(orig_data):
    vol_col=[]
    speed_col=[]
    #time_col = pd.date_range('11/14/2012',periods=1440,freq='1min')
    time_col = pd.date_range(datetime(2012,11,13,0,0),periods=1440,freq='1min')
    for i in time_col:
        if i in orig_data.index:
            vol_item=orig_data.loc[i]['vol']
            speed_item=orig_data.loc[i]['speed']
            vol_col.append(vol_item)
            speed_col.append(speed_item)
        else:
            vol_item=np.nan
            speed_item=np.nan
            vol_col.append(vol_item)
            speed_col.append(speed_item)
    return time_col,vol_col,speed_col

def build_newdataframe(speed_col,vol_col,time_col):
    df =pd.DataFrame(
        {
            'road':'gongyuanzhonglu(renminglu-henanlu)',
            'vol':np.array(vol_col),
            'speed':np.array(speed_col),
            'last-update-time':time_col,
        }
    )
    df.set_index(['last-update-time'],inplace=True)
    return df 


if __name__=="__main__":
    filepath='52_csv.csv'
    data = read_csv(filepath)
    time_col,vol_col,speed_col = fill_time_col(data)
    newdf = build_newdataframe(speed_col,vol_col,time_col)
