import streamlit as st
from chat_handler import generate_response  # Importing the chat handler

# Constants
MODEL_NAME = "gpt-4"  # Change model to GPT-4 for enhanced capabilities.

# Streamlit app title
st.title("ChatGPT-like Clone with GPT-4")

# Set default model in session state (using the constant)
if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = MODEL_NAME

# Initialize chat history in session state
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Accept user input
if prompt := st.chat_input("What is up?"):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate assistant response using the chat handler
    response = generate_response(
        model_name=st.session_state["openai_model"],
        messages=st.session_state.messages
    )

    # If the response is generated successfully, add it to the chat history
    if response:
        with st.chat_message("assistant"):
            st.markdown(response)
        st.session_state.messages.append({"role": "assistant", "content": response})
