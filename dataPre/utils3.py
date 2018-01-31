"""
这个功能是 切分数据和补全数据
对于一个52_csv.csv 文件，将它切分为每一天，然后用前后天的数据补全他们
"""

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
"""
def select_time_period(data,begin_day=14,end_day=15):
    data1 =data[data['last-update-time']>datetime(2012,11,begin_day,0,0)]
    data2 =data1[data1['last-update-time']<datetime(2012,11,end_day,0,0)]
    print ("select data shape is : ",data2.shape)
    return data2
"""

# time
def select_col(orig_data,select_day=13):
    vol_col=[]
    speed_col=[]
    #time_col = pd.date_range('11/14/2012',periods=1440,freq='1min')
    time_col = pd.date_range(datetime(2012,11,select_day,0,0),periods=1440,freq='1min')
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

def find_col_index(df,columns_name):
    for i in range(len(data.columns)):
        if data.columns[i]==columns_name:
            return i 
    sys.exit("sorry, find_col_index can't find correct colnums_name .")

def miss_rate(data,colname='speed'):
    df = pd.isnull(data[colname])
    df_list = df.tolist()
    miss_rate = sum(df_list)/float(len(df_list))
    print ("col : ",colname,", miss rate is : ",miss_rate)

def fill_df(result_df):
    speed_col_index = find_col_index(result_df[0],'speed')
    vol_col_index = find_col_index(result_df[0],'vol')
    for df_index in range(len(result_df)):
        for i in range(result_df[df_index].shape[0]):
            if np.isnan(result_df[df_index].iloc[i,speed_col_index]):
                if df_index ==0:  #从后面找
                    find_index=df_index+1
                    while find_index < len(result_df):
                        if np.isnan(result_df[find_index].iloc[i,speed_col_index])==False:
                            result_df[df_index].iloc[i,speed_col_index] = result_df[find_index].iloc[i,speed_col_index]
                            result_df[df_index].iloc[i,vol_col_index]   = result_df[find_index].iloc[i,vol_col_index]
                            break
                        find_index+=1
                    result_df[df_index]=result_df[df_index].fillna(method='bfill')
                else:   #从前面找
                    result_df[df_index].iloc[i,speed_col_index] = result_df[df_index-1].iloc[i,speed_col_index]
                    result_df[df_index].iloc[i,vol_col_index]   = result_df[df_index-1].iloc[i,vol_col_index]



if __name__=="__main__":
    filepath='52_csv.csv' 
    data = read_csv(filepath)
    
     # 9-22
    select_day=[9,10,11,12,13,14,15,16,17,18,19,20,21,22]
    result_df=[]
    
    for day in select_day:
        time_col,vol_col,speed_col = select_col(data,day)
        result_df.append(build_newdataframe(speed_col,vol_col,time_col))

    for i in result_df:
        miss_rate(i)

    fill_df(result_df)

    for i in result_df:
        miss_rate(i)

    for df ,day in zip(result_df,select_day):
        df.to_csv(filepath+str(day)+'.csv')
