# utils/ui.py — Enterprise Design System v4
# Inspired by: Apple HIG, Linear, Vercel, Notion
# Zero business logic. Pure presentation layer.

import streamlit as st
from datetime import datetime

# ── Strict token set ──────────────────────────────────
C = {
    # Backgrounds — layered depth
    "bg":           "#080C14",      # deepest — app shell
    "bg_mid":       "#0D1117",      # page body
    "card":         "#0F1623",      # card surface
    "card_hover":   "#131B2A",      # card hover
    "overlay":      "#161D2E",      # elevated overlay

    # Borders
    "border":       "rgba(255,255,255,0.07)",
    "border_mid":   "rgba(255,255,255,0.11)",
    "border_focus": "rgba(99,102,241,0.5)",

    # Accent — Indigo
    "accent":       "#6366F1",
    "accent_light": "#818CF8",
    "accent_dim":   "rgba(99,102,241,0.10)",
    "accent_glow":  "rgba(99,102,241,0.20)",

    # Semantic
    "success":      "#22C55E",
    "success_dim":  "rgba(34,197,94,0.10)",
    "warning":      "#F59E0B",
    "warning_dim":  "rgba(245,158,11,0.10)",
    "danger":       "#EF4444",
    "danger_dim":   "rgba(239,68,68,0.10)",
    "purple":       "#A855F7",
    "purple_dim":   "rgba(168,85,247,0.10)",

    # Typography
    "text":         "#F1F5F9",      # primary
    "text2":        "#94A3B8",      # secondary
    "text3":        "#475569",      # muted
    "text4":        "#2D3B52",      # very muted

    # Charts
    "chart_bg":     "rgba(0,0,0,0)",
}

T = C  # backward-compat alias

# ── Global CSS ────────────────────────────────────────
GLOBAL_CSS = """
<style>
/* ── Fonts ── */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

/* ── Reset ── */
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

html, body, [class*="css"], .stMarkdown, p, span, div {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'SF Pro Text',
                 'Segoe UI', sans-serif !important;
    -webkit-font-smoothing: antialiased !important;
    -moz-osx-font-smoothing: grayscale !important;
    text-rendering: optimizeLegibility !important;
}

/* ── App shell ── */
.stApp {
    background: #080C14 !important;
    background-image:
        radial-gradient(ellipse 80% 50% at 50% -20%,
            rgba(99,102,241,0.06) 0%,
            transparent 100%) !important;
    min-height: 100vh;
}

/* ── Content constraint ── */
.block-container {
    max-width: 1380px !important;
    padding: 0 2.5rem 6rem !important;
    margin: 0 auto !important;
}

/* ── Hide Streamlit chrome ── */
#MainMenu, footer, header,
[data-testid="stToolbar"],
.stDeployButton,
[data-testid="stDecoration"] {
    display: none !important;
}

/* ══════════════════════════════════════
   SIDEBAR
══════════════════════════════════════ */
section[data-testid="stSidebar"] {
    background: #0A0F1A !important;
    border-right: 1px solid rgba(255,255,255,0.055) !important;
    width: 228px !important;
}
section[data-testid="stSidebar"] > div { padding: 0 !important; }

/* Sidebar nav buttons */
section[data-testid="stSidebar"] .stButton > button {
    background: transparent !important;
    border: none !important;
    border-radius: 8px !important;
    color: #64748B !important;
    font-size: 12.5px !important;
    font-weight: 500 !important;
    text-align: left !important;
    padding: 8px 12px 8px 14px !important;
    height: auto !important;
    width: calc(100% - 16px) !important;
    margin: 1px 8px !important;
    transition: background 0.12s ease, color 0.12s ease !important;
    box-shadow: none !important;
    letter-spacing: 0.005em !important;
}
section[data-testid="stSidebar"] .stButton > button:hover {
    background: rgba(255,255,255,0.04) !important;
    color: #CBD5E1 !important;
    transform: none !important;
    box-shadow: none !important;
}
section[data-testid="stSidebar"] .stButton > button[kind="primary"] {
    background: rgba(99,102,241,0.12) !important;
    color: #E0E7FF !important;
    border: none !important;
    font-weight: 600 !important;
}
section[data-testid="stSidebar"] .stButton > button[kind="primary"]:hover {
    background: rgba(99,102,241,0.16) !important;
}

/* ══════════════════════════════════════
   METRIC CARDS
══════════════════════════════════════ */
div[data-testid="metric-container"] {
    background: #0F1623 !important;
    border: 1px solid rgba(255,255,255,0.07) !important;
    border-radius: 14px !important;
    padding: 22px 24px !important;
    box-shadow:
        0 1px 3px rgba(0,0,0,0.3),
        0 4px 12px rgba(0,0,0,0.2),
        inset 0 1px 0 rgba(255,255,255,0.04) !important;
    transition: border-color 0.2s ease, box-shadow 0.2s ease !important;
}
div[data-testid="metric-container"]:hover {
    border-color: rgba(255,255,255,0.12) !important;
    box-shadow:
        0 1px 3px rgba(0,0,0,0.3),
        0 8px 24px rgba(0,0,0,0.25),
        inset 0 1px 0 rgba(255,255,255,0.05) !important;
}
div[data-testid="metric-container"] [data-testid="stMetricLabel"] {
    font-size: 10.5px !important;
    font-weight: 600 !important;
    letter-spacing: 0.09em !important;
    color: #475569 !important;
    text-transform: uppercase !important;
}
div[data-testid="metric-container"] [data-testid="stMetricValue"] {
    font-size: 30px !important;
    font-weight: 700 !important;
    color: #F1F5F9 !important;
    letter-spacing: -0.04em !important;
    line-height: 1.05 !important;
}
div[data-testid="metric-container"] [data-testid="stMetricDelta"] {
    font-size: 12px !important;
    font-weight: 500 !important;
    margin-top: 4px !important;
}

/* ══════════════════════════════════════
   TYPOGRAPHY
══════════════════════════════════════ */
h1 {
    font-size: 26px !important;
    font-weight: 700 !important;
    color: #F1F5F9 !important;
    letter-spacing: -0.04em !important;
    line-height: 1.18 !important;
    margin: 0 !important;
}
h2 {
    font-size: 18px !important;
    font-weight: 600 !important;
    color: #E2E8F0 !important;
    letter-spacing: -0.025em !important;
    line-height: 1.3 !important;
    margin: 0 !important;
}
h3 {
    font-size: 14px !important;
    font-weight: 600 !important;
    color: #94A3B8 !important;
    letter-spacing: -0.01em !important;
}
p, li {
    font-size: 14px !important;
    color: #94A3B8 !important;
    line-height: 1.65 !important;
}

/* ══════════════════════════════════════
   BUTTONS
══════════════════════════════════════ */
/* Main content buttons */
.block-container .stButton > button {
    height: 36px !important;
    border-radius: 8px !important;
    font-size: 13px !important;
    font-weight: 600 !important;
    letter-spacing: 0.005em !important;
    border: 1px solid rgba(255,255,255,0.09) !important;
    background: #0F1623 !important;
    color: #CBD5E1 !important;
    transition: all 0.15s ease !important;
    padding: 0 18px !important;
    box-shadow: 0 1px 2px rgba(0,0,0,0.3),
                inset 0 1px 0 rgba(255,255,255,0.04) !important;
}
.block-container .stButton > button:hover {
    border-color: rgba(255,255,255,0.15) !important;
    background: #161D2E !important;
    color: #F1F5F9 !important;
    transform: none !important;
    box-shadow: 0 2px 6px rgba(0,0,0,0.35),
                inset 0 1px 0 rgba(255,255,255,0.05) !important;
}
.block-container .stButton > button[kind="primary"] {
    background: linear-gradient(135deg, #6366F1 0%, #5254E7 100%) !important;
    border-color: rgba(99,102,241,0.4) !important;
    color: #fff !important;
    box-shadow: 0 1px 3px rgba(0,0,0,0.3),
                0 0 0 0 rgba(99,102,241,0),
                inset 0 1px 0 rgba(255,255,255,0.15) !important;
}
.block-container .stButton > button[kind="primary"]:hover {
    background: linear-gradient(135deg, #7173F3 0%, #6163EA 100%) !important;
    border-color: rgba(129,140,248,0.5) !important;
    box-shadow: 0 2px 8px rgba(99,102,241,0.35),
                0 0 20px rgba(99,102,241,0.12),
                inset 0 1px 0 rgba(255,255,255,0.18) !important;
}

/* ══════════════════════════════════════
   FORM INPUTS
══════════════════════════════════════ */
div[data-testid="stSelectbox"] > div > div,
div[data-testid="stTextInput"] > div > div input,
div[data-testid="stMultiSelect"] > div > div {
    background: #0F1623 !important;
    border: 1px solid rgba(255,255,255,0.08) !important;
    border-radius: 9px !important;
    color: #E2E8F0 !important;
    font-size: 13.5px !important;
    box-shadow: 0 1px 2px rgba(0,0,0,0.2) !important;
    transition: border-color 0.15s ease !important;
}
div[data-testid="stSelectbox"] > div > div:focus-within,
div[data-testid="stTextInput"] > div > div:focus-within {
    border-color: rgba(99,102,241,0.45) !important;
    box-shadow: 0 0 0 3px rgba(99,102,241,0.12) !important;
}

/* ══════════════════════════════════════
   DATAFRAME / TABLES
══════════════════════════════════════ */
div[data-testid="stDataFrame"] {
    border-radius: 12px !important;
    border: 1px solid rgba(255,255,255,0.07) !important;
    overflow: hidden !important;
    box-shadow: 0 1px 3px rgba(0,0,0,0.25),
                0 4px 12px rgba(0,0,0,0.15) !important;
}
div[data-testid="stDataFrame"] [data-testid="stDataFrameResizable"] {
    border-radius: 12px !important;
}

/* ══════════════════════════════════════
   TABS
══════════════════════════════════════ */
.stTabs [data-baseweb="tab-list"] {
    background: #0F1623 !important;
    border: 1px solid rgba(255,255,255,0.07) !important;
    border-radius: 10px !important;
    padding: 3px !important;
    gap: 2px !important;
    box-shadow: 0 1px 3px rgba(0,0,0,0.2) !important;
}
.stTabs [data-baseweb="tab"] {
    border-radius: 7px !important;
    font-size: 13px !important;
    font-weight: 500 !important;
    color: #64748B !important;
    padding: 6px 16px !important;
    border: none !important;
    transition: all 0.12s ease !important;
}
.stTabs [data-baseweb="tab"]:hover {
    color: #94A3B8 !important;
    background: rgba(255,255,255,0.03) !important;
}
.stTabs [aria-selected="true"] {
    background: rgba(255,255,255,0.06) !important;
    color: #E2E8F0 !important;
    box-shadow: 0 1px 3px rgba(0,0,0,0.2),
                inset 0 1px 0 rgba(255,255,255,0.05) !important;
}

/* ══════════════════════════════════════
   EXPANDER
══════════════════════════════════════ */
div[data-testid="stExpander"] {
    background: #0F1623 !important;
    border: 1px solid rgba(255,255,255,0.07) !important;
    border-radius: 12px !important;
    box-shadow: 0 1px 3px rgba(0,0,0,0.2) !important;
    overflow: hidden !important;
}
div[data-testid="stExpander"] summary {
    font-size: 13px !important;
    font-weight: 500 !important;
    color: #64748B !important;
    padding: 14px 18px !important;
    transition: color 0.12s !important;
}
div[data-testid="stExpander"] summary:hover { color: #94A3B8 !important; }

/* ══════════════════════════════════════
   ALERTS
══════════════════════════════════════ */
.stAlert {
    border-radius: 10px !important;
    font-size: 13px !important;
    border-width: 1px !important;
}

/* ══════════════════════════════════════
   PROGRESS
══════════════════════════════════════ */
.stProgress > div > div > div {
    background: linear-gradient(90deg, #6366F1, #818CF8) !important;
    border-radius: 99px !important;
    box-shadow: 0 0 8px rgba(99,102,241,0.4) !important;
}
.stProgress > div > div {
    background: rgba(255,255,255,0.05) !important;
    border-radius: 99px !important;
}

/* ══════════════════════════════════════
   SPINNER
══════════════════════════════════════ */
.stSpinner > div {
    border-color: rgba(255,255,255,0.06) !important;
    border-top-color: #6366F1 !important;
}

/* ══════════════════════════════════════
   RADIO
══════════════════════════════════════ */
.stRadio > div { gap: 4px !important; }
.stRadio label {
    font-size: 13px !important;
    color: #64748B !important;
    font-weight: 500 !important;
    padding: 6px 12px !important;
    border-radius: 7px !important;
    border: 1px solid rgba(255,255,255,0.06) !important;
    background: #0F1623 !important;
    cursor: pointer !important;
    transition: all 0.12s !important;
}
.stRadio label:has(input:checked) {
    color: #E2E8F0 !important;
    background: rgba(99,102,241,0.1) !important;
    border-color: rgba(99,102,241,0.3) !important;
}

/* ══════════════════════════════════════
   CAPTION
══════════════════════════════════════ */
.stCaption {
    font-size: 12px !important;
    color: #334155 !important;
    letter-spacing: 0.01em !important;
}

/* ══════════════════════════════════════
   DIVIDER
══════════════════════════════════════ */
hr {
    border: none !important;
    border-top: 1px solid rgba(255,255,255,0.055) !important;
    margin: 32px 0 !important;
}

/* ══════════════════════════════════════
   SCROLLBAR
══════════════════════════════════════ */
::-webkit-scrollbar { width: 4px; height: 4px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb {
    background: rgba(255,255,255,0.08);
    border-radius: 99px;
}
::-webkit-scrollbar-thumb:hover { background: rgba(255,255,255,0.14); }

/* ══════════════════════════════════════
   SIDEBAR EXTRAS
══════════════════════════════════════ */
.sidebar-brand {
    padding: 22px 18px 14px;
}
.sidebar-brand-name {
    font-size: 13px;
    font-weight: 700;
    color: #E2E8F0;
    letter-spacing: -0.02em;
}
.sidebar-brand-sub {
    font-size: 11px;
    color: #334155;
    margin-top: 3px;
    font-weight: 500;
    letter-spacing: 0.01em;
}
.sidebar-sep {
    height: 1px;
    background: rgba(255,255,255,0.055);
    margin: 0 12px 8px;
}
.sidebar-section-label {
    font-size: 10px;
    font-weight: 700;
    letter-spacing: 0.1em;
    color: #1E293B;
    text-transform: uppercase;
    padding: 14px 20px 5px;
}
.sidebar-status {
    font-size: 11px;
    color: #334155;
    line-height: 1.8;
    letter-spacing: 0.01em;
}

/* ══════════════════════════════════════
   FOOTER
══════════════════════════════════════ */
.app-footer {
    position: fixed; bottom: 0; left: 0; right: 0;
    height: 36px;
    display: flex; align-items: center; justify-content: center;
    background: rgba(8,12,20,0.95);
    backdrop-filter: blur(12px);
    -webkit-backdrop-filter: blur(12px);
    border-top: 1px solid rgba(255,255,255,0.045);
    font-size: 11px;
    color: #1E293B;
    letter-spacing: 0.05em;
    z-index: 999;
}

/* ══════════════════════════════════════
   CUSTOM COMPONENTS
══════════════════════════════════════ */

/* Page header bottom rule */
.page-header-rule {
    border: none;
    border-top: 1px solid rgba(255,255,255,0.055);
    margin: 0 0 28px;
}

/* Data timestamp */
.data-ts {
    font-size: 11px;
    color: #2D3B52;
    text-align: right;
    margin-bottom: 10px;
    letter-spacing: 0.02em;
}

/* ══════════════════════════════════════
   MOBILE
══════════════════════════════════════ */
@media (max-width: 768px) {
    h1 { font-size: 20px !important; }
    h2 { font-size: 16px !important; }
    .block-container { padding: 0 1rem 5rem !important; }
    section[data-testid="stSidebar"] { width: 100% !important; }
}
</style>
"""


# ─────────────────────────────────────────────────────
# Component library
# ─────────────────────────────────────────────────────

def inject_css():
    st.markdown(GLOBAL_CSS, unsafe_allow_html=True)


def page_header(title: str, subtitle: str = "", right_content: str = ""):
    ts    = datetime.now().strftime("%H:%M")
    right = right_content or (
        f'<span style="font-size:11px;color:{C["text4"]};letter-spacing:.03em;">'
        f'Updated {ts}</span>'
    )
    st.markdown(f"""
    <div style="display:flex;justify-content:space-between;align-items:flex-start;
                padding:32px 0 22px;">
        <div>
            <h1>{title}</h1>
            {'<p style="margin:7px 0 0;font-size:13.5px;color:'+C["text3"]+';line-height:1.5;font-weight:400;">'+subtitle+'</p>' if subtitle else ''}
        </div>
        <div style="padding-top:5px;flex-shrink:0;margin-left:24px;">{right}</div>
    </div>
    <div class="page-header-rule"></div>
    """, unsafe_allow_html=True)


def section_header(title: str, subtitle: str = ""):
    st.markdown(f"""
    <div style="margin:32px 0 16px;">
        <h2>{title}</h2>
        {'<p style="font-size:12.5px;color:'+C["text3"]+';margin:5px 0 0;font-weight:400;">'+subtitle+'</p>' if subtitle else ''}
    </div>
    """, unsafe_allow_html=True)


def kpi_card(label: str, value: str, delta: str = "",
             delta_positive: bool = True, sublabel: str = "",
             accent_color: str = ""):
    display_value = value if value and str(value) not in ("None","","nan") else "—"
    delta_c  = C["success"] if delta_positive else C["danger"]
    delta_bg = C["success_dim"] if delta_positive else C["danger_dim"]
    arrow    = "↑" if delta_positive else "↓"

    delta_html = f"""
        <div style="display:inline-flex;align-items:center;gap:3px;
                    background:{delta_bg};border-radius:5px;
                    padding:2px 7px;margin-top:9px;">
            <span style="font-size:11px;font-weight:600;color:{delta_c};">
                {arrow} {delta}
            </span>
        </div>""" if delta else ""

    sub_html = (
        f'<div style="font-size:11.5px;color:{C["text3"]};'
        f'margin-top:7px;font-weight:400;">{sublabel}</div>'
    ) if sublabel else ""

    top_accent = (
        f"border-top:2px solid {accent_color};"
    ) if accent_color else ""

    shadow = "0 1px 3px rgba(0,0,0,0.25),0 4px 12px rgba(0,0,0,0.15),inset 0 1px 0 rgba(255,255,255,0.03)"
    st.markdown(f"""
    <div style="background:{C['card']};border:1px solid {C['border']};border-radius:14px;padding:22px 24px;height:100%;{top_accent}box-shadow:{shadow};transition:border-color .2s;">
        <div style="font-size:10.5px;font-weight:600;letter-spacing:0.09em;
                    color:{C['text3']};text-transform:uppercase;
                    margin-bottom:11px;">{label}</div>
        <div style="font-size:30px;font-weight:700;color:{C['text']};
                    letter-spacing:-0.04em;line-height:1.05;">{display_value}</div>
        {delta_html}
        {sub_html}
    </div>
    """, unsafe_allow_html=True)


def insight_card(priority: str, title: str, reason: str,
                 action: str, confidence: int = 0, impact: str = ""):
    pmap = {
        "HIGH":   (C["danger"],  C["danger_dim"]),
        "MEDIUM": (C["warning"], C["warning_dim"]),
        "LOW":    (C["accent"],  C["accent_dim"]),
    }
    c, bg = pmap.get(priority.upper(), pmap["MEDIUM"])

    conf_html = f"""
        <div style="display:flex;align-items:center;gap:10px;margin-top:14px;">
            <div style="flex:1;height:2px;background:rgba(255,255,255,0.05);
                        border-radius:99px;overflow:hidden;">
                <div style="width:{confidence}%;height:100%;
                            background:{c};border-radius:99px;"></div>
            </div>
            <span style="font-size:11px;color:{C['text3']};white-space:nowrap;">
                {confidence}%</span>
        </div>""" if confidence else ""

    impact_html = (
        f'<div style="font-size:12px;color:{C["text3"]};margin-top:10px;'
        f'padding-top:10px;border-top:1px solid {C["border"]};">{impact}</div>'
    ) if impact else ""

    st.markdown(f"""
    <div style="background:{C['card']};border:1px solid {C['border']};border-left:2px solid {c};border-radius:12px;padding:18px 20px;margin-bottom:10px;box-shadow:0 1px 3px rgba(0,0,0,0.2);transition:border-color .15s;">
        <div style="display:flex;align-items:center;gap:9px;margin-bottom:11px;">
            <span style="background:{bg};color:{c};
                         font-size:9.5px;font-weight:700;
                         letter-spacing:0.09em;border-radius:4px;
                         padding:2px 8px;text-transform:uppercase;">{priority}</span>
            <span style="font-size:14px;font-weight:600;color:{C['text']};
                         letter-spacing:-0.01em;">{title}</span>
        </div>
        <p style="font-size:13px;color:{C['text2']};margin:0 0 12px;
                  line-height:1.6;">{reason}</p>
        <div style="background:rgba(255,255,255,0.025);
                    border-radius:8px;padding:11px 14px;
                    border-left:2px solid rgba(255,255,255,0.08);">
            <div style="font-size:9.5px;font-weight:700;letter-spacing:0.09em;
                        color:{C['text4']};margin-bottom:5px;
                        text-transform:uppercase;">Suggested Action</div>
            <div style="font-size:13px;color:{C['text']};
                        line-height:1.55;">{action}</div>
        </div>
        {conf_html}{impact_html}
    </div>
    """, unsafe_allow_html=True)


def alert_card(message: str, type: str = "info"):
    cmap = {
        "info":    (C["accent"],  C["accent_dim"],  "·"),
        "warning": (C["warning"], C["warning_dim"], "·"),
        "success": (C["success"], C["success_dim"], "·"),
        "danger":  (C["danger"],  C["danger_dim"],  "·"),
    }
    c, bg, icon = cmap.get(type, cmap["info"])
    st.markdown(f"""
    <div style="background:{bg};
                border:1px solid {c}22;
                border-left:2px solid {c};
                border-radius:9px;
                padding:10px 16px;
                display:flex;align-items:flex-start;gap:10px;
                margin-bottom:9px;">
        <span style="color:{c};font-size:16px;flex-shrink:0;
                     margin-top:-1px;line-height:1.4;">{icon}</span>
        <span style="color:{C['text2']};font-size:13px;
                     line-height:1.55;">{message}</span>
    </div>
    """, unsafe_allow_html=True)


def report_section(title: str, content: str):
    st.markdown(f"""
    <div style="background:{C['card']};
                border:1px solid {C['border']};
                border-radius:12px;
                padding:22px 26px;
                margin-bottom:12px;
                box-shadow:0 1px 3px rgba(0,0,0,0.2);">
        <div style="font-size:10px;font-weight:700;letter-spacing:.12em;
                    color:{C['accent']};text-transform:uppercase;
                    margin-bottom:14px;">{title}</div>
        <div style="font-size:13.5px;color:{C['text2']};
                    line-height:1.75;">{content}</div>
    </div>
    """, unsafe_allow_html=True)


def data_timestamp():
    ts = datetime.now().strftime("%d %b %Y, %H:%M")
    st.markdown(
        f'<div class="data-ts">Data as of {ts} · Cached 1h</div>',
        unsafe_allow_html=True,
    )


def empty_state(message: str, icon: str = ""):
    icon_html = (
        f'<div style="font-size:20px;margin-bottom:12px;'
        f'opacity:0.2;filter:grayscale(1);">{icon}</div>'
    ) if icon else ""
    st.markdown(f"""
    <div style="text-align:center;padding:52px 24px;
                background:{C['card']};
                border:1px dashed rgba(255,255,255,0.07);
                border-radius:14px;">
        {icon_html}
        <div style="font-size:13.5px;color:{C['text3']};
                    font-weight:500;letter-spacing:-0.01em;">{message}</div>
    </div>
    """, unsafe_allow_html=True)


def divider():
    st.markdown(
        '<hr style="border:none;border-top:1px solid rgba(255,255,255,0.055);'
        'margin:32px 0;"/>',
        unsafe_allow_html=True,
    )


def badge(text: str, color: str = "accent") -> str:
    c  = C.get(color, C["accent"])
    bg = C.get(f"{color}_dim", C["accent_dim"])
    return (
        f'<span style="background:{bg};color:{c};border-radius:4px;'
        f'padding:2px 9px;font-size:10px;font-weight:700;'
        f'letter-spacing:0.07em;text-transform:uppercase;">{text}</span>'
    )


def plotly_defaults(height: int = 320) -> dict:
    return dict(
        template="plotly_dark",
        paper_bgcolor=C["chart_bg"],
        plot_bgcolor=C["chart_bg"],
        font=dict(
            family="Inter, -apple-system, sans-serif",
            color=C["text3"],
            size=12,
        ),
        title_font=dict(
            family="Inter, -apple-system, sans-serif",
            color=C["text2"],
            size=14,
        ),
        margin=dict(l=0, r=4, t=42, b=0),
        height=height,
        xaxis=dict(
            gridcolor="rgba(255,255,255,0.035)",
            linecolor="rgba(255,255,255,0.035)",
            tickfont=dict(size=11, color=C["text3"]),
            showgrid=True,
            zeroline=False,
        ),
        yaxis=dict(
            gridcolor="rgba(255,255,255,0.035)",
            linecolor="rgba(255,255,255,0.035)",
            tickfont=dict(size=11, color=C["text3"]),
            showgrid=False,
            zeroline=False,
        ),
    )
