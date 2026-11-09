#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
==============================================================================
 🏮 Al-Manara AI Dev Hub Pro - المنارة كريبتو
 محطة المطور والذكاء الاصطناعي الموحدة (Local & Cloud & GitHub)
==============================================================================
"""

import os
import sys
import json
import shutil
import argparse
import subprocess
from pathlib import Path

VERSION = "2.1.0"

# إعداد المسارات
ROOT_DIR = Path(__file__).resolve().parent
CONFIG_FILE = ROOT_DIR / "config/models.json"
BRAND_FILE = ROOT_DIR / "config/brand.json"
ENV_FILE = ROOT_DIR / "config/.env"

# Rich Library support
try:
    from rich.console import Console
    from rich.table import Table
    from rich.panel import Panel
    from rich.markdown import Markdown
    from rich.text import Text
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
        if p.exists() and p.is_dir():
            return p
    for fallback in [Path("/storage/emulated/0/LLM's"), Path.home() / "models", Path.home() / "LLMs"]:
        if fallback.exists() and fallback.is_dir():
            return fallback
    return Path.home() / "models"

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

# --- شاشة التبرعات ودعم المنارة كريبتو [D] ---
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

        console.print("[dim]• يمكنك تعديل هذه العناوين لاحقاً في أي وقت من ملف: [bold cyan]config/brand.json[/bold cyan][/dim]")
    else:
        print("\n=== 🪙 دعم وتطوير المشروع - المنارة كريبتو ===")
        print("المحافظ الرقمية المعتمدة:")
        for k, w in wallets.items():
            print(f"- {w.get('network', k)}: {w.get('address')}")
        print("\nروابط المجتمع:")
        for k, v in comm.items():
            print(f"- {k}: {v}")
    
    safe_input("\nاضغط Enter للعودة إلى القائمة الرئيسية...")

# --- دليل استخدام وتوجيهات ربط الـ APIs [H] ---
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
- **طريقة التفعيل:** أنشئ حساباً، انسخ المفتاح الذي يبدأ بـ `sk-or-`، وضعه في الخيار `[K]`.

---

### 2. ⚡ Groq Cloud (أسرع استجابة في العالم)
- **الموقع:** [https://console.groq.com/keys](https://console.groq.com/keys)
- **المزايا:** مجاني وسريع جداً، ممتاز لنماذج **علّام 2** و **GPT-OSS 120B** و **Qwen 3.8 27B**.

---

### 3. 🇨🇳 منصة DeepSeek الرسمية المباشرة
- **الموقع:** [https://platform.deepseek.com/api_keys](https://platform.deepseek.com/api_keys)
- **المزايا:** رصيد تجريبي مجاني وأرخص تكلفة استعلام عالمياً.

---

### 4. 🌙 منصة Moonshot AI (Kimi)
- **الموقع:** [https://platform.moonshot.cn/console/api-keys](https://platform.moonshot.cn/console/api-keys)
- **المزايا:** سياق ضخم ومناسب لقراءة المشاريع والأكواد المطولة.

---

### 💡 إدارة المفاتيح محلياً:
- استخدم الخيار **`[K]`** داخل السكربت لإدخال مفاتيحك.
- تُحفظ مفاتيحك في ملف محلي خاص `config/.env` محمي بموجب `.gitignore`.
"""
    if USE_RICH:
        console.print(Markdown(guide_md))
    else:
        print(guide_md)
    safe_input("\nاضغط Enter للعودة للقائمة الرئيسية...")

# --- إدارة المفاتيح [K] ---
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

# --- GitHub Integration [G] ---
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
            tbl.add_row("0", "رجوع للقائمة الرئيسية", "العودة لقائمة النماذج")
            console.print(tbl)
            choice = safe_input("[bold yellow]اختر العملية ❯ [/bold yellow]").strip()
        else:
            print(f"\n--- 🐙 قائمة GitHub ({git_user}) ---")
            print("1) عرض مستودعاتك")
            print("2) فحص حالة التعديلات الحالية")
            print("3) مراجعة التعديلات بالذكاء الاصطناعي")
            print("4) رفع التعديلات (Push)")
            print("5) استنساخ مستودع (Clone)")
            print("0) رجوع")
            choice = safe_input("اختر ❯ ").strip()

        if choice == "0":
            break
        elif choice == "1":
            print("\n[*] جاري جلب مستودعاتك من GitHub...")
            if not shutil.which("gh"):
                print("[-] أداة gh (GitHub CLI) غير متوفرة في النظام.")
            else:
                try:
                    subprocess.run(["gh", "repo", "list", "--limit", "15"], cwd=str(ROOT_DIR))
                except Exception as e:
                    print(f"[-] خطأ: {e}")
            safe_input("\nاضغط Enter للمتابعة...")
        elif choice == "2":
            print("\n[*] حالة Git في المجلد الحالي:")
            if not shutil.which("git"):
                print("[-] أداة git غير متوفرة في النظام.")
            else:
                try:
                    subprocess.run(["git", "status", "-s"], cwd=str(ROOT_DIR))
                except Exception as e:
                    print(f"[-] خطأ: {e}")
            safe_input("\nاضغط Enter للمتابعة...")
        elif choice == "3":
            print("\n[*] جاري استخراج git diff وإرساله للتحليل...")
            if not shutil.which("git"):
                print("[-] أداة git غير متوفرة في النظام.")
                safe_input("\nاضغط Enter للمتابعة...")
                continue
            try:
                res = subprocess.run(["git", "diff"], cwd=str(ROOT_DIR), capture_output=True, text=True)
                diff_text = res.stdout.strip()
                if not diff_text:
                    res_st = subprocess.run(["git", "status", "-s"], cwd=str(ROOT_DIR), capture_output=True, text=True)
                    diff_text = res_st.stdout.strip()
            except Exception as e:
                print(f"[-] خطأ في قراءة حالة git: {e}")
                safe_input("\nاضغط Enter للمتابعة...")
                continue

            if not diff_text:
                print("[-] لا توجد أي تعديلات غير محفوظة حالياً.")
            else:
                prompt = f"راجع هذه التعديلات واشرحها وقدم اقتراح commit message احترافي:\n```\n{diff_text}\n```"
                groq_bin = shutil.which("groq")
                cmd = [groq_bin] if groq_bin else [sys.executable, str(ROOT_DIR / "bin" / "groq")]
                try:
                    subprocess.run(cmd + ["-m", "allam-2-7b", prompt], cwd=str(ROOT_DIR))
                except FileNotFoundError:
                    print("[-] أداة groq غير متوفرة في النظام أو المجلد.")
                except Exception as e:
                    print(f"[-] خطأ أثناء تشغيل مراجعة الكود: {e}")
            safe_input("\nاضغط Enter للمتابعة...")
        elif choice == "4":
            if not shutil.which("git"):
                print("[-] أداة git غير متوفرة في النظام.")
                safe_input("\nاضغط Enter للمتابعة...")
                continue
            # Security verification before staging
            try:
                st = subprocess.run(["git", "status", "--porcelain"], cwd=str(ROOT_DIR), capture_output=True, text=True)
                sensitive_patterns = [".env", ".key", ".token", ".pem", ".gguf"]
                risky = []
                for line in st.stdout.splitlines():
                    fname = line[3:].strip()
                    if any(p in fname for p in sensitive_patterns):
                        risky.append(fname)
                if risky:
                    print(f"[-] تنبيه أمني خطير: تم اكتشاف ملفات حساسة غير متجاهلة ({', '.join(risky)})!")
                    print("    يرجى التأكد من إضافة هذه الملفات إلى .gitignore قبل رفع التعديلات لتجنب تسريب المفاتيح.")
                    safe_input("\nاضغط Enter للعودة...")
                    continue
            except Exception as e:
                print(f"[-] تعذر التحقق من حالة git: {e}")

            msg = safe_input("\nاكتب رسالة الـ Commit: ").strip() or "Update codebase"
            try:
                subprocess.run(["git", "add", "."], cwd=str(ROOT_DIR))
                subprocess.run(["git", "commit", "-m", msg], cwd=str(ROOT_DIR))
                subprocess.run(["git", "push"], cwd=str(ROOT_DIR))
            except Exception as e:
                print(f"[-] خطأ أثناء تنفيذ git push: {e}")
            safe_input("\nاضغط Enter للمتابعة...")
        elif choice == "5":
            if not shutil.which("gh"):
                print("[-] أداة gh غير متوفرة في النظام.")
                safe_input("\nاضغط Enter للمتابعة...")
                continue
            repo_name = safe_input("\nاسم المستودع المطلوب استنساخه: ").strip()
            if repo_name:
                try:
                    subprocess.run(["gh", "repo", "clone", repo_name], cwd=str(ROOT_DIR))
                except Exception as e:
                    print(f"[-] خطأ: {e}")
            safe_input("\nاضغط Enter للمتابعة...")

# --- Models Logic ---
def get_local_models():
    models = []
    models_dir = get_local_models_dir()
    if models_dir.exists() and models_dir.is_dir():
        for f in sorted(models_dir.glob("*.gguf")):
            if not f.name.startswith("mmproj"):
                size_gb = f.stat().st_size / (1024 * 1024 * 1024)
                models.append({
                    "name": f.name,
                    "path": str(f),
                    "size": f"{size_gb:.1f} GB"
                })
    return models

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

    # Branded Persona
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
                # Handle DeepSeek R1 / Reasoning tokens
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

def cli_list():
    local_models = get_local_models()
    cloud_models = get_all_cloud_models()

    if USE_RICH and console:
        tbl_l = Table(title="💻 النماذج المحلية (Local GGUF)", border_style="green", header_style="bold green")
        tbl_l.add_column("#", justify="center", style="bold yellow", width=4)
        tbl_l.add_column("اسم النموذج", style="white")
        tbl_l.add_column("الحجم", style="cyan", width=12)
        tbl_l.add_column("المسار", style="dim white")
        if local_models:
            for i, m in enumerate(local_models, 1):
                tbl_l.add_row(str(i), m["name"], m["size"], m["path"])
        else:
            tbl_l.add_row("-", "لا توجد نماذج .gguf في المسار المكتشف", "-", str(get_local_models_dir()))
        console.print(tbl_l)

        tbl_c = Table(title="☁️ النماذج السحابية (Cloud Models)", border_style="blue", header_style="bold blue")
        tbl_c.add_column("#", justify="center", style="bold yellow", width=4)
        tbl_c.add_column("النموذج", style="white")
        tbl_c.add_column("المعرف التقني", style="dim cyan")
        tbl_c.add_column("المزود", style="yellow")
        tbl_c.add_column("الباقة", style="magenta")
        start = len(local_models) + 1
        for j, c in enumerate(cloud_models):
            tbl_c.add_row(str(start + j), c["label"], c["model_name"], c["provider_name"], c["tier"])
        console.print(tbl_c)
    else:
        print("=== النماذج المحلية (Local GGUF) ===")
        if local_models:
            for i, m in enumerate(local_models, 1):
                print(f" [{i}] {m['name']} ({m['size']}) -> {m['path']}")
        else:
            print(" لا توجد نماذج .gguf في مجلد النماذج المكتشف.")
        print("\n=== النماذج السحابية (Cloud Models) ===")
        start = len(local_models) + 1
        for j, c in enumerate(cloud_models):
            print(f" [{start + j}] {c['label']} ({c['model_name']}) | المزود: {c['provider_name']} | الباقة: {c['tier']}")

def cli_check():
    issues = 0
    print("==========================================================")
    print(" 🏮 Al-Manara AI Dev Hub Pro - فحص بيئة العمل والتشخيص")
    print("==========================================================")

    # 1. Configs
    print("\n[1] فحص ملفات الإعدادات:")
    if CONFIG_FILE.exists():
        try:
            with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                c = json.load(f)
                num_p = len(c.get("providers", {}))
                print(f"  [✓] {CONFIG_FILE.name}: سليم ({num_p} مزودين مهيأين)")
        except Exception as e:
            print(f"  [✗] {CONFIG_FILE.name}: تالف ({e})")
            issues += 1
    else:
        print(f"  [✗] {CONFIG_FILE.name}: غير موجود")
        issues += 1

    if BRAND_FILE.exists():
        try:
            with open(BRAND_FILE, "r", encoding="utf-8") as f:
                json.load(f)
                print(f"  [✓] {BRAND_FILE.name}: سليم")
        except Exception as e:
            print(f"  [✗] {BRAND_FILE.name}: تالف ({e})")
            issues += 1
    else:
        print(f"  [✗] {BRAND_FILE.name}: غير موجود")
        issues += 1

    # 2. Tools in PATH
    print("\n[2] فحص الأدوات في PATH:")
    tools = [
        ("python3", "مفسر بايثون", True),
        ("git", "أداة Git لإدارة الإصدارات", False),
        ("gh", "GitHub CLI لأتمتة المستودعات", False),
        ("llama-cli", "محرك تشغيل النماذج المحلية llama.cpp", False),
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

    # Check groq binary
    if shutil.which("groq"):
        print(f"  [✓] {'groq':<10} (أداة Groq CLI): متوفرة في {shutil.which('groq')}")
    elif (ROOT_DIR / "bin" / "groq").exists():
        print(f"  [✓] {'groq':<10} (أداة Groq CLI): متوفرة محلياً في {ROOT_DIR / 'bin' / 'groq'}")
    else:
        print(f"  [-] {'groq':<10} (أداة Groq CLI): غير متوفرة")

    # 3. Environment Variables & Keys
    print("\n[3] فحص مفاتيح الـ API المسجلة:")
    keys = ["GROQ_API_KEY", "OPENROUTER_API_KEY", "DEEPSEEK_API_KEY", "MOONSHOT_API_KEY"]
    for k in keys:
        v = get_provider_key(k)
        if v:
            masked = v[:4] + "..." + v[-4:] if len(v) > 8 else "***"
            print(f"  [✓] {k:<20}: مسجل ({masked})")
        else:
            print(f"  [-] {k:<20}: غير مسجل")

    # 4. Local models dir
    models_dir = get_local_models_dir()
    print(f"\n[4] فحص مجلد النماذج المحلية:")
    if models_dir.exists():
        ggufs = list(models_dir.glob("*.gguf"))
        print(f"  [✓] المسار: {models_dir} (تم العثور على {len(ggufs)} ملف .gguf)")
    else:
        print(f"  [-] المسار: {models_dir} (المجلد غير موجود حالياً)")

    print("\n" + "=" * 58)
    if issues == 0:
        print(" [✓] التشخيص اكتمل: البيئة الأساسية جاهزة وسليمة بنجاح.")
    else:
        print(f" [-] التشخيص اكتمل مع وجود {issues} ملاحظة تحتاج مراجعة.")
    print("==========================================================")

def main():
    while True:
        clear_screen()
        local_models = get_local_models()
        cloud_models = get_all_cloud_models()

        if USE_RICH:
            # شعار وبانر المنارة كريبتو
            b_name = BRAND.get("brand_name", "المنارة كريبتو")
            b_tag = BRAND.get("tagline", "المحطة الطرفية الذكية")
            
            h_text = Text(f"🏮 {b_name} - AI Dev Hub Pro", style="bold gold1")
            sub_text = Text(f"{b_tag} | Local & Cloud & GitHub", style="dim white")
            console.print(Panel(Text.assemble(h_text, "\n", sub_text), border_style="gold1"))

            # جدول النماذج المحلية
            tbl_local = Table(title="💻 النماذج المحلية في جهازك (Offline)", border_style="green", header_style="bold green")
            tbl_local.add_column("الرقم", justify="center", style="bold yellow", width=5)
            tbl_local.add_column("اسم النموذج", style="white")
            tbl_local.add_column("الحجم", justify="center", style="cyan", width=10)
            tbl_local.add_column("الحالة", justify="center", style="green", width=12)
            if local_models:
                for i, m in enumerate(local_models, 1):
                    tbl_local.add_row(str(i), m["name"], m["size"], "🟢 محلي")
            else:
                tbl_local.add_row("-", "لم يتم العثور على نماذج .gguf في مجلد النماذج", "-", "⚪ فارغ")
            console.print(tbl_local)

            # جدول النماذج السحابية
            tbl_cloud = Table(title="☁️ النماذج السحابية (DeepSeek, Kimi, Groq, Claude)", border_style="blue", header_style="bold blue")
            tbl_cloud.add_column("الرقم", justify="center", style="bold yellow", width=5)
            tbl_cloud.add_column("النموذج وميزاته", style="white")
            tbl_cloud.add_column("المزود (Provider)", style="cyan")
            tbl_cloud.add_column("الباقة (Tier)", justify="center", style="bold magenta", width=18)

            start_idx = len(local_models) + 1
            for j, c in enumerate(cloud_models):
                idx = start_idx + j
                tbl_cloud.add_row(str(idx), c["label"], c["provider_name"], c["tier"])
            console.print(tbl_cloud)

            # شريط التحكم السفلي متضمناً زر الدعم [D]
            console.print(Panel(
                "[bold magenta][G][/bold magenta] 🐙 إدارة GitHub  |  "
                "[bold yellow][K][/bold yellow] 🔑 إدارة المفاتيح  |  "
                "[bold cyan][H][/bold cyan] 📖 دليل الـ APIs  |  "
                "[bold gold1][D][/bold gold1] 🪙 دعم وتبرعات  |  "
                "[bold red][Q][/bold red] خروج",
                border_style="gold1"
            ))
            choice = safe_input("[bold yellow]اختر رقم النموذج أو أمر التحكم ❯ [/bold yellow]").strip()
        else:
            print("==================================================")
            print("      Al-Manara Crypto - AI Dev Hub Pro")
            print("==================================================")
            print("\n💻 النماذج المحلية (Local GGUF):")
            if local_models:
                for i, m in enumerate(local_models, 1):
                    print(f" [{i}] {m['name']} ({m['size']})")
            else:
                print(" [-] لا توجد نماذج .gguf في مجلد النماذج.")
            print("\n☁️ النماذج السحابية (Cloud Models):")
            start_idx = len(local_models) + 1
            for j, c in enumerate(cloud_models):
                idx = start_idx + j
                print(f" [{idx}] {c['label']} [{c['provider_name']}] ({c['tier']})")
            print("\n[G=GitHub / K=مفاتيح / H=دليل / D=تبرع / Q=خروج]")
            choice = safe_input("اختر رقم النموذج أو أمر التحكم ❯ ").strip()

        if choice.lower() in ['q', 'exit']:
            print("مع السلامة!")
            break
        elif choice.lower() == 'g':
            github_menu()
        elif choice.lower() == 'k':
            add_api_key_prompt()
        elif choice.lower() == 'h':
            show_api_guide()
        elif choice.lower() == 'd':
            show_donation_screen()
        elif choice.isdigit():
            c_int = int(choice)
            if local_models and 1 <= c_int <= len(local_models):
                chosen_local = local_models[c_int - 1]
                if not shutil.which("llama-cli"):
                    print("\n[-] تنبيه: أداة 'llama-cli' غير متوفرة في مسار النظام (PATH).")
                    print("    على Termux: pkg install llama-cpp")
                    print("    على Linux: قم بتثبيت llama.cpp من مستودعات التوزيعة أو بنائها.")
                    safe_input("\nاضغط Enter للعودة للمركز...")
                    continue
                print(f"\n[*] تشغيل النموذج المحلي: {chosen_local['name']} ...")
                try:
                    subprocess.run([
                        "llama-cli", "-m", chosen_local["path"],
                        "-t", "6", "-c", "2048", "-rea", "off", "--flash-attn", "on"
                    ])
                except FileNotFoundError:
                    print("[-] لم يتم العثور على أداة llama-cli.")
                except Exception as e:
                    print(f"[-] خطأ أثناء تشغيل النموذج المحلي: {e}")
                safe_input("\nاضغط Enter للعودة للمركز...")
            elif len(local_models) < c_int <= len(local_models) + len(cloud_models):
                c_idx = c_int - len(local_models) - 1
                chosen_cloud = cloud_models[c_idx]
                run_cloud_model(chosen_cloud)
                safe_input("\nاضغط Enter للعودة للمركز...")
            else:
                safe_input("[-] رقم غير صحيح. اضغط Enter...")

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

    # If non-interactive stdin (e.g. redirected or /dev/null), exit cleanly without blocking
    if not sys.stdin.isatty():
        print(f"Al-Manara AI Dev Hub Pro v{VERSION} - Run with --help for CLI usage.")
        sys.exit(0)

    main()

if __name__ == "__main__":
    cli_entry()
