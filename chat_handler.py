import openai
import streamlit as st

# Constants
MAX_TOKENS = 2048  # Maximum number of tokens for the response (controls response length).
TEMPERATURE = 0.2  # Temperature controls creativity: Lower values make responses more focused/deterministic, higher values make responses more creative/unpredictable.
TOP_P = 1.0  # Controls the diversity of the output. A value of 1.0 means no filtering, lower values reduce diversity.
FREQUENCY_PENALTY = 0.0  # Discourages repeated phrases. Higher values reduce repetition in responses.
PRESENCE_PENALTY = 0.0  # Encourages the model to discuss new topics. Higher values encourage novelty.

# Set the OpenAI API key
openai.api_key = st.secrets["OPENAI_API_KEY"]

# Generate AI Response Function
def generate_response(model_name, messages):
    """
    Function to generate an AI response using OpenAI's Chat API.
    
    Parameters:
    - model_name: The model to use, e.g., "gpt-4".
    - messages: The conversation history as a list of dicts with "role" and "content".
    
    Returns:
    - response_content: The generated response content as a string.
    """
    try:
        response = openai.ChatCompletion.create(
            model=model_name,
            messages=messages,
            max_tokens=MAX_TOKENS,
            temperature=TEMPERATURE,
            top_p=TOP_P,
            frequency_penalty=FREQUENCY_PENALTY,
            presence_penalty=PRESENCE_PENALTY
        )
        response_content = response.choices[0].message['content'].strip()
        return response_content
    except Exception as e:
        st.error(f"An error occurred while generating the response: {str(e)}")
        return None
