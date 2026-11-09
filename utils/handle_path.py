'''
对每个包的路径进行封装
'''
import os
#定义项目包路径
base_path=os.path.dirname(os.path.dirname(__file__))
#定义data包路径
data_path=os.path.join(base_path,'data')
#定义report包路径
report_path=os.path.join(base_path,'report')
#定义conf包路径
conf_path=os.path.join(base_path,'conf')
#定义testcase路径
case_path=os.path.join(base_path,'testcase')
#定义run包路径
run_path=os.path.join(base_path,'run')
#定义utils包路径
utils_path=os.path.join(base_path,'utils')
