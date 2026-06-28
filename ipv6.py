import socket
import smtplib
import urllib.request
import urllib.error
import time
import sys
import os
import json
from email.mime.text import MIMEText
from email.header import Header
from email.utils import formataddr


def load_config():
    """加载配置文件"""
    config_path = "config.json"

    if os.path.exists(config_path):
        with open(config_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    else:
        # 创建默认配置文件
        default_config = {
            "from_email": "your_email@qq.com",
            "auth_code": "your_auth_code_here",
            "to_email": "receiver@qq.com",
            "check_interval": 300,
            "retry_times": 3,
            "log_file": "ipv6_sender.log",
            "ip_check_services": [
                "https://ipv6.icanhazip.com",
                "https://v6.ident.me",
                "https://ipv6.lookup.test-ipv6.com/ip/",
                "https://ipv6.whatismyip.akamai.com",
                "https://ifconfig.co/ip"
            ]
        }

        with open(config_path, 'w', encoding='utf-8') as f:
            json.dump(default_config, f, indent=4, ensure_ascii=False)

        print(f"已创建配置文件：{config_path}")
        print("请修改配置文件中的邮箱和授权码信息")
        return default_config


def log_message(message, log_file=None):
    """记录日志"""
    timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
    log_msg = f"[{timestamp}] {message}"
    print(log_msg)

    if log_file:
        with open(log_file, 'a', encoding='utf-8') as f:
            f.write(log_msg + "\n")


def is_global_ipv6(ip):
    """检查是否为公网IPv6地址"""
    if not ip:
        return False

    ip = ip.lower().strip()

    # 排除常见的非公网IPv6地址
    non_global_prefixes = [
        '::1',  # 本地回环
        'fe80::',  # 链路本地
        'fc00::',  # 唯一本地地址 (ULA)
        'fd00::',  # 唯一本地地址 (ULA)
        'ff00::',  # 组播地址
        '2001:db8::',  # 文档地址
        '2001:10:',  # ORCHID地址
        '2002::',  # 6to4隧道地址
    ]

    # 检查是否匹配非公网前缀
    for prefix in non_global_prefixes:
        if ip.startswith(prefix):
            return False

    # 检查是否为公网地址（2000::/3 是全局单播地址范围）
    try:
        # 获取第一个16位块
        first_block = ip.split(':')[0]
        if not first_block:
            return False

        # 转换为十进制
        first_hex = int(first_block, 16)

        # 2000::/3 范围：0x2000 到 0x3fff
        return 0x2000 <= first_hex <= 0x3fff
    except:
        # 如果解析失败，保守判断
        return False


def get_public_ipv6_address(config):
    """获取公网IPv6地址"""
    public_ipv6_list = []

    # 方法1：通过在线API获取公网IPv6
    services = config.get('ip_check_services', [
        "https://ipv6.icanhazip.com",
        "https://v6.ident.me",
        "https://ipv6.lookup.test-ipv6.com/ip/",
        "https://ipv6.whatismyip.akamai.com",
        "https://ifconfig.co/ip"
    ])

    for service in services:
        try:
            log_message(f"尝试从 {service} 获取IPv6地址...")

            # 设置较短的超时时间
            timeout = 8

            req = urllib.request.Request(service, headers={'User-Agent': 'Mozilla/5.0'})
            if service == "https://ifconfig.co/ip":
                req.add_header('Host', 'ifconfig.co')

            with urllib.request.urlopen(req, timeout=timeout) as response:
                if response.getcode() == 200:
                    ip = response.read().decode('utf-8').strip()

                    # 清理可能的换行符和多余空格
                    ip = ip.replace('\n', '').replace('\r', '').strip()

                    if ip:
                        # 验证是否为有效的IPv6地址
                        if ':' in ip and is_global_ipv6(ip):
                            # 去重
                            if ip not in public_ipv6_list:
                                public_ipv6_list.append(ip)
                                log_message(f"✓ 从 {service} 获取到公网IPv6地址: {ip}")
                                # 获取到一个就退出循环
                                break
                        else:
                            log_message(f"✗ 从 {service} 获取到的地址不是公网IPv6: {ip}")
                else:
                    log_message(f"✗ {service} 响应状态码: {response.getcode()}")

        except urllib.error.URLError as e:
            if isinstance(e.reason, socket.timeout):
                log_message(f"✗ {service} 请求超时")
            else:
                log_message(f"✗ {service} 请求失败: {str(e)}")
            continue
        except socket.timeout:
            log_message(f"✗ {service} 请求超时")
            continue
        except Exception as e:
            log_message(f"✗ {service} 解析失败: {str(e)}")
            continue

    # 方法2：从本地网络接口获取
    if not public_ipv6_list:
        try:
            log_message("尝试从本地网络接口获取公网IPv6地址...")

            # 使用公共DNS服务器
            test_services = [
                ('2620:fe::fe', 53),  # Quad9 DNS IPv6
                ('2606:4700:4700::1111', 53),  # Cloudflare DNS IPv6
                ('2001:678:e34:1::1', 53),  # DNSPod Public DNS IPv6
            ]

            for dns_server, port in test_services:
                try:
                    # 创建一个socket连接到DNS服务器
                    s = socket.socket(socket.AF_INET6, socket.SOCK_DGRAM)
                    s.settimeout(5)
                    s.connect((dns_server, port))
                    local_ip = s.getsockname()[0]
                    s.close()

                    if is_global_ipv6(local_ip):
                        if local_ip not in public_ipv6_list:
                            public_ipv6_list.append(local_ip)
                            log_message(f"✓ 获取到公网IPv6地址: {local_ip}")
                            break
                except socket.gaierror:
                    continue
                except Exception:
                    continue

        except Exception as e:
            log_message(f"✗ 从本地接口获取IPv6失败: {str(e)}")

    return public_ipv6_list


def send_email_qmail(config, ipv6_list):
    """发送邮件到QQ邮箱 - 只发送IPv6地址列表"""
    # 邮件服务器配置
    smtp_server = "smtp.qq.com"
    smtp_port = 465

    # 准备邮件内容 - 简化为只有IP地址列表
    current_time = time.strftime('%Y-%m-%d %H:%M:%S')
    subject = f"IPv6地址 - {current_time}"

    if ipv6_list:
        # 只保留IPv6地址，每个地址一行
        body = "\n".join([ip for ip in ipv6_list])
    else:
        body = "未检测到公网IPv6地址"

    try:
        # 创建MIMEText对象
        msg = MIMEText(body, 'plain', 'utf-8')

        # 关键：正确设置邮件头部（符合QQ邮箱要求）
        from_email = config['from_email']
        to_email = config['to_email']

        # 使用formataddr确保格式正确
        msg['From'] = formataddr(('IPv6监控', from_email))
        msg['To'] = formataddr(('接收者', to_email))
        msg['Subject'] = Header(subject, 'utf-8')

        # 添加Date头部（RFC要求）
        msg['Date'] = time.strftime('%a, %d %b %Y %H:%M:%S +0800', time.localtime())

        # 连接服务器并发送
        log_message(f"正在连接SMTP服务器: {smtp_server}:{smtp_port}")
        server = smtplib.SMTP_SSL(smtp_server, smtp_port)

        log_message("正在登录邮箱...")
        server.login(from_email, config['auth_code'])

        log_message("正在发送邮件...")
        server.sendmail(from_email, [to_email], msg.as_string())

        server.quit()
        log_message("邮件发送成功！")
        return True

    except smtplib.SMTPException as e:
        log_message(f"SMTP错误: {str(e)}")
        # 详细错误信息
        if hasattr(e, 'smtp_code'):
            log_message(f"错误代码: {e.smtp_code}")
        if hasattr(e, 'smtp_error'):
            log_message(f"错误详情: {e.smtp_error}")
        return False

    except Exception as e:
        log_message(f"发送邮件失败: {str(e)}")
        return False


def check_network():
    """检查网络连接"""
    test_urls = [
        "https://www.qq.com",
        "https://www.baidu.com",
        "https://www.taobao.com",
        "https://www.jd.com",
        "http://connect.rom.miui.com/generate_204"
    ]

    for url in test_urls:
        try:
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req, timeout=8) as response:
                if response.getcode() in [200, 204]:
                    log_message(f"✓ 网络连接测试通过: {url}")
                    return True
        except urllib.error.URLError as e:
            log_message(f"✗ 网络测试 {url} 失败: {str(e)}")
            continue
        except socket.timeout:
            log_message(f"✗ 网络测试 {url} 失败: 超时")
            continue
        except Exception as e:
            log_message(f"✗ 网络测试 {url} 失败: {str(e)}")
            continue

    return False


def run_ipv6_monitor(config, run_count):
    """运行IPv6监控任务"""
    log_file = config.get('log_file')
    
    log_message("=" * 60, log_file)
    log_message(f"第 {run_count} 次运行IPv6地址监控", log_file)
    log_message(f"运行时间: {time.strftime('%Y-%m-%d %H:%M:%S')}", log_file)

    # 等待网络连接
    log_message("正在等待网络连接...", log_file)

    max_wait_time = 300  # 最多等待5分钟
    start_time = time.time()
    network_connected = False

    while time.time() - start_time < max_wait_time:
        if check_network():
            network_connected = True
            log_message("网络连接成功！", log_file)
            break

        log_message("网络未连接，等待10秒后重试...", log_file)
        time.sleep(10)

    if not network_connected:
        log_message("网络连接超时，继续执行...", log_file)

    # 等待一段时间确保IPv6地址分配
    log_message("等待IPv6地址分配...", log_file)
    time.sleep(15)

    # 获取公网IPv6地址
    log_message("正在获取公网IPv6地址...", log_file)
    ipv6_addresses = get_public_ipv6_address(config)

    if ipv6_addresses:
        log_message(f"✓ 成功获取到 {len(ipv6_addresses)} 个公网IPv6地址", log_file)
        for idx, ip in enumerate(ipv6_addresses, 1):
            log_message(f"  [{idx}] {ip}", log_file)
    else:
        log_message("✗ 未检测到公网IPv6地址", log_file)

    # 发送邮件
    log_message("准备发送邮件通知...", log_file)
    success = False

    for attempt in range(config['retry_times']):
        log_message(f"第 {attempt + 1} 次尝试发送邮件...", log_file)

        if send_email_qmail(config, ipv6_addresses):
            success = True
            log_message("✓ 邮件发送成功！", log_file)
            break
        else:
            if attempt < config['retry_times'] - 1:
                retry_wait = 30  # 等待30秒后重试
                log_message(f"发送失败，{retry_wait}秒后重试...", log_file)
                time.sleep(retry_wait)

    if success:
        log_message(f"✓ 第 {run_count} 次运行完成！", log_file)
    else:
        log_message(f"✗ 第 {run_count} 次运行失败", log_file)

    log_message("=" * 60, log_file)
    
    return success


def main():
    """主函数"""
    # 加载配置
    config = load_config()
    log_file = config.get('log_file')

    log_message("=" * 60, log_file)
    log_message("IPv6地址监控程序启动 (单次执行模式)", log_file)
    log_message(f"启动时间: {time.strftime('%Y-%m-%d %H:%M:%S')}", log_file)

    # 检查配置
    if config['from_email'] == "your_email@qq.com":
        log_message("错误：请先修改配置文件 config.json 中的邮箱和授权码信息", log_file)
        time.sleep(10)
        return

    # 执行一次 IPv6 监控任务
    run_ipv6_monitor(config, 1)


if __name__ == "__main__":
    main()