'''
新增删除用户用例类
'''
import unittest
from utils.handle_path import *
from utils.handle_ini import Handle_Ini
from utils.handle_requests import Handle_Request
from utils.hand_exl import Handle_Excel
from ddt import ddt,data
from utils.handle_db import Handle_db
import json
import re
ini_file=os.path.join(conf_path,'config.ini')
i_file=Handle_Ini(ini_file)

#服务器层
host=i_file.get_value('test_env','host')
port=i_file.get_value('test_env','port')
cookie=i_file.get_value('test_env','cookie')
headers=eval(i_file.get_value('test_env','headers'))
headers['Cookie']=cookie

#数据库层
db_host=i_file.get_value('mysql_env','host')
db_port=i_file.get_value('mysql_env','port')
db_username=i_file.get_value('mysql_env','username')
db_password=i_file.get_value('mysql_env','password')
db_database=i_file.get_value('mysql_env','database')

#测试数据层
exl_file=os.path.join(data_path,'case_data.xlsx')
e_file=Handle_Excel(exl_file,'deleteuser')
cases=e_file.read_data()

