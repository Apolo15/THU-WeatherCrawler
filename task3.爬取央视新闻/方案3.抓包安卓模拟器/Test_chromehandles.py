'''
@File  :Test_chromehandles.py
@Author:zhangxu
@Date  :2022/1/1012:33
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


options = webdriver.ChromeOptions()
# 添加无界面参数
options.add_argument('--headless')
# browser = webdriver.Chrome(options=options)

browser = webdriver.Chrome(options=options)
print (browser.current_window_handle)
print(browser.window_handles)
