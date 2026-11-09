#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
==============================================================================
 🧪 وحدة مفسر الأكواد المعزول ومحرك الـ Sandbox (OpenSandbox Engine)
 يدعم الاتصال بخادم OpenSandbox الحقيقي أو المشغل المحلي الآمن المعزول (Fallback)
==============================================================================
"""

import os
import re
import sys
import time
import shutil
import tempfile
import subprocess
from typing import Dict, Any, Tuple, List, Optional

# التحقق من توفر مكتبة opensandbox الرسمية
try:
    import opensandbox
    from opensandbox import Sandbox
    from opensandbox.config import ConnectionConfig
    OPENSANDBOX_SDK_AVAILABLE = True
except ImportError:
    opensandbox = None
    OPENSANDBOX_SDK_AVAILABLE = False


def get_sandbox_config() -> Dict[str, Any]:
    """قراءة إعدادات OpenSandbox من البيئة أو القيم الافتراضية."""
    endpoint = os.getenv("OPENSANDBOX_ENDPOINT", "http://localhost:8080").strip()
    api_key = os.getenv("OPENSANDBOX_API_KEY", "").strip()
    timeout = int(os.getenv("OPENSANDBOX_TIMEOUT", "45"))
    return {
        "endpoint": endpoint,
        "api_key": api_key,
        "timeout": timeout,
        "sdk_installed": OPENSANDBOX_SDK_AVAILABLE,
    }


def check_sandbox_server(endpoint: str = None) -> Tuple[bool, str]:
    """فحص الاتصال بسيرفر OpenSandbox."""
    if not endpoint:
        cfg = get_sandbox_config()
        endpoint = cfg["endpoint"]

    if not endpoint or endpoint.lower() in ["none", "disabled", "off"]:
        return False, "معطل يدويًا (الاعتماد على المشغل المحلي المعزول)"

    import urllib.request
    try:
        # اختبار ping سريع مع مهلة ثانية واحدة
        test_url = endpoint.rstrip("/")
        if not test_url.startswith("http"):
            test_url = f"http://{test_url}"
        
        req = urllib.request.Request(f"{test_url}/health", headers={"User-Agent": "AlManara-DevHub"})
        with urllib.request.urlopen(req, timeout=1.5) as resp:
            if resp.status in [200, 204]:
                return True, f"متصل بسيرفر OpenSandbox ({test_url})"
    except Exception:
        pass

    return False, "الخادم غير متصل (المشغل المحلي المعزول نشط)"


def extract_code_blocks(text: str) -> List[Tuple[str, str]]:
    """استخراج كتل الأكواد البرمجية ولغتها من نصوص الذكاء الاصطناعي."""
    pattern = r"```([a-zA-Z0-9_\-\+]*)\n(.*?)```"
    matches = re.findall(pattern, text, re.DOTALL)
    blocks = []
    for lang, code in matches:
        lang = lang.strip().lower() or "python"
        blocks.append((lang, code.strip()))
    return blocks


def run_code_isolated_local(code: str, language: str = "python", timeout: int = 30) -> Dict[str, Any]:
    """
    مشغل محلي آمن ومعزول (Local Ephemeral Sandbox):
    - بيئة تشغيل مؤقتة تنشأ وتُحذف فوراً في مجلد Temp معزول.
    - تطهير وتجريد متغيرات البيئة الحساسة (مثل مفاتيح API ورموز GitHub) لمنع تسريبها.
    - تحديد مدة التنفيذ لحماية موارد المعالج والذاكرة.
    """
    lang = language.lower()
    
    # تحديد مسار وبيئة معزولة
    with tempfile.TemporaryDirectory(prefix="manara_sandbox_") as tmp_dir:
        # بيئة بدون مفاتيح حساسة
        clean_env = {
            "PATH": os.environ.get("PATH", "/usr/bin:/bin"),
            "HOME": tmp_dir,
            "TMPDIR": tmp_dir,
            "LANG": "en_US.UTF-8",
            "PYTHONIOENCODING": "utf-8",
        }

        file_name = "script.py" if lang in ["python", "py"] else "script.sh"
        script_path = os.path.join(tmp_dir, file_name)

        with open(script_path, "w", encoding="utf-8") as f:
            f.write(code)

        if lang in ["python", "py"]:
            cmd = [sys.executable, "-u", script_path]
        elif lang in ["bash", "sh"]:
            cmd = ["bash", script_path]
        else:
            return {
                "success": False,
                "stdout": "",
                "stderr": f"اللغة غير مدعومة في المشغل المحلي: {lang}",
                "exit_code": 1,
                "runtime_sec": 0,
                "mode": "local_fallback"
            }

        start_time = time.time()
        try:
            res = subprocess.run(
                cmd,
                cwd=tmp_dir,
                env=clean_env,
                capture_output=True,
                text=True,
                timeout=timeout
            )
            elapsed = round(time.time() - start_time, 2)
            return {
                "success": (res.returncode == 0),
                "stdout": res.stdout.strip(),
                "stderr": res.stderr.strip(),
                "exit_code": res.returncode,
                "runtime_sec": elapsed,
                "mode": "local_fallback"
            }
        except subprocess.TimeoutExpired:
            return {
                "success": False,
                "stdout": "",
                "stderr": f"انتهت المهلة الزمنية المحددة للتنفيذ ({timeout} ثانية). تم إيقاف الكود أماناً.",
                "exit_code": 124,
                "runtime_sec": timeout,
                "mode": "local_fallback"
            }
        except Exception as e:
            return {
                "success": False,
                "stdout": "",
                "stderr": f"خطأ أثناء تشغيل البيئة المعزولة: {str(e)}",
                "exit_code": 1,
                "runtime_sec": 0,
                "mode": "local_fallback"
            }


def execute_in_sandbox(code: str, language: str = "python", timeout: int = 30) -> Dict[str, Any]:
    """
    الواجهة الموحدة لتنفيذ الأكواد:
    تحاول التنفيذ عبر سيرفر OpenSandbox إن وُجد، أو ترجع إلى المشغل المحلي الآمن تلقائياً.
    """
    cfg = get_sandbox_config()
    is_server_alive, server_msg = check_sandbox_server(cfg["endpoint"])

    # 1. التنفيذ عبر OpenSandbox Server إذا كان متاحاً
    if is_server_alive and OPENSANDBOX_SDK_AVAILABLE:
        try:
            import asyncio
            from opensandbox.config import ConnectionConfig

            async def _run_remote():
                c_cfg = ConnectionConfig(
                    domain=cfg["endpoint"].replace("http://", "").replace("https://", ""),
                    api_key=cfg["api_key"] or None
                )
                sb = await Sandbox.create("python:3.11-slim", connection_config=c_cfg)
                try:
                    res = await sb.commands.run(f"python3 -c {repr(code)}")
                    stdout = "\n".join(log.text for log in res.logs.stdout)
                    stderr = "\n".join(log.text for log in res.logs.stderr)
                    return {
                        "success": (res.exit_code == 0),
                        "stdout": stdout.strip(),
                        "stderr": stderr.strip(),
                        "exit_code": res.exit_code,
                        "mode": "opensandbox_server"
                    }
                finally:
                    await sb.destroy()

            return asyncio.run(_run_remote())
        except Exception as e:
            # التراجع التلقائي للمشغل المحلي في حال حدوث خطأ أثناء الاتصال بالخادم
            pass

    # 2. المشغل المحلي المعزول (Default Local Safe Fallback)
    return run_code_isolated_local(code, language=language, timeout=timeout)
