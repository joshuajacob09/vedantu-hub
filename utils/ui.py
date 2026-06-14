# utils/api_clients.py
# ─────────────────────────────────────────────────────
# Handles YouTube and Groq (LLM) API connections.
#
# WHY GROQ:
#   - 14,400 free requests/day (vs Gemini's 1,500)
#   - No quota hangs — instant responses
#   - Uses llama-3.3-70b — smarter than Gemini Flash
#   - Same interface as before — zero changes in modules
#
# The GroqModel wrapper makes Groq's API look identical
# to Gemini's .generate_content(prompt) pattern so all
# existing module code works without any changes.
# ─────────────────────────────────────────────────────

import streamlit as st
from googleapiclient.discovery import build


def _get_key(name: str) -> str:
    """Read API key from Streamlit secrets or .env file."""
    try:
        return st.secrets[name]
    except Exception:
        pass
    try:
        import os
        from dotenv import load_dotenv
        load_dotenv()
        return os.getenv(name, "")
    except Exception:
        return ""


# ── YouTube client ────────────────────────────────────
@st.cache_resource
def get_youtube_client():
    api_key = _get_key("YOUTUBE_API_KEY")
    if not api_key:
        st.error("YOUTUBE_API_KEY not found. Add it to .env or Streamlit secrets.")
        st.stop()
    return build("youtube", "v3", developerKey=api_key)


# ── Groq wrapper — mimics Gemini's .generate_content() ─
class _GroqResponse:
    """Wraps Groq response to match Gemini's response.text interface."""
    def __init__(self, text: str):
        self.text = text


class _GroqModel:
    """
    Drop-in replacement for Gemini's GenerativeModel.
    Usage: model.generate_content(prompt) → response.text
    Identical to how modules already call get_gemini_model().
    """
    def __init__(self, client, model_name: str):
        self._client     = client
        self._model_name = model_name

    def generate_content(self, prompt: str) -> _GroqResponse:
        completion = self._client.chat.completions.create(
            model=self._model_name,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=4096,
        )
        return _GroqResponse(completion.choices[0].message.content)


@st.cache_resource
def get_gemini_model() -> _GroqModel:
    """
    Returns a Groq-backed model with the same interface as Gemini.
    All modules call this exactly as before — nothing changes.
    """
    api_key = _get_key("GROQ_API_KEY")
    if not api_key:
        st.error(
            "GROQ_API_KEY not found. "
            "Get a free key at https://console.groq.com "
            "then add it to your .env file or Streamlit secrets."
        )
        st.stop()

    try:
        from groq import Groq
    except ImportError:
        st.error("Groq package not installed. Run: pip install groq")
        st.stop()

    client = Groq(api_key=api_key)
    return _GroqModel(client, "llama-3.3-70b-versatile")
