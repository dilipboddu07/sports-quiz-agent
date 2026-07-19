import os
from dotenv import load_dotenv

load_dotenv()

try:
    import streamlit as st
    GEMINI_API_KEY = st.secrets.get(
        "GEMINI_API_KEY",
        os.getenv("GEMINI_API_KEY")
    )
except Exception:
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

CHROMA_DB_PATH = "./chroma_db"
COLLECTION_NAME = "sports_history"

if not GEMINI_API_KEY:
    raise ValueError(
        "GEMINI_API_KEY not found. Add it to Streamlit Secrets or your .env file."
    )
