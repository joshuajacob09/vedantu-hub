# utils/api_clients.py
# Handles YouTube and Gemini API connections.
# Reads keys from st.secrets (Streamlit Cloud) or .env (local).

import streamlit as st
from googleapiclient.discovery import build
import google.generativeai as genai


def _get_key(name: str) -> str:
    """Read API key from Streamlit secrets or .env file."""
    # Try Streamlit Cloud secrets first
    try:
        return st.secrets[name]
    except Exception:
        pass
    # Fall back to .env / environment variable
    try:
        import os
        from dotenv import load_dotenv
        load_dotenv()
        return os.getenv(name, "")
    except Exception:
        return ""


@st.cache_resource
def get_youtube_client():
    api_key = _get_key("YOUTUBE_API_KEY")
    if not api_key:
        st.error("YOUTUBE_API_KEY not found. Add it to .env or Streamlit secrets.")
        st.stop()
    return build("youtube", "v3", developerKey=api_key)


@st.cache_resource
def get_gemini_model():
    api_key = _get_key("GEMINI_API_KEY")
    if not api_key:
        st.error("GEMINI_API_KEY not found. Add it to .env or Streamlit secrets.")
        st.stop()

    genai.configure(api_key=api_key)
    return genai.GenerativeModel("gemini-2.0-flash")
