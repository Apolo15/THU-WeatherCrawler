# -*- coding:utf-8 -*-


'''
@File  :Test_multiCrawler.py
@Author:zhangxu
@Date  :2022/3/315:42
@Desc  :
'''


from threading import Thread
import time

def do(k):
    # for i in range(10):
        print(k)
        time.sleep(1)
        print(k)
        print(k)
        time.sleep(1)
        print(k)
        time.sleep(1)
        print(k)
        time.sleep(1)


if __name__=='__main__':

    th_pool=[]

    for i in range(5):
        print("当前线程号：",i)
        th=Thread(target=do,args=(i,))
        th.start()
        th_pool.append(th)

    for th in th_pool:
        th.join()

    print("结束")