import streamlit as st
from agent import run_agent

st.set_page_config(page_title="Smart Research AI Agent", layout="wide")

st.title("🧠 Smart Research AI Agent")

# Chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display old messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# User input
prompt = st.chat_input("Ask anything...")

if prompt:
    # Show user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Call agent
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = run_agent(prompt)

            st.markdown(response)  # 🔥 THIS LINE IS CRITICAL

    st.session_state.messages.append({"role": "assistant", "content": response})