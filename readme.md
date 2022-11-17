# 北京青年大学习

在运行时获取最新一集,如未学习进行学习,已学习则结束

## 特性

- 多账号支持
- 已学习则跳过
- 自动获取组织ID
- 验证码识别

## 运行环境

- Python 3.7 +
- 运行 `pip install -r requirements.txt`

> Mac ARM 系列的同学需要使用 [miniforge](https://github.com/conda-forge/miniforge) 安装，运行 `conda install --file requirements.txt` 即可。

## 本地运行

### 1. 填写 account.json

将 `account.json.example` 复制一份并重命名为 `account.json` 后，按照格式填写若干个用户名、密码。

> 注意 json 文件的格式，在每个大括号内部的*结尾*不能有多余的逗号：
>
> ![CleanShot 2022-11-17 at 17.10.08@2x](https://tva1.sinaimg.cn/large/008vxvgGly1h888phmxd8j30ca05iwek.jpg)

### 2. 运行脚本

使用 `python main.py` 命令运行脚本即可。

## 定时运行（Linux）

1. 使用 crontab 配置自动运行，执行 `crontab -e`。
2. 在打开的编辑器中写入
  ```
  0 8 */3 * * /你的文件夹绝对路径/run.sh
  ```
3. 退出文件编辑并保存即可。