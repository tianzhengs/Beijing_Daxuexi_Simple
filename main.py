import os

from study import study


def getAccounts():
    result = []

    usernameRaw = os.getenv("USERNAME", "")
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
               'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.80 Safari/537.36 Edg/98.0.1108.50')

accounts = getAccounts()
print(f'账号数量：{len(accounts)}')
successful = 0
count = 0
for username, password in accounts:
    count += 1
    print(f'--User {count}--')
    if study(username, password, ua):
        successful += 1

failed = count - successful
print('--Summary--')
print(f'成功：{successful}，失败：{failed}')
if failed != 0:
    raise Exception(f'有{failed}个失败！')

raise Exception('貌似自己这显示完成了，但实际上没有？建议自己检查下(尤其是有团支书账号可以看到情况的)，然后可以在issue#31里反馈下')
