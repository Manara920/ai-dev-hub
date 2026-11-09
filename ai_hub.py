#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
==============================================================================
 🏮 Al-Manara AI Dev Hub Pro - المنارة كريبتو
 محطة المطور والذكاء الاصطناعي الموحدة (Local & Cloud & GitHub)
 إصدار 2.3.0 - دعم تمييز النماذج السحابية، المحرك الموصى به، وتوجيهات AirLLM & venv
==============================================================================
"""

import os
import sys
import json
import shutil
import argparse
import subprocess
import platform
import urllib.request
from pathlib import Path

VERSION = "2.3.0"

# إعداد المسارات
ROOT_DIR = Path(__file__).resolve().parent
CONFIG_DIR = ROOT_DIR / "config"
CONFIG_FILE = CONFIG_DIR / "models.json"
CATALOG_FILE = CONFIG_DIR / "models_catalog.json"
BRAND_FILE = CONFIG_DIR / "brand.json"
ENV_FILE = CONFIG_DIR / ".env"

# Rich Library support
try:
    from rich.console import Console
    from rich.table import Table
    from rich.panel import Panel
    from rich.markdown import Markdown
    from rich.text import Text
    from rich.progress import Progress, BarColumn, DownloadColumn, TransferSpeedColumn, TimeRemainingColumn
    USE_RICH = True
    console = Console()
except ImportError:
    USE_RICH = False
    console = None

def clear_screen():
    if USE_RICH and console:
        console.clear()
    else:
        os.system("cls" if os.name == "nt" else "clear")

def safe_input(prompt=""):
    try:
        if USE_RICH and console:
            return console.input(prompt)
        return input(prompt)
    except (KeyboardInterrupt, EOFError):
        print("\nمع السلامة!")
        sys.exit(0)

def load_json(file_path):
    if file_path.exists():
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    return {}

CONFIG = load_json(CONFIG_FILE)
BRAND = load_json(BRAND_FILE)
CATALOG = load_json(CATALOG_FILE) if CATALOG_FILE.exists() else []

def load_env():
    env_vars = {}
    if ENV_FILE.exists():
        with open(ENV_FILE, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    k, v = line.split("=", 1)
                    k = k.strip()
                    v = v.strip().strip('"').strip("'")
                    env_vars[k] = v
                    if k not in os.environ:
                        os.environ[k] = v
    return env_vars

ENV_VARS = load_env()

def get_provider_key(provider_key_name):
    return os.getenv(provider_key_name) or ENV_VARS.get(provider_key_name)

def get_local_models_dir():
    custom_path = os.getenv("LOCAL_MODELS_PATH") or ENV_VARS.get("LOCAL_MODELS_PATH")
    if custom_path:
        p = Path(custom_path).expanduser()
        p.mkdir(parents=True, exist_ok=True)
        return p
    for fallback in [Path("/storage/emulated/0/LLM's"), Path.home() / "models", Path.home() / "LLMs"]:
        if fallback.exists() and fallback.is_dir():
            return fallback
    default_dir = Path.home() / "models"
    default_dir.mkdir(parents=True, exist_ok=True)
    return default_dir

def get_current_git_user():
    try:
        res = subprocess.run(["gh", "api", "user", "--jq", ".login"], cwd=str(ROOT_DIR), capture_output=True, text=True, timeout=3)
        if res.returncode == 0 and res.stdout.strip():
            return res.stdout.strip()
    except Exception:
        pass
    try:
        res = subprocess.run(["git", "config", "user.name"], cwd=str(ROOT_DIR), capture_output=True, text=True, timeout=2)
        if res.returncode == 0 and res.stdout.strip():
            return res.stdout.strip()
    except Exception:
        pass
    return "User"

# ==============================================================================
# 🧠 وحدة الفحص العتادي والتشخيص الذكي (Hardware Profiler & Recommender)
# ==============================================================================

def detect_hardware():
    """فحص مواصفات الجهاز بدقة عالية دون الحاجة لمكتبات ثقيلة."""
    ram_total_gb = 0.0
    ram_avail_gb = 0.0
    
    # 1. فحص RAM عبر /proc/meminfo في لينكس وأندرويد
    try:
        if os.path.exists("/proc/meminfo"):
            mem = {}
            with open("/proc/meminfo", "r", encoding="utf-8") as f:
                for line in f:
                    parts = line.split(":")
                    if len(parts) == 2:
                        mem[parts[0].strip()] = int(parts[1].strip().split()[0])
            ram_total_gb = mem.get("MemTotal", 0) / (1024 * 1024)
            ram_avail_gb = mem.get("MemAvailable", mem.get("MemFree", 0)) / (1024 * 1024)
    except Exception:
        pass

    # في حال فشل قراءة /proc نستخدم psutil إن كان متوفراً
    if ram_total_gb == 0.0:
        try:
            import psutil
            vm = psutil.virtual_memory()
            ram_total_gb = vm.total / (1024**3)
            ram_avail_gb = vm.available / (1024**3)
        except Exception:
            ram_total_gb = 4.0
            ram_avail_gb = 2.0

    # 2. فحص المساحة المتبقية للتحميل
    models_dir = get_local_models_dir()
    try:
        usage = shutil.disk_usage(models_dir)
        disk_free_gb = usage.free / (1024**3)
    except Exception:
        disk_free_gb = 10.0

    # 3. المعمارية وعدد الأنوية ونظام التشغيل
    arch = platform.machine()
    cores = os.cpu_count() or 4
    is_proot = os.path.exists("/.proot") or os.environ.get("PROOT_TMP_DIR") is not None or os.path.exists("/etc/os-release")
    is_termux = ("com.termux" in os.environ.get("PREFIX", "") or "com.termux" in sys.executable) and not is_proot

    # 4. محركات التشغيل المتوفرة
    has_llama = shutil.which("llama-cli") is not None
    has_airllm = shutil.which("airllm") is not None
    try:
        import airllm
        has_airllm_py = True
    except ImportError:
        has_airllm_py = False

    # 5. تصنيف فئة الجهاز واقتراح الحد الأقصى للمعاملات
    if ram_total_gb < 3.5:
        tier = "low"
        tier_title = "محدود الموارد (0.5B - 1.5B)"
        rec_size = "1.0 - 1.5 GB"
    elif ram_total_gb < 7.0:
        tier = "medium"
        tier_title = "متوسط (3B - 4B)"
        rec_size = "2.0 - 3.5 GB"
    elif ram_total_gb < 14.0:
        tier = "high"
        tier_title = "قوي (7B - 9B)"
        rec_size = "4.5 - 6.0 GB"
    else:
        tier = "ultra"
        tier_title = "فائق (14B - 32B / 70B AirLLM)"
        rec_size = "8.0 - 16.0+ GB"

    return {
        "ram_total_gb": round(ram_total_gb, 1),
        "ram_avail_gb": round(ram_avail_gb, 1),
        "disk_free_gb": round(disk_free_gb, 1),
        "arch": arch,
        "cores": cores,
        "is_termux": is_termux,
        "has_llama": has_llama,
        "has_airllm": has_airllm or has_airllm_py,
        "tier": tier,
        "tier_title": tier_title,
        "rec_size": rec_size,
    }

def get_recommended_models():
    """جلب النماذج المتوافقة مع عتاد الجهاز الحالي."""
    hw = detect_hardware()
    catalog = load_json(CATALOG_FILE) if CATALOG_FILE.exists() else []
    if not catalog:
        return []
    
    recommended = []
    for m in catalog:
        # فحص هل يكفي الرام ومساحة القرص
        min_ram = m.get("min_ram_gb", 3.0)
        size_gb = m.get("size_gb", 2.0)
        
        fit = True
        status_note = "مناسب جداً"
        if hw["ram_total_gb"] < min_ram:
            fit = False
            status_note = "يحتاج ذاكرة RAM أكبر"
        elif hw["disk_free_gb"] < size_gb * 1.3:
            fit = False
            status_note = "المساحة التخزينية غير كافية"
        
        m_copy = dict(m)
        m_copy["is_fit"] = fit
        m_copy["note"] = status_note
        recommended.append(m_copy)
        
    return recommended

# ==============================================================================
# 📥 وحدة التنزيل من Hugging Face (Direct Resumable Downloader)
# ==============================================================================

def download_file_with_progress(url, dest_path):
    """تنزيل ملف مع شريط تقدم ودعم استئناف التحميل تلقائياً."""
    dest = Path(dest_path)
    part_path = dest.with_name(dest.name + ".part")
    
    existing_bytes = 0
    if part_path.exists():
        existing_bytes = part_path.stat().st_size

    req = urllib.request.Request(url, headers={
        "User-Agent": "Mozilla/5.0 (Al-Manara AI Dev Hub Pro)",
    })
    if existing_bytes > 0:
        req.add_header("Range", f"bytes={existing_bytes}-")

    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            total_bytes = resp.headers.get("Content-Length")
            if total_bytes:
                total_bytes = int(total_bytes) + existing_bytes
            else:
                total_bytes = 0

            mode = "ab" if existing_bytes > 0 else "wb"
            
            if USE_RICH and console and total_bytes > 0:
                with Progress(
                    "[bold green]{task.description}",
                    BarColumn(bar_width=None, style="cyan", complete_style="bold green"),
                    DownloadColumn(),
                    TransferSpeedColumn(),
                    TimeRemainingColumn(),
                    console=console
                ) as progress:
                    task = progress.add_task(f"📥 تحميل {dest.name}", total=total_bytes, completed=existing_bytes)
                    with open(part_path, mode) as f:
                        while True:
                            chunk = resp.read(1024 * 512) # 512 KB
                            if not chunk:
                                break
                            f.write(chunk)
                            progress.update(task, advance=len(chunk))
            else:
                print(f"[*] جاري تحميل {dest.name} (حجم تقريبي: {total_bytes / (1024*1024):.1f} MB)...")
                with open(part_path, mode) as f:
                    downloaded = existing_bytes
                    while True:
                        chunk = resp.read(1024 * 512)
                        if not chunk:
                            break
                        f.write(chunk)
                        downloaded += len(chunk)
                        if total_bytes > 0:
                            pct = (downloaded / total_bytes) * 100
                            sys.stdout.write(f"\r  - التقدم: {pct:.1f}% ({downloaded / (1024*1024):.1f} MB)")
                            sys.stdout.flush()
                print()

        part_path.rename(dest)
        return True, "تم التحميل بنجاح"
    except urllib.error.HTTPError as e:
        if e.code == 416: # Range not satisfiable, file already complete
            if part_path.exists():
                part_path.rename(dest)
            return True, "الملف مكتمل بالفعل"
        return False, f"خطأ HTTP {e.code}: {e.reason}"
    except Exception as e:
        return False, str(e)

def download_manager_menu():
    """واجهة مستكشف وتنزيل النماذج من Hugging Face."""
    while True:
        clear_screen()
        hw = detect_hardware()
        models = get_recommended_models()

        if USE_RICH:
            # بطاقة العتاد
            h_text = Text(f"📥 مستكشف ومُنزل النماذج من Hugging Face", style="bold green")
            sub_text = Text(
                f"💻 جهازك: {hw['ram_total_gb']} GB RAM (متاح: {hw['ram_avail_gb']} GB) | "
                f"قرص متاح: {hw['disk_free_gb']} GB | المعمارية: {hw['arch']} | الفئة: {hw['tier_title']}",
                style="dim white"
            )
            console.print(Panel(Text.assemble(h_text, "\n", sub_text), border_style="green"))

            tbl = Table(title="🌟 النماذج الموصى بها لجهازك (مكممة وجاهزة للتشغيل)", border_style="cyan", header_style="bold cyan")
            tbl.add_column("#", justify="center", style="bold yellow", width=4)
            tbl.add_column("النموذج والمحرك المقترح", style="white")
            tbl.add_column("الحجم", justify="center", style="cyan", width=10)
            tbl.add_column("التوافق مع جهازك", justify="center", width=22)

            for i, m in enumerate(models, 1):
                if m["engine"] == "llama.cpp":
                    eng_badge = "[bold green]⚡ llama.cpp[/bold green] [dim](محلي/Termux)[/dim]"
                else:
                    eng_badge = "[bold magenta]🧠 AirLLM[/bold magenta] [bold yellow](يحتاج Linux PRoot)[/bold yellow]"

                if m["is_fit"]:
                    fit_style = "[bold green]✅ مثالي لجهازك[/bold green]"
                else:
                    fit_style = f"[dim red]⚠️ {m['note']}[/dim red]"

                model_cell = f"[bold cyan]{m['name']}[/bold cyan]  {eng_badge}\n[dim]{m['desc']}[/dim]"
                tbl.add_row(str(i), model_cell, f"{m['size_gb']} GB", fit_style)
            
            console.print(tbl)
            console.print("[dim]• يمكنك تنزيل أي نموذج بالرقم، أو كتابة [bold yellow]S[/bold yellow] للبحث في Hugging Face عن أي نموذج GGUF آخر.[/dim]")
            console.print("[bold yellow][0][/bold yellow] رجوع للقائمة الرئيسية")
            choice = safe_input("\nاختر رقم النموذج للتحميل أو [S للبحث] ❯ ").strip()
        else:
            print("\n=== 📥 مستكشف وتنزيل النماذج ===")
            print(f"العتاد: {hw['ram_total_gb']} GB RAM | قرص: {hw['disk_free_gb']} GB | الفئة: {hw['tier_title']}")
            for i, m in enumerate(models, 1):
                status = "✅ متوافق" if m["is_fit"] else f"⚠️ {m['note']}"
                eng_note = "llama.cpp (محلي)" if m["engine"] == "llama.cpp" else "AirLLM (Linux PRoot)"
                print(f" [{i}] {m['name']} | المحرك: {eng_note} ({m['size_gb']} GB) -> {status}")
            print(" [S] بحث مخصص في Hugging Face")
            print(" [0] رجوع")
            choice = safe_input("اختر ❯ ").strip()

        if choice == "0":
            break
        elif choice.lower() == "s":
            search_huggingface_custom()
        elif choice.isdigit() and 1 <= int(choice) <= len(models):
            chosen = models[int(choice) - 1]
            repo_id = chosen["repo"]
            filename = chosen["preferred_file"]
            models_dir = get_local_models_dir()
            dest_file = models_dir / filename
            
            if dest_file.exists():
                print(f"\n[✓] النموذج موجود بالفعل في: {dest_file}")
                safe_input("\nاضغط Enter للمتابعة...")
                continue

            dl_url = f"https://huggingface.co/{repo_id}/resolve/main/{filename}"
            print(f"\n[*] جاري بدء تنزيل: {chosen['name']}")
            print(f"[*] المستودع: https://huggingface.co/{repo_id}")
            print(f"[*] مسار الحفظ: {dest_file}")
            if chosen.get("engine") == "airllm":
                if USE_RICH:
                    console.print(Panel(
                        "[bold yellow]⚠️ ملاحظة هامة حول نموذج AirLLM:[/bold yellow]\n"
                        "هذا النموذج يعمل بمحرك [bold magenta]AirLLM[/bold magenta] الذي يتطلب بيئة [bold cyan]Linux (proot-distro / Ubuntu)[/bold cyan].\n"
                        "لا يمكن تشغيل AirLLM مباشرة في تيرمكس الخام، بل يتم الدخول للبيئة أولاً لتشغيله.",
                        border_style="yellow", title="تنبيه المحرك"
                    ))
                else:
                    print("\n[!] تنبيه: هذا النموذج مخصص لمحرك AirLLM ويتطلب بيئة Linux (proot-distro) لتشغيله في Termux.")
            
            confirm = safe_input("تأكيد بدء التحميل؟ [Y/n]: ").strip().lower()
            if confirm in ["", "y", "yes"]:
                ok, msg = download_file_with_progress(dl_url, dest_file)
                if ok:
                    print(f"\n[✓] تم تحميل النموذج بنجاح وهو الآن متاح فوراً في قائمة النماذج المحلية!")
                else:
                    print(f"\n[-] فشل التحميل: {msg}")
                safe_input("\nاضغط Enter للمتابعة...")

def search_huggingface_custom():
    """بحث حي ومباشر في Hugging Face عن أي نموذج GGUF وتنزيله."""
    clear_screen()
    print("=== 🔍 بحث مخصص في Hugging Face عن نماذج GGUF ===")
    query = safe_input("اكتب اسم النموذج أو الكلمة المفتاحية (مثال: qwen, mistral, deepseek): ").strip()
    if not query:
        return

    print(f"\n[*] جاري البحث في Hugging Face عن: {query} ...")
    url = f"https://huggingface.co/api/models?search={query}&filter=gguf&sort=downloads&direction=-1&limit=6"
    req = urllib.request.Request(url, headers={"User-Agent": "AlManara-AIDevHub/2.2.0"})
    
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read().decode())
    except Exception as e:
        print(f"[-] خطأ أثناء البحث: {e}")
        safe_input("\nاضغط Enter للمتابعة...")
        return

    if not data:
        print("[-] لم يتم العثور على أي نتائج مطابقة.")
        safe_input("\nاضغط Enter للمتابعة...")
        return

    print("\nالنتائج الأكثر تحميلاً في العالم:")
    for i, item in enumerate(data, 1):
        dl = item.get("downloads", 0)
        likes = item.get("likes", 0)
        print(f" {i}) {item.get('id')}  (⬇️ {dl:,} | ❤️ {likes})")
    print(" 0) إلغاء")

    c = safe_input("\nاختر رقم المستودع لعرض ملفات الـ GGUF المتاحة: ").strip()
    if not c.isdigit() or int(c) < 1 or int(c) > len(data):
        return

    chosen_repo = data[int(c) - 1].get("id")
    print(f"\n[*] فحص ملفات المستودع {chosen_repo} ...")
    tree_url = f"https://huggingface.co/api/models/{chosen_repo}/tree/main"
    tree_req = urllib.request.Request(tree_url, headers={"User-Agent": "AlManara-AIDevHub/2.2.0"})
    
    try:
        with urllib.request.urlopen(tree_req, timeout=10) as resp:
            files_data = json.loads(resp.read().decode())
    except Exception as e:
        print(f"[-] خطأ في جلب الملفات: {e}")
        safe_input("\nاضغط Enter للمتابعة...")
        return

    ggufs = [f for f in files_data if f.get("path", "").lower().endswith(".gguf") and not f.get("path", "").lower().startswith("mmproj")]
    if not ggufs:
        print("[-] لم يتم العثور على ملفات .gguf مباشرة في جذر هذا المستودع.")
        safe_input("\nاضغط Enter للمتابعة...")
        return

    print("\nالملفات المتوفرة للتحميل:")
    for j, gf in enumerate(ggufs, 1):
        size_gb = round(gf.get("size", 0) / (1024**3), 2)
        print(f" {j}) {gf.get('path')} ({size_gb} GB)")
    print(" 0) إلغاء")

    fc = safe_input("\nاختر رقم الملف للتحميل: ").strip()
    if not fc.isdigit() or int(fc) < 1 or int(fc) > len(ggufs):
        return

    target_file = ggufs[int(fc) - 1].get("path")
    dl_url = f"https://huggingface.co/{chosen_repo}/resolve/main/{target_file}"
    models_dir = get_local_models_dir()
    dest = models_dir / target_file

    print(f"\n[*] سيتم حفظ النموذج في: {dest}")
    ok, msg = download_file_with_progress(dl_url, dest)
    if ok:
        print(f"\n[✓] تم تنزيل {target_file} بنجاح!")
    else:
        print(f"\n[-] خطأ أثناء التنزيل: {msg}")
    safe_input("\nاضغط Enter للمتابعة...")

# ==============================================================================
# 💻 إدارة وتشغيل النماذج المحلية (Dual Engine: llama.cpp & AirLLM)
# ==============================================================================

def get_local_models():
    """كشف النماذج المحلية وتحديد محرك التشغيل الأنسب لكل منها."""
    models = []
    models_dir = get_local_models_dir()
    if models_dir.exists() and models_dir.is_dir():
        # نماذج GGUF لمحرك llama.cpp
        for f in sorted(models_dir.glob("*.gguf")):
            if not f.name.startswith("mmproj"):
                size_gb = f.stat().st_size / (1024 * 1024 * 1024)
                models.append({
                    "name": f.name,
                    "path": str(f),
                    "size": f"{size_gb:.1f} GB",
                    "engine": "llama.cpp",
                    "engine_label": "⚡ llama.cpp (سريع/محلي)"
                })
        # نماذج مجلدات Safetensors المخصصة لـ AirLLM
        for d in sorted(models_dir.iterdir()):
            if d.is_dir() and any(d.glob("*.safetensors")):
                total_size = sum(f.stat().st_size for f in d.glob("*.safetensors")) / (1024**3)
                models.append({
                    "name": d.name,
                    "path": str(d),
                    "size": f"{total_size:.1f} GB",
                    "engine": "airllm",
                    "engine_label": "🧠 AirLLM (طبقات / بيئة Linux)"
                })
    return models

def run_local_model_interactive(chosen):
    """تشغيل النموذج المحلي وفق محركه المخصص."""
    clear_screen()
    engine = chosen.get("engine", "llama.cpp")

    if engine == "llama.cpp":
        if not shutil.which("llama-cli"):
            print("\n[-] تنبيه: أداة 'llama-cli' غير متوفرة في مسار النظام (PATH).")
            print("    • على Termux: pkg install llama-cpp")
            print("    • على Linux/Ubuntu: قم بتثبيت حزمة llama.cpp أو بنائها.")
            safe_input("\nاضغط Enter للعودة...")
            return

        print("=" * 65)
        print(f"  ⚡ تشغيل النموذج: {chosen['name']}")
        print(f"  • المحرك: llama.cpp (Optimized Native C++)")
        print(f"  • المسار: {chosen['path']}")
        print("=" * 65)
        
        # كشف الأنوية لاختيار عدد threads مثالي
        cores = os.cpu_count() or 4
        threads = str(max(2, cores - 2))
        
        cmd = [
            "llama-cli", "-m", chosen["path"],
            "-t", threads, "-c", "2048", "-rea", "off", "--flash-attn", "on"
        ]
        try:
            subprocess.run(cmd)
        except Exception as e:
            print(f"[-] خطأ أثناء تشغيل llama.cpp: {e}")
        safe_input("\nاضغط Enter للعودة...")

    elif engine == "airllm":
        print("=" * 65)
        print(f"  🧠 تشغيل النموذج: {chosen['name']}")
        print(f"  • المحرك: AirLLM (Layer-wise Inference)")
        print(f"  • المسار: {chosen['path']}")
        print("=" * 65)

        # فحص هل البيئة الحالية Termux أصلية أم بيئة Linux
        is_termux = "com.termux" in os.environ.get("PREFIX", "") or "com.termux" in sys.executable
        in_proot = os.path.exists("/.proot") or os.environ.get("PROOT_TMP_DIR") is not None or (not is_termux and os.path.exists("/etc/os-release"))

        if is_termux and not in_proot:
            if USE_RICH:
                console.print(Panel(
                    "[bold red]⛔ تعذر تشغيل محرك AirLLM في بيئة Termux المباشرة[/bold red]\n\n"
                    "محرك AirLLM يعتمد على مكتبات [bold cyan]PyTorch[/bold cyan] و [bold cyan]Transformers[/bold cyan]، "
                    "ولا يمكن تثبيتها أو تشغيلها في تيرمكس مباشرة (بسبب قيود نظام أندرويد bionic libc).\n\n"
                    "[bold green]💡 للتشغيل بنجاح، يجب تشغيله من داخل بيئة Linux حقيقية على هاتفك عبر PRoot:[/bold green]\n"
                    "  1. تثبيت مدير توزيعات لينكس في تيرمكس:\n"
                    "     [bold yellow]pkg install proot-distro[/bold yellow]\n"
                    "  2. تثبيت توزيعة أوبونتو والدخول إليها:\n"
                    "     [bold yellow]proot-distro install ubuntu[/bold yellow]\n"
                    "     [bold yellow]proot-distro login ubuntu[/bold yellow]\n"
                    "  3. داخل بيئة Ubuntu ثبت بايثون ومكتبة airllm:\n"
                    "     [bold yellow]apt update && apt install python3 python3-pip git -y[/bold yellow]\n"
                    "     [bold yellow]pip install airllm transformers torch[/bold yellow]\n"
                    "  4. شغل هذا البرنامج ai_hub من داخل بيئة أوبونتو وسيعمل بكفاءة فائقة!",
                    border_style="red",
                    title="تنبيه بيئة التشغيل (Linux PRoot Required)"
                ))
            else:
                print("\n[-] تنبيه: AirLLM لا يثبت ولا يعمل مباشرة داخل بيئة Termux الأصلية.")
                print("    يجب تشغيله داخل بيئة Linux على تيرمكس عبر:")
                print("    1. pkg install proot-distro")
                print("    2. proot-distro install ubuntu && proot-distro login ubuntu")
                print("    3. pip install airllm")
                print("    ثم تشغيل البرنامج من داخل بيئة Ubuntu.")
            safe_input("\nاضغط Enter للعودة...")
            return

        # فحص هل مكتبة airllm مثبتة في بيئة لينكس
        try:
            import airllm
        except ImportError:
            print("\n[-] مكتبة AirLLM غير مثبتة في بيئة بايثون الحالية.")
            inst = safe_input("هل ترغب في تثبيت airllm الآن عبر pip؟ [Y/n]: ").strip().lower()
            if inst in ["", "y", "yes"]:
                subprocess.run([sys.executable, "-m", "pip", "install", "airllm", "transformers", "torch"])
                try:
                    import airllm
                except ImportError:
                    print("[-] تعذر استيراد airllm بعد التثبيت.")
                    safe_input("\nاضغط Enter للعودة...")
                    return
            else:
                return

        print("\n[*] جاري تحميل طبقات النموذج عبر AirLLM (قد يستغرق بضع لحظات للتهيئة)...")
        runner_code = f"""
import sys
from airllm import AutoModel
print('[*] تهيئة النموذج من: {chosen["path"]} ...')
model = AutoModel.from_pretrained('{chosen["path"]}')
print('[✓] النموذج جاهز! اكتب سؤالك واضغط Enter (اكتب exit للخروج):')
while True:
    try:
        q = input('\\nأنت ❯ ')
        if not q or q.lower() in ['exit', 'q']:
            break
        print('\\nالنموذج ❯ ', end='', flush=True)
        input_text = [q]
        input_tokens = model.tokenizer(input_text, return_tensors='pt', return_attention_mask=False, truncation=True, max_length=2048)
        generation_output = model.generate(input_tokens['input_ids'].cuda() if False else input_tokens['input_ids'], max_new_tokens=256, use_cache=True, return_dict_in_generate=True)
        output = model.tokenizer.decode(generation_output.sequences[0])
        print(output)
    except (KeyboardInterrupt, EOFError):
        break
"""
        try:
            subprocess.run([sys.executable, "-c", runner_code])
        except Exception as e:
            print(f"[-] حدث خطأ أثناء تشغيل AirLLM: {e}")
        safe_input("\nاضغط Enter للعودة...")

def local_models_menu():
    """واجهة مخصصة ومرتبة للنماذج المحلية فقط."""
    while True:
        clear_screen()
        models = get_local_models()

        if USE_RICH:
            console.print(Panel(Text("💻 النماذج المحلية المثبتة على جهازك (Offline)", style="bold green"), border_style="green"))
            tbl = Table(show_header=True, header_style="bold green", border_style="green")
            tbl.add_column("#", justify="center", style="bold yellow", width=4)
            tbl.add_column("اسم النموذج", style="white")
            tbl.add_column("الحجم", justify="center", style="cyan", width=10)
            tbl.add_column("محرك التشغيل", style="magenta", width=22)

            if models:
                for i, m in enumerate(models, 1):
                    tbl.add_row(str(i), m["name"], m["size"], m["engine_label"])
            else:
                tbl.add_row("-", "لم يتم العثور على نماذج محلية حتى الآن", "-", "-")

            console.print(tbl)
            console.print(
                "[bold green][D][/bold green] 📥 تنزيل نماذج جديدة من Hugging Face  |  "
                "[bold yellow][F][/bold yellow] 📂 فتح وتغيير مجلد النماذج  |  "
                "[bold red][0][/bold red] رجوع"
            )
            choice = safe_input("\nاختر رقم النموذج لتشغيله أو أمراً ❯ ").strip()
        else:
            print("\n=== 💻 النماذج المحلية ===")
            if models:
                for i, m in enumerate(models, 1):
                    print(f" [{i}] {m['name']} ({m['size']}) -> {m['engine_label']}")
            else:
                print(" [-] لا توجد نماذج محلية.")
            print("\n[D] تنزيل نماذج جديدة | [F] مسار النماذج | [0] رجوع")
            choice = safe_input("اختر ❯ ").strip()

        if choice == "0":
            break
        elif choice.lower() == "d":
            download_manager_menu()
        elif choice.lower() == "f":
            print(f"\n[*] المجلد الحالي: {get_local_models_dir()}")
            new_p = safe_input("أدخل المسار الجديد للنماذج (أو اضغط Enter للإبقاء): ").strip()
            if new_p:
                ENV_FILE.write_text(f'LOCAL_MODELS_PATH="{new_p}"\n', encoding="utf-8")
                os.environ["LOCAL_MODELS_PATH"] = new_p
                print("[✓] تم تحديث مسار النماذج بنجاح.")
                safe_input("اضغط Enter...")
        elif choice.isdigit() and 1 <= int(choice) <= len(models):
            run_local_model_interactive(models[int(choice) - 1])

# ==============================================================================
# ☁️ إدارة وتشغيل النماذج السحابية (Cloud Models)
# ==============================================================================

def get_all_cloud_models():
    cloud_list = []
    providers = CONFIG.get("providers", {})
    for p_key, p_data in providers.items():
        p_name = p_data.get("name", p_key)
        for m in p_data.get("models", []):
            cloud_list.append({
                "provider": p_key,
                "provider_name": p_name,
                "id": m["id"],
                "model_name": m["model_name"],
                "label": m["label"],
                "tier": m.get("tier", "غير محدد")
            })
    return cloud_list

def run_cloud_model(chosen):
    p_key = chosen["provider"]
    p_data = CONFIG.get("providers", {}).get(p_key, {})
    env_key = p_data.get("env_key")
    api_key = get_provider_key(env_key)

    if not api_key:
        print(f"\n[-] تنبيه: مفتاح [{env_key}] غير مسجل!")
        print(f"🔗 يمكنك جلبه من: {p_data.get('site_url')}")
        add_now = safe_input("\nهل ترغب في إدخال المفتاح الآن؟ [y/N]: ").strip().lower()
        if add_now == "y":
            add_api_key_prompt()
        return

    # Check if Groq can be run via standalone CLI
    if p_key == "groq":
        groq_bin = shutil.which("groq")
        cmd = [groq_bin] if groq_bin else [sys.executable, str(ROOT_DIR / "bin" / "groq")]
        try:
            subprocess.run(cmd + ["-m", chosen["model_name"]], cwd=str(ROOT_DIR))
            return
        except FileNotFoundError:
            pass

    print(f"\n[*] جاري فتح الاتصال بـ {chosen['label']} ...")
    try:
        from openai import OpenAI
    except ImportError:
        print("[*] تثبيت مكتبة الاتصال...")
        subprocess.run([sys.executable, "-m", "pip", "install", "openai"])
        from openai import OpenAI

    base_url = p_data.get("base_url")
    client = OpenAI(base_url=base_url, api_key=api_key)

    system_prompt = (
        "أنت مساعد برمجي ومهندس ذكي مدعوم من المنارة كريبتو (Al-Manara Crypto). "
        "قدم حلولاً متقدمة وأكواداً ممتازة ودقيقة مع خبرة بالبرمجة وتقنيات البلوكشين والتحليل التقني."
    )

    print("=" * 60)
    print(f"  ⚡ تم الاتصال بالنموذج: {chosen['label']}")
    print(f"  • المزود: {chosen['provider_name']}")
    print("  • اكتب رسالتك واضغط Enter. للخروج اكتب /exit أو q")
    print("=" * 60)

    history = [{"role": "system", "content": system_prompt}]
    while True:
        try:
            user_msg = safe_input("\nأنت ❯ ").strip()
            if not user_msg:
                continue
            if user_msg.lower() in ["/exit", "exit", "q"]:
                break

            history.append({"role": "user", "content": user_msg})
            print(f"\n{chosen['label'].split('(')[0].strip()} ❯ ", end="", flush=True)

            stream = client.chat.completions.create(
                model=chosen["model_name"],
                messages=history,
                stream=True
            )
            full = ""
            thinking = False
            for chunk in stream:
                if not getattr(chunk, "choices", None) or len(chunk.choices) == 0:
                    continue
                delta = chunk.choices[0].delta
                if not delta:
                    continue
                # DeepSeek R1 reasoning tokens
                reasoning = getattr(delta, "reasoning_content", None) or getattr(delta, "reasoning", None)
                if reasoning:
                    if not thinking:
                        print("\n[🧠 تفكير النموذج]: ", end="", flush=True)
                        thinking = True
                    sys.stdout.write(reasoning)
                    sys.stdout.flush()
                txt = getattr(delta, "content", None) or ""
                if txt:
                    if thinking:
                        print("\n[⚡ الإجابة]:\n", end="", flush=True)
                        thinking = False
                    sys.stdout.write(txt)
                    sys.stdout.flush()
                    full += txt
            print()
            history.append({"role": "assistant", "content": full})
        except (KeyboardInterrupt, EOFError):
            break
        except Exception as e:
            print(f"\n[-] خطأ في الاتصال: {e}")

def cloud_models_menu():
    """واجهة منسقة ومفروزة للنماذج السحابية."""
    while True:
        clear_screen()
        cloud_models = get_all_cloud_models()

        if USE_RICH:
            banner_text = Text.assemble(
                ("☁️ النماذج السحابية الفائقة (DeepSeek, Groq, Kimi, Claude)\n", "bold blue"),
                ("🟢 باقات مجانية بالكامل (Free)  |  💎 باقات مدفوعة (Paid)", "dim cyan")
            )
            console.print(Panel(banner_text, border_style="blue"))
            tbl = Table(show_header=True, header_style="bold blue", border_style="blue")
            tbl.add_column("#", justify="center", style="bold yellow", width=4)
            tbl.add_column("النموذج وميزاته", style="white")
            tbl.add_column("المزود (Provider)", style="cyan")
            tbl.add_column("الباقة والتكلفة", justify="center", width=22)

            for i, c in enumerate(cloud_models, 1):
                raw_tier = c.get("tier", "")
                if "مجاني" in raw_tier or "Free" in raw_tier:
                    tier_styled = f"[bold green]{raw_tier}[/bold green]"
                elif "مدفوع" in raw_tier or "Paid" in raw_tier:
                    tier_styled = f"[bold red]{raw_tier}[/bold red]"
                else:
                    tier_styled = f"[bold yellow]{raw_tier}[/bold yellow]"

                tbl.add_row(str(i), c["label"], c["provider_name"], tier_styled)

            console.print(tbl)
            console.print(
                "[bold yellow][K][/bold yellow] 🔑 إدارة مفاتيح الـ API  |  "
                "[bold cyan][H][/bold cyan] 📖 دليل الحصول على المفاتيح  |  "
                "[bold red][0][/bold red] رجوع"
            )
            choice = safe_input("\nاختر رقم النموذج للبدء أو أمراً ❯ ").strip()
        else:
            print("\n=== ☁️ النماذج السحابية (مجانية ومدفوعة) ===")
            for i, c in enumerate(cloud_models, 1):
                raw_tier = c.get("tier", "")
                tier_tag = "[FREE]" if ("مجاني" in raw_tier or "Free" in raw_tier) else "[PAID]"
                print(f" [{i}] {tier_tag} {c['label']} [{c['provider_name']}] ({raw_tier})")
            print("\n[K] إدارة المفاتيح | [H] دليل الـ API | [0] رجوع")
            choice = safe_input("اختر ❯ ").strip()

        if choice == "0":
            break
        elif choice.lower() == "k":
            add_api_key_prompt()
        elif choice.lower() == "h":
            show_api_guide()
        elif choice.isdigit() and 1 <= int(choice) <= len(cloud_models):
            run_cloud_model(cloud_models[int(choice) - 1])
            safe_input("\nاضغط Enter للمتابعة...")

# ==============================================================================
# 🔑 إدارة المفاتيح ودليل الربط والدعم
# ==============================================================================

def add_api_key_prompt():
    clear_screen()
    if USE_RICH:
        console.print(Panel(Text("🔑 إدارة وتحديث مفاتيح الـ API", style="bold yellow"), border_style="yellow"))
    
    providers = CONFIG.get("providers", {})
    p_keys = list(providers.keys())

    print("اختر المزود الذي تريد إضافة مفتاحه:")
    for i, pk in enumerate(p_keys, 1):
        p_info = providers[pk]
        status = "✅ مسجل" if get_provider_key(p_info.get("env_key")) else "❌ غير مسجل"
        print(f" {i}) {p_info.get('name')} [{p_info.get('env_key')}] -> {status}")
    print(" 0) رجوع")

    c = safe_input("\nاختر رقم المزود: ").strip()
    if not c.isdigit() or int(c) < 1 or int(c) > len(p_keys):
        return

    sel_p = p_keys[int(c) - 1]
    p_info = providers[sel_p]
    env_name = p_info.get("env_key")

    print(f"\n[*] الرابط: {p_info.get('site_url')}")
    print(f"[*] توجيه: {p_info.get('guide')}")
    val = safe_input(f"\nالصق قيمة {env_name}: ").strip()

    if val:
        lines = []
        if ENV_FILE.exists():
            lines = [l for l in ENV_FILE.read_text(encoding="utf-8").splitlines() if not l.startswith(f"{env_name}=")]
        lines.append(f'{env_name}="{val}"')
        ENV_FILE.write_text("\n".join(lines) + "\n", encoding="utf-8")
        ENV_VARS[env_name] = val
        os.environ[env_name] = val
        print("\n[✓] تم حفظ المفتاح بنجاح محلياً!")
        safe_input("اضغط Enter للمتابعة...")

def show_api_guide():
    clear_screen()
    guide_md = """
# 📖 دليل إعداد وربط المفاتيح (Setup Guide)

أهلاً بك في **Al-Manara AI Dev Hub**! 

---

### 1. 🌟 بوابة OpenRouter (الخيار الشامل الموصى به)
- **الموقع:** [https://openrouter.ai/keys](https://openrouter.ai/keys)
- **المزايا:** مفتاح واحد يمنحك وصولاً إلى:
  - **DeepSeek V3 و DeepSeek R1 مجاناً بالكامل (Free tier)**
  - نماذج **Kimi Moonshot**
  - نماذج **Claude 3.7 Sonnet** و **GPT-4o**
- **طريقة التفعيل:** أنشئ حساباً، انسخ المفتاح الذي يبدأ بـ `sk-or-`، وضعه في إدارة المفاتيح.

---

### 2. ⚡ Groq Cloud (أسرع استجابة في العالم)
- **الموقع:** [https://console.groq.com/keys](https://console.groq.com/keys)
- **المزايا:** مجاني وسريع جداً، ممتاز لنماذج **علّام 2** و **GPT-OSS 120B** و **Qwen 3.8 27B**.

---

### 3. 🇨🇳 منصة DeepSeek الرسمية المباشرة
- **الموقع:** [https://platform.deepseek.com/api_keys](https://platform.deepseek.com/api_keys)
- **المزايا:** رصيد تجريبي مجاني وأرخص تكلفة استعلام عالمياً.

---

### 💡 إدارة المفاتيح محلياً:
- تُحفظ مفاتيحك بأمان تام في ملف `config/.env` محمي بموجب `.gitignore`.
"""
    if USE_RICH:
        console.print(Markdown(guide_md))
    else:
        print(guide_md)
    safe_input("\nاضغط Enter للعودة...")

def show_donation_screen():
    clear_screen()
    wallets = BRAND.get("donation_wallets", {})
    comm = BRAND.get("community", {})

    if USE_RICH:
        title = Text("🪙 دعم وتطوير المشروع - المنارة كريبتو", style="bold gold1")
        sub = Text("إذا نال هذا المشروع استحسانك، يمكنك المساهمة في استمراره وتطويره عبر المحافظ الرقمية:", style="dim white")
        console.print(Panel(Text.assemble(title, "\n", sub), border_style="gold1", padding=(1, 2)))

        tbl = Table(title="💎 المحافظ الرقمية المعتمدة للدعم", border_style="yellow", header_style="bold yellow")
        tbl.add_column("العملة والشبكة", style="cyan", width=26)
        tbl.add_column("عنوان المحفظة (Address)", style="bold white")
        tbl.add_column("ملاحظات", style="dim green", width=28)

        for k, w in wallets.items():
            tbl.add_row(w.get("network", k), w.get("address", "-"), w.get("note", ""))
        console.print(tbl)

        c_table = Table(title="🌐 مجتمع وقنوات المنارة كريبتو", border_style="cyan", header_style="bold cyan")
        c_table.add_column("المنصة", style="yellow", width=16)
        c_table.add_column("الرابط المباشر", style="bold blue")
        c_table.add_row("الموقع الرسمي", comm.get("website", "-"))
        c_table.add_row("قناة تيليجرام", comm.get("telegram", "-"))
        c_table.add_row("منصة X (تويتر)", comm.get("twitter", "-"))
        console.print(c_table)
    else:
        print("\n=== 🪙 دعم وتطوير المشروع - المنارة كريبتو ===")
        for k, w in wallets.items():
            print(f"- {w.get('network', k)}: {w.get('address')}")
    
    safe_input("\nاضغط Enter للعودة...")

# ==============================================================================
# 🐙 أتمتة وتطوير GitHub
# ==============================================================================

def github_menu():
    git_user = get_current_git_user()
    while True:
        clear_screen()
        if USE_RICH:
            console.print(Panel(Text(f"🐙 إدارة وتطوير مستودعات GitHub (المستخدم: {git_user})", style="bold magenta"), border_style="magenta"))
            tbl = Table(show_header=True, header_style="bold magenta", border_style="magenta")
            tbl.add_column("الخيار", justify="center", style="bold yellow", width=8)
            tbl.add_column("العملية", style="white")
            tbl.add_column("الوصف", style="dim white")
            tbl.add_row("1", "قائمة المستودعات (List Repos)", "عرض المستودعات الخاصة بك على GitHub")
            tbl.add_row("2", "حالة الكود الحالي (Git Status)", "فحص التعديلات في المشروع الحالي")
            tbl.add_row("3", "مراجعة الكود بالذكاء الاصطناعي (AI Review)", "قراءة git diff وشرح التعديلات واقتراح Commit message")
            tbl.add_row("4", "رفع التعديلات (Auto Commit & Push)", "حفظ التغييرات ورفعها بضغطة زر مع الحماية")
            tbl.add_row("5", "استنساخ مستودع (Git Clone)", "سحب أي مستودع من حسابك إلى بيئتك")
            tbl.add_row("0", "رجوع للقائمة الرئيسية", "العودة للقائمة السابقة")
            console.print(tbl)
            choice = safe_input("[bold yellow]اختر العملية ❯ [/bold yellow]").strip()
        else:
            print(f"\n--- 🐙 قائمة GitHub ({git_user}) ---")
            print("1) عرض مستودعاتك | 2) حالة Git | 3) مراجعة AI | 4) Push | 5) Clone | 0) رجوع")
            choice = safe_input("اختر ❯ ").strip()

        if choice == "0":
            break
        elif choice == "1":
            if not shutil.which("gh"):
                print("[-] أداة gh (GitHub CLI) غير متوفرة في النظام.")
            else:
                try:
                    subprocess.run(["gh", "repo", "list", "--limit", "15"], cwd=str(ROOT_DIR))
                except Exception as e:
                    print(f"[-] خطأ: {e}")
            safe_input("\nاضغط Enter للمتابعة...")
        elif choice == "2":
            if not shutil.which("git"):
                print("[-] أداة git غير متوفرة في النظام.")
            else:
                try:
                    subprocess.run(["git", "status", "-s"], cwd=str(ROOT_DIR))
                except Exception as e:
                    print(f"[-] خطأ: {e}")
            safe_input("\nاضغط Enter للمتابعة...")
        elif choice == "3":
            if not shutil.which("git"):
                print("[-] أداة git غير متوفرة.")
                safe_input("\nاضغط Enter...")
                continue
            try:
                res = subprocess.run(["git", "diff"], cwd=str(ROOT_DIR), capture_output=True, text=True)
                diff_text = res.stdout.strip()
                if not diff_text:
                    res_st = subprocess.run(["git", "status", "-s"], cwd=str(ROOT_DIR), capture_output=True, text=True)
                    diff_text = res_st.stdout.strip()
            except Exception as e:
                print(f"[-] خطأ: {e}")
                safe_input("\nاضغط Enter...")
                continue

            if not diff_text:
                print("[-] لا توجد أي تعديلات غير محفوظة حالياً.")
            else:
                prompt = f"راجع هذه التعديلات واشرحها وقدم اقتراح commit message احترافي:\n```\n{diff_text}\n```"
                groq_bin = shutil.which("groq")
                cmd = [groq_bin] if groq_bin else [sys.executable, str(ROOT_DIR / "bin" / "groq")]
                try:
                    subprocess.run(cmd + ["-m", "allam-2-7b", prompt], cwd=str(ROOT_DIR))
                except Exception as e:
                    print(f"[-] خطأ أثناء تشغيل مراجعة الكود: {e}")
            safe_input("\nاضغط Enter للمتابعة...")
        elif choice == "4":
            if not shutil.which("git"):
                print("[-] أداة git غير متوفرة.")
                safe_input("\nاضغط Enter...")
                continue
            try:
                st = subprocess.run(["git", "status", "--porcelain"], cwd=str(ROOT_DIR), capture_output=True, text=True)
                sensitive_patterns = [".env", ".key", ".token", ".pem", ".gguf"]
                risky = [line[3:].strip() for line in st.stdout.splitlines() if any(p in line[3:] for p in sensitive_patterns)]
                if risky:
                    print(f"[-] تنبيه أمني خطير: تم اكتشاف ملفات حساسة ({', '.join(risky)})!")
                    safe_input("\nاضغط Enter للعودة...")
                    continue
            except Exception as e:
                pass

            msg = safe_input("\nاكتب رسالة الـ Commit: ").strip() or "Update codebase"
            try:
                subprocess.run(["git", "add", "."], cwd=str(ROOT_DIR))
                subprocess.run(["git", "commit", "-m", msg], cwd=str(ROOT_DIR))
                subprocess.run(["git", "push"], cwd=str(ROOT_DIR))
            except Exception as e:
                print(f"[-] خطأ: {e}")
            safe_input("\nاضغط Enter للمتابعة...")
        elif choice == "5":
            repo_name = safe_input("\nاسم المستودع المطلوب استنساخه: ").strip()
            if repo_name and shutil.which("gh"):
                try:
                    subprocess.run(["gh", "repo", "clone", repo_name], cwd=str(ROOT_DIR))
                except Exception as e:
                    print(f"[-] خطأ: {e}")
            safe_input("\nاضغط Enter للمتابعة...")

# ==============================================================================
# 🛠️ الفحص والتشخيص الشامل
# ==============================================================================

def cli_check():
    hw = detect_hardware()
    issues = 0
    print("==========================================================")
    print(" 🏮 Al-Manara AI Dev Hub Pro - فحص بيئة العمل والتشخيص")
    print("==========================================================")

    print("\n[1] فحص مواصفات العتاد (Hardware Profiler):")
    print(f"  • الذاكرة العشوائية (RAM): {hw['ram_total_gb']} GB (متاح حالياً: {hw['ram_avail_gb']} GB)")
    print(f"  • مساحة القرص المتبقية للنماذج: {hw['disk_free_gb']} GB")
    print(f"  • المعمارية والمعالج: {hw['arch']} ({hw['cores']} أنوية)")
    print(f"  • فئة الجهاز المقدرة: {hw['tier_title']}")

    print("\n[2] فحص محركات التشغيل في النظام:")
    tools = [
        ("python3", "مفسر بايثون", True),
        ("git", "أداة Git لإدارة الإصدارات", False),
        ("gh", "GitHub CLI لأتمتة المستودعات", False),
        ("llama-cli", "محرك تشغيل GGUF (llama.cpp)", False),
    ]
    for b, desc, req in tools:
        found = shutil.which(b)
        if found:
            print(f"  [✓] {b:<10} ({desc}): متوفر في {found}")
        else:
            tag = "[✗]" if req else "[-]"
            print(f"  {tag} {b:<10} ({desc}): غير متوفر")
            if req:
                issues += 1

    # Check AirLLM
    if hw["has_airllm"]:
        print("  [✓] airllm     (محرك تشغيل الطبقات Safetensors): متوفر")
    else:
        if hw.get("is_termux", False):
            print("  [-] airllm     (محرك تشغيل الطبقات Safetensors): غير مثبت (يتطلب بيئة Linux PRoot على Termux)")
        else:
            print("  [-] airllm     (محرك تشغيل الطبقات Safetensors): غير مثبت (يمكن تثبيته عبر pip install airllm)")

    # Check Groq
    if shutil.which("groq") or (ROOT_DIR / "bin" / "groq").exists():
        print("  [✓] groq       (أداة Groq السحابية السريعة): متوفرة")

    print("\n[3] فحص مفاتيح الـ API المسجلة:")
    keys = ["GROQ_API_KEY", "OPENROUTER_API_KEY", "DEEPSEEK_API_KEY", "MOONSHOT_API_KEY"]
    for k in keys:
        v = get_provider_key(k)
        if v:
            masked = v[:4] + "..." + v[-4:] if len(v) > 8 else "***"
            print(f"  [✓] {k:<20}: مسجل ({masked})")
        else:
            print(f"  [-] {k:<20}: غير مسجل")

    models_dir = get_local_models_dir()
    ggufs = list(models_dir.glob("*.gguf")) if models_dir.exists() else []
    print(f"\n[4] مجلد النماذج المحلية: {models_dir} (يحتوي على {len(ggufs)} نموذج جاهز)")

    print("\n" + "=" * 58)
    if issues == 0:
        print(" [✓] التشخيص اكتمل: البيئة الأساسية ممتازة وجاهزة للعمل.")
    else:
        print(f" [-] التشخيص اكتمل مع وجود {issues} ملاحظة.")
    print("==========================================================")

def cli_list():
    hw = detect_hardware()
    local_models = get_local_models()
    cloud_models = get_all_cloud_models()

    print(f"=== العتاد: {hw['ram_total_gb']} GB RAM | قرص متاح: {hw['disk_free_gb']} GB | {hw['tier_title']} ===\n")
    print("💻 النماذج المحلية (Local Models):")
    if local_models:
        for i, m in enumerate(local_models, 1):
            print(f"  [{i}] {m['name']} ({m['size']}) -> {m['engine_label']}")
    else:
        print("  [-] لا توجد نماذج محلية.")

    print("\n☁️ النماذج السحابية (Cloud Models):")
    for j, c in enumerate(cloud_models, 1):
        raw_tier = c.get("tier", "")
        tag = "🟢 [مجاني/Free]" if ("مجاني" in raw_tier or "Free" in raw_tier) else "💎 [مدفوع/Paid]"
        print(f"  [{j}] {tag} {c['label']} [{c['provider_name']}] ({c['tier']})")

# ==============================================================================
# 🏮 الواجهة الرئيسية المضغوطة والأنيقة (Compact Modular Dashboard)
# ==============================================================================

def main():
    while True:
        clear_screen()
        hw = detect_hardware()
        local_count = len(get_local_models())
        cloud_count = len(get_all_cloud_models())

        b_name = BRAND.get("brand_name", "المنارة كريبتو")
        b_tag = BRAND.get("tagline", "المحطة الطرفية الذكية الموحدة")

        if USE_RICH:
            # 1. شريط العتاد والرأس المدمج
            header_text = Text(f"🏮 {b_name} - AI Dev Hub Pro v{VERSION}\n", style="bold gold1")
            hw_bar = Text(
                f"💻 العتاد: {hw['ram_total_gb']} GB RAM (متاح: {hw['ram_avail_gb']} GB) | "
                f"قرص: {hw['disk_free_gb']} GB | {hw['arch']} ({hw['cores']}C) | "
                f"الفئة: {hw['tier_title']}",
                style="dim cyan"
            )
            console.print(Panel(Text.assemble(header_text, hw_bar), border_style="gold1"))

            # 2. القائمة الرئيسية المدمجة والمصنفة
            menu_tbl = Table(show_header=False, box=None, padding=(0, 2))
            menu_tbl.add_column("الخيار", justify="center", style="bold yellow", width=6)
            menu_tbl.add_column("القسم", style="bold white", width=30)
            menu_tbl.add_column("الحالة / المحتوى", style="dim white")

            menu_tbl.add_row(
                "[1]", "💻 النماذج المحلية (Offline Models)",
                f"[green]{local_count} نموذج متوفر[/green] (llama.cpp & AirLLM)"
            )
            menu_tbl.add_row(
                "[2]", "☁️ النماذج السحابية (Cloud Models)",
                f"[blue]{cloud_count} نماذج جاهزة[/blue] (DeepSeek R1, Groq, Kimi, Claude)"
            )
            menu_tbl.add_row(
                "[3]", "📥 تنزيل نماذج من Hugging Face",
                f"[bold magenta]ترشيحات ذكية تناسب عتاد جهازك تلقائياً[/bold magenta]"
            )
            menu_tbl.add_row(
                "[4]", "🐙 إدارة ومطور GitHub التلقائي",
                "أتمتة، مراجعة الكود بالذكاء الاصطناعي، واستنساخ"
            )
            menu_tbl.add_row(
                "[5]", "🔑 إدارة المفاتيح وإعدادات البيئة",
                "تهيئة مفاتيح الـ API وضبط مسارات النظام بأمان"
            )
            menu_tbl.add_row(
                "[6]", "🛠️ فحص النظام والتشخيص الشامل",
                "اختبار سرعة العتاد وسلامة الأدوات والمحركات"
            )
            console.print(Panel(menu_tbl, border_style="cyan", title="القائمة الرئيسية", title_align="right"))

            # 3. شريط الأوامر السريعة
            console.print(Panel(
                "[bold cyan][H][/bold cyan] 📖 دليل الـ APIs  |  "
                "[bold gold1][D][/bold gold1] 🪙 دعم وتبرعات  |  "
                "[bold red][0 / Q][/bold red] خروج",
                border_style="gold1"
            ))
            choice = safe_input("[bold yellow]اختر رقم القسم أو أمر التحكم ❯ [/bold yellow]").strip()
        else:
            print("==================================================")
            print(f"  🏮 {b_name} - AI Dev Hub Pro v{VERSION}")
            print(f"  💻 العتاد: {hw['ram_total_gb']}GB RAM | {hw['disk_free_gb']}GB قرص | {hw['tier_title']}")
            print("==================================================")
            print(f" [1] 💻 النماذج المحلية Offline ({local_count} متوفرة)")
            print(f" [2] ☁️ النماذج السحابية Cloud ({cloud_count} نماذج)")
            print(f" [3] 📥 تنزيل نماذج تناسب جهازك من Hugging Face")
            print(f" [4] 🐙 أتمتة ومطور GitHub")
            print(f" [5] 🔑 إدارة مفاتيح الـ API")
            print(f" [6] 🛠️ فحص النظام والتشخيص")
            print(" [H] دليل الـ APIs | [D] دعم | [0] خروج")
            choice = safe_input("اختر ❯ ").strip()

        if choice.lower() in ["0", "q", "exit"]:
            print("مع السلامة!")
            break
        elif choice == "1":
            local_models_menu()
        elif choice == "2":
            cloud_models_menu()
        elif choice == "3":
            download_manager_menu()
        elif choice == "4":
            github_menu()
        elif choice == "5":
            add_api_key_prompt()
        elif choice == "6":
            clear_screen()
            cli_check()
            safe_input("\nاضغط Enter للعودة...")
        elif choice.lower() == "h":
            show_api_guide()
        elif choice.lower() == "d":
            show_donation_screen()

def cli_entry():
    parser = argparse.ArgumentParser(
        description="🏮 Al-Manara AI Dev Hub Pro - المنصة الطرفية الشاملة للذكاء الاصطناعي",
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument("-v", "--version", action="version", version=f"Al-Manara AI Dev Hub Pro v{VERSION}")
    parser.add_argument("-l", "--list", action="store_true", help="عرض قائمة بجميع النماذج المحلية والسحابية المتوفرة")
    parser.add_argument("-c", "--check", action="store_true", help="إجراء فحص تشخيصي شامل للبيئة والإعدادات والمفاتيح")

    args = parser.parse_args()

    if args.list:
        cli_list()
        sys.exit(0)
    elif args.check:
        cli_check()
        sys.exit(0)

    if not sys.stdin.isatty():
        print(f"Al-Manara AI Dev Hub Pro v{VERSION} - Run with --help for CLI usage.")
        sys.exit(0)

    main()

if __name__ == "__main__":
    cli_entry()
