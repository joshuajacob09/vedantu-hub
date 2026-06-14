# modules/debug.py — temporary diagnostic page
# DELETE THIS FILE after fixing the API key issue

import streamlit as st

def render():
    st.header("API Key Diagnostic")
    st.caption("Delete this page after fixing.")

    # Check what keys exist in secrets
    st.subheader("1. Keys found in Streamlit secrets:")
    try:
        keys = list(st.secrets.keys())
        for k in keys:
            val = st.secrets[k]
            masked = val[:6] + "..." + val[-4:] if len(val) > 10 else "TOO SHORT"
            st.write(f"**{k}** = `{masked}`")
    except Exception as e:
        st.error(f"Could not read secrets: {e}")

    st.divider()

    # Test Groq connection directly
    st.subheader("2. Groq connection test:")
    try:
        groq_key = st.secrets.get("GROQ_API_KEY", "")
        if not groq_key:
            st.error("GROQ_API_KEY is empty or missing from secrets")
        else:
            st.success(f"GROQ_API_KEY found: `{groq_key[:8]}...`")
            from groq import Groq
            client = Groq(api_key=groq_key)
            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role": "user", "content": "Say OK"}],
                max_tokens=5,
            )
            st.success(f"Groq responded: {response.choices[0].message.content}")
    except Exception as e:
        st.error(f"Groq error: {e}")
