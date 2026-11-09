#!/usr/bin/env bash
# ==============================================================================
# Al-Manara AI Dev Hub Pro - Universal Auto Installer (Linux & Android / Termux)
# ==============================================================================

set -e

echo "=========================================================="
echo " 🏮 Al-Manara AI Dev Hub Pro - تثبيت وإعداد المشروع"
echo "=========================================================="

# 1. فحص بيئة التشغيل وتثبيت المتطلبات الأساسية
if [ -d "/data/data/com.termux/files" ]; then
    echo "[*] تم التعرف على بيئة: Android (Termux)"
    echo "[*] جاري التحقق من الحزم الأساسية..."
    pkg update -y
    pkg install -y python git llama-cpp 2>/dev/null || pkg install -y python git
else
    echo "[*] تم التعرف على بيئة: Linux (Ubuntu / Debian / Arch / etc.)"
    echo "[*] جاري التحقق من Python و Git..."
    if command -v apt-get >/dev/null 2>&1; then
        sudo apt-get update && sudo apt-get install -y python3 python3-pip python3-venv git
    fi
fi

# 2. إنشاء بيئة افتراضية أو تثبيت الحزم
echo "[*] جاري تثبيت حزم بايثون المطلوبة..."
python3 -m pip install --upgrade pip 2>/dev/null || true
python3 -m pip install -r requirements.txt

# 3. إعداد الصلاحيات
chmod +x ai_hub.py

# 4. إعداد ملف .env إن لم يكن موجوداً
if [ ! -f "config/.env" ] && [ -f "config/.env.example" ]; then
    cp config/.env.example config/.env
    echo "[+] تم إنشاء ملف config/.env"
fi

echo "=========================================================="
echo " [✓] اكتمل التثبيت بنجاح!"
echo " لتشغيل البرنامج الآن، اكتب:"
echo " ./ai_hub.py"
echo "=========================================================="
