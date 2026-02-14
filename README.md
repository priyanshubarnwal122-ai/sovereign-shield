<div align="center">

# 🛡️ SOVEREIGN SHIELD AI
### **The Ultimate Offline Privacy Defense System**

[![Python](https://img.shields.io/badge/Python-3.9%2B-blue?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-App-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)](https://streamlit.io/)
[![Model](https://img.shields.io/badge/AI-TinyLlama%201.1B-green?style=for-the-badge)](https://huggingface.co/TheBloke/TinyLlama-1.1B-Chat-v1.0-GGUF)
[![License](https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge)](LICENSE)

*Built for the Sovereign AI Challenge | 100% Local Inference | Zero Data Leakage*

[View Demo](#) • [Report Bug](https://github.com/priyanshubarnwal122-ai/sovereign-shield/issues) • [Request Feature](https://github.com/priyanshubarnwal122-ai/sovereign-shield/issues)

</div>

---

## 📖 Overview

**Sovereign Shield AI** is a military-grade, offline PII (Personally Identifiable Information) redaction engine designed to protect sensitive Indian data. 

Unlike cloud-based solutions that risk data sovereignty by sending information to external servers, this application runs a quantized **Large Language Model (LLM)** entirely on your local CPU. It identifies and redacts entities like Names, Phone Numbers, Aadhaar, and PAN cards in real-time without ever connecting to the internet.

## ✨ Key Features

* **🔒 Zero-Trust Offline Architecture**: The AI brain runs locally. No API keys, no cloud uploads, no data leakage.
* **👻 Ghost Mode (Synthetic Data)**: Instead of just blacking out text, the AI generates realistic *synthetic* Indian identities to replace sensitive data, allowing developers to test systems safely.
* **⚔️ Military-Grade Wipe**: Complete removal of all proper nouns, dates, and locations for maximum security.
* **💻 Cyberpunk Terminal UI**: A custom-styled "Hacker Mode" interface with real-time telemetry (Processing Speed, Character Count) and neon visuals.
* **🇮🇳 Hinglish Support**: Optimized prompts to handle mixed Hindi-English text often found in Indian banking and chat logs.

---

## 🛠️ Tech Stack

* **Core Framework**: Python 3.9+
* **Interface**: Streamlit (with Custom CSS Injection)
* **Inference Engine**: `ctransformers` (GGML/GGUF Library)
* **Model**: TinyLlama-1.1B-Chat (Quantized to 4-bit for CPU efficiency)

---

## 📥 Model Setup (Critical)

> **Note regarding `.gitignore`**: To adhere to DevOps best practices and GitHub file size limits, the large model file (`model.gguf`, ~638MB) is **excluded** from this repository. You must download it manually.

1.  **Download the Model**:
    Go to Hugging Face and download **`tinyllama-1.1b-chat-v1.0.Q4_K_M.gguf`**.
    👉 [Direct Download Link](https://huggingface.co/TheBloke/TinyLlama-1.1B-Chat-v1.0-GGUF/resolve/main/tinyllama-1.1b-chat-v1.0.Q4_K_M.gguf?download=true)

2.  **Place the File**:
    Move the downloaded file into the **root folder** of this project.

3.  **Rename**:
    Rename the file to exactly: `model.gguf`

---

## 🚀 Installation & Run (Windows)

Follow these steps to deploy the shield on your local machine.

### 1. Clone the Repository
```bash
git clone [https://github.com/priyanshubarnwal122-ai/sovereign-shield.git](https://github.com/priyanshubarnwal122-ai/sovereign-shield.git)
cd sovereign-shield

