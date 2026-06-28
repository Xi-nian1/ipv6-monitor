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

### 4. 设置 Windows 任务计划程序自动唤醒
我们需要配置 Windows 任务计划程序，让它在**开机**和**唤醒**时运行 `ipv6.exe`：

1. 按下 `Win + X`，打开 **Windows PowerShell (管理员)**。
2. 进入项目目录并导入任务（假设您的代码在 `D:\ipv6`，需要自行替换下面 XML 中的路径）：
```powershell
schtasks /create /tn "IPv6_Monitor" /xml .\task.xml /f
```
3. 导入成功后，系统每次开机或休眠唤醒时，均会自动触发运行该脚本并发送邮件。
