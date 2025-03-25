import win32com.client
import string
from google import genai
import os
import datetime
import time
import re
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# 🔐 Gemini API Key

print("🤖 Welcome to Agentic AI Task Assistant\n")

# 👤 Get user's name
MY_NAME = input("🔹 Enter your full name (for email matching): ").strip()

# 🔢 How many emails to scan
try:
    EMAIL_LIMIT = int(input("🔹 How many recent emails should I scan? (e.g., 5, 10): ").strip())
except ValueError:
    EMAIL_LIMIT = 5
    print("⚠️ Invalid number, defaulting to 5 emails.")

# 🔐 Gemini API Key
GEMINI_API_KEY = input("🔹 Paste your Gemini API Key: ").strip()

# 📂 Google credentials file path
CREDENTIALS_PATH = input("🔹 Enter path to Google credentials.json (or press Enter if in same folder): ").strip()
if not CREDENTIALS_PATH:
    CREDENTIALS_PATH = "credentials.json"
    
client = genai.Client(api_key=GEMINI_API_KEY)

# 🔑 Google OAuth scope
SCOPES = ['https://www.googleapis.com/auth/tasks']

# 📅 Google Tasks: Create task with due date
def create_google_task(title, notes, reminder_hours):
    creds = None

    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)

    if not creds or not creds.valid:
        flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_PATH, SCOPES)
        creds = flow.run_local_server(port=0)

        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    service = build('tasks', 'v1', credentials=creds)

    # Calculate due datetime
    due_datetime = datetime.datetime.utcnow() + datetime.timedelta(hours=reminder_hours)
    due_iso = due_datetime.isoformat("T") + "Z"

    task = {
        'title': title,
        'notes': notes,
        'due': due_iso
    }

