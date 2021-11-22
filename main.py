import json
import os
import re
import time
import traceback
from base64 import b64encode

import requests
from Crypto.Cipher import PKCS1_v1_5 as Cipher_pksc1_v1_5
from Crypto.PublicKey import RSA
from ddddocr import DdddOcr

from cap_denoise import dn


username = os.environ["USERNAME"]
password = os.environ["PASSWORD"]

if not (username and password):
    raise Exception("请设置Secret: USERNAME和PASSWORD")


org_id = '172442'  # "北京市海淀团区委"
# or check string type
try:
    org_id_input = os.environ["ORGID"]
    if org_id_input:
        org_id = int(org_id_input)
except:
    ...


def encrypt(t):
    public_key = "-----BEGIN PUBLIC KEY-----\nMIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQD5uIDebA2qU746e/NVPiQSBA0Q3J8/G23zfrwMz4qoip1vuKaVZykuMtsAkCJFZhEcmuaOVl8nAor7cz/KZe8ZCNInbXp2kUQNjJiOPwEhkGiVvxvU5V5vCK4mzGZhhawF5cI/pw2GJDSKbXK05YHXVtOAmg17zB1iJf+ie28TbwIDAQAB\n-----END PUBLIC KEY-----"
    rsa_key = RSA.importKey(public_key)
    cipher = Cipher_pksc1_v1_5.new(rsa_key)
    cipher_text = b64encode(cipher.encrypt(t.encode()))
    return cipher_text.decode()



url = ''
for _ in range(10):
    try:
        bjySession = requests.session()
        # set session timeout
        bjySession.timeout = 5
        fake_ua = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36 Edg/80.0.361.111'
        bjySession.headers.update({
            "User-Agent": fake_ua, })

        r = bjySession.get(url="https://m.bjyouth.net/site/login")
        cap_url = "https://m.bjyouth.net" + re.findall(
            r'src="/site/captcha.+" alt=', r.text)[0][5:-6]

        cap = bjySession.get(url=cap_url)
        ocr = DdddOcr()
        cap = dn(cap.content)
        cap_text = ocr.classification(cap)
        print(f'Captcha OCR: {cap_text}')
        _csrf_mobile = bjySession.cookies.get_dict()['_csrf_mobile']
        login_password = encrypt(password)
        login_username = encrypt(username)
        login_r = bjySession.post('https://m.bjyouth.net/site/login',
                                  data={
                                      '_csrf_mobile': _csrf_mobile,
                                      'Login[username]': login_username,
                                      'Login[password]': login_password,
                                      'Login[verifyCode]': cap_text
                                  })
        if login_r.text == '8':
            print('Login: 验证码错误')
        print(f'Login: [{login_r.status_code}]{login_r.text}')
        r = json.loads(bjySession.get("https://m.bjyouth.net/dxx/index").text)
        if 'newCourse' not in r:
            print(r)
        url = r['newCourse']['url']
        title = r['newCourse']['title']
        break
    except:
        time.sleep(3)
        print(traceback.format_exc())

if not url:
    print('Fail in login')
    exit(1)

r2 = bjySession.get('https://m.bjyouth.net/dxx/my-integral?type=2&page=1&limit=15')
res = json.loads(r2.text)
if f"学习课程：《{title}》" in list(map(lambda x: x['text'], res['data'])):
    print(f'{title} 在运行前已完成')
    exit(0)

pattern = re.compile(r'https://h5.cyol.com/special/daxuexi/(\w+)/m.html\?t=1&z=201')
result = pattern.search(url)
if not result:
    print(f'Url pattern not matched: {url}')
    exit(1)

end_img_url = f'https://h5.cyol.com/special/daxuexi/{result.group(1)}/images/end.jpg'
study_url = f"https://m.bjyouth.net/dxx/check?id={r['newCourse']['id']}&org_id={org_id}"

r = bjySession.get(study_url)

if r.text:
    print(
        f'Unexpected response: {r.text}'
    )
    exit(1)

r = bjySession.get('https://m.bjyouth.net/dxx/my-integral?type=2&page=1&limit=15')
res = json.loads(r.text)
if f"学习课程：《{title}》" in list(map(lambda x: x['text'], res['data'])):
    print(f'{title} 成功完成学习')
    exit(0)
else:
    print(f'Seem finished {title}, but not confirmed as {f"学习课程：《{title}》"}' not in {
        list(map(lambda x: x['text'], res['data']))})
    exit(1)
