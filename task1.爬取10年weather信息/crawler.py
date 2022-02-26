import requests
from bs4 import BeautifulSoup
import chardet
import json as js
import re
import time
import pandas as pd
import pymysql
from Entity.Entity_weather import Entity_weather
from DataBaseDao.DataBaseDao import DataBaseDao
from queue import Queue
from threading import Thread




def crawler(url, province, city, district, Dao):
    try:
        print(url)
        header = {
            'user-agent': 'Mozilla / 5.0(WindowsNT10.0;Win64;x64) AppleWebKit / 537.36(KHTML, like Gecko) Chrome / 91.0.4472.77 Safari / 537.36'
        }

        i = 0
        while (i < 3):
            try:
                r = requests.get(url, headers=header, timeout=500, verify=True, allow_redirects=True)
                break
            except requests.exceptions.RequestException as e:
                print(e)
                i += 1
        r.encoding = chardet.detect(r.content)['encoding']


        soup = BeautifulSoup(r.text, 'html5lib')

        ## 获取sunrise和sunset
        sunTime = soup.find("div", class_="sunTimes")
        sunRise = sunTime.select("span.sunrise.swip > span.time")[0].text.strip()
        sunSet = sunTime.select("span.sunset.swap > span.time")[0].text.strip()

        ## 获取script
        script = soup.select("body.day > script")[0].text
        m = re.search('var hours = (.+)[,;]{1}', script)
        if m:
            found = m.group(1)
            json =js.loads(found)
        # print(type(found))
        else:
            print("此条script为空，作废，下一条")
            return
        '''
        @Author:zhangxu
        @Desc  :41行代码我往后挪了挪，避免未申明就引用的情况并加入判空
        '''



        # 取中午十二点
        data = json[12] # type:'dict'
        b = data["time"] if "time" in data else None
        date = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(b)) #time
        apparentTemperature = data["apparentTemperature"] if "apparentTemperature" in data else None #apparentTemperature
        pressure = data["pressure"] if "pressure" in data else None#pressure
        cloudCover = data["cloudCover"] if "cloudCover" in data else None#cloudCover
        dewPoint = data["dewPoint"] if "dewPoint" in data else None#dewPoint
        humidity = data["humidity"] if "humidity" in data else None#humidity
        precipProbability = data["precipProbability"] if "precipProbability" in data else None#preciRate
        ozone = data["ozone"] if "ozone" in data else None#ozone
        precipType = data["precipType"] if "precipType" in data else None#preciType

        precipAccumulation = soup.select("div.precipAccum > span.val.swap > span.num.swip")
        if precipAccumulation != []:
            precipAccumulation = precipAccumulation[0].text.strip()
            if precipAccumulation == "???":
                precipAccumulation = None
        else:
            precipAccumulation = data["precipAccumulation"] if "precipAccumulation" in data else None#snowFall

        temperature = data["temperature"] if "temperature" in data else None#temperature
        textSummary = data["summary"] if "summary" in data else None#textSummary
        UVIndex = data["uvIndex"] if "uvIndex" in data else None#UVIndex
        windGust = data["windGust"] if "windGust" in data else None#windGust
        windSpeed = data["windSpeed"] if "windSpeed" in data else None#windSpeed
        windBearing = data["windBearing"] if "windBearing" in data else None#windBearing

        '''以下字段无法获取'''
        # moonPhase
        # nearestStormDis
        # nearestStormDir


        # print(date, province, city, district, apparentTemperature, pressure, cloudCover, dewPoint, humidity, precipProbability, ozone, precipType, precipAccumulation,temperature, textSummary, UVIndex, windGust, sunRise, windSpeed, sunSet, windBearing, lat, long)
        # print(date,data["temperature"])
        # js_test=js.loads(bs.find("script",{"id":"DATA_INFO"}).get_text())

        entityWeather= Entity_weather(province, city, district, sunRise, sunSet, date, apparentTemperature, pressure, cloudCover, dewPoint, humidity, precipProbability, ozone, precipType, precipAccumulation, temperature, textSummary, UVIndex, windGust, windSpeed, windBearing)
        # Dao.insert_weather(entityWeather)
        Dao.put_queueof_entity(entityWeather)


    except Exception as e:
        print(e)
        print(e.__traceback__.tb_frame.f_globals["__file__"])  # 发生异常所在的文件
        print(e.__traceback__.tb_lineno)  # 发生异常所在的行数
        return

class Spider():
    def __init__(self):
        self.qurl = Queue()

        self.thread_num = 10
        self.Dao=DataBaseDao()


    def produce_queue(self):
        '''
        @Author:zhangxu
        @Date  ：${DATE}${TIME}
        @Desc  :把excel里面所有数据存到一个队列里；     供多线程拿取
        '''
        df = pd.read_excel("gpsInfo.xlsx", sheet_name='gpsinfo')
        # print(df)
        for i in range(0, df.shape[0]):
            data = df.iloc[i].to_list()
            self.qurl.put(data)


    def get_info(self):
        while not self.qurl.empty(): # 保证url遍历结束后能退出线程
            data = self.qurl.get() # 从队列中获取URL

            print('目前爬取的城市区县的元组为', data)


            id, province, city, district, lat, long = data
            t = time.mktime(time.strptime("2010-01-01", '%Y-%m-%d'))
            t_end = time.mktime(time.strptime("2021-10-01", '%Y-%m-%d'))
            while t < t_end:
                date = time.strftime("%Y-%m-%d", time.localtime(t))
                url = "https://darksky.net/details/" + str(lat) + "," + str(long) + "/" + date + "/si12/en"

                crawler(url, province, city, district, self.Dao)
                t += 24 * 60 * 60  # 一天
                time.sleep(2)

    def run(self):
        self.produce_queue()

        ths = []
        for _ in range(self.thread_num):
            th = Thread(target=self.get_info)
            th.start()
            ths.append(th)
        print('【爬虫线程】：所有都启动完毕')

        th_insert=Thread(target=self.Dao.get_queueof_entity())
        th_insert.start()
        print('【搬运工线程】：启动完毕')







if __name__ == "__main__":

    Spider().run()
        

