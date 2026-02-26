# ui.py
import streamlit as st
from agent import run_agent
from PyPDF2 import PdfReader

# Page configuration
st.set_page_config(page_title="Smart Research AI Agent", layout="wide")

# CSS Styling for ChatGPT-like UI
st.markdown(
    """
    <style>
    .chat-box {
        background-color: #f7f7f8;
        border-radius: 10px;
        padding: 10px;
        margin-bottom: 10px;
        max-height: 500px;
        overflow-y: auto;
    }
    .user-msg {
        background-color: #1f77b4;
        color: white;
        padding: 8px;
        border-radius: 10px;
        text-align: left;
        margin-bottom: 5px;
        max-width: 70%;
    }
    .assistant-msg {
        background-color: #e5e5ea;
        color: black;
        padding: 8px;
        border-radius: 10px;
        text-align: left;
        margin-bottom: 5px;
        max-width: 70%;
    }
    .stButton>button {
        background-color: #4CAF50;
        color: white;
        border-radius: 8px;
        padding: 8px 16px;
        font-weight: bold;
    }
    .stButton>button:hover {
        background-color: #45a049;
        color: white;
    }
    .clear-btn>button {
        background-color: #f44336;
        color: white;
        border-radius: 8px;
        padding: 8px 16px;
        font-weight: bold;
    }
    .clear-btn>button:hover {
        background-color: #d7372f;
        color: white;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Initialize chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

st.title("🧠 Smart Research AI Agent")

# Sidebar - multiple file uploader
st.sidebar.title("Upload Documents (Optional)")
uploaded_files = st.sidebar.file_uploader(
    "Upload PDFs or TXT files",
    type=["pdf", "txt"],
    accept_multiple_files=True
)

# Function to read uploaded files
def read_files(files):
    content = ""
    for file in files:
        if file.type == "application/pdf":
            reader = PdfReader(file)
            for page in reader.pages:
                content += page.extract_text() or ""
        else:  # TXT file
            content += file.read().decode("utf-8")
        content += "\n"
    return content

file_text = read_files(uploaded_files) if uploaded_files else ""

# User input
user_input = st.text_input("Ask anything...", key="input_box")

# Buttons
col1, col2 = st.columns([1, 1])
with col1:
    send = st.button("Send")
with col2:
    clear = st.button("Clear Chat")

# Clear chat
if clear:
    st.session_state.chat_history = []

# Send query
if send and user_input.strip():
    st.session_state.chat_history.append(("user", user_input))
    answer = run_agent(user_input, file_text)
    st.session_state.chat_history.append(("assistant", answer))

# Display chat messages in scrollable chat box
st.markdown('<div class="chat-box">', unsafe_allow_html=True)
for role, msg in st.session_state.chat_history:
    if role == "user":
        st.markdown(f'<div class="user-msg">{msg}</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="assistant-msg">{msg}</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)