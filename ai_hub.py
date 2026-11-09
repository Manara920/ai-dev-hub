#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
==============================================================================
 🛠️ AI Dev Hub Pro - Open Source Unified AI & Git Workspace
 Clean, Generic & Secure Version for Any User
==============================================================================
"""

import os
import sys
import json
import subprocess
from pathlib import Path

# Base Paths (Local to where the user clones the project)
ROOT_DIR = Path(__file__).resolve().parent
CONFIG_FILE = ROOT_DIR / "config/models.json"
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

def load_env():
    env_vars = {}
    if ENV_FILE.exists():
        with open(ENV_FILE, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    k, v = line.split("=", 1)
                    env_vars[k.strip()] = v.strip().strip('"').strip("'")
    return env_vars

ENV_VARS = load_env()

def get_config():
    if CONFIG_FILE.exists():
        try:
            with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    return {}

CONFIG = get_config()

def get_provider_key(provider_key_name):
    return os.getenv(provider_key_name) or ENV_VARS.get(provider_key_name)

def get_local_models_dir():
    custom_path = os.getenv("LOCAL_MODELS_PATH") or ENV_VARS.get("LOCAL_MODELS_PATH")
    if custom_path:
        p = Path(custom_path).expanduser()
        if p.exists() and p.is_dir():
            return p
    # Standard fallback paths
    for fallback in [Path("/storage/emulated/0/LLM's"), Path.home() / "models", Path.home() / "LLMs"]:
        if fallback.exists() and fallback.is_dir():
            return fallback
    return Path.home() / "models"

# --- User & GitHub Helpers ---
def get_current_git_user():
    try:
        res = subprocess.run(["gh", "api", "user", "--jq", ".login"], capture_output=True, text=True, timeout=3)
        if res.returncode == 0 and res.stdout.strip():
            return res.stdout.strip()
    except Exception:
        pass
    try:
        res = subprocess.run(["git", "config", "user.name"], capture_output=True, text=True, timeout=2)
        if res.returncode == 0 and res.stdout.strip():
            return res.stdout.strip()
    except Exception:
        pass
    return "User"

# --- Help & Documentation [H] ---
def show_api_guide():
    os.system("clear")
    guide_md = """
# 📖 دليل إعداد وربط المفاتيح (Setup Guide)

أهلاً بك في **AI Dev Hub**! صُمم هذا المشروع ليعمل فورياً على أي جهاز دون ربط مسبق بأي حساب.

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
- **المزايا:** مجاني وسريع جداً، ممتاز لنماذج **علّام 2** و **GPT-OSS 120B**.

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
- تُحفظ مفاتيحك في ملف محلي خاص `config/.env` محمي بموجب `.gitignore` ولن يتم رفعه نهائياً لأي مستودع عام.
"""
    if USE_RICH:
        console.print(Markdown(guide_md))
    else:
        print(guide_md)
    input("\nاضغط Enter للعودة للقائمة الرئيسية...")

# --- Key Management [K] ---
def add_api_key_prompt():
    os.system("clear")
    if USE_RICH:
        console.print(Panel(Text("🔑 إدارة مفاتيح الـ API الخاصة بك", style="bold yellow"), border_style="yellow"))
    
    providers = CONFIG.get("providers", {})
    p_keys = list(providers.keys())

    print("اختر المزود الذي تريد إضافة مفتاحه:")
    for i, pk in enumerate(p_keys, 1):
        p_info = providers[pk]
        status = "✅ مسجل" if get_provider_key(p_info.get("env_key")) else "❌ غير مسجل"
        print(f" {i}) {p_info.get('name')} [{p_info.get('env_key')}] -> {status}")
    print(" 0) رجوع")

    c = input("\nاختر رقم المزود: ").strip()
    if not c.isdigit() or int(c) < 1 or int(c) > len(p_keys):
        return

    sel_p = p_keys[int(c) - 1]
    p_info = providers[sel_p]
    env_name = p_info.get("env_key")

    print(f"\n[*] الرابط: {p_info.get('site_url')}")
    print(f"[*] توجيه: {p_info.get('guide')}")
    val = input(f"\nالصق قيمة {env_name}: ").strip()

    if val:
        lines = []
        if ENV_FILE.exists():
            lines = [l for l in ENV_FILE.read_text().splitlines() if not l.startswith(f"{env_name}=")]
        lines.append(f"{env_name}=\"{val}\"")
        ENV_FILE.write_text("\n".join(lines) + "\n")
        ENV_VARS[env_name] = val
        print("\n[✓] تم حفظ المفتاح بنجاح محلياً!")
        input("اضغط Enter للمتابعة...")

# --- GitHub Integration [G] ---
def github_menu():
    git_user = get_current_git_user()
    while True:
        os.system("clear")
        if USE_RICH:
            console.print(Panel(Text(f"🐙 إدارة وتطوير مستودعات GitHub (المستخدم: {git_user})", style="bold magenta"), border_style="magenta"))
            tbl = Table(show_header=True, header_style="bold magenta", border_style="magenta")
            tbl.add_column("الخيار", justify="center", style="bold yellow", width=8)
            tbl.add_column("العملية", style="white")
            tbl.add_column("الوصف", style="dim white")
            tbl.add_row("1", "قائمة المستودعات (List Repos)", "عرض المستودعات الخاصة بك على GitHub")
            tbl.add_row("2", "حالة الكود الحالي (Git Status)", "فحص التعديلات في المشروع الحالي")
            tbl.add_row("3", "مراجعة الكود بالذكاء الاصطناعي (AI Review)", "قراءة git diff وشرح التعديلات واقتراح Commit message")
            tbl.add_row("4", "رفع التعديلات (Auto Commit & Push)", "حفظ التغييرات ورفعها بضغطة زر")
            tbl.add_row("5", "استنساخ مستودع (Git Clone)", "سحب أي مستودع من حسابك إلى بيئتك")
            tbl.add_row("0", "رجوع للقائمة الرئيسية", "العودة لقائمة النماذج")
            console.print(tbl)
            choice = console.input("[bold yellow]اختر العملية ❯ [/bold yellow]").strip()
        else:
            print(f"\n--- 🐙 قائمة GitHub ({git_user}) ---")
            print("1) عرض مستودعاتك")
            print("2) فحص حالة التعديلات الحالية")
            print("3) مراجعة التعديلات بالذكاء الاصطناعي")
            print("4) رفع التعديلات (Push)")
            print("5) استنساخ مستودع (Clone)")
            print("0) رجوع")
            choice = input("اختر ❯ ").strip()

        if choice == "0":
            break
        elif choice == "1":
            print("\n[*] جاري جلب مستودعاتك من GitHub...")
            subprocess.run(["gh", "repo", "list", "--limit", "15"])
            input("\nاضغط Enter للمتابعة...")
        elif choice == "2":
            print("\n[*] حالة Git في المجلد الحالي:")
            subprocess.run(["git", "status", "-s"])
            input("\nاضغط Enter للمتابعة...")
        elif choice == "3":
            print("\n[*] جاري استخراج git diff وإرساله للتحليل...")
            res = subprocess.run(["git", "diff"], capture_output=True, text=True)
            diff_text = res.stdout.strip()
            if not diff_text:
                res_st = subprocess.run(["git", "status", "-s"], capture_output=True, text=True)
                diff_text = res_st.stdout.strip()
            if not diff_text:
                print("[-] لا توجد أي تعديلات غير محفوظة حالياً.")
            else:
                prompt = f"راجع هذه التعديلات واشرحها وقدم اقتراح commit message احترافي:\n```\n{diff_text}\n```"
                subprocess.run(["groq", "-m", "allam-2-7b", prompt])
            input("\nاضغط Enter للمتابعة...")
        elif choice == "4":
            msg = input("\nاكتب رسالة الـ Commit: ").strip() or "Update codebase"
            subprocess.run(["git", "add", "."])
            subprocess.run(["git", "commit", "-m", msg])
            subprocess.run(["git", "push"])
            input("\nاضغط Enter للمتابعة...")
        elif choice == "5":
            repo_name = input("\nاسم المستودع المطلوب استنساخه: ").strip()
            if repo_name:
                subprocess.run(["gh", "repo", "clone", repo_name])
            input("\nاضغط Enter للمتابعة...")

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
    p_data = CONFIG["providers"].get(p_key, {})
    env_key = p_data.get("env_key")
    api_key = get_provider_key(env_key)

    if not api_key:
        print(f"\n[-] تنبيه: مفتاح [{env_key}] غير مسجل!")
        print(f"🔗 يمكنك جلبه من: {p_data.get('site_url')}")
        add_now = input("\nهل ترغب في إدخال المفتاح الآن؟ [y/N]: ").strip().lower()
        if add_now == "y":
            add_api_key_prompt()
        return

    # Check if Groq CLI exists locally
    if p_key == "groq" and shutil.which("groq"):
        subprocess.run(["groq", "-m", chosen["model_name"]])
        return

    # Standard OpenAI API client
    print(f"\n[*] جاري فتح الاتصال بـ {chosen['label']} ...")
    try:
        from openai import OpenAI
    except ImportError:
        print("[*] تثبيت مكتبة الاتصال...")
        subprocess.run([sys.executable, "-m", "pip", "install", "openai"])
        from openai import OpenAI

    base_url = p_data.get("base_url")
    client = OpenAI(base_url=base_url, api_key=api_key)

    print("=" * 60)
    print(f"  ⚡ تم الاتصال بالنموذج: {chosen['label']}")
    print(f"  • المزود: {chosen['provider_name']}")
    print("  • اكتب رسالتك واضغط Enter. للخروج اكتب /exit أو q")
    print("=" * 60)

    history = [{"role": "system", "content": "أنت مساعد برمجي ومهندس محترف، تجيب بوضوح وتكتب أكواداً ممتازة بالعربية والإنجليزية."}]
    while True:
        try:
            user_msg = input("\nأنت ❯ ").strip()
            if not user_msg: continue
            if user_msg.lower() in ["/exit", "exit", "q"]: break

            history.append({"role": "user", "content": user_msg})
            print(f"\n{chosen['label'].split('(')[0].strip()} ❯ ", end="", flush=True)

            stream = client.chat.completions.create(
                model=chosen["model_name"],
                messages=history,
                stream=True
            )
            full = ""
            for chunk in stream:
                txt = chunk.choices[0].delta.content or ""
                sys.stdout.write(txt)
                sys.stdout.flush()
                full += txt
            print()
            history.append({"role": "assistant", "content": full})
        except (KeyboardInterrupt, EOFError):
            break
        except Exception as e:
            print(f"\n[-] خطأ في الاتصال: {e}")

def main():
    while True:
        os.system("clear")
        local_models = get_local_models()
        cloud_models = get_all_cloud_models()

        if USE_RICH:
            h_text = Text("🛠️ AI Dev Hub Pro - محطة المطور والذكاء الاصطناعي الشاملة", style="bold cyan")
            sub_text = Text("نماذج محلية + DeepSeek & Kimi & Groq + إدارة ومتابعة GitHub", style="dim white")
            console.print(Panel(Text.assemble(h_text, "\n", sub_text), border_style="cyan"))

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

            # شريط التحكم
            console.print(Panel(
                "[bold magenta][G][/bold magenta] 🐙 إدارة ومتابعة GitHub  |  "
                "[bold yellow][K][/bold yellow] 🔑 إدارة وتحديث المفاتيح  |  "
                "[bold cyan][H][/bold cyan] 📖 دليل ربط الـ APIs  |  "
                "[bold red][Q][/bold red] خروج",
                border_style="dim white"
            ))
            choice = console.input("[bold yellow]اختر رقم النموذج أو أمر التحكم ❯ [/bold yellow]").strip()
        else:
            print("==================================================")
            print("           AI Dev Hub Pro (Terminal)")
            print("==================================================")
            choice = input("اختر رقم النموذج أو (G=GitHub / K=مفاتيح / H=دليل / Q=خروج) ❯ ").strip()

        if choice.lower() in ['q', 'exit']:
            print("مع السلامة!")
            break
        elif choice.lower() == 'g':
            github_menu()
        elif choice.lower() == 'k':
            add_api_key_prompt()
        elif choice.lower() == 'h':
            show_api_guide()
        elif choice.isdigit():
            c_int = int(choice)
            if local_models and 1 <= c_int <= len(local_models):
                chosen_local = local_models[c_int - 1]
                print(f"\n[*] تشغيل النموذج المحلي: {chosen_local['name']} ...")
                subprocess.run([
                    "llama-cli", "-m", chosen_local["path"],
                    "-t", "6", "-c", "2048", "-rea", "off", "--flash-attn", "on"
                ])
                input("\nاضغط Enter للعودة للمركز...")
            elif len(local_models) < c_int <= len(local_models) + len(cloud_models):
                c_idx = c_int - len(local_models) - 1
                chosen_cloud = cloud_models[c_idx]
                run_cloud_model(chosen_cloud)
                input("\nاضغط Enter للعودة للمركز...")
            else:
                input("[-] رقم غير صحيح. اضغط Enter...")

if __name__ == "__main__":
    main()
