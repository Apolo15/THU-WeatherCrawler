import pymysql.cursors


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