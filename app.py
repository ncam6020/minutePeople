import streamlit as st
import openai

# Basic Streamlit title
st.title("ChatGPT-like Clone")

# Set OpenAI API key from Streamlit secrets
openai.api_key = st.secrets["OPENAI_API_KEY"]  # Use OpenAI API directly without a client object

# Set a default model in session state (GPT-3.5 Turbo for simplicity)
if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-3.5-turbo"

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
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate assistant response using OpenAI's GPT-3.5 Turbo
    try:
        response = openai.ChatCompletion.create(
            model=st.session_state["openai_model"],
            messages=st.session_state.messages,
            max_tokens=150,  # Keep responses short initially
            temperature=0.5   # Balanced between creative and factual
        )
        response_content = response.choices[0].message['content'].strip()
        # Add assistant response to chat history
        st.session_state.messages.append({"role": "assistant", "content": response_content})
        
        # Display assistant response in chat message container
        with st.chat_message("assistant"):
            st.markdown(response_content)
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
