'''
@File  :Dao_for_cctvnews.py
@Author:zhangxu
@Date  :2021/11/2814:22
@Desc  :
'''

import pymysql.cursors
from queue import Queue
import time


class DataBaseDao():
    def __init__(self):
        # 初始化connection
        self.connection = pymysql.connect(
            host='10.1.0.13',
            user='root',
            password='root',
            db='thu-weatherdata',
            charset='utf8',
        )
        self.queue_b=Queue()
        self.count=0

    def insert_cctvnews(self, entitycctvnews):
        cursor = self.connection.cursor()

        entitycctvnews.print()
        sql = "INSERT INTO cctv_news (time,title,url,url2,title_2,sourceandtime,content,author) VALUES (%s,%s,%s,%s,%s,%s,%s) "
        val = [
               entitycctvnews.time,
               entitycctvnews.title,
               entitycctvnews.url,
               entitycctvnews.url2,
               entitycctvnews.title_2,
               entitycctvnews.sourceandtime,
               entitycctvnews.content,
               entitycctvnews.author

               ]

        try:
            cursor.execute(sql, val)
            print("插入成功")
        except Exception as r:
            print('未知错误 %s' % r)

        # print("已插入第 :" + str(count) + "条数据")

        # 创建的connection是非自动提交，需要手动commit
        self.connection.commit()

    def insert_cctvnews_2(self, entitycctvnews):
        cursor = self.connection.cursor()

        entitycctvnews.print()
        sql = "INSERT INTO cctv_news (time,title,url) VALUES (%s,%s,%s) "
        val = [
               entitycctvnews.time,
               entitycctvnews.title,
               entitycctvnews.url

               ]

        try:
            cursor.execute(sql, val)
            print("==插入成功======")
            entitycctvnews.print()
        except Exception as r:
            print('未知错误 %s' % r)

        # print("已插入第 :" + str(count) + "条数据")

        # 创建的connection是非自动提交，需要手动commit
        self.connection.commit()


    def get_allcctvnews(self):
        cursor = self.connection.cursor()
        sql = "select * from cctv_news where id >200858"
        cursor.execute(sql)
        return cursor.fetchall()

    def get_10cctvnews(self):
        cursor = self.connection.cursor()
        sql = "select * from cctv_news limit 10"
        cursor.execute(sql)
        return cursor.fetchall()

    def update(self):
        cursor=self.connection.cursor()
        count=0
        while(count<3):
            while not self.queue_b.empty():
                entity=self.queue_b.get()
                entity.print()
                sql="update cctv_news set url2=%s,title_2= %s,sourceandtime= %s,content= %s,author= %s WHERE id= %s"
                val=[entity.url2,entity.title_2,entity.sourceandtime,entity.content,entity.author,entity.id]
                cursor.execute(sql,val)
                print("四列数据update成功")
                self.connection.commit()

            self.connection.commit()
            count=count+1
            print("数据已插入一次，开始沉睡")
            time.sleep(7)

        print("沉睡三次已满，没有新数据插入，插入接受")
        # self.connection.commit()



    def update2(self,entity):
        cursor = self.connection.cursor()
        try:
            entity.print()
            sql="update cctv_news set url2=%s,title_2= %s,sourceandtime= %s,content= %s,author= %s WHERE id= %s"
            val=[entity.url2,entity.title_2,entity.sourceandtime,entity.content,entity.author,entity.id]
            cursor.execute(sql,val)
            print("插入update成功")
            self.connection.commit()
        except:
            print("插入过程中出错")

