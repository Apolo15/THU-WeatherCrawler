'''
@File  :爬取现在新闻存入txtx.py
@Author:zhangxu
@Date  :2021/11/2510:14
@Desc  :
'''
import requests
import re
from lxml import etree
import time

if __name__ == '__main__':
    start_time = time.time()
    print('正在爬取。。。')
    fp = open('央视新闻.txt', 'w', encoding='utf-8')
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) \
                        AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.125 Safari/537.36 Edg/84.0.522.59'
    }
    url = 'https://news.cctv.com/2019/07/gaiban/cmsdatainterface/page/china_1.jsonp?cb=china'
    params = {
        'cb': 'china'
    }
    response = requests.get(url=url, params=params, headers=headers)
    response.encoding = 'utf-8'
    page_text = response.text
    ex1 = '"id".*?"title":"(.*?)","keywords"'
    ex2 = '"brief".*?,"url":"(.*?)"'
    title = re.findall(ex1, page_text)
    url = re.findall(ex2, page_text)

    for i in range(len(url)):
        res = requests.get(url=url[i], headers=headers)
        res.encoding = 'utf-8'
        response = res.text
        tree = etree.HTML(response)
        data = tree.xpath('//*[@id="content_area"]//text()')
        data = ''.join(data).strip().replace(' ', '')
        fp.write(title[i] + '\n' + data)

    end_time = time.time()
    print('爬取结束！用时{}s'.format(end_time - start_time))

