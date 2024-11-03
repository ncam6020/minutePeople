# google_sheets_logger.py
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime
import re
import streamlit as st

# Function to connect to Google Sheets
def connect_to_google_sheets():
    try:
        scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
        creds = ServiceAccountCredentials.from_json_keyfile_dict(st.secrets["connections"]["gsheets"], scopes=scope)
        client = gspread.authorize(creds)
        return client.open_by_url(st.secrets["connections"]["gsheets"]["spreadsheet"]).sheet1
    except Exception as e:
        st.warning(f"Google Sheets connection is currently disabled. Error: {str(e)}")
        return None

# Function to log data to Google Sheets
def log_to_google_sheets(email, pdf_name, action, result, tokens_used=0, feedback=None):
    try:
        sheet = connect_to_google_sheets()
        if not sheet:
            # Google Sheets is disabled or the connection failed.
            return

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
        sheet.append_row(row)
    except Exception as e:
        st.error(f"An error occurred while logging to Google Sheets: {str(e)}")
