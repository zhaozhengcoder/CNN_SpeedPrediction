import pandas as pd 
import numpy as np 
import matplotlib.pyplot as plt 

df = pd.read_csv("test_csv.csv")
print (df) 

print (df[df['vol'] >4])