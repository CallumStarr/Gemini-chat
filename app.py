import os
import streamlit as st
from google import genai

MODEL_ID = "gemini-3-pro-preview"

st.set_page_config(page_title="Gemini 3 Pro Chat", page_icon="💬")
st.title("💬 Gemini 3 Pro")

# Read API key from Streamlit secrets (preferred) or environment variable
api_key = st.secrets.get("GEMINI_API_KEY", None) or os.getenv("GEMINI_API_KEY")

if not api_key:
    st.error("Missing API key. Add GEMINI_API_KEY to Streamlit secrets or environment variables.")
    st.stop()

client = genai.Client(api_key=api_key)

# Keep conversation history
if "history" not in st.session_state:
    st.session_state.history = []  # list of {"role": "user"|"model", "text": str}

# Display chat history
for msg in st.session_state.history:
    role = "user" if msg["role"] == "user" else "assistant"
    with st.chat_message(role):
        st.markdown(msg["text"])

# Input box
user_text = st.chat_input("Type your message...")

if user_text:
    # show user message
    st.session_state.history.append({"role": "user", "text": user_text})
    with st.chat_message("user"):
        st.markdown(user_text)

    # build contents for Gemini
    contents = []
    for m in st.session_state.history:
        contents.append({"role": m["role"], "parts": [{"text": m["text"]}]})

    # call Gemini
    response = client.models.generate_content(
        model=MODEL_ID,
        contents=contents,
    )

    assistant_text = response.text or "(no text returned)"

    # show assistant message
    st.session_state.history.append({"role": "model", "text": assistant_text})
    with st.chat_message("assistant"):
        st.markdown(assistant_text)
