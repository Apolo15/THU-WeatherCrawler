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
#设置浏览器不加载图片
options.add_argument('--blink-settings=imagesEnabled=false')

'''其实可以加到list里面去，然后直接按照下标索引进行调用[].append'''
'''参考Test_listappend，里面我写好了样例，下次再用可以把browser放进去，进行封装爬取'''

browser_0 = webdriver.Chrome(options=options)
browser_1 = webdriver.Chrome(options=options)
browser_2 = webdriver.Chrome(options=options)
browser_3 = webdriver.Chrome(options=options)
browser_4 = webdriver.Chrome(options=options)

def test_chromedriver():
    print("11111111")
    print (browser_0.current_window_handle)
    print (browser_0.window_handles)
    time.sleep(2)
    browser_0.get('http://www.baidu.com');
    print("222222222")
    print (browser_0.current_window_handle)
    print (browser_0.window_handles)
    time.sleep(2)
    browser_0.get('http://www.jianshu.com');
    print("333333333")
    print (browser_0.current_window_handle)
    print (browser_0.window_handles)
    time.sleep(2)
    browser_0.close()
    print (browser_0.current_window_handle)
    print (browser_0.window_handles)




def resolve_info(i):
    '''

    :return: 不return ，会把爬取到的entity存入到一个队列中
    '''

    while 1:
        time.sleep(0.5)
        if  queue_a.empty() is False:
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

                if i ==0:
                    browser = browser_0
                if i ==1:
                    browser = browser_1
                if i ==2:
                    browser = browser_2
                if i == 3:
                    browser = browser_3
                if i == 4:
                    browser = browser_4


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
                queue_b.put(entity)
                print("--------解析成功并装载，当前线程号：", i)


            except Exception as e:
                print("解析出错",e)

def insert_entity():
    while 1:
        if not queue_b.empty() :
            dao.update2(queue_b.get())
            print("-------插入成功")
        else:
            print("error：插入队列中无数据，正在继续探测")
            time.sleep(15)

#获取一个存着所有url的队列A

#启动多线程爬取队列A中的数据后再存到一个队列B中

#由一个单独的线程从B中提取并插入到数据库


if __name__=="__main__":

    #存放所有从数据库里拿出来的链接
    queue_a=Queue()
    #存放所有爬取到的entity
    queue_b=Queue()


    rows=dao.get_allcctvnews()
    for row in rows:
        queue_a.put(row)

    th_pool=[]
    for i in range(5):
        #线程错峰出行
        time.sleep(1)
        #好像之前多线程一直启动的不到位指这个下面的参数问题我写的不对。
        th=Thread(target=resolve_info,args=(i,))
        th.start()
        th_pool.append(th)

    th_insert=Thread(target=insert_entity)
    th_insert.start()


    #这个是为了子线程结束之后阻塞子线程用的，免得主线程提前结束。
    for th in th_pool:
        th.join()
    th_insert.join()

    browser_0.quit()
    browser_1.quit()
    browser_2.quit()
    browser_3.quit()
    browser_4.quit()

    print("全部完毕")



