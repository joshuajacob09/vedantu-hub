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

    st.markdown('<div class="nav-section">Navigation</div>', unsafe_allow_html=True)
    active = st.radio("nav", options=[
        "🌅  Morning Briefing",
        "📄  Weekly Report",
        "🏫  Vedantu Network",
        "🕵️  Competitor Intelligence",
        "📈  Trend Detection",
        "🔍  Content Gap Analysis",
        "🔎  Search",
        "🤖  AI Strategist",
        "⬇️  Export",
    ], label_visibility="collapsed", key="main_nav")

    st.markdown(f'<hr style="border:none;border-top:1px solid {T["border_subtle"]};margin:12px 0 8px 0;"/>', unsafe_allow_html=True)
    st.markdown(f"""
    <div style="font-size:11px;color:{T['text_muted']};line-height:1.8;">
        78 channels tracked<br>
        Data cached 1 hr<br>
        Free tier API
    </div>
    """, unsafe_allow_html=True)

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
