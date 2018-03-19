import numpy as np 
import pickle
import tensorflow as tf


#原始的data里面的数据格式是dataframe，arr改成了里面也是list
def transfer(data):
    speed_col_index = 2
    height = len(data)
    width = data[0].shape[0]
    arr = np.zeros((height, width))
    for i in range(height):
        for j in range(width):
            arr[i,j]=data[i].iloc[j,speed_col_index]
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
    train_x_len=12
    train_y_len=3
    train_x=[]
    train_y=[]
    np_arr= np.array(arr)
    for i in range(np_arr.shape[1]-train_x_len-train_y_len):
        train_x.append(arr[:,i:i+train_x_len])
        train_y.append(arr[:,i+train_x_len:i+train_x_len+train_y_len])
    #return train_x,train_y
    np_train_x = np.array(train_x)
    np_train_y = np.array(train_y)
    #reshape 成 （sample * 每一个样本的特征）
    np_train_x_reshape = np_train_x.reshape(np_arr.shape[1]-train_x_len-train_y_len,-1) #（45 * 20 * 12）
    np_train_y_reshape = np_train_y.reshape(np_arr.shape[1]-train_x_len-train_y_len,-1) #（45 * 20 * 3）
    return np_train_x_reshape,np_train_y_reshape

def compute_accuracy(v_xs, v_ys):
    global prediction
    y_pre = sess.run(prediction, feed_dict={xs: v_xs, keep_prob: 1})
    correct_prediction = tf.equal(tf.argmax(y_pre,1), tf.argmax(v_ys,1))
    accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))
    result = sess.run(accuracy, feed_dict={xs: v_xs, ys: v_ys, keep_prob: 1})
    return result

def weight_variable(shape):
    initial = tf.truncated_normal(shape, stddev=0.1)
    return tf.Variable(initial)

def bias_variable(shape):
    initial = tf.constant(0.1, shape=shape)
    return tf.Variable(initial)

def conv2d(x, W):
    # stride [1, x_movement, y_movement, 1]
    # Must have strides[0] = strides[3] = 1
    return tf.nn.conv2d(x, W, strides=[1, 1, 1, 1], padding='SAME')

def max_pool_2x2(x):
    # stride [1, x_movement, y_movement, 1]
    return tf.nn.max_pool(x, ksize=[1,2,2,1], strides=[1,2,2,1], padding='SAME')

def my_normalize(arr):
    amin,amax =arr.min(),arr.max()
    arr = (arr-amin)/(amax-amin)
    return arr

def cal_mre(pre_y,train_y):
    diff = abs(pre_y-train_y)
    mre_matrix = diff/train_y
    return mre_matrix.mean()

def replace_ele(train_y):
    train_y[train_y<0.01]=0.1
    return train_y

if __name__=="__main__":
    #load
    data = myload()
    #transfer
    arr = transfer(data)
    #print (arr)  #shape 20*60 
    #归一化
    arr = my_normalize(arr)
    train_x,train_y = arr_split_traindata(arr)  #train_x shape:45*240(240=20*12) ;train_y shape :45*60(60=20*3)
    #train_y中有为0的元素，改成一个非0的数字
    train_y = replace_ele(train_y)

    xs = tf.placeholder(tf.float32, [None, 240])
    ys = tf.placeholder(tf.float32, [None, 60])

    x_image = tf.reshape(xs, [-1, 20, 12, 1])

    #第一层
    W_conv1 = weight_variable([5,5, 1,32])  
    b_conv1 = bias_variable([32])
    #卷积运算
    h_conv1 = tf.nn.relu(conv2d(x_image, W_conv1) + b_conv1)  # output size 20*12*32
    h_pool1 = max_pool_2x2(h_conv1)                           # output size 10*6*32

    #第二层
    W_conv2 = weight_variable([5,5, 32, 64]) 
    b_conv2 = bias_variable([64])
    h_conv2 = tf.nn.relu(conv2d(h_pool1, W_conv2) + b_conv2) # output size 10x6x64
    h_pool2 = max_pool_2x2(h_conv2)                          # output size 5x3x64

    W_fc1 = weight_variable([5*3*64, 60])
    b_fc1 = bias_variable([60])

    h_pool2_flat = tf.reshape(h_pool2, [-1, 5*3*64])
    prediction = tf.nn.relu(tf.matmul(h_pool2_flat, W_fc1) + b_fc1)

    #loss
    loss = tf.reduce_mean(tf.reduce_sum(tf.square(ys - prediction),reduction_indices=[1]))
    #loss = tf.reduce_mean(tf.reduce_sum(tf.square(ys - prediction))
    train_step = tf.train.GradientDescentOptimizer(1e-4).minimize(loss)
    #train_step = tf.train.GradientDescentOptimizer(0.05).minimize(loss)

    #init
    sess = tf.Session()
    if int((tf.__version__).split('.')[1]) < 12 and int((tf.__version__).split('.')[0]) < 1:
        init = tf.initialize_all_variables()
    else:
        init = tf.global_variables_initializer()
    sess.run(init)

    # 原来是1000 为了快一点 改成了1000
    for i in range(50000):
        sess.run(train_step, feed_dict={xs: train_x, ys: train_y})
        if i % 50 == 0:
            #print (sess.run(prediction, feed_dict={xs: train_x, ys: train_y}).shape)  # 45 * 60
            pre_y = sess.run(prediction, feed_dict={xs: train_x, ys: train_y})
            print (cal_mre(pre_y,train_y))
            print ("loss : ",sess.run(loss, feed_dict={xs: train_x, ys: train_y}))