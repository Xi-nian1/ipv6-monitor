[简体中文](README.md) | [English](README_en.md) | [日本語](README_ja.md) | [Français](README_fr.md)

# IPv6 Monitor & Email Notifier

This is an extremely lightweight Windows background application that automatically detects your local machine's public IPv6 address and sends it to a specified email address via SMTP when the system **boots up** or **wakes up from sleep/hibernation**.

## Features
- **Zero Dependencies**: Utilizes only Python's built-in standard libraries (`urllib`, `smtplib`, `socket`, etc.). No need to `pip install` any third-party packages.
- **Single Run**: Does not stay resident in the background with an endless loop. It runs once, sends the email, and exits immediately, strictly preserving system resources.
- **System-Level Triggers**: Perfectly integrates with Windows Task Scheduler for system event triggering.

## Usage

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

### 4. Setup Windows Task Scheduler Auto-Wake (GUI Tutorial)

To run the program seamlessly in the background on startup and when waking up from sleep, configure it via the built-in Windows "Task Scheduler":

1. **Open Task Scheduler**: Press `Win + S`, search for "Task Scheduler", and open it.
2. **Create Task**: On the right Actions pane, click **"Create Task..."** (Note: Do not click "Create Basic Task").
3. **General**:
   - Name: `IPv6_Monitor`.
   - Check **"Hidden"** at the bottom.
   - Check **"Run whether user is logged on or not"** and **"Run with highest privileges"**.
4. **Triggers** (Create the following two triggers):
   - Trigger 1: Begin the task **"At log on"**.
   - Trigger 2: Begin the task **"On an event"**. Select Log: **System**, Source: **Power-Troubleshooter**, and Event ID: **1** (This event indicates waking up from sleep/hibernation).
5. **Actions**:
   - Action: **"Start a program"**.
   - **Program/script**: Browse and select your packaged `ipv6.exe`.
   - **Start in**: Enter the absolute path of the folder containing `ipv6.exe` (e.g., `D:\ipv6\`, **make sure it ends with a backslash and do not use quotes**).
6. **Conditions**:
   - Uncheck "Start the task only if the computer is on AC power" (if using a laptop).
7. Click OK and enter your Windows account password to save!
