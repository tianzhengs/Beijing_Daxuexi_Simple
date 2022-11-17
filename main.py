import os
import json
from study import study

# cur dir to main.py file dir
os.chdir(os.path.dirname(os.path.abspath(__file__)))


task_name = "Daxuexi_18S4F65D"
if os.name == 'nt':
    if task_name in os.popen("SCHTASKS /query").read():
        print("脚本配置的计划任务已存在")
        # + 检测路径
    else:
        if 1:  # change to 0 if you want to manage it yourself
            input("没有脚本配置的计划任务，按任意键创建；或者退出并把main.py 43行的1改成0")
            k = os.popen(f"{sys.executable} ./runtest.py").read()
            if 'SHOULDBEFINE\n' != k:
                if 'FAILIMPORT\n' == k:
                    print("依赖问题")
                else:
                    print('创建失败？Python位置不对？')
                exit(1)
            create = os.popen(
                f'''SchTasks /Create /SC DAILY /MO 2 /TN {task_name} /TR "'{sys.executable}' '{os.path.realpath(__file__)}'" /ST 09:00''')
            print('创建成功')

# read account data and check they all satisfy 'username', 'password' pattern
if not os.path.exists('account.json'):
    print('account.json not found')
    exit(1)
with open('account.json', 'r', encoding='utf-8') as f:
    accounts = json.load(f)

if type(accounts) != list or not all('username' in account and 'password' in account for account in accounts):
    print('检查 accounts.json 数据格式')
    exit(1)

successful = 0
for i, account in enumerate(accounts):
    print(f'User {i+1}')
    if study(account['username'], account['password']):
        successful += 1

print('--Summary--')
print(f'成功：{successful}，失败：{len(accounts) - successful}')
