'''
新增数据测试用例类
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
e_file=Handle_Excel(exl_file,'adduser')
cases=e_file.read_data()

@ddt
class Test_Save_Data(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.req=Handle_Request()
        cls.db = Handle_db(
            host=db_host,
            port=db_port,
            user=db_username,
            password=db_password,
            database=db_database,
        )

    @data(*cases)
    def test_saveuser(self,case):
        save_url=f'http://{host}:{port}{case["url"]}'
        method=case['method']
        save_data=case['data']
        #先查原用户数
        table_name=case['table_name'] #数据所在表名
        sql1=f'select count(*) from {table_name}'
        before_count=self.db.count(sql1)
        resp=self.req.send(method=method,url=save_url,data=save_data,headers=headers)
        result=resp.json()
        #result = json.loads(resp.content.decode('utf-8-sig'))
        expected=eval(case['expected'])
        case_row=int(case['case_id'])+1
        case_data=eval(case['data'])
        account=case_data['userAccount']

        #新增断言
        try:
            #断言1：断言状态码和信息
            self.assertEqual(expected['code'], result['code'])
            self.assertEqual(expected['msg'], result['msg'])

            #断言2：断言数据库
            if result['code']==200:
                #查询是否存在
                sql2=f'select * from {table_name} where user_account=%s'
                row=self.db.query_one(sql2,(account,))
                self.assertIsNotNone(row,f'数据库中没有找到新增账号：{account}')
                #字段对比


        except Exception as e:
            print(e)
            e_file.write_data(case_row, 9, '测试不通过')
            raise AssertionError('断言失败')
        else:
            e_file.write_data(case_row, 9, '测试通过')


if __name__ == '__main__':
    unittest.main(buffer=False)