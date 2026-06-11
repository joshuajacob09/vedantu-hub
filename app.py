# app.py — Entry point. Streamlit runs this file only.

import streamlit as st
from config import APP_TITLE, APP_ICON, FOOTER_TEXT
from utils.ui import inject_css, T

st.set_page_config(
    page_title=APP_TITLE,
    page_icon=APP_ICON,
    layout="wide",
    initial_sidebar_state="expanded",
)

inject_css()

# ── Sidebar ───────────────────────────────────────────
with st.sidebar:
    st.markdown(f"""
    <div style="padding:8px 4px 16px 4px;">
        <div style="font-size:20px;font-weight:700;
                    color:{T['text_primary']};letter-spacing:-0.02em;">
            {APP_ICON} Vedantu
        </div>
        <div style="font-size:12px;font-weight:500;
                    color:{T['text_muted']};margin-top:2px;">
            Content Intelligence Hub
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f'<hr style="border:none;border-top:1px solid {T["border_subtle"]};margin:0 0 8px 0;"/>', unsafe_allow_html=True)

    def nav_label(text):
        st.markdown(f'<div class="nav-section">{text}</div>', unsafe_allow_html=True)

    nav_label("Manager")
    page = st.radio("nav", options=[
        "🌅  Morning Briefing",
        "📄  Weekly Report",
        "🏫  Vedantu Network",
    ], label_visibility="collapsed", key="nav1")

    nav_label("Analyst")
    page2 = st.radio("nav2", options=[
        "🕵️  Competitor Intelligence",
        "📈  Trend Detection",
        "🔍  Content Gap Analysis",
        "🔎  Search",
    ], label_visibility="collapsed", key="nav2")

    nav_label("AI Tools")
    page3 = st.radio("nav3", options=[
        "🤖  AI Strategist",
    ], label_visibility="collapsed", key="nav3")

    nav_label("Data")
    page4 = st.radio("nav4", options=[
        "⬇️  Export",
    ], label_visibility="collapsed", key="nav4")

    st.markdown(f'<hr style="border:none;border-top:1px solid {T["border_subtle"]};margin:12px 0 8px 0;"/>', unsafe_allow_html=True)
    st.markdown(f"""
    <div style="font-size:11px;color:{T['text_muted']};line-height:1.8;">
        78 channels tracked<br>
        Data cached 1 hr<br>
        Free tier API
    </div>
    """, unsafe_allow_html=True)

# ── Active page resolution ────────────────────────────
_all = {"nav1": page, "nav2": page2, "nav3": page3, "nav4": page4}
if "last_nav" not in st.session_state:
    st.session_state.last_nav = "nav1"
for key, val in _all.items():
    if val != st.session_state.get(f"prev_{key}"):
        st.session_state.last_nav = key
        st.session_state[f"prev_{key}"] = val
active = _all[st.session_state.last_nav]

# ── Router ────────────────────────────────────────────
if   active == "🌅  Morning Briefing":
    from modules.dashboard              import render; render()
elif active == "📄  Weekly Report":
    from modules.weekly_report          import render; render()
elif active == "🏫  Vedantu Network":
    from modules.vedantu_intelligence   import render; render()
elif active == "🕵️  Competitor Intelligence":
    from modules.competitor_intelligence import render; render()
elif active == "📈  Trend Detection":
    from modules.trend_detection        import render; render()
elif active == "🔍  Content Gap Analysis":
    from modules.content_gap            import render; render()
elif active == "🔎  Search":
    from modules.search                 import render; render()
elif active == "🤖  AI Strategist":
    from modules.ai_strategist          import render; render()
elif active == "⬇️  Export":
    from modules.export                 import render; render()
else:
    from modules.dashboard              import render; render()

# ── Footer ────────────────────────────────────────────
st.markdown(f'<div class="footer">{FOOTER_TEXT}</div>', unsafe_allow_html=True)
