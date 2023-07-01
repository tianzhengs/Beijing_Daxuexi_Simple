import os
import time
import requests
import json
import hmac
import hashlib
import base64
import urllib.parse
import time
from study import study


def getAccounts():
    result = []
    usernameRaw = os.getenv("USERNAME", "")
    print("https://m.bjyouth.net/site/login")
    print("请在上面的青年大学习网站尝试登录, 以确保你输入的账号和密码是正确的")

    if len(usernameRaw.split('\n')) == 1:
        # Single User
        passwd = os.environ["PASSWORD"]
        if usernameRaw and passwd:
            result.append((usernameRaw, passwd))
    else:
        # Multiple Users
        account_lines = usernameRaw.split('\n')
        for lineN, line in enumerate(account_lines):
            lineSplit = line.split(' ')
            if len(lineSplit) == 3:
                lineSplit = lineSplit[:2]
                print('现在可以删除组织ID了')
            elif len(lineSplit) != 2:
                raise Exception(f"第{lineN}行账号格式错误")
            result.append(lineSplit)

    if not result:
        raise Exception("没有被配置的账号！请设置Secret: USERNAME(和PASSWORD)")
    return result


ua = os.getenv('UA',
               'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36 Edg/106.0.1370.42')
msg="青年大学习\n\n"
accounts = getAccounts()
print(f'账号数量：{len(accounts)}')
msg+=f'账号数量：{len(accounts)}\n'
successful = 0
count = 0
for username, password in accounts:
    count += 1
    print(f'--User {count}--')
    msg+=f'--User {count}--\n'
    state=study(username, password, ua)
    if state!=0:
        msg+=state
        successful += 1

failed = count - successful
print('--Summary--')
msg+='--Summary--\n'
print(f'成功：{successful}，失败：{failed}')
msg+=f'成功：{successful}，失败：{failed}\n'
if failed != 0:
    raise Exception(f'有{failed}个失败！')


# 钉钉机器人的access_token
access_token = ""

# 钉钉机器人的Secret
secret = ""

# 获取当前时间戳（毫秒级），转换为字符串
timestamp = str(round(time.time() * 1000))

# 拼接需要加密的字符串
secret_enc = secret.encode('utf-8')
string_to_sign = '{}\n{}'.format(timestamp, secret)
string_to_sign_enc = string_to_sign.encode('utf-8')

# 使用HmacSHA256算法计算签名，并进行Base64编码
hmac_code = hmac.new(secret_enc, string_to_sign_enc, digestmod=hashlib.sha256).digest()
sign = urllib.parse.quote_plus(base64.b64encode(hmac_code))

# 构建请求头部
header = {
    "Content-Type": "application/json",
    "Charset": "UTF-8"
}

# 构建请求数据，此处为发送文本信息
message ={
    "msgtype": "text",
    "text": {
        "content": msg
    },
    "at": {
        "isAtAll": True
    }
}

# 对请求数据进行json封装
message_json = json.dumps(message)

# 构建请求的URL，包含签名和时间戳
webhook = "https://oapi.dingtalk.com/robot/send?access_token={}&timestamp={}&sign={}".format(access_token, timestamp, sign)

# 发送HTTP POST请求到钉钉webhook
info = requests.post(url=webhook, data=message_json, headers=header)

# 打印请求结果
print(info.text)
