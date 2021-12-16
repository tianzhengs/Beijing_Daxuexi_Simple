import os

from study import study


def getAccounts():
    result = []

    usernameRaw = os.getenv("USERNAME", "")
    if len(usernameRaw.split('\n'))==1:
        # Single User
        passwd = os.environ["PASSWORD"]
        if usernameRaw and passwd:
            result.append((usernameRaw, passwd, os.getenv("ORGID", "172442")))
    else:
        # Multiple Users
        account_lines = usernameRaw.split('\n')
        for lnum, line in enumerate(account_lines):
            if len(line.split(' ')) != 3:
                raise Exception(f"第{lnum}行账号格式错误")
            result.append(line.split(' '))

    if not result:
        raise Exception("没有被配置的账号！请设置Secret: USERNAME和PASSWORD")
    return result


ua = os.getenv('UA',
               'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36 Edg/80.0.361.111')

accounts = getAccounts()
print(f'账号数量：{len(accounts)}')
successful = 0
failed = 0
count = 0
for username, password, org_id in accounts:
    count+= 1
    print(f'--User {count}--')
    if study(username, password, org_id, ua):
        successful += 1
    else:
        failed += 1

print(f'成功：{successful}，失败：{failed}')
if failed != 0:
    raise Exception(f'有{failed}个失败！')
