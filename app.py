# app.py
import streamlit as st
from upload_handler import upload_document
from ocr_handler import process_uploaded_file
from prompt_handler import create_summary_prompt
from chat_handler import generate_response

# Main Streamlit Application
st.set_page_config(page_title="Minutes in a Minute", page_icon="🛏")

# Initialize session state variables
if 'messages' not in st.session_state:
    st.session_state.messages = []  # Initialize messages as an empty list
if 'feedback' not in st.session_state:
    st.session_state.feedback = {}
if 'email' not in st.session_state:
    st.session_state.email = ""
if 'extracted_text' not in st.session_state:
    st.session_state.extracted_text = None
if 'pdf_name' not in st.session_state:
    st.session_state.pdf_name = ""

# Sidebar: Upload Documents
email, uploaded_file = upload_document()

# Process Uploaded File (OCR or PDF Extraction)
if uploaded_file:
    extracted_text = process_uploaded_file(uploaded_file)
    if extracted_text:
        st.success("File processed successfully!")
        st.session_state.extracted_text = extracted_text
        st.session_state.pdf_name = uploaded_file.name
    else:
        st.warning("Unable to extract text from the uploaded file.")

# Display Chat Interface if Document is Processed
if st.session_state.extracted_text:
    st.sidebar.subheader("**Key Actions**")

    if st.sidebar.button("Generate Executive Summary"):
        summary_prompt = create_summary_prompt(st.session_state.extracted_text)
        response_content = generate_response(
            summary_prompt,
            st.session_state.email,
            st.session_state.pdf_name,
            "Generate Executive Summary"
        )
        if response_content:
            st.session_state.messages.append({"role": "assistant", "content": response_content})
            st.write(response_content)

# Render main UI
def render_main_ui():
    st.title("Minutes in a Minute 🛏")

    if not st.session_state.email:
        st.write("Please enter your email address and upload a document in the sidebar to start. \n\nRemember, this is generative AI and is experimental.")
    elif not st.session_state.pdf_name:
        st.write("Please load your document in the sidebar.\n\nRemember, this is generative AI and is experimental.")
    else:
        st.markdown('---')
        st.subheader("**Chat Interface**")

        for i, message in enumerate(st.session_state.messages):
            with st.chat_message(message["role"]):
                st.write(message["content"])

# Run the App
render_main_ui()
