'''
@File  :Test_local_beautifulsoup.py
@Author:zhangxu
@Date  :2021/11/2611:23
@Desc  :
'''
from bs4 import BeautifulSoup
import re
import requests
import chardet


path='sanyan.html'

htmlfile=open(path,'r',encoding='utf-8')

r=htmlfile.read()

soup=BeautifulSoup(r,'html5lib')


# wrapper=soup.select("div[class~=wrapper]")
# soup_wrapper=BeautifulSoup(str(wrapper),'html5lib')
# p=soup_wrapper("p")
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
