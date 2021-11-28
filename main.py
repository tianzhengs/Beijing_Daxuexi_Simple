import json
import os
import re
import time
import traceback

import requests

from utility import encrypt, cap_recognize

username = os.environ["USERNAME"]
password = os.environ["PASSWORD"]

if not (username and password):
    raise Exception("请设置Secret: USERNAME和PASSWORD")

try:
    org_id = str(int(os.environ["ORGID"]))  # check type
except:
    org_id = '172442'

url = ''
ua = os.getenv('UA',
               'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36 Edg/80.0.361.111')
for _ in range(10):
    try:
        bjySession = requests.session()
        bjySession.timeout = 5  # set session timeout
        bjySession.headers.update({"User-Agent": ua, })
        touch = bjySession.get(url="https://m.bjyouth.net/site/login")
        cap_url = "https://m.bjyouth.net" + re.findall(
            r'src="/site/captcha.+" alt=', touch.text)[0][5:-6]
        cap_text = cap_recognize(bjySession.get(url=cap_url).content)
        print(f'验证码识别: {cap_text}')
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
            raise Exception('Login:识别的验证码错误')
        print(f'Login:[{login_r.status_code}]{login_r.text}')
        r = json.loads(bjySession.get("https://m.bjyouth.net/dxx/index").text)
        if 'newCourse' not in r:
            print(r)
        url = r['newCourse']['url']
        title = r['newCourse']['title']
        course_id = r['newCourse']['id']
        break
    except:
        time.sleep(3)
        print(traceback.format_exc())

if not url:
    print('Fail in login, terminating...')
    exit(1)

r2 = bjySession.get('https://m.bjyouth.net/dxx/my-integral?type=2&page=1&limit=15')
have_learned = json.loads(r2.text)
if f"学习课程：《{title}》" in list(map(lambda x: x['text'], have_learned['data'])):
    print(f'{title} 在运行前已完成')
    exit(0)

pattern = re.compile(r'https://h5.cyol.com/special/daxuexi/(\w+)/m.html\?t=1&z=201')
result = pattern.search(url)
if not result:
    print(f'Url pattern not matched: {url}')
    exit(1)

end_img_url = f'https://h5.cyol.com/special/daxuexi/{result.group(1)}/images/end.jpg'
study_url = f"https://m.bjyouth.net/dxx/check?id={course_id}&org_id={org_id}"

r = bjySession.get(study_url)
if r.text:
    print(
        f'Unexpected response: {r.text}'
    )
    exit(1)

r = bjySession.get('https://m.bjyouth.net/dxx/my-integral?type=2&page=1&limit=15')
have_learned = json.loads(r.text)
if f"学习课程：《{title}》" in list(map(lambda x: x['text'], have_learned['data'])):
    print(f'{title} 成功完成学习')
    exit(0)
else:
    print(f'完成{title}, 但未在检查中确认 {f"学习课程：《{title}》"}' not in {
        list(map(lambda x: x['text'], have_learned['data']))})
    exit(1)
