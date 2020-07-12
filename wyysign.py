# 更新时间 2020年7月12日14:48:58
# 支持pc和移动端签到，支持听歌打卡，加速升级
# 签到可兑换网易云黑胶会员
# 作者：ck
import json
import requests
import ssl
import smtplib
ssl._create_default_https_context = ssl._create_unverified_context
#用于方法失效后微信通知的Server酱，获取地址https://sc.ftqq.com/
def signelse():
    requests.get('https://sc.ftqq.com/修改为Server酱的密钥.send?text=网易云签到失败&desp=签到失败，方法失效')

def sendEmail(data):
    from email.mime.text import MIMEText
    # email 用于构建邮件内容
    from email.header import Header
    # 用于构建邮件头
    # 发信方的信息：发信邮箱，QQ 邮箱授权码
    from_addr = '这里修改为发件人邮箱账号'
    password = '这里修改为邮箱授权码'
    # 收信方邮箱
    to_addr = '这里修改为收件人邮箱'
    # 发信服务器
    smtp_server = 'smtp.qq.com'
    # 邮箱正文内容，第一个参数为内容，第二个参数为格式(plain 为纯文本)，第三个参数为编码
    msg = MIMEText(data, 'plain', 'utf-8')
    # 邮件头信息
    msg['From'] = Header(from_addr)
    msg['To'] = Header(to_addr)
    msg['Subject'] = Header('网易云音乐签到')
    # 开启发信服务，这里使用的是加密传输
    server = smtplib.SMTP_SSL(smtp_server)
    server.connect(smtp_server, 465)
    # 登录发信邮箱
    server.login(from_addr, password)
    # 发送邮件
    server.sendmail(from_addr, to_addr, msg.as_string())
    # 关闭服务器
    server.quit()
def sign():
    base_url = "https://music.cloudsvip.club"
    login_url = base_url + "/api.php?do=login"  # 登录URL
    daka_url = base_url + "/api.php?do=daka"  # 打卡URL
    sign_url = base_url + "/api.php?do=sign"  # 移动端签到URL
    signpc_url = base_url + "/api.php?do=signpc"  # PC端签到URL
    #账号，和密码，密码为md5值
    data = {'uin': '这里修改为自己的网易云账号', 'pwd': '这里修改为密码的md5值'}
    req = requests.post(login_url, data=data)
    cookies = req.cookies
    # 登录判断
    reqJsonObj = json.loads(req.text)
    if reqJsonObj['code'] == 200:
        nickName = reqJsonObj['profile']['nickname']
        print(nickName)
    else:
        signelse()
# 移动端签到
    sign = requests.post(sign_url, cookies=cookies)
    signJsonObj = json.loads(sign.text)
    if signJsonObj['code'] == 200:
        result1 = '移动端签到成功: ' + '经验+' + str(signJsonObj['point'])
        print(result1)

    else:
        result = '移动端签到失败: ' + str(signJsonObj['msg'])
        print(result)
        signelse()


    # PC端签到
    signpc = requests.post(signpc_url, cookies=cookies)
    signPcJsonObj = json.loads(signpc.text)
    if signPcJsonObj['code'] == 200:
        result2 = 'PC端签到成功: ' + '经验+' + str(signPcJsonObj['point'])
        print(result2)
    else:
        result = 'PC端签到失败: ' + str(signPcJsonObj['msg'])
        print(result)
        signelse()

    # 打卡
    daka = requests.post(daka_url, cookies=cookies)
    dakaJsonObj = json.loads(daka.text)
    if dakaJsonObj['code'] == 200:
        result3 = '打卡成功: ' + str(dakaJsonObj['count']) + '首'
        print(result3)
    else:
        result = '打卡失败: 未知错误'
        print(result)
        signelse()

    data ='昵称:'+nickName+"\n"+result1+"\n"+result2+"\n"+result3
    print(data)
    sendEmail(data)

def main_handler(event, context):
  return sign()
if __name__ == '__main__':
    sign()
