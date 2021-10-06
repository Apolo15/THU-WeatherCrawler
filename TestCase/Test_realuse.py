
import requests
from lxml import etree
import pandas as pd
from prettytable import PrettyTable
import os
import re


def get_html(url):
    # 定义头文件
    headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.190 Safari/537.36'}
    # 发起请求
    response = requests.get(url, headers=headers)
    # 修改编码
    response.encoding = 'utf8'
    # 处理成HTML格式
    html = etree.HTML(response.text)
    # print(response.text)
    return html


if __name__ == '__main__':
    # 实例化输出类
    p = PrettyTable()
    # 接口URL
    url = 'https://darksky.net/details/39.9027,116.4008/2021-10-4/si12/zh'
    # 调用获取HTML的方法
    html = get_html(url)
    # print()

    hours=html.xpath('/html/body/script[1]/text()')
    print(hours)
    storage_hours=re.findall('var hours = \[{.*?}\]',str(hours),re.S)
    # test=re.findall('"time":1.*?0',str(hours),re.S)
    print(storage_hours)
