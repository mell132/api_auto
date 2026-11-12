# coding:utf-8

# 此模块主要是对excel文件进行读写的工具类

import os
import openpyxl
from utils.handle_path import *

class Handle_Excel():

    def __init__(self,filename,sheetname):
        self.filename = filename
        self.sheetname = sheetname
        self.wk = openpyxl.load_workbook(filename)  # 通过openpyxl库中的load_workbook函数打开指定的excel文件，并返回一个文件流对象
        self.st = self.wk[sheetname]   # 获取文件流对象中的指定sheet页对象

    def read_data(self):
        """
        读取指定sheet页对象中所有数据的方法
        :return:
        """
        list1 = list(self.st.rows)
        title_list = [i.value for i in list1[0]]   # 获取首行所有单元格中的数据，并保存到一个列表中
        all_datas = []
        for j in list1[1:]:   # 对list1中的第2个元素开始一直遍历到最后一个元素
            data_list = [k.value for k in j]      # 每获取一个元组，对元组做遍历，获取单元格对象，并将单元格对象中的数据保存到列表中
            data_dic = dict(zip(title_list,data_list))   # 打包生成一个字典
            all_datas.append(data_dic)   # 将字典保存到列表中
        return all_datas

    def write_data(self,row,col,value=None):
        '''
        向指定位置单元格写入数据
        :param row:
        :param col:
        :param value:
        :return:
        '''
        # 重新加载后再写入。多个用例同时打开同一个工作簿时，后保存的对象会盖掉先写入的结果
        self.wk = openpyxl.load_workbook(self.filename)
        self.st = self.wk[self.sheetname]
        self.st.cell(row,col,value) #通过sheet页对象调用cell方法指定单元格写入
        self.wk.save(self.filename) #通过excel文件流对象调用save方法，将写入到sheet页对象中的数据保存到excel中
        self.wk.close()



if __name__ == '__main__':
    e_file = os.path.join(data_path,'case_data.xlsx')
    h = Handle_Excel(e_file,'login')
    h.write_data(2,8,'通过')
    print(h.read_data())



