#!/usr/bin/env bash
# ==============================================================================
# Al-Manara AI Dev Hub Pro - Universal Auto Installer (Linux & Android / Termux)
# ==============================================================================

set -e

# ضمان التشغيل من المجلد الرئيسي للمشروع دائماً
cd "$(dirname "$0")" || exit 1
SCRIPT_DIR="$(pwd)"

echo "=========================================================="
echo " 🏮 Al-Manara AI Dev Hub Pro - تثبيت وإعداد المشروع"
echo "=========================================================="

# 1. فحص بيئة التشغيل وتثبيت المتطلبات الأساسية
BIN_DIR=""
if [ -n "$TERMUX_VERSION" ] || [ -d "/data/data/com.termux/files" ]; then
    echo "[*] تم التعرف على بيئة: Android (Termux)"
    echo "[*] جاري التحقق من الحزم الأساسية عبر pkg..."
    pkg update -y || true
    pkg install -y python git llama-cpp 2>/dev/null || pkg install -y python git
    BIN_DIR="$PREFIX/bin"
else
    echo "[*] تم التعرف على بيئة: Linux"
    echo "[*] جاري التحقق من الحزم الأساسية..."
    if command -v apt-get >/dev/null 2>&1; then
        echo "[*] استخدام مدير الحزم apt..."
        sudo apt-get update -y && sudo apt-get install -y python3 python3-pip python3-venv git || true
    elif command -v dnf >/dev/null 2>&1; then
        echo "[*] استخدام مدير الحزم dnf..."
        sudo dnf install -y python3 python3-pip git || true
    elif command -v pacman >/dev/null 2>&1; then
        echo "[*] استخدام مدير الحزم pacman..."
        sudo pacman -Sy --noconfirm python python-pip git || true
    fi
    BIN_DIR="$HOME/.local/bin"
    mkdir -p "$BIN_DIR"
fi

# 2. تحديد وضع التثبيت (بيئة افتراضية معزولة أو في النظام العام)
echo ""
echo "----------------------------------------------------------"
echo "❓ كيف تفضل تثبيت متطلبات بايثون؟"
echo "  [1] إنشاء بيئة افتراضية معزولة (.venv) - [موصى به لحماية النظام]"
echo "  [2] التثبيت المباشر في بيئة النظام / تيرمكس العامة"
echo "----------------------------------------------------------"

ENV_CHOICE="1"
USER_INPUT_CHOICE=""

if [ -c /dev/tty ]; then
    read -r -p "اختر [1 أو 2] (الافتراضي 1): " USER_INPUT_CHOICE </dev/tty || USER_INPUT_CHOICE="1"
else
    read -r -p "اختر [1 أو 2] (الافتراضي 1): " USER_INPUT_CHOICE || USER_INPUT_CHOICE="1"
fi

if [ "$USER_INPUT_CHOICE" = "2" ]; then
    ENV_CHOICE="2"
fi

if [ "$ENV_CHOICE" = "1" ]; then
    echo "[*] تهيئة البيئة الافتراضية (.venv)..."
    if [ ! -d ".venv" ]; then
        python3 -m venv .venv
    fi
    source .venv/bin/activate
    echo "[*] جاري تحديث pip وتثبيت المتطلبات داخل البيئة الافتراضية..."
    pip install --upgrade pip 2>/dev/null || true
    pip install -r requirements.txt
    USE_VENV_MSG=1
else
    echo "[*] جاري تثبيت حزم بايثون مباشرة في بيئة النظام العامة..."
    PIP_EXTRA_ARGS=""
    if python3 -m pip install --help 2>&1 | grep -q -- '--break-system-packages'; then
        PIP_EXTRA_ARGS="--break-system-packages"
    fi
    python3 -m pip install --upgrade pip $PIP_EXTRA_ARGS 2>/dev/null || true
    python3 -m pip install -r requirements.txt $PIP_EXTRA_ARGS
    USE_VENV_MSG=0
fi

# 3. إعداد الصلاحيات
echo "[*] إعداد صلاحيات التشغيل..."
chmod +x ai_hub.py bin/groq run.sh setup_venv.sh 2>/dev/null || true

# 4. إعداد الرابط الرمزي (Symlink) لأداة groq
if [ -n "$BIN_DIR" ] && [ -d "$BIN_DIR" ]; then
    ln -sf "$SCRIPT_DIR/bin/groq" "$BIN_DIR/groq"
    echo "[+] تم ربط أداة groq في: $BIN_DIR/groq"
    if [[ ":$PATH:" != *":$BIN_DIR:"* ]]; then
        echo "[!] تنبيه: يرجى إضافة $BIN_DIR إلى مسار PATH إذا لم يكن مضافاً."
    fi
fi

# 5. إعداد ملف .env إن لم يكن موجوداً
if [ ! -f "config/.env" ] && [ -f "config/.env.example" ]; then
    cp config/.env.example config/.env
    echo "[+] تم إنشاء ملف config/.env من النموذج"
fi

echo "=========================================================="
echo " [✓] اكتمل التثبيت بنجاح!"
if [ "$USE_VENV_MSG" = "1" ]; then
    echo " 💡 تم التثبيت داخل بيئة افتراضية معزولة (.venv)"
    echo " لتشغيل البرنامج مباشرة (يقوم بتفعيل البيئة تلقائياً):"
    echo "   ./run.sh"
    echo " أو تفعيل البيئة يدوياً:"
    echo "   source .venv/bin/activate && python3 ai_hub.py"
else
    echo " لتشغيل لوحة التحكم الرئيسية:"
    echo "   ./ai_hub.py   أو   python3 ai_hub.py"
fi
echo " لتشغيل أداة الذكاء الاصطناعي المباشرة:"
echo "   groq --help"
echo "=========================================================="
