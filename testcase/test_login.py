'''
登录设计的测试用例类
'''
import unittest
from utils.handle_path import *
from utils.handle_ini import Handle_Ini
from utils.handle_requests import Handle_Request
from utils.hand_exl import Handle_Excel
from ddt import ddt,data
ini_file=os.path.join(conf_path,'config.ini')
i_file=Handle_Ini(ini_file)
host=i_file.get_value('test_env','host')
port=i_file.get_value('test_env','port')
exl_file=os.path.join(data_path,'case_data.xlsx')
e_file=Handle_Excel(exl_file,'login')
cases=e_file.read_data()
@ddt
class Test_Login(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.req=Handle_Request()

    @data(*cases)
    def test_login(self,case):
        #获取登录接口url
        login_url=f'http://{host}:{port}{case["url"]}'
        #获取接口请求方法
        method=case['method']
        #获取接口请求参数
        login_data=case['data']
        # print(login_data)
        # print(type(login_data))
        #获取接口的请求头
        headers=i_file.get_headers()
        headers.pop('Cookie', None)
        #print(headers)
        #发送接口请求
        resp=self.req.send(method=method,url=login_url,data=login_data,headers=headers)
        result=self.req.to_json(resp)
        #获取期望结果
        expected=self.req.parse_body(case['expected'])

        #获取用例所在行
        case_row=int(case['case_id'])+1

        #登录断言
        try:
            self.assertEqual(str(expected['code']),str(result['code']))
            self.assertEqual(expected['msg'],result['msg'])
            if result['msg']=='登录成功！':
                cookie_items=resp.cookies.get_dict()
                if not cookie_items:
                    raise AssertionError('登录成功但响应中没有 cookie')
                cookie='; '.join('%s=%s' % (key, value) for key, value in cookie_items.items())
                i_file.write_data('test_env','cookie',cookie)

        except Exception as e:
            print(result)
            print(e)
            e_file.write_data(case_row,8,'测试不通过')
            raise
        else:
            e_file.write_data(case_row, 8, '测试通过')



if __name__ == '__main__':
    # h=Test_Login()
    # h.test_login
    # # str1='{"username":"zhangsan"}'
    # # dict1=eval(str1) #eval提取字符的元格式
    unittest.main()
