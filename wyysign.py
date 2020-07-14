# 更新时间 2020年7月15日01:10:58
# 支持pc和移动端签到
# 签到可兑换网易云黑胶会员
# 作者：ck
import requests
import re
from DecryptLogin import login
from DecryptLogin.platforms.music163 import Cracker


def run(username, password):
    try:
        lg = login.Login()
        _, session = lg.music163(username, password)
        csrf = re.findall('__csrf=(.*?) for', str(session.cookies))[0]
        cracker = Cracker()
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Referer': 'http://music.163.com/discover',
            'Accept': '*/*'
        }
        signin_url = 'https://music.163.com/weapi/point/dailyTask?csrf_token=' + csrf
        # 模拟签到(typeid为0代表APP上签到, 为1代表在网页上签到)
        typeids = [0, 1]
        for typeid in typeids:
            client_name = 'Web端' if typeid == 1 else 'APP端'
            # --构造请求获得响应
            data = {
                'type': typeid
            }
            data = cracker.get(data)
            res = session.post(signin_url, headers=headers, data=data)
            res_json = res.json()
            # --判断签到是否成功
            if res_json['code'] == 200:
                print('账号%s在%s签到成功...' % (username, client_name))


            else:
                print('账号%s在%s签到失败, 原因: %s...' % (username, client_name, res_json.get('msg')))
    except Exception as e:
        requests.get(
            'https://sc.ftqq.com/sever酱密钥.send?text=网易云签到脚本运行失败&desp=具体情况未知')


my_list = [
    {
        'username': '账号1',
        'password': '密码1',
    },
    {
        'username': '账号2',
        'password': '密码2',
    }
]


def main_handler(event, context):
    return run(username, password)


if __name__ == '__main__':
    for i in my_list:
        code = run(i['username'], i['password'])
