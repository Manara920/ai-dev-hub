#!/usr/bin/env bash
# ==============================================================================
# 🏮 مشغل AI Dev Hub Pro السريع (تفعيل تلقائي للبيئة الافتراضية)
# ==============================================================================

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

if [ -f "$SCRIPT_DIR/.venv/bin/activate" ]; then
    source "$SCRIPT_DIR/.venv/bin/activate"
fi

exec python3 "$SCRIPT_DIR/ai_hub.py" "$@"
