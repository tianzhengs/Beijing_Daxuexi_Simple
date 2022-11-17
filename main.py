import os
import json
from study import study

# cur dir to main.py file dir
os.chdir(os.path.dirname(os.path.abspath(__file__)))

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
