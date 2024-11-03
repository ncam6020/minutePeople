from openai import OpenAI
import streamlit as st

# Constants
MAX_TOKENS = 2048  # Maximum number of tokens for the response (controls response length).
TEMPERATURE = 0.2  # Temperature controls creativity: Lower values make responses more focused/deterministic, higher values make responses more creative/unpredictable.
MODEL_NAME = "gpt-4o-mini"  # The model to use for generating responses. Default is set to "gpt-4o-mini", change if needed.
TOP_P = 1.0  # Controls the diversity of the output. A value of 1.0 means no filtering, lower values reduce diversity.
FREQUENCY_PENALTY = 0.0  # Discourages repeated phrases. Higher values reduce repetition in responses.
PRESENCE_PENALTY = 0.0  # Encourages the model to discuss new topics. Higher values encourage novelty.

st.title("ChatGPT-like Clone")

# Initialize the OpenAI client
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

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

    # Generate assistant response with error handling
    try:
        with st.chat_message("assistant"):
            stream = client.chat.completions.create(
                model=st.session_state["openai_model"],
                messages=[
                    {"role": m["role"], "content": m["content"]}
                    for m in st.session_state.messages
                ],
                max_tokens=MAX_TOKENS,
                temperature=TEMPERATURE,
                top_p=TOP_P,
                frequency_penalty=FREQUENCY_PENALTY,
                presence_penalty=PRESENCE_PENALTY,
                stream=True,
            )
            response = st.write_stream(stream)
        # Add assistant response to chat history
        st.session_state.messages.append({"role": "assistant", "content": response})
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
