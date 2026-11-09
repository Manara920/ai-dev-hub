# 🛠️ AI Dev Hub Pro

> **A Unified Terminal Workspace for Local LLMs (`llama.cpp`), Cloud AI Models (DeepSeek, Kimi, Groq, Claude), and Automated GitHub Workflow Management.**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Platform: Linux / Termux / macOS](https://img.shields.io/badge/Platform-Linux%20%7C%20Termux%20%7C%20macOS-blue.svg)](#)

---

## 🌟 Features

- **🏠 Offline Local Models**: Run GGUF models directly on device CPU with `llama.cpp` (Qwen, Llama 3, Ministral, Gemma).
- **☁️ Multi-Cloud AI Hub**:
  - **DeepSeek V3 & R1**: Access free models via OpenRouter or official DeepSeek API.
  - **Kimi (Moonshot AI)**: Long-context specialized models for large documents.
  - **Groq Cloud (LPU)**: Ultra-fast inference (< 1 second) for Arabic (Allam) and code.
  - **Claude 3.7 & GPT-4o**: Direct developer integration.
- **🐙 Integrated GitHub Manager**:
  - Live repository inspection.
  - `git diff` AI code review & smart commit message generator.
  - One-click `git add`, `commit`, and `push`.
- **🔐 Privacy & Security First**: Zero hardcoded personal tokens or credentials. All keys stay locally on your machine in `config/.env`.

---

## 🚀 Quick Start

### 1. Clone the Repository
```bash
git clone https://github.com/YOUR_USERNAME/ai-dev-hub.git
cd ai-dev-hub
```

### 2. Install Dependencies
```bash
# On Termux or Linux
pip install -r requirements.txt
chmod +x ai_hub.py
```

### 3. Setup Your API Keys (Optional)
```bash
cp config/.env.example config/.env
```
*(Or simply launch the script and press `[K]` to enter your keys interactively!)*

### 4. Run AI Dev Hub
```bash
./ai_hub.py
```

---

## 📂 Project Structure

```text
ai-dev-hub/
├── ai_hub.py           # Main interactive terminal application
├── config/
│   ├── models.json     # Declarative cloud model registry & provider endpoints
│   └── .env.example    # Safe template for API keys
├── requirements.txt    # Python dependencies
├── .gitignore          # Strict ignore rules to protect API keys & local models
└── README.md           # Documentation
```

---

## 🔑 Getting Free API Keys

1. **OpenRouter (Recommended)**: Get a single unified key for DeepSeek & Kimi at [openrouter.ai/keys](https://openrouter.ai/keys).
2. **Groq Cloud**: Free high-speed keys at [console.groq.com/keys](https://console.groq.com/keys).
3. **DeepSeek Direct**: [platform.deepseek.com/api_keys](https://platform.deepseek.com/api_keys).
4. **Moonshot AI**: [platform.moonshot.cn](https://platform.moonshot.cn).

---

## 📄 License
MIT License. Free to use, fork, and distribute.
