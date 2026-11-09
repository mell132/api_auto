# coding:utf-8

"""
此模块主要是对ini配置文件进行操作的工具类
"""

from configparser import ConfigParser   # 导入configparser模块中的ConfigParser类。

class Handle_Ini(ConfigParser):

    def __init__(self,filename):
        super().__init__()
        self.read(filename)
        self.filename = filename   # 将文件设置为一个实例变量

    def get_value(self,section,option):
        """
        获取ini配置文件中指定section下option对应的值
        :param section:
        :param option:
        :return:
        """
        v = self.get(section,option)
        return v

    def write_data(self,section,option,value):
        """
        封装一个向ini文件中指定section中写入指定option的值
        :param section:
        :param option:
        :param value:
        :return:
        """
        self.set(section,option,value)  # 通过当前类对象调用set方法设置指定的section中的option以及对应的值
        f = open(self.filename,'w')   # 通过open函数将配置文件创建出一个文件流对象f
        self.write(f)   # 通过当前类对象调用write方法，将当前对象中设置好的section和option写入到配置文件中
        f.close()   # 关闭文件流对象


if __name__ == '__main__':
    # i_file = r'C:\code_project\api_auto_framework\conf\config.ini'
    # h = Handle_Ini(i_file)
    # value=h.get_value('mysql_env','username')
    # h.write_data('test_env','token','123123123')
    pass