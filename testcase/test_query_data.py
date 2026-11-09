'''
查询数据测试用例类
'''
import unittest
from utils.handle_path import *
from utils.handle_ini import Handle_Ini
from utils.handle_requests import Handle_Request
from utils.hand_exl import Handle_Excel
from ddt import ddt,data
import re
import json
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
e_file=Handle_Excel(exl_file,'query')
cases=e_file.read_data()
@ddt
class Test_Query_Data(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.req=Handle_Request()

    @data(*cases)
    def test_query(self,case):
        query_url = f'http://{host}:{port}{case["url"]}'
        # 获取接口请求方法
        method = case['method']
        # 获取接口请求参数
        query_data = case['data']
        # 发送接口请求
        resp = self.req.send(method=method, url=query_url, data=query_data, headers=headers)
        #result = resp.json()
        result = json.loads(resp.content.decode('utf-8-sig'))
        # 获取期望结果
        expected = eval(case['expected'])
        # 获取用例所在行
        case_row = int(case['case_id']) + 1
        try:
            self.assertEqual(expected['code'],result['code'])
            self.assertEqual(expected['msg'],result['msg'])

        except Exception as e:
            print(result)
            print(e)
            e_file.write_data(case_row,8,'测试不通过')
            raise AssertionError('断言失败')
        else:
            e_file.write_data(case_row, 8, '测试通过')



if __name__ == '__main__':
    unittest.main()