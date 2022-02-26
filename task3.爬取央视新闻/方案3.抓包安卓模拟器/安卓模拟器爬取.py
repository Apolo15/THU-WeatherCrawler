'''
@File  :安卓模拟器爬取.py
@Author:zhangxu
@Date  :2021/11/2515:01
@Desc  :根据安卓模拟器的抓包获取过去的新闻的标题和链接
'''
import requests
from time import sleep

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
# time_stamp = 1577875564000    #2020-01-01
time_stamp=1514797567000
count = 0      # 用来计算天数，如果超过31天就是2月份了，我没有去分析跨月份的规律是不是也是这样
while True:
    page += 1
    response = requests.get(url, params=get_params(page, time_stamp), headers=headers)
    result = response.json()['itemList']
    # print(result)
    if result:
        for data in result:
            news_url = data['detailUrl']
            news_title = data['itemTitle']
            print(news_title + '\t' + news_url)
    if len(result) == 0:
        page = 0
        time_stamp += 864640003#加一天
        count += 1
    sleep(2)
    if count > 31:
        break
