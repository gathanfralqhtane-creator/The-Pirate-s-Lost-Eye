import os
import subprocess
import json
import time
import requests

# ألوان القراصنة
CYAN = '\033[36m'
RED = '\033[31m'
YELLOW = '\033[33m'
GREEN = '\033[32m'
RESET = '\033[0m'

CONFIG_FILE = ".config.json"

def logo():
    print(f"{CYAN}")
    print("   ____  _           _   's Lost Eye ")
    print("  |  _ \(_)_ __ __ _| |_ ___           ")
    print("  | |_) | | '__/ _` | __/ _ \          ")
    print("  |  __/| | | | (_| | ||  __/          ")
    print("  |_|   |_|_|  \__,_|\__\___| v1.5     ")
    print(f"       -- Your Personal Guardian --     {RESET}")

def setup():
    """إعداد البوت للمستخدم الجديد"""
    if not os.path.exists(CONFIG_FILE):
        print(f"{YELLOW}[!] First time setup required...{RESET}")
        token = input(f"{CYAN}Enter your Telegram Bot Token: {RESET}")
        chat_id = input(f"{CYAN}Enter your Telegram Chat ID: {RESET}")
        config = {"token": token, "chat_id": chat_id}
        with open(CONFIG_FILE, 'w') as f:
            json.dump(config, f)
        print(f"{GREEN}[+] Config saved successfully!{RESET}")
    
    with open(CONFIG_FILE, 'r') as f:
        return json.load(f)

def send_telegram_msg(token, chat_id, message):
    """إرسال التنبيه إلى تلجرام"""
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {"chat_id": chat_id, "text": message, "parse_mode": "HTML"}
    try:
        requests.post(url, data=payload)
    except:
        print(f"{RED}[-] Failed to send Telegram alert!{RESET}")

def get_notifications():
    try:
        result = subprocess.check_output(['termux-notification-list'])
        return json.loads(result)
    except:
        return []

def scan_and_alert(note, token, chat_id):
    title = note.get('title', 'Unknown')
    content = note.get('content', '')
    
    alert_needed = False
    alert_msg = f"⚠️ <b>Pirate Eye Alert!</b>\n\n<b>From:</b> {title}\n<b>Content:</b> {content}\n"

    # كشف الروابط
    if "http" in content:
        alert_needed = True
        alert_msg += "🛡️ <b>Type:</b> Suspicious Link Detected!\n"

    # كشف محاولات الاختراق والتخمين
    security_keywords = ["رمز", "OTP", "login", "تأكيد", "دخول", "password", "كود"]
    if any(word.lower() in content.lower() for word in security_keywords):
        alert_needed = True
        alert_msg += "🚨 <b>Type:</b> Security/Login Attempt!\n"

    if alert_needed:
        print(f"{RED}[!] Danger detected! Sending alert to Telegram...{RESET}")
        send_telegram_msg(token, chat_id, alert_msg)

def start_eye():
    logo()
    user_config = setup()
    token = user_config['token']
    chat_id = user_config['chat_id']
    
    print(f"{GREEN}[+] The Eye is watching... Scanning notifications.{RESET}")
    send_telegram_msg(token, chat_id, "🏴‍☠️ <b>The Pirate's Lost Eye is now ONLINE.</b>\nI am watching your back, Captain!")

    seen_ids = set()
    while True:
        notifications = get_notifications()
        for note in notifications:
            note_id = note.get('id')
            if note_id not in seen_ids:
                scan_and_alert(note, token, chat_id)
                seen_ids.add(note_id)
        time.sleep(2)

if __name__ == "__main__":
    start_eye()
  
