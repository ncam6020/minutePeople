import streamlit as st
from upload_handler import upload_document
from ocr_handler import process_ocr
from prompt_handler import create_prompt
from chat_handler import handle_chat

# Main Application
st.set_page_config(page_title="Minutes in a Minute", page_icon="🛏")

# Upload Component
uploaded_file = upload_document()

# Process OCR Component
if uploaded_file:
    extracted_text = process_ocr(uploaded_file)

# Chat Interface
if extracted_text:
    handle_chat(extracted_text)
