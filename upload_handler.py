# upload_handler.py
import streamlit as st

def upload_document():
    st.sidebar.title("Minutes in a Minute 🛏")
    email = st.sidebar.text_input("Enter your email address so we can track feedback")

    uploaded_file = None
    if email:
        uploaded_file = st.sidebar.file_uploader("Upload your Notes", type=["pdf", "jpg", "jpeg", "png"])

    return email, uploaded_file
