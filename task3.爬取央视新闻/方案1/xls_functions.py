import xlrd
import xlwt
from xlutils.copy import copy


def write_excel_xls(path, sheet_name, value):
    '''
    新建一个xls表格和工作簿，写入一行数据并保存
    :param path: 文件路径
    :param sheet_name: 表格名称
    :param value: 写入表格中的内容
    :return:
    '''
    # 设置字体格式
    style = xlwt.XFStyle()  # 初始化字体样式
    font = xlwt.Font()
    # 字体加粗
    font.bold = True
    font.height = 280
    font.name = '宋体'

    # 设置单元格格式
    alignment = xlwt.Alignment()
    #水平方向居中,0x01(左端对齐)、0x02(水平方向上居中对齐)、0x03(右端对齐)
    alignment.horz = 0x02
    # 竖直方向居中，# 0x00(上端对齐)、 0x01(垂直方向上居中对齐)、0x02(底端对齐)
    alignment.vert = 0x01

    style.font = font
    style.alignment = alignment

    index = len(value)  # 获取需要写入数据的行数
    workbook = xlwt.Workbook()  # 新建一个工作簿
    sheet = workbook.add_sheet(sheet_name)  # 在工作簿中新建一个表格

    for i in range(0, index):
        for j in range(0, len(value[i])):
            sheet.write(i, j, value[i][j],style)  # 向表格中写入数据（对应的行和列）
    workbook.save(path)  # 保存工作簿
    print("xls格式表格写入数据成功！")


def write_excel_xls_append(path, value):
    '''
    向xls表格中追加内容并保存
    :param path: 文件路径
    :param value: 追加内容
    :return:
    '''
    # 设置字体格式
    style0 = xlwt.XFStyle() # 初始化字体样式
    font = xlwt.Font()
    # 字体加粗
    # font.bold = True
    font.height = 240
    font.name = '宋体'
    style0.font = font

    index = len(value)  # 获取需要写入数据的行数
    workbook = xlrd.open_workbook(path)  # 打开工作簿
    sheets = workbook.sheet_names()  # 获取工作簿中的所有表格
    worksheet = workbook.sheet_by_name(sheets[0])  # 获取工作簿中所有表格中的的第一个表格
    rows_old = worksheet.nrows  # 获取表格中已存在的数据的行数
    new_workbook = copy(workbook)  # 将xlrd对象拷贝转化为xlwt对象
    new_worksheet = new_workbook.get_sheet(0)  # 获取转化后工作簿中的第一个表格
    for i in range(0, index):
        for j in range(0, len(value[i])):
            new_worksheet.write(i + rows_old, j, value[i][j],style0)  # 追加写入数据，注意是从i+rows_old行开始写入
    new_workbook.save(path)  # 保存工作簿
    print("xls格式表格【追加】写入数据成功！")


def read_excel_xls(path):
    '''
    读取xls表格内容
    :param path:
    :return:
    '''
    workbook = xlrd.open_workbook(path)  # 打开工作簿
    sheets = workbook.sheet_names()  # 获取工作簿中的所有表格
    worksheet = workbook.sheet_by_name(sheets[0])  # 获取工作簿中所有表格中的的第一个表格
    for i in range(0, worksheet.nrows):
        for j in range(0, worksheet.ncols):
            print(worksheet.cell_value(i, j), "\t", end="")  # 逐行逐列读取数据
        print()
