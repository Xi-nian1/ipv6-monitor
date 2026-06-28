[简体中文](README.md) | [English](README_en.md) | [日本語](README_ja.md) | [Français](README_fr.md)

# IPv6 Monitor & Email Notifier

This is an extremely lightweight Windows background application that automatically detects your local machine's public IPv6 address and sends it to a specified email address via SMTP when the system **boots up** or **wakes up from sleep/hibernation**.

## Features
- **Zero Dependencies**: Utilizes only Python's built-in standard libraries (`urllib`, `smtplib`, `socket`, etc.). No need to `pip install` any third-party packages.
- **Single Run**: Does not stay resident in the background with an endless loop. It runs once, sends the email, and exits immediately, strictly preserving system resources.
- **System-Level Triggers**: Perfectly integrates with Windows Task Scheduler for system event triggering.


## Use Cases
- **Remote Desktop (RDP)**: If you need to remotely access your home PC from work but your home network lacks a static IPv4, you can connect directly using the fresh IPv6 address sent to your email.
- **Personal Server / NAS**: For users running a NAS or web server on a standard PC, this app will instantly push the new access IP to your phone's email if the router's IP changes or the PC reboots after a power outage.
- **Dependency-Free DDNS Alternative**: Compared to setting up complex Dynamic DNS (DDNS) services, this email notification approach is much more foolproof, stable, and requires no domain name purchases.

## Usage

> [!IMPORTANT]
> **Preparation:** Before you begin, you need to modify the following two files to match your local environment:
> 1. **`config.json`**: You must fill in your own sender email, SMTP auth code, and receiver email.
> 2. **`task.xml`**: If you want to setup auto-wake and auto-start, you must replace the placeholder paths inside it with your actual absolute paths.


### 1. Configuration
Copy `config.example.json`, rename it to `config.json`, and fill in your email configuration:
```json
{
    "from_email": "your_sender_email@qq.com",
    "auth_code": "your_smtp_auth_code",
    "to_email": "receiver_email@qq.com",
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
*(Note: standard JSON does not support `//` comments)*

### 2. Run the Script
Run it directly using Python:
```bash
python ipv6.py
```

### 3. Build as an EXE Executable (Optional)
To run silently in the background without a console window, it is highly recommended to package it into an `.exe` file:
```bash
pip install pyinstaller
pyinstaller -F -w ipv6.py
```
After building, move the generated `ipv6.exe` to the project root directory (ensure it is in the same directory as `config.json`).

### 4. Setup Windows Task Scheduler Auto-Wake

We need to configure the Windows Task Scheduler to automatically run `ipv6.exe` on **Startup** and **Wake up**:

1. **Edit the XML paths**: Open the `task.xml` file in Notepad. Locate the `<Command>` and `<WorkingDirectory>` tags at the very bottom, and replace `C:\path\to\your\folder` with the actual absolute path where you saved `ipv6.exe`. Save the file.
2. **Open Terminal**: Press `Win + X` and open **Windows PowerShell (Admin)** or **Terminal (Admin)**.
3. **Import Task**: In the window, use the `cd` command to navigate to your project directory, then run the following command to import the task:
```powershell
schtasks /create /tn "IPv6_Monitor" /xml .\task.xml /f
```
4. Once successfully imported, the script will automatically run silently in the background and send the email every time the system boots up or wakes from sleep/hibernation.
