import pandas as pd 
import matplotlib.pyplot as plt 
import numpy as np 
from datetime import datetime


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


def heatmap2(dfs):
    height = len(dfs)
    width = dfs[0].shape[0]
    arr = np.zeros((height, width))

    for i in range(height):
        for j in range(width):
            arr[i,j]=dfs[i].iloc[j]
    plt.matshow(arr, cmap='hot')
    plt.colorbar()
    plt.show()


if __name__ =="__main__":
    filepath='52' 
    #select_day=[9,10,11,12,13,14,15,16,17,18,19,20,21,22]
    select_day=[9,10,11,12,13,14,15,16,17,18]

    dfs=[]
    begin_time = 5*60
    end_time = begin_time+60*5
    for day_index in range(len(select_day)):
        df = pd.read_csv(filepath+'_'+str(select_day[day_index])+'.csv')
        df = df.iloc[begin_time:end_time,2]
        dfs.append(df)
    
    heatmap2(dfs)






