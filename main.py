import os
import time
import sys
from study import study
from fake_useragent import UserAgent



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


ua = UserAgent().random

# # Windows Automated Task Management
# task_name="Daxuexi_18S4F65D"
# if os.name == 'nt':
#     if task_name in os.popen("SCHTASKS /query").read():
#         print("脚本配置的计划任务已存在")
#         # + 检测路径
#     else:
#         if 1: # change to 0 if you want to manage it yourself
#             input("没有脚本配置的计划任务，按任意键创建；或者退出并把main.py 43行的1改成0")
#             k=os.popen(f"{sys.executable} ./runtest.py").read()
#             if 'SHOULDBEFINE\n'!=k:
#                 if 'FAILIMPORT\n'==k:
#                     print("依赖问题")
#                 else:
#                     print('创建失败？Python位置不对？')
#                 exit(1)
#             create=os.popen(f'''SchTasks /Create /SC DAILY /MO 2 /TN {task_name} /TR "'{sys.executable}' '{os.path.realpath(__file__)}'" /ST 09:00''')
#             print('创建成功')

accounts = getAccounts()
# accounts=[('********', '*********')]
print(f'账号数量：{len(accounts)}')
successful = 0
count = 0
for username, password in accounts:
    if username=='********':
        continue
    count += 1
    print(f'--User {count}--')
    if study(username, password, ua):
        successful += 1
    time.sleep(4)

failed = count - successful
print('--Summary--')
print(f'成功：{successful}，失败：{failed}')
if failed != 0:
    raise Exception(f'有{failed}个失败！')