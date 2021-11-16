# 北京青年大学习
基于Github Action运行,简洁版本

在运行时获取最新一集,如未学习进行学习,已学习则结束

建议配置运行频率一周2次(默认为3天一次),没有成功会出错,默认配置下Github会向邮箱推送,所以没有推送功能

(组织不是海淀区团委可能需要修改org_id)


# How to use
1. Fork  (+ ~~Star~~)
2. 填写以下SECRET （名称均为大写）: 

​		(账号密码为登录青春北京的信息,可以在[这里](https://m.bjyouth.net/site/login)测试登录信息) 

​		USERNAME: 账号  

​		PASSWORD: 密码  

​		[如何添加SECRET](https://docs.github.com/cn/actions/security-guides/encrypted-secrets#creating-encrypted-secrets-for-a-repository)

3. 在Actions界面**手动**(默认被禁用)启用定时任务(并可以手动运行一次试验)，可以在Run python中看到打印的结果信息

# 其他
在Actions中部署了fork后自动跟随本分支更新，如有安全顾虑或其他原因可在Actions配置中手动更改

感谢[ouyen/qndxx-beijing](https://github.com/ouyen/qndxx-beijing)
