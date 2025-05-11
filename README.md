# ai-assistant-reactive-fastapi
# 🤖 AI Chatbot Agents — LangGraph, FastAPI & Streamlit

Experience the future of AI interaction with an intuitive, multi-modal chatbot app. Powered by **LangGraph**, **FastAPI**, **Streamlit**, and **python-dotenv** — this project lets you chat with advanced AI agents using text and voice queries.

---

## ✨ Features

- 🧠 **AI Agents**: Interact with custom LangGraph agents
- 🛠️ **Dynamic Model Switching**: Choose between **Groq** and **OpenAI** models
- 🖋️ **Custom System Prompts**: Configure agent behavior
- 🗂️ **Conversation History**: Track your chat sessions
- 🎤 **Voice Input Support**: Upload **WAV**/**MP3** audio queries (up to 200MB)
- 🌐 **Optional Web Search**: Enhance responses with real-time info
- ⚙️ **Environment Variables via `python-dotenv`**: Secure API keys & configs
- 🕒 **Real-time Clock & Footer Branding**: Professional UI touch

---

## 📂 Project Structure

```
├── ai_agent.py         # LangGraph Agent Definition
├── backend.py          # FastAPI Backend API
├── frontend.py         # Streamlit Frontend App (Main UI)
├── .env                # Environment Variables (API Keys)
├── Pipfile / Pipfile.lock # (For Pipenv users)
└── README.md           # Project Guide
```

---

## ⚙️ Installation Guide

### 1️⃣ Clone Repository
```bash
git clone https://github.com/AIwithhassan/ai-agent-chatbot-with-fastapi.git
cd ai-agent-chatbot-with-fastapi
```

### 2️⃣ Setup Virtual Environment (Choose One)

**Using Pipenv**
```bash
pip install pipenv
pipenv install
pipenv shell
```

**Using pip + venv**
```bash
python -m venv venv
source venv/bin/activate   # macOS/Linux
venv\Scripts\activate      # Windows
pip install -r requirements.txt
```

**Using Conda**
```bash
conda create --name myenv python=3.11
conda activate myenv
pip install -r requirements.txt
```

### 3️⃣ Setup Environment Variables (Important)

Create a `.env` file in your project root:

```
OPENAI_API_KEY=your_openai_api_key
GROQ_API_KEY=your_groq_api_key
OTHER_API_KEY=your_optional_keys
```

---

## ▶️ Running the Application

> **⚠️ Important:** Run **backend.py** in a separate terminal before launching frontend.

**Phase 1: Start AI Agent**
```bash
python ai_agent.py
```

**Phase 2: Start Backend API**
```bash
python backend.py
```

**Phase 3: Launch Frontend UI**
```bash
python frontend.py
```

## 📚 Learn More

- [LangGraph Docs](https://python.langchain.com/docs/langgraph)
- [FastAPI Docs](https://fastapi.tiangolo.com/)
- [Streamlit Docs](https://docs.streamlit.io/)
- [dotenv Docs](https://pypi.org/project/python-dotenv/)

---

> ✨ _Built with ❤️ by Priyanshu Patil_
