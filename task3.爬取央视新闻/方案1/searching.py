from get_data import *
from xls_functions import *
import os
# datatime = '2021-06-01'
datatime = input("请输入需要导出的日期（日期格式为：2020-06-01）：")
local_time = time_trans_stamp(datatime)
print(f"正在查找{datatime}的新闻，请稍等.....")
print('-----------------------------------')
# local_time = 1622728266000  # 2021-6-3
# local_time = 1622649600000
# date = stamp_trans_time(local_time)[1] # 将查询的时间转为日期格式 2021-06-032
filename = f'{datatime}.xls'
sheet_name = f'{datatime}'
data = get_data(local_time)  # 接口获取的数据
if os.path.exists(filename):
    write_excel_xls_append(filename, data)  # 写入表格内容
else:
    title = [['Datetime', 'view', 'video', 'title', 'name', 'url']]
    write_excel_xls(filename, sheet_name, title)  # 创建表格并写入表头
    write_excel_xls_append(filename, data)  # 写入表格内容
