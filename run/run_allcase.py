# coding:utf-8

"""
此模块主要是创建运行对象，运行指定的用例方法
"""

import unittest
from utils.HTMLTestRunnerNew import HTMLTestRunner
from time import *
from utils.handle_path import *

def runcases():
    suite1 = unittest.defaultTestLoader.discover(start_dir=case_path,pattern='test_*.py')
    report_file = report_path + '\\' + 'report' + strftime("%m%d%H%M%S") + '.html'
    f = open(report_file,'wb')
    runner = HTMLTestRunner(stream=f,
                            title='ui自动化测试报告',
                            description='执行情况如下：',
                            tester='小申')
    runner.run(suite1)
    f.close()


if __name__ == '__main__':
    runcases()