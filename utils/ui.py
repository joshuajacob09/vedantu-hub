# utils/ui.py
# ─────────────────────────────────────────────────────
# Vedantu Content Intelligence Hub — Design System
#
# Single source of truth for all UI primitives.
# Every module imports from here. Never write inline
# style strings in module files.
#
# Token structure mirrors Apple HIG:
#   Colors → Typography → Spacing → Components
# ─────────────────────────────────────────────────────

import streamlit as st

# ── Design tokens ─────────────────────────────────────
TOKENS = {
    # Backgrounds
    "bg_base":        "#0a0c12",
    "bg_surface":     "#111318",
    "bg_elevated":    "#181b24",
    "bg_overlay":     "#1e2130",

    # Borders
    "border_subtle":  "#1f2335",
    "border_default": "#2a2d3e",
    "border_strong":  "#3a3d52",

    # Brand
    "indigo":         "#6366f1",
    "indigo_dim":     "#6366f118",
    "indigo_glow":    "#6366f130",

    # Semantic
    "green":          "#22c55e",
    "green_dim":      "#22c55e18",
    "amber":          "#f59e0b",
    "amber_dim":      "#f59e0b18",
    "red":            "#ef4444",
    "red_dim":        "#ef444418",
    "purple":         "#a855f7",
    "purple_dim":     "#a855f718",

    # Text
    "text_primary":   "#e8eaf2",
    "text_secondary": "#8b91a8",
    "text_muted":     "#4b5568",
    "text_accent":    "#6366f1",

    # Chart
    "chart_bg":       "rgba(0,0,0,0)",
}

T = TOKENS   # shorthand


# ── Global CSS injected once in app.py ───────────────
GLOBAL_CSS = f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:ital,wght@0,300;0,400;0,500;0,600;0,700;1,400&display=swap');

/* ── Reset & base ── */
html, body, [class*="css"], .stMarkdown, .stText {{
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
    -webkit-font-smoothing: antialiased;
}}

.stApp {{
    background-color: {T['bg_base']};
    background-image: radial-gradient(ellipse at 20% 0%, #6366f10a 0%, transparent 60%);
}}

/* ── Sidebar ── */
section[data-testid="stSidebar"] {{
    background: {T['bg_surface']} !important;
    border-right: 1px solid {T['border_subtle']} !important;
}}
section[data-testid="stSidebar"] .stRadio label {{
    font-size: 13px !important;
    font-weight: 500;
    color: {T['text_secondary']};
    padding: 6px 10px;
    border-radius: 8px;
    transition: color 0.15s;
}}
section[data-testid="stSidebar"] .stRadio label:hover {{
    color: {T['text_primary']};
}}

/* ── Metric cards ── */
div[data-testid="metric-container"] {{
    background: {T['bg_elevated']};
    border: 1px solid {T['border_default']};
    border-radius: 14px;
    padding: 18px 20px;
    transition: border-color 0.2s;
}}
div[data-testid="metric-container"]:hover {{
    border-color: {T['border_strong']};
}}
div[data-testid="metric-container"] [data-testid="stMetricLabel"] {{
    font-size: 11px !important;
    font-weight: 600 !important;
    letter-spacing: 0.06em;
    color: {T['text_muted']} !important;
    text-transform: uppercase;
}}
div[data-testid="metric-container"] [data-testid="stMetricValue"] {{
    font-size: 24px !important;
    font-weight: 700 !important;
    color: {T['text_primary']} !important;
    letter-spacing: -0.02em;
}}
div[data-testid="metric-container"] [data-testid="stMetricDelta"] {{
    font-size: 12px !important;
    font-weight: 500 !important;
}}

/* ── Headings ── */
h1 {{
    font-size: 26px !important;
    font-weight: 700 !important;
    color: {T['text_primary']} !important;
    letter-spacing: -0.03em !important;
    line-height: 1.2 !important;
}}
h2 {{
    font-size: 18px !important;
    font-weight: 600 !important;
    color: {T['text_primary']} !important;
    letter-spacing: -0.02em !important;
}}
h3 {{
    font-size: 14px !important;
    font-weight: 600 !important;
    color: {T['text_secondary']} !important;
    letter-spacing: 0.01em !important;
}}

/* ── Caption / small text ── */
.stCaption, .caption, small {{
    font-size: 12px !important;
    color: {T['text_muted']} !important;
}}

/* ── Buttons ── */
.stButton > button {{
    border-radius: 10px !important;
    font-weight: 600 !important;
    font-size: 13px !important;
    letter-spacing: 0.01em;
    padding: 8px 20px !important;
    border: 1px solid {T['border_default']} !important;
    transition: all 0.15s ease !important;
}}
.stButton > button:hover {{
    border-color: {T['border_strong']} !important;
    transform: translateY(-1px);
    box-shadow: 0 4px 20px rgba(99,102,241,0.15) !important;
}}
.stButton > button[kind="primary"] {{
    background: linear-gradient(135deg, #6366f1, #818cf8) !important;
    border-color: transparent !important;
    color: white !important;
}}

/* ── Dataframe ── */
div[data-testid="stDataFrame"] {{
    border-radius: 12px !important;
    overflow: hidden !important;
    border: 1px solid {T['border_default']} !important;
}}

/* ── Tabs ── */
.stTabs [data-baseweb="tab-list"] {{
    background: {T['bg_surface']} !important;
    border-radius: 10px !important;
    padding: 4px !important;
    gap: 2px !important;
    border: 1px solid {T['border_subtle']} !important;
}}
.stTabs [data-baseweb="tab"] {{
    border-radius: 8px !important;
    font-weight: 500 !important;
    font-size: 13px !important;
    color: {T['text_secondary']} !important;
    padding: 6px 16px !important;
}}
.stTabs [aria-selected="true"] {{
    background: {T['bg_elevated']} !important;
    color: {T['text_primary']} !important;
}}

/* ── Expander ── */
div[data-testid="stExpander"] {{
    background: {T['bg_elevated']} !important;
    border: 1px solid {T['border_subtle']} !important;
    border-radius: 12px !important;
}}

/* ── Alerts ── */
.stAlert {{
    border-radius: 10px !important;
    font-size: 13px !important;
    border-width: 1px !important;
}}

/* ── Selectbox / inputs ── */
div[data-testid="stSelectbox"] > div,
div[data-testid="stTextInput"] > div > div {{
    border-radius: 10px !important;
    border-color: {T['border_default']} !important;
    background: {T['bg_elevated']} !important;
    font-size: 13px !important;
}}

/* ── Radio ── */
.stRadio [data-testid="stWidgetLabel"] {{
    font-size: 12px !important;
    font-weight: 600 !important;
    color: {T['text_muted']} !important;
    text-transform: uppercase;
    letter-spacing: 0.06em;
}}

/* ── Progress bar ── */
.stProgress > div > div > div {{
    background: linear-gradient(90deg, #6366f1, #818cf8) !important;
    border-radius: 99px !important;
}}

/* ── Divider ── */
hr {{
    border-color: {T['border_subtle']} !important;
    margin: 20px 0 !important;
}}

/* ── Spinner ── */
.stSpinner > div {{
    border-top-color: {T['indigo']} !important;
}}

/* ── Scrollbar ── */
::-webkit-scrollbar {{ width: 4px; height: 4px; }}
::-webkit-scrollbar-track {{ background: {T['bg_base']}; }}
::-webkit-scrollbar-thumb {{ background: {T['border_strong']}; border-radius: 99px; }}

/* ── Nav section labels ── */
.nav-section {{
    font-size: 10px;
    font-weight: 700;
    letter-spacing: 0.12em;
    color: {T['text_muted']};
    text-transform: uppercase;
    padding: 12px 0 4px 2px;
}}

/* ── Page header ── */
.page-header {{
    padding-bottom: 8px;
    margin-bottom: 4px;
}}
.page-header h1 {{ margin-bottom: 2px !important; }}

/* ── Footer ── */
.footer {{
    position: fixed; bottom: 0; left: 0; right: 0;
    text-align: center; padding: 7px;
    background: {T['bg_surface']};
    color: {T['text_muted']};
    font-size: 11px;
    border-top: 1px solid {T['border_subtle']};
    z-index: 999;
    letter-spacing: 0.03em;
}}
</style>
"""


# ── Component library ─────────────────────────────────

def inject_css():
    """Call once at the top of app.py."""
    st.markdown(GLOBAL_CSS, unsafe_allow_html=True)


def page_header(title: str, subtitle: str = "", icon: str = ""):
    """Consistent page header with title and optional subtitle."""
    full_title = f"{icon} {title}" if icon else title
    st.markdown(f"""
    <div class="page-header">
        <h1>{full_title}</h1>
        {'<p style="color:'+T['text_muted']+';font-size:13px;margin:0;line-height:1.5;">'+subtitle+'</p>' if subtitle else ''}
    </div>
    """, unsafe_allow_html=True)


def section_header(title: str, subtitle: str = ""):
    """Section divider with title."""
    st.markdown(f"""
    <div style="margin: 28px 0 12px 0;">
        <h2 style="margin:0;">{title}</h2>
        {'<p style="color:'+T['text_muted']+';font-size:12px;margin:4px 0 0 0;">'+subtitle+'</p>' if subtitle else ''}
    </div>
    """, unsafe_allow_html=True)


def kpi_card(title: str, value: str, subtitle: str = "",
             color: str = None, icon: str = ""):
    """
    Glass KPI card.
    color: 'green' | 'red' | 'amber' | 'indigo' | 'purple' | None
    """
    c = T.get(color, T["indigo"]) if color else T["indigo"]
    c_dim = T.get(f"{color}_dim", T["indigo_dim"]) if color else T["indigo_dim"]
    icon_html = f'<span style="font-size:18px;margin-bottom:6px;display:block;">{icon}</span>' if icon else ""
    st.markdown(f"""
    <div style="
        background: linear-gradient(145deg, {T['bg_elevated']}, {T['bg_surface']});
        border: 1px solid {T['border_default']};
        border-top: 2px solid {c};
        border-radius: 14px;
        padding: 18px 20px;
        height: 100%;
    ">
        {icon_html}
        <div style="font-size:10px;font-weight:700;letter-spacing:.1em;
                    color:{T['text_muted']};text-transform:uppercase;
                    margin-bottom:8px;">{title}</div>
        <div style="font-size:26px;font-weight:700;color:{T['text_primary']};
                    letter-spacing:-0.03em;line-height:1;">{value}</div>
        {'<div style="font-size:12px;color:'+T['text_muted']+';margin-top:6px;">'+subtitle+'</div>' if subtitle else ""}
    </div>
    """, unsafe_allow_html=True)


def glass_card(content_html: str, color: str = "default",
               padding: str = "20px 24px"):
    """
    Generic glass card wrapper.
    color: 'default' | 'green' | 'red' | 'amber' | 'indigo' | 'purple'
    """
    border = {
        "default": T["border_default"],
        "green":   T["green"],
        "red":     T["red"],
        "amber":   T["amber"],
        "indigo":  T["indigo"],
        "purple":  T["purple"],
    }.get(color, T["border_default"])

    bg = {
        "default": T["bg_elevated"],
        "green":   T["green_dim"],
        "red":     T["red_dim"],
        "amber":   T["amber_dim"],
        "indigo":  T["indigo_dim"],
        "purple":  T["purple_dim"],
    }.get(color, T["bg_elevated"])

    st.markdown(f"""
    <div style="
        background:{bg};
        border:1px solid {border};
        border-radius:14px;
        padding:{padding};
        margin-bottom:12px;
    ">{content_html}</div>
    """, unsafe_allow_html=True)


def badge(text: str, color: str = "indigo") -> str:
    """Inline badge HTML — use inside glass_card content."""
    c     = T.get(color, T["indigo"])
    c_dim = T.get(f"{color}_dim", T["indigo_dim"])
    return (f'<span style="background:{c_dim};border:1px solid {c};color:{c};'
            f'border-radius:6px;padding:2px 10px;font-size:10px;'
            f'font-weight:700;letter-spacing:.06em;">{text}</span>')


def label(text: str) -> str:
    """Uppercase section label HTML — use inside cards."""
    return (f'<div style="font-size:10px;font-weight:700;letter-spacing:.12em;'
            f'color:{T["text_muted"]};text-transform:uppercase;'
            f'margin-bottom:10px;">{text}</div>')


def body_text(text: str, muted: bool = False) -> str:
    """Body paragraph HTML."""
    color = T["text_secondary"] if muted else T["text_primary"]
    return f'<p style="color:{color};font-size:13px;line-height:1.65;margin:0;">{text}</p>'


def divider():
    """Thin divider with correct token color."""
    st.markdown(
        f'<hr style="border:none;border-top:1px solid {T["border_subtle"]};'
        f'margin:24px 0;"/>',
        unsafe_allow_html=True,
    )


def stat_row(items: list[tuple]) -> str:
    """
    Horizontal stat row inside a card.
    items = [("Label", "Value"), ...]
    """
    cells = "".join([
        f'''<div style="text-align:center;padding:0 16px;
                        border-right:1px solid {T['border_subtle']};"
                        >
                <div style="font-size:18px;font-weight:700;
                            color:{T['text_primary']};letter-spacing:-0.02em;">
                    {v}
                </div>
                <div style="font-size:10px;font-weight:600;
                            color:{T['text_muted']};letter-spacing:.08em;
                            text-transform:uppercase;margin-top:2px;">
                    {k}
                </div>
            </div>'''
        for k, v in items
    ])
    return f'<div style="display:flex;align-items:center;gap:0;">{cells}</div>'


def empty_state(message: str, icon: str = "📭"):
    """Empty state card shown when no data is available."""
    st.markdown(f"""
    <div style="
        text-align:center;
        padding:48px 24px;
        background:{T['bg_elevated']};
        border:1px dashed {T['border_default']};
        border-radius:14px;
        color:{T['text_muted']};
    ">
        <div style="font-size:32px;margin-bottom:12px;">{icon}</div>
        <div style="font-size:13px;font-weight:500;">{message}</div>
    </div>
    """, unsafe_allow_html=True)


def plotly_defaults() -> dict:
    """
    Standard layout kwargs for every Plotly figure.
    Usage: fig.update_layout(**plotly_defaults())
    """
    return dict(
        template="plotly_dark",
        paper_bgcolor=T["chart_bg"],
        plot_bgcolor=T["chart_bg"],
        font=dict(family="Inter, sans-serif", color=T["text_secondary"], size=12),
        title_font=dict(family="Inter, sans-serif", color=T["text_primary"],
                        size=14, weight="bold"),
        margin=dict(l=0, r=0, t=40, b=0),
        xaxis=dict(
            gridcolor=T["border_subtle"],
            linecolor=T["border_subtle"],
            tickfont=dict(size=11),
        ),
        yaxis=dict(
            gridcolor=T["border_subtle"],
            linecolor=T["border_subtle"],
            tickfont=dict(size=11),
        ),
    )
