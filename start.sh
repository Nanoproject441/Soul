#!/bin/bash

echo "🚀 DRX POWER SYSTEM STARTING..."

# 1. Sabse pehle zaroori libraries install karega
echo "📦 Installing Python libraries..."
pip install flask telebot requests psutil --quiet

# 2. C Binary ko compile karega (High Power Mode)
echo "⚙️ Compiling drx.c binary..."
gcc drx.c -o drx -lpthread -O3
chmod +x drx

# 3. Purane sessions ko band karega agar koi chal raha ho
echo "🧹 Cleaning old sessions..."
pkill -f api.py

# 4. API ko background mein start karega (Port 8080)
echo "🌐 Starting Flask API on port 8080..."
nohup python3 api.py > api_logs.txt 2>&1 &
sleep 2

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "✅ SYSTEM IS NOW LIVE!"
echo "📡 API Status: Running"
echo "📝 Logs saved in: api_logs.txt and bot_logs.txt"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
