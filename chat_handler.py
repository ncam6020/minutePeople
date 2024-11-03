# chat_handler.py
import openai
import streamlit as st
from google_sheets_logger import log_to_google_sheets  # Import Google Sheets logging (can be disabled easily)

# Set OpenAI API key
openai.api_key = st.secrets["OPENAI_API_KEY"]

# Generate AI Response Function (for openai>=1.0.0)
def generate_ai_response(template, action_label):
    try:
        # Correct API method for the newer version
        response = openai.ChatCompletion.create(
            model="gpt-4",  # Replace "gpt-4o-mini" with an appropriate newer model name
            messages=st.session_state.messages + [{"role": "user", "content": template}],
            max_tokens=2048,
            temperature=0.2,
            top_p=1.0,
            frequency_penalty=0.0,
            presence_penalty=0.0
        )
        response_content = response.choices[0].message["content"].strip()
        st.session_state.messages.append({"role": "assistant", "content": response_content})

        # Disable Google Sheets logging by commenting the next line for now
        # tokens_used = len(response_content.split())
        # log_to_google_sheets(st.session_state.email, st.session_state.pdf_name, action_label, response_content, tokens_used=tokens_used)

        return response_content
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
        return None
