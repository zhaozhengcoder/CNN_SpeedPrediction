"""
可视化每一天的数据
"""

import pandas as pd 
import matplotlib.pyplot as plt 
import numpy as np 
from datetime import datetime



filepath='10' 
select_day=[9,10,11,12,13,14,15,16,17,18,19,20,21,22]


plt.figure()
for day_index in range(len(select_day)):
    #print (filepath+'_'+str(select_day[day_index])+'.csv')
    df = pd.read_csv('./'+filepath+'/'+filepath+'_'+str(select_day[day_index])+'.csv')
    plt.plot(df['speed'])
    plt.subplot(2,7,day_index+1)
plt.show()


