# coding:utf-8

"""
此模块主要是创建运行对象，运行指定的用例方法
"""
import sys
import os

# 获取当前文件所在目录的上一级目录（即项目根目录）
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# 如果根目录不在系统路径中，则添加进去
if project_root not in sys.path:
    sys.path.insert(0, project_root)


import unittest
from utils.HTMLTestRunnerNew import HTMLTestRunner
from time import *
from utils.handle_path import *

def runcases():
    # 登录必须先执行，后面的用例依赖它写回的 cookie；删除必须在新增之后
    loader = unittest.TestLoader()
    suite1 = unittest.TestSuite()
    for pattern in ('test_login.py', 'test_save_data.py', 'test_query_data.py', 'test_delete.py'):
        suite1.addTests(loader.discover(start_dir=case_path, pattern=pattern))
    report_file = os.path.join(report_path, 'report' + strftime("%m%d%H%M%S") + '.html')
    with open(report_file, 'wb') as f:
        runner = HTMLTestRunner(stream=f,
                                title='接口自动化测试报告',
                                description='执行情况如下：',
                                tester='小申')
        runner.run(suite1)


if __name__ == '__main__':
    runcases()