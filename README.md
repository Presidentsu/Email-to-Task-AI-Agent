
# 🧠 Agentic AI Email Task Assistant

This is a local, privacy-respecting AI assistant that scans your Outlook emails, summarizes messages addressed to **you**, and creates actionable tasks directly into **Google Tasks** — all using **Gemini** LLM.

---

## ✅ Features

- 📥 Reads recent emails from Microsoft Outlook (.ost locally)
- 🎯 Filters emails addressed to **you** (based on your name)
- 🧠 Uses Gemini LLM to:
  - Summarize the email
  - Extract tasks
  - Suggest reminder time intelligently
- 📅 Adds the task to your **Google Tasks** with due date

---

## 🚀 How to Run

### 1. Clone or Download the Script

```bash
git clone https://github.com/Presidentsu/Email-to-Task-AI-Agent.git
cd agentic-ai-task-assistant
```

### 2. Install Dependencies

Ensure you have Python 3.10+ installed (preferably with `pip`)

```bash
pip install google-auth google-auth-oauthlib google-api-python-client google-generativeai pywin32
```

### 3. Prepare Google OAuth

- Go to [Google Cloud Console](https://console.cloud.google.com/)
- Create a project
- Enable `Google Tasks API`
- While you are at it, GCP will ask to create OAuth Screen Consent
- Complete those steps, and naviage to Audience tab (https://console.cloud.google.com/auth/audience) and add yourself as test user.
- Download `credentials.json` (OAuth Client ID — Desktop App)
- Save it in the same folder as the script


---

## 🧑‍💻 Run the Assistant

```bash
python agentic_ai.py
```

You’ll be prompted for:

- Your full name (e.g. Krishna Sai Marella)
- Number of emails to scan (e.g. 5)
- Gemini API Key (get from [Google AI Studio](https://aistudio.google.com))
- Path to `credentials.json` (optional if in the same folder)

---

Post a web page will be opened for the authn for google task, complete it.

## 🧠 How Gemini Works

Gemini reads each email body and returns:

```
Summary: short description of email
Task: action item addressed to you
Reminder: 2–48 hours (based on urgency)
```

---

## 🔐 Privacy & Locality

- Your emails are read **locally via Outlook**
- Nothing is stored or shared except what Gemini reads per message
- Google Task API is used with your explicit OAuth login

---

## 🙌 Credit

Built with 💛 by Skanda/PresidentSU/Krishna Sai Marella  
Powered by Google Gemini, and ChatGPT for all the corrections and help <3 xD

---

## 🔐 Does Gemini Store My Email Data?

No, Gemini **does not store or train on your email content** if you're using it via API (as this assistant does).

### ✅ Safe via API Key:
According to [Google AI Terms](https://ai.google.dev/terms):

> "Content submitted through the Generative Language API is not used to train our models or shared with others."

- Your email content is not used to improve Gemini
- It is not shared with any third parties
- Google may log data **temporarily** for abuse prevention and billing

### 🧠 Best Practices:
- Only short snippets (trimmed to ~4000 characters) are sent to Gemini
- You can further sanitize content (remove signatures, footers, etc.)
- For highly sensitive data, consider switching to a private/self-hosted LLM

This assistant is designed to maximize privacy and local-first processing while giving you the power of Gemini AI.

