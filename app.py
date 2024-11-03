# app.py
import streamlit as st
from upload_handler import upload_document
from ocr_handler import process_uploaded_file
from prompt_handler import create_summary_prompt, create_pipeline_data_prompt
from chat_handler import generate_ai_response

# Main Streamlit Application
st.set_page_config(page_title="Minutes in a Minute", page_icon="🛏")

# Sidebar: Upload Documents
email, uploaded_file = upload_document()

# Process Uploaded File (OCR or PDF Extraction)
if uploaded_file:
    extracted_text = process_uploaded_file(uploaded_file)
    if extracted_text:
        st.success("File processed successfully!")

# Display Chat Interface if Document is Processed
if extracted_text:
    st.sidebar.subheader("**Key Actions**")

    if st.sidebar.button("Generate Executive Summary"):
        summary_prompt = create_summary_prompt(extracted_text)
        response_content = generate_ai_response(summary_prompt, st.session_state.get('messages', []), email, uploaded_file.name)
        if response_content:
            st.session_state.messages.append({"role": "assistant", "content": response_content})
            st.write(response_content)

    if st.sidebar.button("Generate Pipeline Data"):
        pipeline_prompt = create_pipeline_data_prompt(extracted_text)
        response_content = generate_ai_response(pipeline_prompt, st.session_state.get('messages', []), email, uploaded_file.name)
        if response_content:
            st.session_state.messages.append({"role": "assistant", "content": response_content})
            st.write(response_content)
