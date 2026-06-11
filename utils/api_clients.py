# utils/api_clients.py
# ─────────────────────────────────────────────────────
# Responsible for: creating & caching API client objects.
#
# Why a separate file?
#   Instead of connecting to YouTube / Gemini in every
#   module, we build the client ONCE here and reuse it.
#   @st.cache_resource makes sure Streamlit doesn't
#   reconnect on every user interaction.
# ─────────────────────────────────────────────────────

import streamlit as st
from googleapiclient.discovery import build
import google.generativeai as genai


@st.cache_resource   # ← runs only once per app session
def get_youtube_client():
    """
    Builds and returns the YouTube Data API v3 client.

    Reads the key from:
      1. st.secrets (Streamlit Cloud deployment)
      2. Environment variable / .env file (local dev)
    """
    # Try Streamlit secrets first (cloud), then env var (local)
    try:
        api_key = st.secrets["YOUTUBE_API_KEY"]
    except Exception:
        import os
        from dotenv import load_dotenv
        load_dotenv()
        api_key = os.getenv("YOUTUBE_API_KEY", "")

    if not api_key:
        st.error("❌ YOUTUBE_API_KEY not found. Check your .env or Streamlit secrets.")
        st.stop()

    return build("youtube", "v3", developerKey=api_key)


@st.cache_resource
def get_gemini_model():
    """
    Configures and returns the Gemini generative model.
    Uses gemini-1.5-flash — fast and free-tier compatible.
    """
    try:
        api_key = st.secrets["GEMINI_API_KEY"]
    except Exception:
        import os
        from dotenv import load_dotenv
        load_dotenv()
        api_key = os.getenv("GEMINI_API_KEY", "")

    if not api_key:
        st.error("❌ GEMINI_API_KEY not found. Check your .env or Streamlit secrets.")
        st.stop()

    genai.configure(api_key=api_key)
    from config import GEMINI_MODEL
    return genai.GenerativeModel(GEMINI_MODEL)
