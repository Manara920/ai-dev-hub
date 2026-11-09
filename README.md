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
  - **DeepSeek V3 & R1**: النسخ الرسمية وأقوى نماذج التفكير المنطقي المجانية عالمياً.
  - **Groq Cloud (LPU)**: سرعة فائقة (< 1 ثانية) لنموذج **علّام 2 (Allam)** العربي و **GPT-OSS 120B** و **Llama 3.3 70B**.
  - **Kimi (Moonshot AI)**: الرائد عالمياً في معالجة المستندات الضخمة والأكواد الطويلة جداً.
- **النماذج المتقدمة والمدفوعة 💎**:
  - **Claude 3.7 Sonnet**: النموذج رقم #1 في هندسة وبرمجة التطبيقات المعقدة.
  - **OpenAI o3-mini & GPT-4o**: الاستدلال المتعمق والخوارزميات المعقدة.
- **بوابة موحدة عبر OpenRouter**: تتيح تشغيل جميع هذه النماذج بمفتاح API واحد فقط.

### 3. 🐙 إدارة وأتمتة مستودعات GitHub بضغطة زر:
- استعراض مستودعاتك السحابية والتحقق من حالة الكود اللحظية (`git status`).
- **مراجعة الكود بالذكاء الاصطناعي (AI Review)**: قراءة `git diff` تلقائياً وشرح التعديلات واقتراح رسالة Commit احترافية.
- **Auto Commit & Push**: حفظ ورفع التعديلات فوراً بضغطة زر دون أوامر معقدة.
- استنساخ المستودعات (Git Clone) مباشرة من حسابك.

### 4. 🔐 أمان مطلق وخصوصية كاملة (Zero-Data Leak):
- لا يتم حفظ أي مفاتيح API أو بيانات اعتماد في كود المستودع.
- إدارة محلية كاملة للمفاتيح داخل ملف `config/.env` محمي بموجب `.gitignore`.
- إمكانية إضافة وتعديل المفاتيح من داخل واجهة البرنامج بالضغط على `[K]`.

### 5. 🪙 هوية "المنارة كريبتو" ودعم العملات الرقمية:
- شاشة تبرعات تفاعلية بالضغط على `[D]` تدعم شبكات **USDT (TRC-20)** و **EVM (ETH/BNB/Arbitrum)** و **Solana** و **Bitcoin**.
- ملف إعدادات مستقل [`config/brand.json`](config/brand.json) لتخصيص الروابط وعناوين المحافظ بسهولة.

---

## 🛠️ دليل التثبيت الشامل حسب نظامك (Installation)

### 1. 📱 أندرويد (Android عبر Termux)
```bash
pkg update && pkg install -y git python
git clone https://github.com/Manara920/ai-dev-hub.git
cd ai-dev-hub
bash install.sh
./ai_hub.py
```

### 2. 🐧 لينكس (Linux - Ubuntu / Debian / Arch / Fedora)
```bash
git clone https://github.com/Manara920/ai-dev-hub.git
cd ai-dev-hub
chmod +x install.sh && ./install.sh
./ai_hub.py
```

### 3. 🪟 ويندوز (Windows)
من موجه الأوامر (**CMD**):
```cmd
git clone https://github.com/Manara920/ai-dev-hub.git
cd ai-dev-hub
install.bat
python ai_hub.py
```

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
مرخص تحت رخصة **MIT** - متاح ومجاني للاستخدام والتطوير وإعادة النشر.
