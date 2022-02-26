'''
@File  :weather_and_air.py
@Author:zhangxu
@Date  :2021/11/1020:08
@Desc  :
'''

from datetime import datetime
import time
from DataBaseDao.Dao_for_weatherandair import Dao
from threading import Thread

class update_weather_and_air():

    def __init__(self):
        self.thread_num = 10
        self.dao = Dao()
        self.queue = self.dao.produce_queue()
        self.count=0 #粗略统计已经执行的总的数目


    def get_rowinfo_and_insert(self,count_thead):
        dao=self.dao
        while not self.queue.empty():

            row = self.queue.get()
            city = row[0]
            date = str(datetime.strptime(str(row[1]), '%Y-%m-%d %H:%M:%S').strftime('%Y-%m-%d'))
            AQI = str(row[2])
            PM2_5 = str(row[3])
            PM2_5_24h = str(row[4])
            PM10 = str(row[5])
            PM10_24h = str(row[6])
            SO2 = str(row[7])
            SO2_24h = str(row[8])
            NO2 = str(row[9])
            NO2_24h = str(row[10])
            O3 = str(row[11])
            O3_24h = str(row[12])
            O3_8h = str(row[13])
            O3_8h_24h = str(row[14])
            CO = str(row[15])
            CO_24h = str(row[16])

            self.count=self.count+1
            print("当前遍历过的air数目条数为：","【",count_thead,"】     ",self.count)

            if AQI == "None" and PM2_5 == "None" and PM2_5_24h == "None" and PM10 == "None" and PM10_24h == "None" and SO2 == "None" and SO2_24h == "None" and NO2 == "None" and NO2_24h == "None" and O3 == "None" and O3_24h == "None" and O3_8h == "None" and O3_8h_24h == "None" and CO == "None" and CO_24h == "None":
                print("该条数据全都是空值，已跳过")
                continue

            dao.update_weather_and_air(PM2_5, PM2_5_24h, PM10, PM10_24h, SO2, SO2_24h, NO2, NO2_24h, O3, O3_24h, O3_8h,
                                   O3_8h_24h, CO, CO_24h, city, date)

            # print("插入过程中出错，此条已经跳过")

    def run(self):
        ths = []
        count=0
        for _ in range(self.thread_num):
            count=count+1
            th = Thread(target=self.get_rowinfo_and_insert(count))
            th.start()

            print("该线程启动完毕")
            ths.append(th)
        print('【线程】：所有都启动完毕')



if __name__ =="__main__":
    update_weather_and_air().run()
    print("数据全部完毕")






# dao=Dao()
#
# #1、遍历整个air表，提取city（对应weather里的city）  data（对应weather里的time）  都是包含关系
# #2、符合就插入
# #3、不符合就继续下一条
#
# queue=dao.produce_queue()
#
#
#
#
#
# rows=dao.get_all_air()
# count=0
# for row in rows:
#
#     city = row[0]
#     date = str(datetime.strptime(str(row[1]), '%Y-%m-%d %H:%M:%S').strftime('%y-%m-%d'))
#     AQI=str(row[2])
#     PM2_5=str(row[3])
#     PM2_5_24h=str(row[4])
#     PM10=str(row[5])
#     PM10_24h=str(row[6])
#     SO2=str(row[7])
#     SO2_24h=str(row[8])
#     NO2=str(row[9])
#     NO2_24h=str(row[10])
#     O3=str(row[11])
#     O3_24h=str(row[12])
#     O3_8h=str(row[13])
#     O3_8h_24h=str(row[14])
#     CO=str(row[15])
#     CO_24h=str(row[16])
#
#
#     count=count+1
#     print("当前遍历过的air数目条数为：",count)
#
#
#     # if AQI is None and PM2_5 is None and PM2_5_24h is None and PM10 is None and PM10_24h is None and SO2 is None and SO2_24h is None and NO2 is None and NO2_24h is None and O3 is None and O3_24h is None and O3_8h is None and O3_8h_24h is None and CO is None and CO_24h is None:
#     #     continue
#     if AQI =="None" and PM2_5 =="None" and PM2_5_24h =="None" and PM10 =="None" and PM10_24h =="None" and SO2 =="None" and SO2_24h =="None" and NO2 =="None" and NO2_24h =="None" and O3 =="None" and O3_24h =="None" and O3_8h =="None" and O3_8h_24h =="None" and CO =="None" and CO_24h =="None":
#         print("该条数据全都是空值，已跳过")
#         continue
#
#
#
#     dao.update_weather_and_air(PM2_5,PM2_5_24h,PM10,PM10_24h,SO2,SO2_24h,NO2,NO2_24h,O3,O3_24h,O3_8h,O3_8h_24h,CO,CO_24h,city,date)