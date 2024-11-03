import openai
import fitz  # PyMuPDF
import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime
import re
import time
import pytesseract
from PIL import Image
import io

# Constants
MAX_TOKENS = 2048
TEMPERATURE = 0.2
MODEL_NAME = "gpt-4o-mini"

# Load the OpenAI API key and set up the page configuration
openai.api_key = st.secrets["OPENAI_API_KEY"]
st.set_page_config(page_title="Minutes in a Minute", page_icon="🛏")

# Initialize session state variables
if 'messages' not in st.session_state:
    st.session_state.messages = []
if 'feedback' not in st.session_state:
    st.session_state.feedback = {}
if 'email' not in st.session_state:
    st.session_state.email = ""
if 'extracted_text' not in st.session_state:
    st.session_state.extracted_text = None
if 'pdf_name' not in st.session_state:
    st.session_state.pdf_name = ""
if 'ocr_text' not in st.session_state:
    st.session_state.ocr_text = ""

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
        TEMPERATURE,
        tokens_used,
        feedback
    ]
    try:
        sheet.append_row(row)
    except Exception as e:
        st.error(f"An error occurred while logging to Google Sheets: {str(e)}")

# PDF Extraction Function
def extract_text_from_pdf(file_content):
    doc = fitz.open(stream=file_content, filetype="pdf")
    pdf_text = "\n".join(
        [f"--- Page {i+1} ---\n{page.get_text()}" for i, page in enumerate(doc)]
    )
    return pdf_text

# OCR Extraction Function
def extract_text_with_ocr(image_content):
    image = Image.open(io.BytesIO(image_content))
    ocr_text = pytesseract.image_to_string(image)
    
    # Use OpenAI API to further clean and enhance OCR output
    prompt = f"Clean up the following OCR-extracted text to improve readability and correct any obvious errors:\n\n{ocr_text}"
    enhanced_text = generate_ai_response(prompt, "Enhance OCR Output")
    
    return enhanced_text if enhanced_text else ocr_text

# AI Generation Function
def generate_ai_response(template, action_label):
    try:
        response = openai.ChatCompletion.create(
            model=MODEL_NAME,
            messages=st.session_state.messages + [{"role": "user", "content": template}],
            max_tokens=MAX_TOKENS,
            temperature=TEMPERATURE,
            top_p=1.0,
            frequency_penalty=0.0,
            presence_penalty=0.0
        )
        response_content = response.choices[0].message.content.strip()
        st.session_state.messages.append({"role": "assistant", "content": response_content})
        tokens_used = len(response_content.split())
        log_to_google_sheets(st.session_state.email, st.session_state.pdf_name, action_label, response_content, tokens_used=tokens_used)
        return response_content
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
        return None

# Button Handlers
def handle_generate_summary():
    summary_template = f"""
    Create an executive summary of this RFP document tailored for an executive architectural designer. Include key dates (issue date, response/submission due date, selection date, other important dates and times), a project overview, the scope of work, a list of deliverables, Selection Criteria, and other important information. Conclude with a concise and brief one-sentence summary identifying specific areas in the RFP where it may align with Perkins&Will's core values, such as Design Excellence, Living Design, Sustainability, Resilience, Research, Diversity and Inclusion, Social Purpose, Well-Being, and Technology, with specific examples from the document.

    RFP Document Text:
    {st.session_state.extracted_text}
    """
    generate_ai_response(summary_template, "Generate Executive Summary")

def handle_generate_pipeline_data():
    pipeline_template = f"""
    Extract and present the following key data points from this RFP document in a table format for CRM entry:
    - Client Name
    - Opportunity Name
    - Primary Contact (name, title, email, and phone)
    - Primary Practice (select from: Branded Environments, Corporate and Commercial, Corporate Interiors, Cultural and Civic, Health, Higher Education, Hospitality, K-12 Education, Landscape Architecture, Planning & Strategies, Science and Technology, Single Family Residential, Sports Recreation and Entertainment, Transportation, Urban Design, Unknown / Other)
    - Discipline (select from: Arch/Interior Design, Urban Design, Landscape Arch, Advisory Services, Branded Environments, Unknown / Other)
    - City
    - State / Province
    - Country
    - RFP Release Date
    - Proposal Due Date
    - Interview Date
    - Selection Date
    - Design Start Date
    - Design Completion Date
    - Construction Start Date
    - Construction Completion Date
    - Project Description (concise one sentence description)
    - Scope(s) of Work (select from: New, Renovation, Addition, Building Repositioning, Competition, Infrastructure, Master Plan, Planning, Programming, Replacement, Study, Unknown / Other)
    - Program Type(s) (select from: Civic and Cultural, Corporate and Commercial, Sports, Recreation + Entertainment, Education, Residential, Science + Technology, Transportation, Misc, Urban Design, Landscape Architecture, Government, Social Purpose, Health, Unknown / Other)
    - Delivery Type (select from: Construction Manager at Risk (CMaR), Design Only, Design-Bid-Build, Design-Build, Integrated Project Delivery (IPD), Guaranteed Maximum Price (GMP), Joint Venture (JV), Public Private Partnership (P3), Other)
    - Estimated Program Area
    - Estimated Budget
    - Sustainability Requirement
    - BIM Requirements

    Additional Information Aligned with Core Values:
    - Design Excellence Opportunities
    - Sustainability Initiatives
    - Resilience Measures
    - Innovation Potential
    - Diversity and Inclusion Aspects
    - Social Purpose Contributions
    - Well-Being Factors
    - Technological Innovation Opportunities
    
    If the information is not found, respond with 'Sorry, I could not find that information.'

    RFP Document Text:
    {st.session_state.extracted_text}
    """
    generate_ai_response(pipeline_template, "Generate Pipeline Data")

# Sidebar UI
def render_sidebar():
    st.sidebar.title("Minutes in a Minute 🛏")
    st.session_state.email = st.sidebar.text_input("Enter your email address so we can track feedback")

    if st.session_state.email:
        uploaded_file = st.sidebar.file_uploader("Upload your Notes", type=["pdf", "jpg", "jpeg", "png"])

        # Only extract content if a new file is uploaded or if it's not already in session state
        if uploaded_file and uploaded_file.name != st.session_state.pdf_name:
            if uploaded_file.type == "application/pdf":
                extracted_text = extract_text_from_pdf(uploaded_file.read())
            else:
                extracted_text = extract_text_with_ocr(uploaded_file.read())
                st.session_state.ocr_text = extracted_text
                
            st.session_state.extracted_text = extracted_text
            st.session_state.pdf_name = uploaded_file.name

            log_to_google_sheets(
                email=st.session_state.email,
                pdf_name=uploaded_file.name,
                action="File Uploaded",
                result="File loaded and text extracted.",
                tokens_used=len(extracted_text.split())
            )
            
            # Add a button to download the OCR output for debugging
            if st.session_state.ocr_text:
                st.sidebar.download_button(
                    label="Download OCR extracted text",
                    data=st.session_state.ocr_text,
                    file_name="ocr_extracted_text.txt",
                    mime="text/plain"
                )

            st.sidebar.markdown('---')

        # Ensure extracted text is available for actions
        if st.session_state.extracted_text:
            st.sidebar.subheader("**Key Actions**")
            if st.sidebar.button("Generate Executive Summary"):
                handle_generate_summary()

            if st.sidebar.button("Generate Pipeline Data"):
                handle_generate_pipeline_data()

# Main
