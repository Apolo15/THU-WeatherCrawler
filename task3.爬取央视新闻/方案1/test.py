'''
测试代码
'''
import os

from xls_functions import *
from get_data import *
import re
import requests

book_name_xls = 'xls格式测试工作簿.xls'
sheet_name_xls = 'xls格式测试表'
value_title = [["姓名", "性别", "年龄", "城市", "职业"], ]
value1 = [["张三", "男", "19", "杭州", "研发工程师"],
          ["李四", "男", "22", "北京", "医生"],
          ["王五", "女", "33", "珠海", "出租车司机"], ]
value2 = [["Tom", "男", "21", "西安", "测试工程师"],
          ["Jones", "女", "34", "上海", "产品经理"],
          ["Cat", "女", "56", "上海", "教师"], ]
if os.path.exists(book_name_xls):
    os.remove(book_name_xls)
write_excel_xls(book_name_xls, sheet_name_xls, value_title)
write_excel_xls_append(book_name_xls, value1)
# write_excel_xls_append(book_name_xls, value2)
read_excel_xls(book_name_xls)

# url = 'http://api.cportal.cctv.com/api/rest/articleInfo/getScrollList?n=20&version=1&p=1&pubDate=1622728276000&app_version=810'
# response = requests.get(url)
# result = response.json()['itemList'][0]
# # print(result)
# item_id = result['itemID']
# params = {
#     'id':item_id
# }
# item_url ='http://api.cportal.cctv.com/api/rest/articleInfo'
# news_response = requests.get(item_url,params=params)
# news_response.encoding = 'unicode_escape'
# news_result = news_response.text
# print(news_result)

# local_time = 1622728276000
# date = time_trans(local_time)
# print(date)
# date = str(date)
# print(date)

# def trans_time(date):
#     '''
#         将输入的日期转换为时间戳
#     :param date: 用户输入的日期
#     :return:当前日期的凌晨0点的时间戳
#     '''
#     date1 = date + ' 00:00:00'
#     print(date1)
#     timeArray = time.strptime(date1, "%Y-%m-%d %H:%M:%S")
#     timeStamp = int(time.mktime(timeArray)) * 1000
#     return timeStamp
#
# date = '2021-06-03'
# a = trans_time(date)
# print(a)

# def get_name(text):
#     # rex1 = "（{1}(.+?)[记者]+(.+?)）"
#     rex1 = "[（|(]{1}[总台记者|总台央视记者|记者]+ [^（,(]*[)|）]"
#     res1 = re.search(rex1, text)
#     if res1:
#         result1 = res1.group()
#         return result1
#     else:
#         return None
#
# text ='（总台记者 贾延宁）<\/p><p><strong>此前消息：<\/strong><\/p><p><span style="color: rgb(0, 112, 192);"><strong>一架从乍得飞往巴黎航班疑似发现爆炸物<\/strong><\/span><\/p><p>据法国内政部3日下午发布的新闻公报，法航一架从乍得飞往巴黎的航班疑似有爆炸物。<\/p><p style="text-align: center;"><img src="https:\/\/p1.img.cctvpic.com\/cportal\/cnews-yz\/img\/2021\/06\/03\/1622734472693_906_800x954.jpg" localname="1622734472693_906_800x954.jpg" localpath="\/img\/2021\/06\/03\/" publishflag="" imginfo="" style="max-width: 100%" _src="https:\/\/p1.img.cctvpic.com\/cportal\/cnews-yz\/img\/2021\/06\/03\/1622734472693_906_800x954.jpg"><\/p><p><span style="font-size: 14px; color: rgb(127, 127, 127)'
# res1 = get_name(text)
# print(res1)