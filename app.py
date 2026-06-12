# app.py — Entry point.

import streamlit as st
from config import APP_TITLE, APP_ICON, FOOTER_TEXT
from utils.ui import inject_css, C

st.set_page_config(
    page_title="Vedantu Intelligence",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded",
)

inject_css()

# ── Sidebar ───────────────────────────────────────────
NAV = [
    ("overview",     "◎",  "Overview",           "Morning Briefing"),
    ("vedantu",      "⊡",  "Vedantu",            "Vedantu Network"),
    ("competitors",  "◈",  "Competitors",        "Competitor Intelligence"),
    ("trends",       "⟳",  "Trends",             "Trend Detection"),
    ("gaps",         "◻",  "Content Gaps",       "Content Gap Analysis"),
    ("ai",           "✦",  "AI Strategist",      "AI Strategist"),
    ("reports",      "⊞",  "Reports",            "Weekly Report"),
    ("search",       "◎",  "Search",             "Search"),
    ("export",       "↓",  "Export",             "Export"),
]

if "page" not in st.session_state:
    st.session_state.page = "Morning Briefing"

with st.sidebar:
    st.markdown(f"""
    <div style="padding:24px 20px 16px;">
        <div style="font-size:13px;font-weight:700;color:#F8FAFC;
                    letter-spacing:-0.01em;">Vedantu Intelligence</div>
        <div style="font-size:11px;color:#334155;margin-top:2px;
                    font-weight:500;">YouTube Operations</div>
    </div>
    <div style="height:1px;background:rgba(255,255,255,0.06);margin:0 8px 8px;"></div>
    """, unsafe_allow_html=True)

    for key, icon, label, page_name in NAV:
        is_active = st.session_state.page == page_name
        active_class = "active" if is_active else ""
        if st.button(
            f"{icon}  {label}",
            key=f"nav_{key}",
            use_container_width=True,
            type="primary" if is_active else "secondary",
        ):
            st.session_state.page = page_name
            st.rerun()

    st.markdown(f"""
    <div style="position:absolute;bottom:0;left:0;right:0;
                padding:16px 20px;border-top:1px solid rgba(255,255,255,0.04);">
        <div style="font-size:11px;color:#334155;line-height:1.9;">
            78 channels · Cached 1h
        </div>
    </div>
    """, unsafe_allow_html=True)

# ── Router ────────────────────────────────────────────
page = st.session_state.page

if   page == "Morning Briefing":
    from modules.dashboard               import render; render()
elif page == "Vedantu Network":
    from modules.vedantu_intelligence    import render; render()
elif page == "Competitor Intelligence":
    from modules.competitor_intelligence import render; render()
elif page == "Trend Detection":
    from modules.trend_detection         import render; render()
elif page == "Content Gap Analysis":
    from modules.content_gap             import render; render()
elif page == "AI Strategist":
    from modules.ai_strategist           import render; render()
elif page == "Weekly Report":
    from modules.weekly_report           import render; render()
elif page == "Search":
    from modules.search                  import render; render()
elif page == "Export":
    from modules.export                  import render; render()
else:
    from modules.dashboard               import render; render()

# ── Footer ────────────────────────────────────────────
st.markdown(
    f'<div class="app-footer">{FOOTER_TEXT}</div>',
    unsafe_allow_html=True,
)
