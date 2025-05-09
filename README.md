# Email-Agent-AI

An **AI-powered email agent** that reads unread emails from Gmail, detects spam, summarizes long messages, and automatically generates and sends polite, professional replies using LLMs — all without human intervention.

> 🔗 [Live Repo](https://github.com/Inbaselvan-ayyanar/email-agent-ai.git)

---

## 🚀 Features

- 📥 **Gmail Integration** – Reads unread emails using the Gmail API
- 🧠 **Spam Filtering** – Detects and skips spam emails using a trained ML model
- 📝 **AI Summarization** – Summarizes lengthy emails with BART (facebook/bart-large-cnn)
- ✉️ **AI Response Generation** – Replies with high-quality, human-like responses using Mistral (via Ollama)
- 📤 **Automated Sending** – Sends replies and marks emails as read automatically
- 🔒 **OAuth 2.0** – Secure token-based authentication for Gmail access

---

## 📦 Tech Stack

| Tool/Library | Purpose |
|--------------|---------|
| Python       | Core language |
| Gmail API       | Email access and control |
| Transformers (Hugging Face)    | Email summarization |
| Ollama + Mistral | AI-based email generation |
| Joblib       | Spam classifier loading |
| BeautifulSoup| HTML email parsing |
| Pickle       | Credential storage |
| OAuth 2.0    | Secure Gmail access |

---

## 📁 Project Structure

📦 email-agent-ai

├── main.py # Workflow controller

├── Unread_Mail_Extraction.py # Fetches unread Gmail messages

├── email_generator.py # Summarizes and generates replies

├── reply_email.py # Sends email replies via Gmail API

├── spam_classifier_pipeline.pkl # Trained ML spam detection model

├── client.json # Gmail API credentials 

├── token_*.pickle # Auth tokens 


## ⚙️ Setup Instructions

1. **Clone the repository**
git clone https://github.com/Inbaselvan-ayyanar/email-agent-ai.git
cd email-agent-ai
Install dependencies

2. **Install dependencies**
pip install -r requirements.txt

3. **Set up Gmail API credentials**
  - Visit Google Cloud Console
  - Create a new project and enable the Gmail API
  - Download client.json and place it in the project root

4. **Run the agent**
python main.py

---
## 🧪 Requirements

- Python 3.8+
- Gmail API credentials
- Ollama with Mistral model 
- Hugging Face Transformers
  
---
## 📬 Contact

For queries or support, contact: a.inbaselvan@gmail.com

---
---
