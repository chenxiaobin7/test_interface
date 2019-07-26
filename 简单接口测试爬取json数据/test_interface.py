import requests
import json
import show
import re
import re
import configparser
import os
curpath = os.path.dirname(os.path.realpath(__file__))
cfgpath = os.path.join(curpath, '1.ini')
print(cfgpath)
cp = configparser.ConfigParser()
cp.read(cfgpath, encoding="utf-8")
s2 = cp.items('login')[0][1]
s3 = cp.items('AUDITING')[0][1]
s4 = cp.items('AUDIT_PASS')[0][1]


class test_interface_xinluo(object):
    """
    接口测试
    """
    def __init__(self, nick_name, login_name):
        self.nick_name = nick_name
        self.login_name = login_name

    def creat(self, nick_name, login_name):
        """
        创建接口测试方法
        :param username:
        :param nick_name:
        :param login_name:
        :param password:
        :return:
        """

        """登录对方的admin账号"""
        # url = "xx"
        params = {'username': 'xx',
                  'password': 'xx'
                  }
        response = requests.post(s2, data=params)
        # 返回值 sessionid
        cookies = requests.utils.dict_from_cookiejar(response.cookies)
        # 处理cookies格式
        key = cookies["SESSION"]
        cookies = "SESSION" + "=" + key
        print(cookies)
        t_headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36",
            "Cookie": cookies
        }
        # 请求创建审核医生接口
        url_s = ""
        params = {
            'nick_name': nick_name,
            'login_name': login_name,
            'role': 'ROLE_AUDITOR',
        }
        response = requests.post(url_s, data=params, headers=t_headers)
        print("状态码为:")
        print(response.status_code)
        print(response.text)


class auditing(object):
    t=[]
    t1=[]

    def __init__(self, username, record_id, state):
        self.username = username
        self.record_id = record_id
        self.state = state

    def passthrough(self, username, record_id, state):
        # 审核医生请求login接口，获取session
        # t_url = "xx"
        params = {'username': username,
                  'password': 'xx'
                  }
        response = requests.post(s2, data=params)
        cookies = requests.utils.dict_from_cookiejar(response.cookies)  # 返回值 sessionid
        # 处理cookies格式
        key = cookies["SESSION"]
        cookies = "SESSION" + "=" + key
        print(cookies)

        # #####################################
        # 通过审核接口/取消审核接口
        # 请求参数：record_id 报告id(必传)
        # state 报告状态(必传, 传AUDIT_PASS/AUDITING）
        # #####################################

        url = "http://ecg-java-test.landmind.cn/user/record_state/"
        t_headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36",
            "Cookie": cookies
        }
        params = {'record_id': record_id,
                  'state': state
                  }
        response = requests.post(url, data=params, headers=t_headers)
        print("状态码为:")
        print(response.status_code)
        print(response.text)


def findid1(username,t):
    # url = "xx"
    params = {'username': username,
              'password': 'xx'
              }

    response = requests.post(s2, params=params)
    cookies = requests.utils.dict_from_cookiejar(response.cookies)
    key = cookies["SESSION"]
    cookies = "SESSION" + "=" + key
    print(cookies)


    t_headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36",
        "Cookie": cookies
    }
    response = requests.get(s3, headers=t_headers)
    print("当前审核中的报告为:")
    data = response.text
    result = response.json()

    datalist = re.findall(r'\"record_id\":.*?(?=,)', data)
    # if datalist:
    for i in range(len(datalist)):
        record_id = (result['users'][i]['record_id'])
        print(record_id)
        t.append(record_id)

    return t
        # print(datalist[i].split(':')[1])
    # else:
    #     print("当前没有可执行的报告")


def findid2(username,t1):
    url = ""
    params = {'username': username,
              'password': 'xx'
              }

    response = requests.post(url, params=params)
    cookies = requests.utils.dict_from_cookiejar(response.cookies)
    key = cookies["SESSION"]
    cookies = "SESSION" + "=" + key
    print(cookies)

    t_headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36",
        "Cookie": cookies
    }
    print("当前已审核的报告为:")
    response1 = requests.get(s4, headers=t_headers)
    data1 = response1.text
    result1 = response1.json()
    datalist1 = re.findall(r'\"record_id\":.*?(?=,)', data1)

    # if datalist1
    for i in range(len(datalist1)):
        record_id1 = (result1['users'][i]['record_id'])
        print(record_id1)
        t1.append(record_id1)
    return t1
        # print(datalist1[i].split(':')[1])
    # else:
    #     print("当前没有可执行的报告")


if __name__ == "__main__":
    while True:
        # TODO 显示功能菜单
        show.show()
        str = input("请输入希望执行的操作:")
        print("你选择的操作是[%s]" % str)
        if str in ["1", "2", "3"]:
            # 创建审核医生
            if str == "1":
                nick_name = input("请输入要创建的用户昵称nick_name:")
                login_name = input("请输入用户账户名login_name:")
                test = test_interface_xinluo(nick_name, login_name)
                test.creat(nick_name, login_name)
            # 通过审核报告
            elif str == "2":
                username = input("请输入审核医生账号:")
                t = []
                findid1(username, t)
                # print(len(t))
                if len(t):
                    record_id = input("请输入要通过审核的报告id")
                    state = 'AUDIT_PASS'  # 传AUDIT_PASS/AUDITING
                    test1 = auditing(state, username, record_id)
                    test1.passthrough(username, record_id, state)
                else:
                    print("当前没有可执行的报告")
                    # pass
            # 取消审核报告
            elif str == "3":
                username = input("请输入审核医生账号:")
                t1 = []
                findid2(username, t1)
                if len(t1):
                    record_id = input("请输入要取消审核的报告id")
                    state = 'AUDITING'  # 传AUDIT_PASS/AUDITING
                    test2 = auditing(state, username, record_id)
                    test2.passthrough(username, record_id, state)
                else:
                    print("当前没有可执行的报告")
                # pass
                # record_id = input("请输入要取消审核的报告id")
                # state = 'AUDITING'  # 传AUDIT_PASS/AUDITING
                # test2 = auditing(state, username, record_id)
                # test2.passthrough(username, record_id, state)
            pass
        elif str == "0":
            print("欢迎再次使用【心络审核医生接口测试】")
            break
        else:
            print("输入不正确，请重新输入")

