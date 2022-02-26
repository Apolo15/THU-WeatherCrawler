import pymysql.cursors
from queue import Queue
import time

class DataBaseDao():

    def __init__(self):
        #初始化connection
        self.connection = pymysql.connect(
            host='localhost',
            user='root',
            password='',
            db='weatherdata',
            charset='utf8mb4',
        )

        self.qentity = Queue()
        '''
        1、插入表的名字我不知道，你按照你的表名更改一下这个函数名字吧
        '''
    def insert_weather(self,entityWeather):
        cursor = self.connection.cursor()
        '''
        2、这个地方的表名字也需要改,还有如果字符类型不一样，%s可能要改成和数据库字段的类型一致的,如果数据库还需要count计数可以再自己赋值一个count
        3、这个insert里面的字段名字要确认和数据一致
        '''
        entityWeather.print()
        sql = "INSERT INTO weather (province,city,district,sunRise,sunSet,apparentTemperature,pressure,cloudCover,dewPoint,humidity,precipProbability,ozone,precipType,precipAccumulation,temperature,summary,uvIndex,windGust,windSpeed,windBearing,time) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) "
        val = [entityWeather.province,
               entityWeather.city, 
               entityWeather.district, 
               entityWeather.sunRise,
               entityWeather.sunSet,
               entityWeather.apparentTemperature,
               entityWeather.pressure,
               entityWeather.cloudCover,
               entityWeather.dewPoint,
               entityWeather.humidity,
               entityWeather.precipProbability,
               entityWeather.ozone,
               entityWeather.precipType,
               entityWeather.precipAccumulation,
               entityWeather.temperature,
               entityWeather.summary,
               entityWeather.uvIndex,
               entityWeather.windGust,
               entityWeather.windSpeed,
               entityWeather.windBearing,
               entityWeather.date
               ]

        try:
            cursor.execute(sql, val)
            print("插入成功")
        except Exception as r:
            print('未知错误 %s' %r)

        # print("已插入第 :" + str(count) + "条数据")

        # 创建的connection是非自动提交，需要手动commit
        self.connection.commit()

    def put_queueof_entity(self, entityWeather):
        '''
        @Author:zhangxu
        @Date  ：${DATE}${TIME}
        @Desc  :把所有爬取到的数据，存到一个队列里，由某一个单独的线程单独插入
        '''
        self.qentity.put(entityWeather)

    def get_queueof_entity(self):
        count=0
        '''连续三次队列里都没数据的话就判断不会继续爬取到数据，整个爬虫停滞'''
        while(count<3):
            while not self.qentity.empty():  # 保证url遍历结束后能退出线程
                count=0
                entityWeather = self.qentity.get()
                self.insert_weather(entityWeather)
                # entityWeather.print()

            time.sleep(10)
            count=count+1
            print("开始沉睡")

        print("【搬运工线程】：沉睡3次，没有新数据插入，插入结束")







        #如果爬取数据插入队列的速度，没有插入数据库的速度快（即队列有时候是空的情况下），这种情况交给线程去判断，延续10秒