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

    result = service.tasks().insert(tasklist='@default', body=task).execute()
    print(f"✅ Task added to Google Tasks: {result['title']} (Due in {reminder_hours} hrs)")

# 🧠 Gemini summary + task + reminder extractor
def get_summary_task_reminder(email_body):
    prompt = f"""
You are a helpful assistant.

Here is an email addressed to "{MY_NAME}":
\"\"\"
{email_body}
\"\"\"

1. Summarize the email in 1-2 lines, if the task is directly assigned to me by mentioning the user "{MY_NAME}" in body, keep it bit more descriptive.
2. Extract any action item or task relevant to "{MY_NAME}". If none, say "No task found" No need to add user name to the "No task found"
3. Suggest a reminder time in hours:
   - 2–5 hours for tasks like sending PPTs or use cases
   - 24 hours for RFP reviews/verifications
   - 1–48 hours based on urgency for other tasks

Return the result like:
Summary: ...
Task: ...
Reminder: ... hours
"""
    try:
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=prompt
        )
        return response.text
    except Exception as e:
        return f"❌ Error from Gemini: {e}"

# 📬 Outlook Email Reader
outlook = win32com.client.Dispatch("Outlook.Application").GetNamespace("MAPI")
account = outlook.Folders.Item(3)  # Adjust if needed
inbox = account.Folders["Inbox"]
messages = inbox.Items
messages.Sort("[ReceivedTime]", True)

print("📨 Processing emails for tasks related to YOU only...\n")

for i, msg in enumerate(messages):
    if i >= EMAIL_LIMIT:
        break

    try:
        subject = msg.Subject
        sender = msg.SenderName
        to = msg.To if hasattr(msg, "To") else ""
        cc = msg.CC if hasattr(msg, "CC") else ""
        body = msg.Body[:4000] if hasattr(msg, "Body") else ""

        # ✅ Filter: Skip if MY_NAME is not in recipients or body
        if MY_NAME.lower() not in (to + cc + body).lower():
            print(f"❌ Skipping: Not addressed to {MY_NAME} — {subject}")
            continue

        print(f"✅ Processing: {subject}")

        result = get_summary_task_reminder(body)

        # Parse Gemini response
        summary, task, reminder_hours = "", "", 24  # Default fallback
        lines = result.strip().split("\n")
        for line in lines:
            if line.lower().startswith("summary:"):
                summary = line.replace("Summary:", "").strip()
            elif line.lower().startswith("task:"):
                task = line.replace("Task:", "").strip()
            elif line.lower().startswith("reminder:"):
                reminder_text = line.replace("Reminder:", "").strip()
                match = re.search(r"(\d+)", reminder_text)
                if match:
                    reminder_hours = int(match.group(1))

        task_cleaned = task.strip().lower().translate(str.maketrans('', '', string.punctuation))
        if task_cleaned in ["", "no task found", "no tasks found"]:
            print(f"🟡 Skipped task creation: Gemini found no actionable task for '{subject}'\n")
        else:
            create_google_task(subject, task, reminder_hours)

        time.sleep(1)

    except Exception as e:
        print(f"⚠️ Skipped due to error: {e}\n")
