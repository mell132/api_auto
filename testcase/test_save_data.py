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
ini_file=os.path.join(conf_path,'config.ini')
i_file=Handle_Ini(ini_file)

#服务器层
host=i_file.get_value('test_env','host')
port=i_file.get_value('test_env','port')

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
        cls.db = None
        cls.db_error = None
        try:
            cls.db = Handle_db(
                host=db_host,
                port=db_port,
                user=db_username,
                password=db_password,
                database=db_database,
            )
        except Exception as e:
            # 数据库连不上时仍发送接口请求，避免整类用例在 setUpClass 直接中断
            cls.db_error = e
            print('数据库连接失败：%s' % e)

    @classmethod
    def tearDownClass(cls) -> None:
        if cls.db:
            cls.db.close()

    def setUp(self):
        self.headers=i_file.get_headers()

    def _require_db(self):
        if self.db is None:
            raise AssertionError('数据库连接失败：%s' % self.db_error)

    @data(*cases)
    def test_saveuser(self,case):
        save_url=f'http://{host}:{port}{case["url"]}'
        method=case['method']
        save_data=case['data']
        table_name=case['table_name'] #数据所在表名
        case_data=self.req.parse_body(case['data'])
        account=case_data['userAccount']
        before_count=None
        if self.db is not None:
            before_count=self.db.count(f'select count(*) from {table_name}')
        resp=self.req.send(method=method,url=save_url,data=save_data,headers=self.headers)
        result=self.req.to_json(resp)
        expected=self.req.parse_body(case['expected'])
        case_row=int(case['case_id'])+1

        #新增断言
        try:
            #断言1：断言状态码和信息
            self.assertEqual(str(expected['code']), str(result['code']))
            self.assertEqual(expected['msg'], result['msg'])

            #断言2：断言数据库。接口返回的 code 是字符串 "200"，不能和整数 200 比较
            if str(result['code'])=='200':
                self._require_db()
                sql2=f'select * from {table_name} where user_account=%s'
                row=self.db.query_one(sql2,(account,))
                self.assertIsNotNone(row,'数据库中没有找到新增账号：%s' % account)
                field_map={
                    'userName':'user_name',
                    'userSex':'user_sex',
                    'userMobile':'user_mobile',
                    'userEmail':'user_email',
                    'userAccount':'user_account',
                }
                for req_key, column in field_map.items():
                    if column in row and req_key in case_data:
                        self.assertEqual(str(row[column]), str(case_data[req_key]))
                after_count=self.db.count(f'select count(*) from {table_name}')
                self.assertEqual(before_count + 1, after_count, '新增后用户数量没有增加')

        except Exception as e:
            print(e)
            e_file.write_data(case_row, 9, '测试不通过')
            raise
        else:
            e_file.write_data(case_row, 9, '测试通过')


if __name__ == '__main__':
    unittest.main(buffer=False)
