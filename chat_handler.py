# chat_handler.py
import openai
import streamlit as st
from datetime import datetime
import re
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Set OpenAI API key
openai.api_key = st.secrets["OPENAI_API_KEY"]

# Google Sheets Setup
def connect_to_google_sheets():
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_dict(st.secrets["connections"]["gsheets"], scopes=scope)
    client = gspread.authorize(creds)
    return client.open_by_url(st.secrets["connections"]["gsheets"]["spreadsheet"]).sheet1

sheet = connect_to_google_sheets()

# Logging Function
def log_to_google_sheets(email, pdf_name, action, result, tokens_used=0, feedback=None):
    def clean_text(text):
        return re.sub(r'[^\x00-\x7F]+', '', text)[:1000]

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    row = [
        timestamp,
        clean_text(email),
        clean_text(pdf_name),
        clean_text(action),
        clean_text(result),
        0.2,  # temperature
        tokens_used,
        feedback
    ]
    try:
        sheet.append_row(row)
    except Exception as e:
        st.error(f"An error occurred while logging to Google Sheets: {str(e)}")

# Generate AI Response Function (for openai>=1.0.0)
def generate_response(template, messages, email, pdf_name, action_label):
    try:
        # Use the correct API method for version >= 1.0.0
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # or gpt-4, replace accordingly
            messages=messages + [{"role": "user", "content": template}],
            max_tokens=2048,
            temperature=0.2,
            top_p=1.0,
            frequency_penalty=0.0,
            presence_penalty=0.0
        )
        response_content = response['choices'][0]['message']['content'].strip()
        tokens_used = len(response_content.split())
        log_to_google_sheets(email, pdf_name, action_label, response_content, tokens_used)
        return response_content
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
        return None
