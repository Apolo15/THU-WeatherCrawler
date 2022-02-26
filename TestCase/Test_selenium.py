'''
@File  :Test_selenium.py
@Author:zhangxu
@Date  :2021/11/2915:55
@Desc  :
'''
from selenium import webdriver
import time

browser=webdriver.Chrome()
browser.get('http://app.cctv.com/special/cportal/detail/arti/index.html?id=ArtiYQmbxnfXwlwpnTSnKIbH180101&isfromapp=1')

time.sleep(3)
print(browser.current_url)