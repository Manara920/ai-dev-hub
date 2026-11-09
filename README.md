# 🛠️ AI Dev Hub Pro
### محطة المطور والذكاء الاصطناعي الموحدة (Terminal-First AI & Git Workspace)

<p align="center">
  <img src="https://img.shields.io/badge/Status-Production%20Ready-brightgreen?style=for-the-badge" alt="Status">
  <img src="https://img.shields.io/badge/Platform-Linux%20%7C%20Termux%20%7C%20macOS-blue?style=for-the-badge" alt="Platform">
  <img src="https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge" alt="License">
</p>

---

## 📌 نبذة عن المشروع (About The Project)

### بالعربية 🇸🇦
**AI Dev Hub Pro** هو بيئة عمل طرفية متكاملة ومفتوحة المصدر للمطورين وهواة الذكاء الاصطناعي على أنظمة **Linux و Termux (أندرويد) و macOS**.  
يهدف المشروع إلى توحيد تجربة الذكاء الاصطناعي في واجهة سطر أوامر تفاعلية واحدة تجمع بين:
1. **النماذج المحلية (Offline)**: تشغيل نماذج الذكاء الاصطناعي المكممة بصيغة `GGUF` مباشرة على معالج الجهاز دون إنترنت عبر محرك `llama.cpp`.
2. **النماذج السحابية (Cloud)**: التبديل الحي بين أحدث النماذج العالمية المجانية والمدفوعة مثل **DeepSeek (V3 & R1)**، و **Kimi (Moonshot AI)**، و **Groq (علّام 2 & GPT-OSS)**، و **Claude 3.7** و **GPT-4o**.
3. **أتمتة وإدارة GitHub**: فحص التعديلات اللحظية، ومراجعة الأكواد بالذكاء الاصطناعي (`git diff`)، وتوليد رسائل Commit احترافية، والرفع المباشر (`Auto Push`).
4. **الخصوصية والأمان أولاً**: لا توجد أي بيانات أو مفاتيح خاصة مخزنة بالكود؛ حيث تبقى جميع مفاتيح الـ API محلياً على جهاز المستخدم داخل ملف بيئة معزول ومحمي.

---

### English 🌐
**AI Dev Hub Pro** is a unified, developer-first terminal workspace designed for **Linux, Termux (Android), and macOS**. It bridges the gap between on-device local AI models and cutting-edge cloud intelligence while seamlessly integrating with your everyday Git and GitHub development workflow.

---

## 🌟 الميزات الرئيسية (Key Features)

- 🏠 **تشغيل محلي بدون إنترنت (Offline Inference)**:
  - متوافق بالكامل مع `llama.cpp`.
  - اكتشاف تلقائي للنماذج المكممة بصيغة `.gguf` (مثل Qwen, Llama 3.2, Ministral, Gemma).
  - سرعة استجابة محسنة للهواتف ومعالجات ARM.

- ☁️ **مركز النماذج السحابية (Unified Cloud Hub)**:
  - **DeepSeek V3 & DeepSeek R1**: وصول مجاني للنسخ الرسمية وأقوى نماذج التفكير والاستدلال في العالم.
  - **Kimi (Moonshot AI)**: دعم معالجة السياق الطويل والملفات البرمجية الضخمة.
  - **Groq Cloud (LPU)**: سرعة استجابة فائقة (أقل من ثانية واحدة) لنموذج علّام العربي و GPT-OSS.
  - **بوابة OpenRouter**: إمكانية تشغيل مئات النماذج بمفتاح API واحد فقط.

- 🐙 **تكامل وإدارة GitHub بضغطة زر**:
  - استعراض المستودعات الخاصة بك مباشرة من الطرفية.
  - قراءة `git diff` وتحليل التغييرات البرمجية وكتابة Commit Messages احترافية.
  - ميزة `Auto Commit & Push` لحفظ ورفع التعديلات فوراً.

- 🔐 **أمان وخصوصية تامة (Zero-Leak Security)**:
  - لا توجد أي بيانات اعتماد مشفرة أو مكشوفة داخل المشروع.
  - إدارة مرنة ومحلية للمفاتيح عبر الخيار `[K]`.
  - ملف `.gitignore` صارم يمنع تسريب أي ملفات تكوين أو بيانات خاصة.

---

## 📁 هيكل المشروع (Directory Structure)

```text
ai-dev-hub/
├── ai_hub.py           # البرنامج التفاعلي الرئيسي (Dashboard)
├── config/
│   ├── models.json     # سجل النماذج السحابية ومزودي الخدمة
│   └── .env.example    # قالب المفاتيح النظيف والآمن
├── requirements.txt    # التبعيات البرمجية (rich, openai, groq)
├── .gitignore          # حماية وتأمين المفاتيح والملفات الخاصة
└── README.md           # دليل التوثيق والتشغيل
```

---

## 🚀 التثبيت والتشغيل السريع (Quick Start)

### 1. استنساخ المستودع (Clone):
```bash
git clone https://github.com/YOUR_USERNAME/ai-dev-hub.git
cd ai-dev-hub
```

### 2. تثبيت الحزم المطلوبة:
```bash
pip install -r requirements.txt
chmod +x ai_hub.py
```

### 3. إعداد المفاتيح (اختياري):
```bash
cp config/.env.example config/.env
```
*(أو يمكنك تخطي هذه الخطوة وإدخال مفاتيحك مباشرة من داخل واجهة البرنامج بالضغط على `[K]`)*.

### 4. التشغيل:
```bash
./ai_hub.py
```

---

## 🔑 كيفية الحصول على المفاتيح السحابية (API Keys)

1. **OpenRouter (الخيار الأفضل والموحد)**: سجل مجاناً عبر [openrouter.ai/keys](https://openrouter.ai/keys) لتفعيل DeepSeek V3 و R1 و Kimi بمفتاح واحد.
2. **Groq Cloud**: مفاتيح مجانية فائقة السرعة عبر [console.groq.com/keys](https://console.groq.com/keys).
3. **DeepSeek Direct**: المنصة الرسمية عبر [platform.deepseek.com](https://platform.deepseek.com).
4. **Moonshot AI (Kimi)**: المنصة الرسمية عبر [platform.moonshot.cn](https://platform.moonshot.cn).

---

## 📄 الترخيص (License)
هذا المشروع مرخص تحت رخصة **MIT** - متاح ومجاني للاستخدام والتطوير وإعادة النشر.
