'''
主要对requests库的请求发送方法进行二次封装
'''

import requests
import json

class Handle_Request():
    def __init__(self):
        self.sess=requests.Session()

    def send(self,method,url,data=None,headers=None):
        '''
        发送请求的方法
        :param method:
        :param url:
        :param data:
        :param headers:
        :return:
        '''
        #print(f"【底层实际接收的请求体data】: {data}")
        if isinstance(data, str):
            try:
                data = json.loads(data)
            except Exception:
                pass
        if method=='get':
            resp=self.sess.get(url=url,params=data,headers=headers)
        elif method=='post_json':
            resp=self.sess.post(url=url,json=data,headers=headers)
        elif method=='post_form':
            resp=self.sess.post(url=url,data=data,headers=headers)
            print(resp.text)
        elif method=='put':
            resp=self.sess.put(url=url,data=data,headers=headers)
        elif method=='delete':
            resp=self.sess.delete(url=url,data=data,headers=headers)
        else:
            raise TypeError("请求方法异常，无法发送请求")
        #print(f"【底层实际发出的请求体】: {resp.request.body}")
        return resp

if __name__ == '__main__':
    pass
    # login_url = 'http://192.168.3.133:8080/cms/manage/loginJump.do'
    # login_data = {"userAccount": "admin", "loginPwd": "123456"}
    # login_headers = {"Content-Type": "application/x-www-form-urlencoded"}
    # h=Handle_Request()
    # result=h.send("post_form",url=login_url,data=login_data,headers=login_headers)
    # print(result.text)
