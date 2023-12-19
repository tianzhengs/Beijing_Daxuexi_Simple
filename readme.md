# 北京青年大学习

~~基于GitHub Action运行,简洁版本~~

~~GitHub IP被封啦，只能本地运行了~~

现在好像GitHub Actions又可以了

在运行时获取最新一集,如未学习进行学习,已学习则结束

建议配置运行频率一周2次(默认为3天一次),没有成功会出错,默认配置下GitHub会向邮箱推送,所以没有推送功能

一些特性：多账号支持,已学习则跳过,自动获取组织ID,验证码识别



# How to use

1. Fork  (+ Star)
2. 填写以下SECRET （名称均为大写）

​		(账号密码为登录青春北京的信息,可以在[这里](https://m.bjyouth.net/site/login)测试登录信息,[如何添加SECRET](https://docs.github.com/cn/actions/security-guides/encrypted-secrets#creating-encrypted-secrets-for-a-repository)) 

​		方法1:单用户

| Name     |                Description                 |
| -------- | :----------------------------------------: |
| USERNAME |                 账号(必须)                 |
| PASSWORD |                 密码(必须)                 |

​		方法2:支持多用户

| Name     | Description                                                |
| -------- | ---------------------------------------------------------- |
| USERNAME | 账号信息(必须): 每一行为 ***账号 密码*** 中间由空格隔开(由于需要手动权限更新workflow只能用USERNAME这个名字了) |




# 本地运行 -Windows
下载[Python](https://www.python.org/downloads/),已知3.7-3.9都可以,3.11某些依赖的库不支持。

下载这个repo并解压。

安装依赖： 在解压出来的目录里运行`pip install -r requirements.txt`或`pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple` (如果国内环境+没配置代理)

配置账号： main.py 中 accounts = getAccounts() 一行改成 accounts=[('账号1', '密码1'),('账号2', '密码2'),('账号3', '密码3')]形式

运行： 运行`main.py`

自动运行：可搜索“计划任务”相关，Windows下脚本会自动尝试配置2天一次的计划任务

# 本地运行 -Linux


```sh
# 首次运行建立环境
git clone https://github.com/startkkkkkk/Beijing_Daxuexi_Simple.git
cd Beijing_Daxuexi_Simple
pip install -r requirements.txt
```

然后新建 `run.sh`，写入

```
#!/usr/bin/bash
export USERNAME=你的用户名
export PASSWORD=你的密码
python main.py
```

添加执行权限 `chmod +x run.sh`，之后使用 crontab 配置自动运行，执行 `crontab -e`，在打开的编辑器中写入

```
0 8 */3 * * /home/username/Beijing_Daxuexi_Simple/run.sh
```

注意修改以上路径到你自己的路径。

然后重启 cron （`sudo service cron restart`） 即可。

3. 在Actions界面**手动启用(默认被禁用)** Workflows，**DaXueXi** 自动跟随本分支更新(以希望在有变化时不用再手动fetch upstream)，如有安全顾虑**或需要修改**等可选择没有自动更新的 **DaXueXi (No update)**
4. (可以手动运行一次试验)，可以在Run python中看到打印的结果信息


