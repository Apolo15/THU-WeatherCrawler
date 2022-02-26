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
from urllib import request



# url='http://m.news.cctv.com/2020/01/01/ARTIqrQF7e1puAmgoN4b7oaW200101.shtml'
url='http://app.cctv.com/special/cportal/detail/arti/index.html?id=ArtiYQmbxnfXwlwpnTSnKIbH180101&isfromapp=1 '

# print(request.urlopen(url).geturl())
header={
     'user-agent': 'Mozilla/5.0 (Linux; U; Android 9; zh-cn; Redmi Note 5 Build/PKQ1.180904.001) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/71.0.3578.141 Mobile Safari/537.36 XiaoMi/MiuiBrowser/11.10.8'

}

r=requests.get(url,headers=header,timeout=500,allow_redirects=False)
# print(r.headers.get('Location'))
print(r.status_code)
print(r.history)



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
print("",r_title)


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

p_content=""
for row in p:
    # p_content=p_content+row.text.replace(" ", "").replace('\n', '').replace('\r', '')
    try:
        # p_content=p_content+row.contents[0].replace(" ", "")
        p_content = p_content + row.contents[0].replace(" ", "").replace('\n', '').replace('\r', '')
    except:
        continue
    #筛选出了三段
    #flash视频没有去除
    #右边的相关新闻也被加入了

print(p_content)


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
