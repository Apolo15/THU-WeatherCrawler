'''
@File  :Test_listappend.py
@Author:zhangxu
@Date  :2022/3/411:26
@Desc  :
'''


list=[]

for i in range(5):
    list.append("现在的内容是："+str(i))



for i in range(len(list)):
    print(list[i])

# print(list[0])