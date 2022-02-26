'''
@File  :Dao_for_weatherandair.py
@Author:zhangxu
@Date  :2021/11/1020:12
@Desc  :
'''
import pymysql.cursors
from queue import Queue
import time

class Dao():

    def __init__(self):
        #初始化connection
        self.connection = pymysql.connect(
            host='10.1.0.13',
            user='root',
            password='root',
            db='thu-weatherdata',
            charset='utf8',
        )
        self.cursor=self.connection.cursor()
        self.count=0
        self.queue_entity=Queue()

    #将所有的air的元组都放到一个queue里面来，供后续的多线程调取
    def produce_queue(self):
        rows=self.get_all_air()
        for row in rows:
            self.queue_entity.put(row)
        return self.queue_entity


    def get_one_test(self):
        cursor=self.cursor
        sql="select * from air where city='七台河' and date='2015-01-02 00:00:00'"
        cursor.execute(sql)
        return cursor.fetchall()

    #获取air表中的所有元组并返回
    def get_all_air(self):
        cursor=self.cursor
        sql="select * from air"
        cursor.execute(sql)
        return cursor.fetchall()

    def update_weather_and_air(self,PM2_5,PM2_5_24h,PM10,PM10_24h,SO2,SO2_24h,NO2,NO2_24h,O3,O3_24h,O3_8h,O3_8h_24h,CO,CO_24h,city,date):
        cursor = self.cursor

        # entityWeather.print()

        sql = "update weather_copy1 set "+\
              "PM2_5="+"'"+PM2_5+"'"+\
              ",PM2_5_24h="+"'"+PM2_5_24h+"'"+\
              ",PM10=" +"'"+PM10+"'"+\
              ",PM10_24h=" +"'"+PM10_24h+"'"+\
              ",SO2="+"'"+SO2+"'"+ \
              ",SO2_24h="+"'"+SO2_24h+"'"+ \
              ",NO2=" +"'"+NO2+"'"+\
              ",NO2_24h="+"'"+NO2_24h+"'"+ \
              ",O3=" +"'"+O3+"'"+\
              ",O3_24h=" +"'"+O3_24h+"'"+\
              ",O3_8h=" +"'"+O3_8h+"'"+\
              ",O3_8h_24h=" +"'"+O3_8h_24h+"'"+\
              ",CO=" +"'"+CO+"'"+\
              ",CO_24h="+"'"+CO_24h+ "'"+\
              " WHERE city like '" +city+ "%' AND time like '"+date+"%'"  ""

        # try:
        print(sql)
        try:
            cursor.execute(sql)
        except Exception as e:
            print("本条错误指令:",sql)
            print(e)
            return
        self.count=self.count+1
        print("插入成功,总数目：",self.count)
        # except Exception as r:
        #     print('未知错误 %s' %r)

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