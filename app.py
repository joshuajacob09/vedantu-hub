# app.py — Premium enterprise shell.

import streamlit as st
from config import FOOTER_TEXT
from utils.ui import inject_css, C

st.set_page_config(
    page_title="Vedantu Intelligence",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded",
)

inject_css()

# ── Navigation definition ─────────────────────────────
# (key, icon, label, page_name)
# Icons: clean geometric, no emojis
NAV_ITEMS = [
    ("overview",    "○",  "Morning Briefing",   "Morning Briefing"),
    ("vedantu",     "□",  "Vedantu Channels",   "Vedantu Network"),
    ("competitors", "◇",  "Competitors",        "Competitor Intelligence"),
    ("trends",      "△",  "Trends",             "Trend Detection"),
    ("gaps",        "▽",  "Content Gaps",       "Content Gap Analysis"),
    ("ai",          "✦",  "AI Strategist",      "AI Strategist"),
    ("reports",     "≡",  "Weekly Report",      "Weekly Report"),
    ("search",      "⌕",  "Search",             "Search"),
    ("export",      "↓",  "Export Data",        "Export"),
    ("debug",       "?",  "Debug",              "Debug"),
]

if "page" not in st.session_state:
    st.session_state.page = "Morning Briefing"

# ── Sidebar ───────────────────────────────────────────
with st.sidebar:
    # Brand mark
    st.markdown("""
    <div class="sidebar-brand">
        <div class="sidebar-brand-name">Vedantu Intelligence</div>
        <div class="sidebar-brand-sub">YouTube Operations Platform</div>
    </div>
    <div class="sidebar-sep"></div>
    """, unsafe_allow_html=True)

    # Nav items
    for key, icon, label, page_name in NAV_ITEMS:
        active = st.session_state.page == page_name
        if st.button(
            f"{icon}   {label}",
            key=f"nav_{key}",
            use_container_width=True,
            type="primary" if active else "secondary",
        ):
            st.session_state.page = page_name
            st.rerun()

    # Footer status
    st.markdown("""
    <div style="padding:20px 18px 16px;margin-top:8px;
                border-top:1px solid rgba(255,255,255,0.04);">
        <div class="sidebar-status">
            78 channels tracked<br>
            Data cached 1 hour
        </div>
    </div>
    """, unsafe_allow_html=True)

# ── Error-safe router ─────────────────────────────────
ROUTES = {
    "Morning Briefing":        "modules.dashboard",
    "Vedantu Network":         "modules.vedantu_intelligence",
    "Competitor Intelligence": "modules.competitor_intelligence",
    "Trend Detection":         "modules.trend_detection",
    "Content Gap Analysis":    "modules.content_gap",
    "AI Strategist":           "modules.ai_strategist",
    "Weekly Report":           "modules.weekly_report",
    "Search":                  "modules.search",
    "Export":                  "modules.export",
    "Debug":                   "modules.debug",
}

def _render(module_path: str):
    try:
        import importlib
        importlib.import_module(module_path).render()
    except Exception as e:
        st.error("This page encountered an error. Please try refreshing.")
        with st.expander("Technical details"):
            st.code(str(e))

_render(ROUTES.get(st.session_state.page, "modules.dashboard"))

# ── Footer ────────────────────────────────────────────
st.markdown(
    f'<div class="app-footer">{FOOTER_TEXT}</div>',
    unsafe_allow_html=True,
)
