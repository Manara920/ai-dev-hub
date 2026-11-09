# 🏮 Al-Manara AI Dev Hub Pro
### المنارة كريبتو (Al-Manara Crypto) - محطة المطور والذكاء الاصطناعي الشاملة

<p align="center">
  <img src="https://img.shields.io/badge/Brand-Al--Manara%20Crypto-gold?style=for-the-badge&logo=bitcoin" alt="Brand">
  <img src="https://img.shields.io/badge/Platforms-Android%20%7C%20Linux%20%7C%20Windows-blue?style=for-the-badge" alt="Platforms">
  <img src="https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge" alt="License">
</p>

---

## 📌 نبذة عن المشروع (About)

**Al-Manara AI Dev Hub Pro** هو بيئة عمل طرفية متطورة برعاية **المنارة كريبتو (Al-Manara Crypto)** تجمع بين:
1. **النماذج المحلية (Offline)**: تشغيل نماذج الذكاء الاصطناعي المكممة بصيغة `GGUF` مباشرة على معالج جهازك دون إنترنت عبر محرك `llama.cpp`.
2. **النماذج السحابية (Cloud)**: التبديل السلس بين أحدث النماذج العالمية المجانية والمدفوعة (**DeepSeek V3 & R1**, **Kimi**, **Groq/علّام 2**, **Claude 3.7**, **GPT-4o**).
3. **أتمتة وإدارة GitHub**: فحص التعديلات اللحظية، مراجعة الأكواد بالذكاء الاصطناعي (`git diff`)، وتوليد رسائل Commit احترافية والرفع المباشر (`Auto Push`).
4. **دعم العملات الرقمية والتبرعات**: شاشة مدمجة لاستقبال التبرعات عبر شبكات الكريبتو لدعم استمرار المشروع.

---

## 🛠️ دليل التثبيت الشامل حسب نظام التشغيل (Installation Guide)

اختر نظامك واتبع الخطوات البسيطة التالية:

### 1. 📱 أندرويد (Android عبر Termux)
افتح تطبيق **Termux** ونفّذ الأوامر التالية:
```bash
# تثبيت Git و Python
pkg update && pkg install -y git python

# استنساخ المستودع
git clone https://github.com/Manara920/ai-dev-hub.git
cd ai-dev-hub

# التشغيل عبر سكربت التثبيت التلقائي
bash install.sh

# لتشغيل البرنامج في أي وقت:
./ai_hub.py
```

---

### 2. 🐧 لينكس (Linux - Ubuntu / Debian / Fedora / Arch)
افتح الطرفية (Terminal) ونفّذ:
```bash
# استنساخ المستودع
git clone https://github.com/Manara920/ai-dev-hub.git
cd ai-dev-hub

# تشغيل التثبيت التلقائي
chmod +x install.sh
./install.sh

# لتشغيل البرنامج:
./ai_hub.py
```

---

### 3. 🪟 ويندوز (Windows)
1. تأكد من تثبيت **Python** من الموقع الرسمي [python.org](https://www.python.org/downloads/) مع تفعيل خيار **"Add Python to PATH"**.
2. افتح موجه الأوامر (**CMD**) أو **PowerShell** ونفّذ:
```cmd
git clone https://github.com/Manara920/ai-dev-hub.git
cd ai-dev-hub

install.bat
```
3. لتشغيل البرنامج في أي وقت:
```cmd
python ai_hub.py
```

---

## 🔑 كيفية الحصول على المفاتيح السحابية (API Keys)

- **OpenRouter (الخيار الشامل الموصى به)**: يمنحك وصولاً مجانياً لـ **DeepSeek V3 & R1** ونموذج **Kimi** عبر [openrouter.ai/keys](https://openrouter.ai/keys).
- **Groq Cloud (فائق السرعة مجاناً)**: يدعم نموذج علّام العربي وسرعة تفوق 300 كلمة/ثانية عبر [console.groq.com/keys](https://console.groq.com/keys).
- **DeepSeek Direct**: المنصة الرسمية عبر [platform.deepseek.com](https://platform.deepseek.com).
- **Moonshot AI (Kimi)**: المنصة الرسمية عبر [platform.moonshot.cn](https://platform.moonshot.cn).

> [!TIP]
> يمكنك إدخال وتعديل أي مفتاح في أي وقت مباشرة من واجهة البرنامج بالضغط على زر **`[K]`**.

---

## 🪙 دعم وتطوير المشروع (Donations & Support)

إذا نال هذا المشروع استحسانك وأردت المساهمة في استمراريته وتطويره، يمكنك دعمه عبر المحافظ الرقمية المعتمدة لـ **المنارة كريبتو**:

| العملة / الشبكة | نوع المحفظة | عنوان المحفظة (Address) |
|---|---|---|
| **USDT (TRC-20)** | Tron Network | `ضع_عنوان_محفظة_TRC20_هنا` |
| **USDT / BNB / ETH** | EVM (Arbitrum / BSC / ERC-20) | `ضع_عنوان_محفظة_EVM_هنا_0x...` |
| **Solana (SOL)** | Solana Network | `ضع_عنوان_محفظة_سولانا_هنا` |
| **Bitcoin (BTC)** | Bitcoin Network | `ضع_عنوان_محفظة_البيتكوين_هنا` |

*(ملاحظة: يمكنك تعديل أو إضافة عناوينك الخاصة في أي وقت عبر ملف التكوين [`config/brand.json`](config/brand.json)).*

---

## 🌐 مجتمع المنارة كريبتو (Community)
- **الموقع الرسمي:** [almanaracrypto.com](https://almanaracrypto.com)
- **قناة التيليجرام:** [t.me/your_channel](https://t.me/your_channel)
- **حساب منصة X (تويتر):** [x.com/your_handle](https://x.com/your_handle)

---

## 📄 الترخيص (License)
مرخص تحت رخصة **MIT** - متاح مجاناً للمجتمع التقني والمطورين.
