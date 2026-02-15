<div align="center">

# 🛡️ SOVEREIGN SHIELD AI
### **The Ultimate Offline Privacy Defense System**

[![Python](https://img.shields.io/badge/Python-3.9%2B-blue?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=Streamlit&logoColor=white)](https://streamlit.io/)
[![HuggingFace](https://img.shields.io/badge/HuggingFace-Transformers-yellow?style=for-the-badge&logo=huggingface&logoColor=black)](https://huggingface.co/)
[![SmolifyAI](https://img.shields.io/badge/Built%20With-Smolify.AI-orange?style=for-the-badge)](https://smolify.ai/)


> **Built for Privacy-First AI Systems | 100% Local Inference | Zero Data Leakage**

[View Demo](#)

</div>

---

## 📖 Overview

**Sovereign Shield AI** is an offline-first PII (Personally Identifiable Information) redaction engine designed to protect sensitive data—specifically optimized for the Indian context—without relying on cloud APIs.

In an era where data privacy laws (like the DPDP Act) are tightening, most redaction tools still send your sensitive data to external servers for processing. **Sovereign Shield changes that.** It runs entirely on your local machine using a custom BERT-based pipeline and rule-based logic.

**No API calls. No telemetry. No cloud dependency.**. 

## ✨ Key Features

### 🔒 Zero-Trust Offline Architecture
* **Fully Local Inference:** Powered by PyTorch and HuggingFace Transformers running on your hardware.
* **Air-Gap Ready:** Can be deployed in high-security environments with no internet access.
* **No API Keys:** Save costs and eliminate third-party risk.

### 🇮🇳 Hinglish Support: 
Sovereign Shield AI handles informal Indian text patterns including Hinglish (Hindi written in Roman script).

* **Input**: `mera naam Rahul Sharma hai aur mera phone number 9876543210 hai`
 * **Output**:`Name: [NAME] Phone: [PHONE]`

The system combines NER and rule-based detection to process mixed Hindi-English text commonly found in banking complaints and chat logs.

### 🟢 Standard Mode – Structured Redaction
Designed for compliance workflows and document sanitization. It detects PII and replaces it with standardized tags.

* **Input:** `My name is Rahul Sharma. Phone: 9876543210`
* **Output:** `Name: [NAME] Phone: [PHONE]`

### 👻 Ghost Mode – Synthetic Identity Replacement
Instead of simply masking data (which ruins context for ML training), Ghost Mode generates **realistic synthetic Indian identities**. This maintains the semantic structure of the data while anonymizing the subject.

* **Input:** `My name is Rahul Sharma. Call me at 9876543210.`
* **Output:** `My name is Aarav Mehta. Call me at 7648293102.`

### 🔴 Military Mode – Secure Wipe
Designed for high-security workflows where data existence itself is a liability.
* **Action:** Immediate null output and memory clearance.
* **Result:** Maximum sanitization.

---

## 🛠️ Tech Stack

* **Language**: Python 3.9+
* **UI Framework**: Streamlit
* **LLM Framework**: HuggingFace Transformers
* **NER Engine**: dslim/bert-base-NER
* **Backend**: PyTorch
* **Execution**: Fully Offline

---

## 🚀 Installation & Run (Windows)

Follow these steps to deploy the shield on your local machine.

### 1. Clone the Repository
```
git clone [https://github.com/priyanshubarnwal122-ai/sovereign-shield.git](https://github.com/priyanshubarnwal122-ai/sovereign-shield.git)
cd sovereign-shield
```

### 2. Create Virtual Environment
```
python -m venv .venv
.\.venv\Scripts\activate
```

### 3. Install Dependencies
```
pip install -r requirements.txt
```

### 4. Run the Application
``` 
streamlit run app.py
```
The application will launch in your browser.

---

## 🔐 Privacy Principles

* **100% offline execution**
* **No external API calls**
* **No user data logging**
* **Local model loading only**
* **Cached resources using** `st.cache_resource`

---

## 🎯 Use Cases

* **Legal document sanitization**
* **Banking complaint redaction**
* **Government data protection**
* **Secure enterprise workflows**
* **Synthetic data generation for testing**
