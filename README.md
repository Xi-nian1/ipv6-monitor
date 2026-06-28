[简体中文](README.md) | [English](README_en.md) | [日本語](README_ja.md) | [Français](README_fr.md)

# IPv6 Monitor & Email Notifier

这是一个极其轻量的 Windows 后台程序，用于在**系统开机**或**从休眠/睡眠中唤醒**时，自动检测本机的公网 IPv6 地址，并通过 SMTP 发送到指定的邮箱。

## 特点
- **零依赖**：只使用 Python 内置的标准库（`urllib`, `smtplib`, `socket` 等），无需 `pip install` 任何第三方库。
- **单次运行**：不驻留后台死循环。运行一次、发送完毕后立即退出，极限节省系统资源。
- **系统级触发**：完美配合 Windows 任务计划程序 (Task Scheduler) 的系统事件触发。

## 使用方法

### 1. 配置文件
复制 `config.example.json` 并重命名为 `config.json`，填写您的邮箱配置：
```json
{
    "from_email": "你的发件邮箱@qq.com",
    "auth_code": "你的邮箱SMTP授权码",
    "to_email": "接收通知的邮箱@qq.com",
    "check_interval": 300,
    "retry_times": 3,
    "log_file": "ipv6_sender.log",
    "ip_check_services": [
        "https://ipv6.icanhazip.com",
        "https://v6.ident.me",
        "https://ipv6.lookup.test-ipv6.com/ip/"
    ]
}
```
*(注意：JSON 文件中不能包含 `//` 等注释)*

### 2. 运行脚本
直接使用 Python 运行：
```bash
python ipv6.py
```

### 3. 打包为 EXE可执行文件 (可选)
为了在后台无黑框静默运行，推荐打包为 `.exe` 文件：
```bash
pip install pyinstaller
pyinstaller -F -w ipv6.py
```
打包后，将生成的 `ipv6.exe` 移动到项目根目录（保证和 `config.json` 同级）。

### 4. 设置 Windows 任务计划程序自动唤醒 (GUI 图文教程)

为了让程序在后台毫无痕迹地开机自启、并在休眠唤醒时运行，请通过 Windows 自带的“任务计划程序”进行配置：

1. **打开任务计划程序**：按下 `Win + S` 搜索“任务计划程序” (Task Scheduler) 并打开。
2. **创建任务**：在右侧操作栏点击 **“创建任务...”** (注意不是“创建基本任务”)。
3. **常规 (General)**：
   - 名称填入 `IPv6_Monitor`。
   - 勾选底部 **“隐藏”**。
   - 勾选 **“不管用户是否登录都要运行”**，并勾选 **“使用最高权限运行”**。
4. **触发器 (Triggers)**（新建以下两个触发器）：
   - 触发器 1：开始任务选择 **“登录时”**。
   - 触发器 2：开始任务选择 **“发生事件时”**。日志选择 **系统 (System)**，源选择 **Power-Troubleshooter**，事件 ID 输入 **1**（此事件代表系统从睡眠/休眠中唤醒）。
5. **操作 (Actions)**：
   - 操作选择 **“启动程序”**。
   - **程序或脚本**：点击浏览，选择您打包好的 `ipv6.exe`。
   - **起始于 (Start in)**：填入 `ipv6.exe` 所在的文件夹绝对路径（例如 `D:\ipv6\`，**注意最后必须带斜杠，且不要带引号**）。
6. **条件 (Conditions)**：
   - 取消勾选“只有在计算机使用交流电源时才启动此任务”（针对笔记本）。
7. 点击确定，输入您的 Windows 账号密码保存即可！
