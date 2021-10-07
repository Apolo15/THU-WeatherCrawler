import shutil
from pandas.core.frame import DataFrame
import xlrd
import sys
import os
import time
import pandas as pd

gpsfile=[]
for root, dirs, files in os.walk(os.getcwd()):
    for file in files:
        if os.path.splitext(file)[1] == '.xlsx':
            gpsfile.append(os.path.join(root, file))
column = ['Province','City','District','Lat','Long']
data = pd.DataFrame(columns = column) 
for i in gpsfile:
    df=pd.read_excel(i,sheet_name='Sheet1')
    header = set(df.columns)
    if set(column).issubset(header):
        print(i, "：表格完整")
    else:
        print(i, "：该表格并不完整！")
        break
    data = data.append(df.loc[:,column].drop_duplicates(),ignore_index=True)
    # print(data)
    time.sleep(10)

data.to_excel("gpsinfo.xlsx",encoding="utf-8", index=True)