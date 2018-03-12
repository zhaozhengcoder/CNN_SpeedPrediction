import numpy as np 
import pickle


#原始的data里面的数据格式是dataframe，arr改成了里面也是list
def transfer(data):
    speed_col_index = 2
    height = len(data)
    width = data[0].shape[0]
    arr = np.zeros((height, width))
    for i in range(height):
        for j in range(width):
            arr[i,j]=int(data[i].iloc[j,speed_col_index])
    return arr

def myload():
    abs_path='C:/Users/wwwa8/Documents/GitHub/CNN_SpeedPrediction/dataPre2/master2/'
    filename ='dump.txt'
    f = open(abs_path+filename,'rb')
    data =pickle.load(f)
    f.close()
    #print (data)   # 路段数 * 每个路段的信息（df的数据结构）
    return data

def arr_split_traindata(arr):
    train_x_len=10
    train_y_len=3
    train_x=[]
    train_y=[]
    np_arr= np.array(arr)
    for i in range(np_arr.shape[1]-train_x_len-train_y_len):
        train_x.append(arr[:,i:i+train_x_len])
        train_y.append(arr[:,i+train_x_len:i+train_x_len+train_y_len])
    return train_x,train_y



if __name__=="__main__":
    #load
    data = myload()
    #transfer
    arr = transfer(data)
    print (arr)  #shape 20*60 

    train_x,train_y = arr_split_traindata(arr)