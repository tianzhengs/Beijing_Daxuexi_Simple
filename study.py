import json
import re
import time
import traceback

import requests

from utility import encrypt, cap_recognize


def study(username, password, ua):
    # return 1:success;0:fail
    url = ''
    tryTime = 0
    while tryTime < 4:
        try:
            bjySession = requests.session()
            bjySession.timeout = 5  # set session timeout
            bjySession.headers.update({"User-Agent": ua, })
            touch = bjySession.get(url="https://m.bjyouth.net/site/login")
            capUrl = "https://m.bjyouth.net" + re.findall(
                r'src="(/site/captcha.+)" alt=', touch.text)[0]
            if "MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQD5uIDebA2qU746e/NVPiQSBA0Q" not in touch.text:
                print("记录的公钥没有出现")
            capText = cap_recognize(bjySession.get(url=capUrl).content)
            # print(f'验证码识别: {capText}')
            login_r = bjySession.post('https://m.bjyouth.net/site/login',
                                      data={
                                          '_csrf_mobile': bjySession.cookies.get_dict()['_csrf_mobile'],
                                          'Login[password]': encrypt(password),
                                          'Login[username]': encrypt(username),
                                          'Login[verifyCode]': capText
                                      })

            if login_r.text == '8':
                print('Login:识别的验证码错误')
                continue
            if 'fail' in login_r.text:
                tryTime += 9
                raise Exception('Login:账号密码错误')
            print('登录成功')
            r = json.loads(bjySession.get("https://m.bjyouth.net/dxx/index").text)
            # "rize" LOL
            if 'newCourse' not in r:
                print(r)
            url = r['newCourse']['url']
            title = r['newCourse']['title']
            courseId = r['newCourse']['id']
            break
        except:
            time.sleep(3)
            tryTime += 1
            print(traceback.format_exc())

    if not url:
        print('登入失败,退出')
        return 0

    orgIdTemp = ''
    orgPattern = re.compile(r'\(|（\s*(\d+)\s*）|\)')  # 组织id应该是被括号包的
    learnedInfo = 'https://m.bjyouth.net/dxx/my-study?page=1&limit=15&year=' + time.strftime("%Y", time.localtime())
    haveLearned = bjySession.get(learnedInfo).json()

    orgID = ""
    try:
        orgIdTemp = orgPattern.search(haveLearned['data'][0]['orgname'])
        orgID = orgIdTemp.group(1)
    except:
        print('获取组织id-2')
        orgIdTemp = orgPattern.search(bjySession.get('https://m.bjyouth.net/dxx/my').json()['data']['org'])
        if orgIdTemp:
            orgID = orgIdTemp.group(1)

    if not orgID:
        orgID = '172442'
        print(f"无法获取orgID")

    nOrgID = int(bjySession.get('https://m.bjyouth.net/dxx/is-league').text)

    if f"学习课程：《{title}》" in list(map(lambda x: x['text'], haveLearned['data'])):
        print(f'{title} 在运行前已完成,退出')
        return 1

    # pattern = re.compile(r'https://h5.cyol.com/special/daxuexi/(\w+)/m.html\?t=1&z=201')
    # result = pattern.search(url)
    # if not result:
    #     print(f'Url pattern not matched: {url}')
    #     return 0
    #
    # end_img_url = f'https://h5.cyol.com/special/daxuexi/{result.group(1)}/images/end.jpg'
    study_url = f"https://m.bjyouth.net/dxx/check"
    r = bjySession.post(study_url, json={"id": str(courseId), "org_id": int(nOrgID)})  # payload

    if r.text:
        print(f'Unexpected response: {r.text}')
        return 0

    haveLearned = bjySession.get(learnedInfo).json()

    if int(orgID) != nOrgID:
        raise Exception('组织id不匹配，如果看到这个请开个issue说下')

    if f"学习课程：《{title}》" in list(map(lambda x: x['text'], haveLearned['data'])):
        print(f'{title} 成功完成学习')
        return 1
    else:
        print(f'完成{title}, 但未在检查中确认')
        return 0
