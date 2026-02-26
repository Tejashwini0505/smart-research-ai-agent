import os
import requests
from dotenv import load_dotenv
from rag import retrieve, add_doc_to_index
from PyPDF2 import PdfReader

load_dotenv()

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"
MODEL = "openrouter/auto"


def extract_text_from_file(uploaded_file):
    text = ""
    if uploaded_file.type == "application/pdf":
        reader = PdfReader(uploaded_file)
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
    elif uploaded_file.type == "text/plain":
        text = uploaded_file.read().decode("utf-8")
    return text


def call_llm(prompt):

    if not OPENROUTER_API_KEY:
        return "API key not found. Check your .env file."

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": MODEL,
        "messages": [
            {
                "role": "system",
                "content": """
You are an advanced Smart Research AI Agent.

Generate:
- Title
- Abstract
- Introduction
- Background
- Key Concepts
- Current Developments
- Advantages
- Challenges
- Future Scope
- Conclusion

Write in formal academic tone.
Be detailed, structured, analytical.
Avoid repetition.
"""
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        "temperature": 0.6,
        "max_tokens": 1200
    }

    try:
        response = requests.post(OPENROUTER_URL, headers=headers, json=data, timeout=60)

        if response.status_code == 200:
            return response.json()["choices"][0]["message"]["content"]

        return f"API Error {response.status_code}: {response.text}"

    except Exception as e:
        return f"Connection Error: {str(e)}"


def run_agent(query, uploaded_files=None):

    # If files uploaded → add to vector DB
    if uploaded_files:
        for file in uploaded_files:
            text = extract_text_from_file(file)
            if text.strip():
                add_doc_to_index(text)

        context_docs = retrieve(query, k=5)

        if context_docs:
            context = "\n".join(context_docs)
            prompt = f"""
Use the following context to answer in detailed research format.

Context:
{context}

User Query:
{query}
"""
            return call_llm(prompt)

    # Default: no RAG
    return call_llm(f"Write a detailed research report on: {query}")