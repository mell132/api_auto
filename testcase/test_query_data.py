'''
查询数据测试用例类
'''
import unittest
from utils.handle_path import *
from utils.handle_ini import Handle_Ini
from utils.handle_requests import Handle_Request
from utils.hand_exl import Handle_Excel
from ddt import ddt,data
ini_file=os.path.join(conf_path,'config.ini')
i_file=Handle_Ini(ini_file)

#服务器层
host=i_file.get_value('test_env','host')
port=i_file.get_value('test_env','port')

#测试数据层
exl_file=os.path.join(data_path,'case_data.xlsx')
e_file=Handle_Excel(exl_file,'query')
cases=e_file.read_data()
@ddt
class Test_Query_Data(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.req=Handle_Request()

    def setUp(self):
        # 登录用例会把新 cookie 写回配置文件，这里每次执行前重新读取
        self.headers=i_file.get_headers()

    @data(*cases)
    def test_query(self,case):
        query_url = f'http://{host}:{port}{case["url"]}'
        # 获取接口请求方法
        method = case['method']
        # 获取接口请求参数
        query_data = case['data']
        # 发送接口请求
        resp = self.req.send(method=method, url=query_url, data=query_data, headers=self.headers)
        result = self.req.to_json(resp)
        # 获取期望结果
        expected = self.req.parse_body(case['expected'])
        # 获取用例所在行
        case_row = int(case['case_id']) + 1
        try:
            self.assertEqual(str(expected['code']),str(result['code']))
            self.assertEqual(expected['msg'],result['msg'])

        except Exception as e:
            print(result)
            print(e)
            e_file.write_data(case_row,8,'测试不通过')
            raise
        else:
            e_file.write_data(case_row, 8, '测试通过')



if __name__ == '__main__':
    unittest.main()