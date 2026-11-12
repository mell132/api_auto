# coding:utf-8

"""
此模块主要是对ini配置文件进行操作的工具类
"""

from configparser import ConfigParser   # 导入configparser模块中的ConfigParser类。

class Handle_Ini(ConfigParser):

    def __init__(self,filename):
        super().__init__()
        self.filename = filename   # 将文件设置为一个实例变量
        self.read(filename, encoding='utf-8')

    def get_value(self,section,option):
        """
        获取ini配置文件中指定section下option对应的值。
        每次读取前重新加载文件，避免登录用例写入 cookie 后，其他用例仍使用旧值。
        :param section:
        :param option:
        :return:
        """
        self.read(self.filename, encoding='utf-8')
        v = self.get(section,option)
        return v

    def get_headers(self):
        """读取最新请求头，并带上登录后写回配置文件的 cookie。"""
        headers = eval(self.get_value('test_env', 'headers'))
        cookie = self.get_value('test_env', 'cookie')
        if cookie:
            headers['Cookie'] = cookie
        return headers

    def write_data(self,section,option,value):
        """
        封装一个向ini文件中指定section中写入指定option的值
        :param section:
        :param option:
        :param value:
        :return:
        """
        self.set(section,option,value)  # 通过当前类对象调用set方法设置指定的section中的option以及对应的值
        with open(self.filename, 'w', encoding='utf-8') as f:  # 通过open函数将配置文件创建出一个文件流对象f
            self.write(f)   # 通过当前类对象调用write方法，将当前对象中设置好的section和option写入到配置文件中


if __name__ == '__main__':
    # i_file = r'C:\code_project\api_auto_framework\conf\config.ini'
    # h = Handle_Ini(i_file)
    # value=h.get_value('mysql_env','username')
    # h.write_data('test_env','token','123123123')
    pass