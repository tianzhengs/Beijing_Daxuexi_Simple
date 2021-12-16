# 北京青年大学习

基于GitHub Action运行,简洁版本

在运行时获取最新一集,如未学习进行学习,已学习则结束

建议配置运行频率一周2次(默认为3天一次),没有成功会出错,默认配置下GitHub会向邮箱推送,所以没有推送功能

更新：多账号支持,由于workflow权限限制,多账号只能重用USERNAME段


# How to use

1. Fork  (+ Star)
2. 填写以下SECRET （名称均为大写）

​		(账号密码为登录青春北京的信息,可以在[这里](https://m.bjyouth.net/site/login)测试登录信息,[如何添加SECRET](https://docs.github.com/cn/actions/security-guides/encrypted-secrets#creating-encrypted-secrets-for-a-repository)) 

​		方法1:单用户

| Name     |                Description                 |
| -------- | :----------------------------------------: |
| USERNAME |                 账号(必须)                 |
| PASSWORD |                 密码(必须)                 |
| ORGID    | 组织ID(可选，默认为172442，北京海淀区团委) |

​		方法2:支持多用户

| Name     | Description                                                |
| -------- | ---------------------------------------------------------- |
| USERNAME | 账号(必须): 每一行为 ***账号 密码 组织ID*** 中间由空格隔开 |

3. 在Actions界面**手动启用(默认被禁用)** Workflows，**DaXueXi** 自动跟随本分支更新(以希望在有变化时不用再手动fetch upstream)，如有安全顾虑**或需要修改**等可选择没有自动更新的 **DaXueXi (No update)**
4. (可以手动运行一次试验)，可以在Run python中看到打印的结果信息
