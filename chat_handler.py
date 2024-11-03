# chat_handler.py
import openai
import streamlit as st
from google_sheets_logger import log_to_google_sheets  # Import Google Sheets logging (can be disabled easily)

# Constants
MAX_TOKENS = 2048
TEMPERATURE = 0.2
MODEL_NAME = "gpt-4"  # Using the GPT-4 model for better conversational abilities

# Set OpenAI API key
openai.api_key = st.secrets["OPENAI_API_KEY"]

# Generate AI Response Function
def generate_response(template, action_label):
    try:
        # Correct API call for chat model using the newer version of the library
        response = openai.ChatCompletion.create(
            model=MODEL_NAME,
            messages=st.session_state.messages + [{"role": "user", "content": template}],
            max_tokens=MAX_TOKENS,
            temperature=TEMPERATURE,
            top_p=1.0,
            frequency_penalty=0.0,
            presence_penalty=0.0
        )
        response_content = response.choices[0].message['content'].strip()
        st.session_state.messages.append({"role": "assistant", "content": response_content})
        
        # Log to Google Sheets if desired (disabled for now)
        tokens_used = len(response_content.split())
        # log_to_google_sheets(st.session_state.email, st.session_state.pdf_name, action_label, response_content, tokens_used=tokens_used)
        
        return response_content
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
        return None
