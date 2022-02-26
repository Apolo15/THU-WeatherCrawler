'''
@File  :Test_beautifulsoup.py
@Author:zhangxu
@Date  :2021/11/2610:58
@Desc  :
http://m.news.cctv.com/2020/01/01/ARTIqrQF7e1puAmgoN4b7oaW200101.shtml
用BeautifulSoup获取央视新闻,这个页面的所有的文字稿，排除掉图片
'''

from bs4 import BeautifulSoup
import requests
import chardet
import re
from selenium import webdriver
import time

url='http://m.news.cctv.com/2020/01/01/ARTIqrQF7e1puAmgoN4b7oaW200101.shtml'

browser = webdriver.Chrome()
browser.get(url)

time.sleep(3)
print("重定向之后的url为：",browser.current_url)
url=browser.current_url
browser.quit()

header={
     'user-agent': 'Mozilla / 5.0(WindowsNT10.0;Win64;x64) AppleWebKit / 537.36(KHTML, like Gecko) Chrome / 91.0.4472.77 Safari / 537.36'

}

r=requests.get(url,headers=header,timeout=500)
r.encoding = chardet.detect(r.content)['encoding']

soup=BeautifulSoup(r.text,'html5lib')

#获取
#——————标题
title=soup.select("div[class~=col_w660] h1")
r_title=""
for row in title:
    try:
        r_title=r_title+row.text.replace(" ", "").replace('\n', '').replace('\r', '')
    except:
        continue
print("标题： ",r_title)


#——————来源时间
source_time=soup.select("div[class~=col_w660] span[class~=info] i")
r_source_time=""
for row in source_time:
    try:
        r_source_time=r_source_time+row.contents[0].replace(" ", "").replace('\n', '').replace('\r', '')
    except:
        continue
print(r_source_time)


#——————正文部分
p=soup.select("div[class~=wrapper] p")

result_p=""
for row in p:
    # result_p=result_p+row.text.replace(" ", "").replace('\n', '').replace('\r', '')
    try:
        # result_p=result_p+row.contents[0].replace(" ", "")
        result_p = result_p + row.contents[0].replace(" ", "").replace('\n', '').replace('\r', '')
    except:
        continue
    #筛选出了三段
    #flash视频没有去除
    #右边的相关新闻也被加入了

print(result_p)


#——————主编名录
tmp=soup.select("div[class~=col_w660]")
soup2=BeautifulSoup(str(tmp),'html5lib')
author=soup2.find_all(style=re.compile('font-size: 14px'))
r_author=""
for row in author:
    try:
        r_author=r_author+row.text+'\n'
    except:
        continue
print(r_author)
