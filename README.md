# 🏮 Al-Manara AI Dev Hub Pro
### المنارة كريبتو (Al-Manara Crypto) - محطة المطور والذكاء الاصطناعي الشاملة

<p align="center">
  <img src="https://img.shields.io/badge/Brand-Al--Manara%20Crypto-gold?style=for-the-badge&logo=bitcoin" alt="Brand">
  <img src="https://img.shields.io/badge/Platforms-Android%20%7C%20Linux%20%7C%20Windows-blue?style=for-the-badge" alt="Platforms">
  <img src="https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge" alt="License">
</p>

> **منصة طرفية موحدة للمطورين تجمع بين تشغيل النماذج المحلية بدون إنترنت (GGUF عبر llama.cpp)، والنماذج السحابية فائقة الذكاء (DeepSeek, Kimi, Groq, Claude)، مع أتمتة مهام ومستودعات GitHub ونظام دعم بالعملات المشفرة.**

---

## 📌 ماذا يقدم المشروع بالتحديد؟ (Core Capabilities)

تم تصميم **Al-Manara AI Dev Hub Pro** ليكون مركز قيادة متكامل في سطر الأوامر يلغي الحاجة للتشتت بين منصات الذكاء الاصطناعي المختلفة أو متصفحات الويب:

### 1. 💻 تشغيل النماذج المحلية بدون إنترنت (Offline Local Inference):
- دعم كامل لصيغة **GGUF** عبر محرك `llama.cpp` عالي الكفاءة.
- اكتشاف تلقائي للنماذج المخزنة في جهازك (مثل `Qwen 2.5`, `Llama 3.2`, `Ministral`, `Gemma`).
- خيارات تسريع مبرمجة مسبقاً (`Flash Attention`، تعدد الأنوية، وإلغاء التفكير المطول غير الضروري) لتوفير أقصى سرعة على الهواتف والأجهزة الشخصية.

### 2. ☁️ دعم وتبديل حي بين أقوى النماذج السحابية (Multi-Cloud AI Hub):
- **النماذج المجانية 🟢**:
  - **DeepSeek V3 & R1**: النسخ الرسمية وأقوى نماذج التفكير المنطقي المجانية عالمياً (مع دعم كامل لرموز التفكير `reasoning_content`).
  - **Groq Cloud (LPU)**: سرعة فائقة (< 1 ثانية) لنموذج **علّام 2 (Allam)** العربي و **GPT-OSS 120B** و **Qwen 3.8 27B**.
  - **Kimi (Moonshot AI)**: الرائد عالمياً في معالجة المستندات الضخمة والأكواد الطويلة جداً.
- **النماذج المتقدمة والمدفوعة 💎**:
  - **Claude 3.7 Sonnet**: النموذج رقم #1 في هندسة وبرمجة التطبيقات المعقدة.
  - **OpenAI GPT-4o**: النموذج الشامل متعدد الاستخدامات.
- **بوابة موحدة عبر OpenRouter**: تتيح تشغيل جميع هذه النماذج بمفتاح API واحد فقط.

### 3. 🐙 إدارة وأتمتة مستودعات GitHub بضغطة زر:
- استعراض مستودعاتك السحابية والتحقق من حالة الكود اللحظية (`git status`).
- **مراجعة الكود بالذكاء الاصطناعي (AI Review)**: قراءة `git diff` تلقائياً وشرح التعديلات واقتراح رسالة Commit احترافية عبر Groq / علّام.
- **Auto Commit & Push**: فحص الملفات غير المتتبعة وحفظ ورفع التعديلات فوراً بضغطة زر مع الحماية من رفع المفاتيح.
- استنساخ المستودعات (Git Clone) مباشرة من حسابك.

### 4. 🔐 أمان مطلق وخصوصية كاملة (Zero-Data Leak):
- لا يتم حفظ أي مفاتيح API أو بيانات اعتماد في كود المستودع.
- إدارة محلية كاملة للمفاتيح داخل ملف `config/.env` محمي بموجب `.gitignore`.
- إمكانية إضافة وتعديل المفاتيح من داخل واجهة البرنامج بالضغط على `[K]`.

### 5. 🪙 هوية "المنارة كريبتو" ودعم العملات الرقمية:
- شاشة تبرعات تفاعلية بالضغط على `[D]` تدعم شبكات **USDT (TRC-20)** و **EVM (ETH/BNB/Arbitrum)** و **Solana** و **Bitcoin**.
- ملف إعدادات مستقل [`config/brand.json`](config/brand.json) لتخصيص الروابط وعناوين المحافظ بسهولة.

### 6. 🧪 مفسر الأكواد المعزول ومختبر الوكلاء (OpenSandbox & Interpreter):
- دمج تقنية **[OpenSandbox](https://github.com/opensandbox-group/OpenSandbox)** لتنفيذ الأكواد التي يولدها الذكاء الاصطناعي بأمان تام.
- **حلقة التصحيح الذاتي (Self-Healing Loop):** في حال حدوث خطأ في الكود، يقرأ النموذج رسالة الخطأ تلقائياً ويعيد كتابته واختباره داخل الـ Sandbox حتى ينجح!
- **معمارية هجينة ومرنة:**
  - اتصال تلقائي بسيرفر OpenSandbox الخارجي (Docker / MicroVMs) عبر `OPENSANDBOX_ENDPOINT` في `config/.env`.
  - مشغل محلي فوري وآمن (Local Safe Fallback) يعمل تلقائياً ومباشرة على الهواتف وبيئات Termux بدون الحاجة لأي خوادم خارجية.
- فحص واختبار سلامة مشاريع بايثون داخل الـ Sandbox قبل عمل Commit و Push إلى GitHub.

---

## ⚡ خيارات سطر الأوامر (CLI Flags & Options)

يدعم `ai_hub.py` تشغيلاً غير تفاعلي كاملاً عبر وسائط سطر الأوامر:

```bash
# عرض دليل المساعدة وخيارات البرنامج
python3 ai_hub.py --help

# عرض رقم الإصدار الحالي
python3 ai_hub.py --version

# عرض قائمة بجميع النماذج المحلية والسحابية المهيأة
python3 ai_hub.py --list

# إجراء فحص تشخيصي شامل للبيئة والإعدادات وتوفر الأدوات والمفاتيح
python3 ai_hub.py --check
```

### أداة Groq Pro CLI المستقلة (`bin/groq`):
المشروع مزود بأداة طرفية متقدمة وسريعة جداً للتعامل المباشر مع نماذج Groq:

```bash
# الاستعلام المباشر عبر سطر الأوامر
groq "اكتب كود بايثون للتحقق من عناوين شبكة إيثريوم"

# تحديد نموذج معين
groq -m openai/gpt-oss-120b "حلل هذا الخوارزم"

# قراءة ملف وتضمينه في السياق
groq -f script.py "قم بمراجعة هذا الملف واكتشاف الثغرات"

# حفظ مخرجات الذكاء الاصطناعي مباشرة في ملف
groq -f main.py -o refactored.py "أعد صياغة هذا الكود بأفضل الممارسات"

# عرض النماذج المتاحة في حسابك
groq -l

# الدخول في وضع المحادثة التفاعلية
groq
```

#### أوامر الوضع التفاعلي داخل `groq`:
- `/help` : عرض قائمة الأوامر التفاعلية.
- `/models` أو `/model` : عرض وتبديل النماذج النشطة.
- `/file <path>` : قراءة ملف محلي وتضمينه في سياق المحادثة.
- `/save <path>` : حفظ الرد أو الكود الأخير في ملف خارجي.
- `/copy` : نسخ آخر رد إلى الحافظة (يدعم Termux و Linux و macOS و Windows).
- `/clear` : تفريغ سياق الجلسة الحالية والبدء من جديد.
- `/exit` أو `/q` : إنهاء الجلسة.

---

## 🛠️ دليل التثبيت والتشغيل (Installation & Setup)

### 🚀 خيار البيئة الافتراضية الموصى به (Virtual Environment):
للحفاظ على نظافة حزم بايثون وعزل المشروع:
```bash
cd ai-dev-hub
bash setup_venv.sh
```
- **للدخول إلى البيئة لاحقاً في أي جلسة جديدة:**
  ```bash
  source ~/ai-dev-hub/.venv/bin/activate
  ```
- **أو استخدم المشغل التلقائي مباشرة:**
  ```bash
  ./run.sh
  ```
- **للخروج من البيئة الافتراضية:**
  ```bash
  deactivate
  ```

---

### 📱 1. أندرويد (Android عبر Termux)
```bash
pkg update && pkg install -y git python llama-cpp
git clone https://github.com/Manara920/ai-dev-hub.git
cd ai-dev-hub
bash install.sh
./run.sh
```
*ملاحظة: يقوم `install.sh` بإنشاء رابط رمزي (Symlink) لأداة `groq` داخل `$PREFIX/bin` ليتسنى لك استخدام أمر `groq` مباشرة من أي مسار.*

> [!TIP]
> **محركات النماذج المحلية في Termux:**
> - **⚡ llama.cpp**: يعمل مباشرة في تيرمكس للأجهزة والهواتف بسرعة فائقة مع صيغ GGUF (`pkg install llama-cpp`).
> - **🧠 AirLLM**: يعتمد على PyTorch و Transformers، ولذا **لا يثبت في تيرمكس مباشرة** بل يجب تشغيله داخل بيئة Linux حقيقية عبر PRoot (`pkg install proot-distro && proot-distro install ubuntu && proot-distro login ubuntu`).

### 🐧 2. لينكس (Linux - Ubuntu / Debian / Arch / Fedora)
```bash
git clone https://github.com/Manara920/ai-dev-hub.git
cd ai-dev-hub
chmod +x install.sh && ./install.sh
./run.sh
```
*ملاحظة: يدعم مثبت النظام مديري الحزم المختلفة (`apt`, `dnf`, `pacman`)، ويثبت الأمر `groq` في `~/.local/bin`.*

### 🪟 3. ويندوز (Windows)
من موجه الأوامر (**CMD**):
```cmd
git clone https://github.com/Manara920/ai-dev-hub.git
cd ai-dev-hub
install.bat
python ai_hub.py
```
*ملاحظة: يقوم `install.bat` بإنشاء الملفين المساعدين `groq.cmd` و `bin\groq.bat` لتمكين تشغيل `groq` في سطر أوامر ويندوز مباشرة.*

---

## 🎯 اختصارات لوحة التحكم داخل البرنامج

| الزر | الوظيفة |
|---|---|
| **`[رقم]`** | تشغيل أي نموذج محلي أو سحابي مباشرة |
| **`[G]`** | فتح لوحة التحكم وأتمتة مستودعات **GitHub** |
| **`[K]`** | إدارة وتحديث مفاتيح الـ API السحابية |
| **`[H]`** | الدليل الإرشادي المدمج لكيفية الحصول على المفاتيح المجانية والمدفوعة |
| **`[D]`** | شاشة الدعم والتبرعات لـ **المنارة كريبتو** |
| **`[Q]`** | الخروج من البرنامج |

---

## 📄 الترخيص (License)
مرخص تحت رخصة **MIT** - متاح ومجاني للاستخدام والتطوير وإعادة النشر. راجع ملف [LICENSE](LICENSE) للتفاصيل الكاملة.
