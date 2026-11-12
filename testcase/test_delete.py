'''
删除用户用例类
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
e_file=Handle_Excel(exl_file,'deleteuser')
cases=e_file.read_data()

@ddt
class Test_Delete(unittest.TestCase):

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

    def _user_id(self, row):
        for key, value in row.items():
            if key is not None and str(key).lower() in ('id', 'user_id', 'userid') and value not in (None, ''):
                return value
        return None

    @data(*cases)
    def test_delete(self,case):
        delete_url=f'http://{host}:{port}{case["url"]}'
        method=case['method']
        table_name=case['table_name']
        case_row=int(case['case_id'])+1
        try:
            case_data=dict(self.req.parse_body(case['data']) or {})
            account=case_data.pop('userAccount', None)
            before_count=None
            if not case_data.get('id') and account:
                self._require_db()
                row=self.db.query_one(
                    f'select * from {table_name} where user_account=%s',
                    (account,),
                )
                self.assertIsNotNone(row, '删除前数据库中没有账号：%s' % account)
                case_data['id']=self._user_id(row)
                self.assertTrue(case_data['id'], '数据库记录中没有找到用户id')
                before_count=self.db.count(f'select count(*) from {table_name}')
            resp=self.req.send(method=method,url=delete_url,data=case_data,headers=self.headers)
            result=self.req.to_json(resp)
            expected=self.req.parse_body(case['expected'])
            self.assertEqual(str(expected['code']), str(result['code']))
            self.assertEqual(expected['msg'], result['msg'])
            if str(result['code'])=='200' and account:
                self._require_db()
                row=self.db.query_one(
                    f'select * from {table_name} where user_account=%s',
                    (account,),
                )
                self.assertIsNone(row, '删除后数据库中仍然存在账号：%s' % account)
                if before_count is not None:
                    after_count=self.db.count(f'select count(*) from {table_name}')
                    self.assertEqual(before_count - 1, after_count, '删除后用户数量没有减少')
        except Exception as e:
            print(e)
            e_file.write_data(case_row, 9, '测试不通过')
            raise
        else:
            e_file.write_data(case_row, 9, '测试通过')


if __name__ == '__main__':
    unittest.main(buffer=False)
