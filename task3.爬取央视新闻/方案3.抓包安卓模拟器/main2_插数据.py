'''
@File  :main2_插数据.py
@Author:zhangxu
@Date  :2021/11/2814:58
@Desc  :
'''
import requests
import time
from Entity.Entity_cctvnews import Entity_cctvnews
from DataBaseDao.Dao_for_cctvnews import DataBaseDao
import datetime
from bs4 import BeautifulSoup
import chardet
import re
from queue import Queue
from threading import Thread
from selenium import webdriver
import os

dao=DataBaseDao()
queue_b=dao.queue_b
options = webdriver.ChromeOptions()
# 添加无界面参数
options.add_argument('--headless')

browser = webdriver.Chrome(options=options)

def test_chromedriver():
    print("11111111")
    print (browser.current_window_handle)
    print (browser.window_handles)
    time.sleep(2)
    browser.get('http://www.baidu.com');
    print("222222222")
    print (browser.current_window_handle)
    print (browser.window_handles)
    time.sleep(2)
    browser.get('http://www.jianshu.com');
    print("333333333")
    print (browser.current_window_handle)
    print (browser.window_handles)
    time.sleep(2)
    browser.close()
    print (browser.current_window_handle)
    print (browser.window_handles)




def resolve_info():
    '''

    :return: 不return ，会把爬取到的entity存入到一个队列中
    '''

    while not queue_a.empty():
        '''
        #默认是有handle1在的

                #1、加入handle2,
                #2、处理handle1
                #3、跳转到handle2
        '''

        try:
            data=queue_a.get()
            id=data[0]
            time1=data[1]
            title1=data[2]
            url=data[3]


            browser.get(url)

            time.sleep(0.5)
            # print("重定向之后的url为：",browser.current_url)
            url2=browser.current_url




            header = {
                'user-agent': 'Mozilla / 5.0(WindowsNT10.0;Win64;x64) AppleWebKit / 537.36(KHTML, like Gecko) Chrome / 91.0.4472.77 Safari / 537.36'

            }

            r = requests.get(url2, headers=header, timeout=500)
            r.encoding = chardet.detect(r.content)['encoding']

            soup = BeautifulSoup(r.text, 'html5lib')

            # 获取
            # ——————标题
            title = soup.select("div[class~=col_w660] h1")
            r_title = ""
            for row in title:
                try:
                    r_title = r_title + row.text.replace(" ", "").replace('\n', '').replace('\r', '')
                except:
                    continue
            # print("标题： ", r_title)

            # ——————来源时间
            source_time = soup.select("div[class~=col_w660] span[class~=info] i")
            r_source_time = ""
            for row in source_time:
                try:
                    r_source_time = r_source_time + row.contents[0].replace(" ", "").replace('\n', '').replace('\r', '')
                except:
                    continue
            # print(r_source_time)

            # ——————正文部分
            p = soup.select("div[class~=wrapper] p")

            r_content = ""
            for row in p:
                # r_content=r_content+row.text.replace(" ", "").replace('\n', '').replace('\r', '')
                try:
                    # r_content=r_content+row.contents[0].replace(" ", "")
                    r_content = r_content + row.contents[0].replace(" ", "").replace('\n', '').replace('\r', '')
                except:
                    continue
                # 筛选出了三段
                # flash视频没有去除
                # 右边的相关新闻也被加入了

            # print(r_content)

            # ——————主编名录
            tmp = soup.select("div[class~=col_w660]")
            soup2 = BeautifulSoup(str(tmp), 'html5lib')
            author = soup2.find_all(style=re.compile('font-size: 14px'))
            r_author = ""
            for row in author:
                try:
                    r_author = r_author + row.text + '\n'
                except:
                    continue
            # print(r_author)

            entity=Entity_cctvnews(id,time1,title1,url,url2,r_title,r_source_time,r_content,r_author)
            dao.update2(entity)
            # queue_b.put(entity)

            # #解决selenium内存过载，cpu过载问题
            # os.system('taskkill /im chrome.exe /F')
            # os.system('taskkill /im chromedriver.exe /F')
            # os.system('taskkill /im webdriver.exe /F')



        except Exception as e:
            print("解析出错",e)



#获取一个存着所有url的队列A

#启动多线程爬取队列A中的数据后再存到一个队列B中

#由一个单独的线程从B中提取并插入到数据库


if __name__=="__main__":

    queue_a=Queue()

    rows=dao.get_allcctvnews()
    for row in rows:
        queue_a.put(row)




    th=Thread(target=resolve_info())
    th.start()

    browser.quit()

    print("全部完毕")



