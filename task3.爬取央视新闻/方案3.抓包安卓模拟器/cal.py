'''
@File  :cal.py
@Author:zhangxu
@Date  :2021/11/2516:23
@Desc  :
'''
import time
import datetime
t_2020=1577875564000
t_oneday=864640003


t_2016=1474118763640
t_2018=1525997163820


t_2018=t_2020-30*(t_oneday) #1474118763640
# print(t_2018)
def trans_time(timestamp):
    #本系统中毫秒级的时间戳转化为2016-09-17 13:26:03 这样的格式
    timeStamp = float(timestamp)/1000
    ret_datetime = datetime.datetime.utcfromtimestamp(timeStamp).strftime("%Y-%m-%d %H:%M:%S")
    print (ret_datetime)

time = 1577875564000
for _ in range(100):
    trans_time(time)
    time += 86464000  # 加一天