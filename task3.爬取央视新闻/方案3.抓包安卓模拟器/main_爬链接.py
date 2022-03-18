'''
@File  :main_爬链接.py
@Author:zhangxu
@Date  :2021/11/2814:04
@Desc  :融合安卓模拟器.py 和 beautifulsoup.py
'''
import requests
from time import sleep
from Entity.Entity_cctvnews import Entity_cctvnews,Entity_cctvnews_tu
from DataBaseDao.Dao_for_cctvnews import DataBaseDao
import datetime
from bs4 import BeautifulSoup
import chardet
import re


count1=0
dao= DataBaseDao()
def trans_time(timestamp):
    # 本系统中毫秒级的时间戳转化为2016-09-17 13:26:03 这样的格式
    timeStamp = float(timestamp) / 1000
    ret_datetime = datetime.datetime.utcfromtimestamp(timeStamp).strftime("%Y-%m-%d %H:%M:%S")
    return (ret_datetime)




def crawler():
    url = 'http://api.cportal.cctv.com/api/rest/articleInfo/getScrollList'
    headers = {
        'user-agent':'Mozilla/5.0 (Linux; U; Android 9; zh-cn; Redmi Note 5 Build/PKQ1.180904.001) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/71.0.3578.141 Mobile Safari/537.36 XiaoMi/MiuiBrowser/11.10.8'

    }

    def get_params(pg, pub_date):
        return {
            'n': '20',
            'version': '1',
            'p': pg,
            'pubDate': pub_date,
        }


    page = 0
    time_stamp = 1577875564000    #2020-01-01
    # time_stamp=1514797567000
    count = 0      # 用来计算天数，如果超过31天就是2月份了，我没有去分析跨月份的规律是不是也是这样
    while True:
        try:
            page += 1
            response = requests.get(url, params=get_params(page, time_stamp), headers=headers,timeout=500)
            print(trans_time(time_stamp))
            result = response.json()['itemList']
            # print(result)
            if result:
                for data in result:
                    news_url = data['detailUrl']
                    news_title = data['itemTitle']
                    entity_title_url=Entity_cctvnews_tu(trans_time(time_stamp),news_title,news_url)
                    dao.insert_cctvnews_2(entity_title_url)
                    # print(news_title + '\t' + news_url)

            if len(result) == 0:
                page = 0
                time_stamp += 86464000 #加一天
                count += 1
            sleep(1)

        except:
            global count1
            count1+=1
            print("解析出现问题，跳过,累计有问题数量为：",count1)
            sleep(5)
            continue




if __name__=="__main__":
    crawler()