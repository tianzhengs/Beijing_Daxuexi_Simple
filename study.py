import json
import re
import time
import traceback

import requests

from utility import encrypt, cap_recognize


def study(username, password, org_id, ua):
    # return 1:success;0:fail
    url = ''
    try_time = 0
    while try_time < 4:
        try:
            bjySession = requests.session()
            bjySession.timeout = 5  # set session timeout
            bjySession.headers.update({"User-Agent": ua, })
            touch = bjySession.get(url="https://m.bjyouth.net/site/login")
            cap_url = "https://m.bjyouth.net" + re.findall(
                r'src="(/site/captcha.+)" alt=', touch.text)[0]
            cap_text = cap_recognize(bjySession.get(url=cap_url).content)
            # print(f'验证码识别: {cap_text}')
            login_r = bjySession.post('https://m.bjyouth.net/site/login',
                                      data={
                                          '_csrf_mobile': bjySession.cookies.get_dict()['_csrf_mobile'],
                                          'Login[password]': encrypt(password),
                                          'Login[username]': encrypt(username),
                                          'Login[verifyCode]': cap_text
                                      })
            print(f'Login:[{login_r.status_code}]{login_r.text}')
            if login_r.text == '8':
                print('Login:识别的验证码错误')
                continue
            if 'fail' in login_r.text:
                try_time += 9
                raise Exception('Login:账号密码错误')
            r = json.loads(bjySession.get("https://m.bjyouth.net/dxx/index").text)
            if 'newCourse' not in r:
                print(r)
            url = r['newCourse']['url']
            title = r['newCourse']['title']
            course_id = r['newCourse']['id']
            break
        except:
            time.sleep(3)
            try_time += 1
            print(traceback.format_exc())

    if not url:
        print('登陆失败,退出')
        return 0

    r2 = bjySession.get('https://m.bjyouth.net/dxx/my-integral?type=2&page=1&limit=15')
    have_learned = json.loads(r2.text)
    if f"学习课程：《{title}》" in list(map(lambda x: x['text'], have_learned['data'])):
        print(f'{title} 在运行前已完成,退出')
        return 1

    pattern = re.compile(r'https://h5.cyol.com/special/daxuexi/(\w+)/m.html\?t=1&z=201')
    result = pattern.search(url)
    if not result:
        print(f'Url pattern not matched: {url}')
        return 0

    end_img_url = f'https://h5.cyol.com/special/daxuexi/{result.group(1)}/images/end.jpg'
    study_url = f"https://m.bjyouth.net/dxx/check?id={course_id}&org_id={org_id}"

    r = bjySession.get(study_url)
    if r.text:
        print(f'Unexpected response: {r.text}')
        return 0

    r = bjySession.get('https://m.bjyouth.net/dxx/my-integral?type=2&page=1&limit=15')
    have_learned = json.loads(r.text)
    if f"学习课程：《{title}》" in list(map(lambda x: x['text'], have_learned['data'])):
        print(f'{title} 成功完成学习')
        return 1
    else:
        print(f'完成{title}, 但未在检查中确认')
        return 0
