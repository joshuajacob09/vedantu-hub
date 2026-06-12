# utils/ui.py — Enterprise Design System v2
# Spec: Apple + Linear + Vercel. Zero student-project energy.

import streamlit as st

# ── Strict token set — no deviations ─────────────────
C = {
    "bg":          "#0B1120",
    "card":        "#111827",
    "border":      "rgba(255,255,255,0.08)",
    "accent":      "#6366F1",
    "success":     "#22C55E",
    "warning":     "#F59E0B",
    "danger":      "#EF4444",
    "text":        "#F8FAFC",
    "text2":       "#94A3B8",
    "text3":       "#475569",
    "accent_dim":  "rgba(99,102,241,0.12)",
    "success_dim": "rgba(34,197,94,0.10)",
    "warning_dim": "rgba(245,158,11,0.10)",
    "danger_dim":  "rgba(239,68,68,0.10)",
    "chart_bg":    "rgba(0,0,0,0)",
}

# shorthand
T = C

GLOBAL_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

*, *::before, *::after { box-sizing: border-box; }

html, body, [class*="css"] {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif !important;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
}

/* ── App shell ── */
.stApp {
    background-color: #0B1120 !important;
    max-width: 1400px;
    margin: 0 auto;
}

/* ── Hide Streamlit chrome ── */
#MainMenu, footer, header { display: none !important; }
.stDeployButton { display: none !important; }
[data-testid="stToolbar"] { display: none !important; }

/* ── Sidebar ── */
section[data-testid="stSidebar"] {
    background: #0D1526 !important;
    border-right: 1px solid rgba(255,255,255,0.06) !important;
    width: 220px !important;
}
section[data-testid="stSidebar"] > div {
    padding: 0 !important;
}

/* ── Metric cards ── */
div[data-testid="metric-container"] {
    background: #111827 !important;
    border: 1px solid rgba(255,255,255,0.08) !important;
    border-radius: 12px !important;
    padding: 20px !important;
}
div[data-testid="metric-container"] [data-testid="stMetricLabel"] {
    font-size: 11px !important;
    font-weight: 600 !important;
    letter-spacing: 0.08em !important;
    color: #94A3B8 !important;
    text-transform: uppercase !important;
}
div[data-testid="metric-container"] [data-testid="stMetricValue"] {
    font-size: 28px !important;
    font-weight: 700 !important;
    color: #F8FAFC !important;
    letter-spacing: -0.03em !important;
    line-height: 1.1 !important;
}
div[data-testid="metric-container"] [data-testid="stMetricDelta"] {
    font-size: 12px !important;
    font-weight: 500 !important;
}

/* ── Typography ── */
h1 {
    font-size: 32px !important;
    font-weight: 700 !important;
    color: #F8FAFC !important;
    letter-spacing: -0.04em !important;
    line-height: 1.15 !important;
    margin: 0 0 4px 0 !important;
}
h2 {
    font-size: 22px !important;
    font-weight: 600 !important;
    color: #F8FAFC !important;
    letter-spacing: -0.02em !important;
    margin: 0 !important;
}
h3 {
    font-size: 15px !important;
    font-weight: 600 !important;
    color: #94A3B8 !important;
}
p, li { font-size: 15px !important; color: #94A3B8 !important; line-height: 1.6 !important; }

/* ── Buttons ── */
.stButton > button {
    height: 38px !important;
    border-radius: 8px !important;
    font-size: 13px !important;
    font-weight: 600 !important;
    letter-spacing: 0.01em !important;
    border: 1px solid rgba(255,255,255,0.1) !important;
    background: #111827 !important;
    color: #F8FAFC !important;
    transition: all 0.15s ease !important;
    padding: 0 18px !important;
}
.stButton > button:hover {
    border-color: rgba(255,255,255,0.2) !important;
    background: #1a2235 !important;
}
.stButton > button[kind="primary"] {
    background: #6366F1 !important;
    border-color: #6366F1 !important;
    color: #fff !important;
}
.stButton > button[kind="primary"]:hover {
    background: #5558e3 !important;
    border-color: #5558e3 !important;
}

/* ── Inputs ── */
div[data-testid="stSelectbox"] > div > div,
div[data-testid="stTextInput"] > div > div input {
    background: #111827 !important;
    border: 1px solid rgba(255,255,255,0.08) !important;
    border-radius: 8px !important;
    color: #F8FAFC !important;
    font-size: 14px !important;
}

/* ── Dataframe ── */
div[data-testid="stDataFrame"] {
    border-radius: 12px !important;
    border: 1px solid rgba(255,255,255,0.08) !important;
    overflow: hidden !important;
}

/* ── Tabs ── */
.stTabs [data-baseweb="tab-list"] {
    background: #111827 !important;
    border: 1px solid rgba(255,255,255,0.08) !important;
    border-radius: 10px !important;
    padding: 4px !important;
    gap: 2px !important;
}
.stTabs [data-baseweb="tab"] {
    border-radius: 7px !important;
    font-size: 13px !important;
    font-weight: 500 !important;
    color: #94A3B8 !important;
    padding: 6px 14px !important;
    border: none !important;
}
.stTabs [aria-selected="true"] {
    background: #1e2a3e !important;
    color: #F8FAFC !important;
}

/* ── Expander ── */
div[data-testid="stExpander"] {
    background: #111827 !important;
    border: 1px solid rgba(255,255,255,0.08) !important;
    border-radius: 10px !important;
}
div[data-testid="stExpander"] summary {
    font-size: 13px !important;
    font-weight: 500 !important;
    color: #94A3B8 !important;
}

/* ── Alerts ── */
.stAlert {
    border-radius: 10px !important;
    font-size: 13px !important;
}

/* ── Progress ── */
.stProgress > div > div > div {
    background: #6366F1 !important;
    border-radius: 99px !important;
}

/* ── Spinner ── */
.stSpinner > div { border-top-color: #6366F1 !important; }

/* ── Radio ── */
.stRadio > div { gap: 2px !important; }
.stRadio label {
    font-size: 13px !important;
    color: #94A3B8 !important;
    font-weight: 500 !important;
}

/* ── Caption ── */
.stCaption { font-size: 13px !important; color: #475569 !important; }

/* ── Divider ── */
hr {
    border: none !important;
    border-top: 1px solid rgba(255,255,255,0.06) !important;
    margin: 28px 0 !important;
}

/* ── Scrollbar ── */
::-webkit-scrollbar { width: 3px; height: 3px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: rgba(255,255,255,0.1); border-radius: 99px; }

/* ── Mobile ── */
@media (max-width: 768px) {
    h1 { font-size: 24px !important; }
    h2 { font-size: 18px !important; }
    section[data-testid="stSidebar"] { width: 100% !important; }
    .stApp { max-width: 100% !important; }
}

/* ── Sidebar nav items ── */
.nav-item {
    display: flex;
    align-items: center;
    gap: 10px;
    padding: 9px 14px;
    border-radius: 8px;
    font-size: 13px;
    font-weight: 500;
    color: #94A3B8;
    cursor: pointer;
    transition: all 0.12s ease;
    margin: 1px 8px;
    text-decoration: none;
}
.nav-item:hover { background: rgba(255,255,255,0.05); color: #F8FAFC; }
.nav-item.active { background: rgba(99,102,241,0.12); color: #F8FAFC; }
.nav-item .icon { font-size: 14px; width: 18px; text-align: center; opacity: 0.7; }
.nav-section-label {
    font-size: 10px;
    font-weight: 700;
    letter-spacing: 0.1em;
    color: #334155;
    text-transform: uppercase;
    padding: 16px 22px 6px;
}

/* ── Page layout ── */
.page-content {
    padding: 28px 32px 80px;
    max-width: 1400px;
}

/* ── Footer ── */
.app-footer {
    position: fixed; bottom: 0; left: 0; right: 0;
    height: 36px;
    display: flex; align-items: center; justify-content: center;
    background: #0B1120;
    border-top: 1px solid rgba(255,255,255,0.06);
    font-size: 11px; color: #334155;
    letter-spacing: 0.04em;
    z-index: 999;
}
</style>
"""

# ─────────────────────────────────────────────────────
# Core functions
# ─────────────────────────────────────────────────────

def inject_css():
    st.markdown(GLOBAL_CSS, unsafe_allow_html=True)


def page_header(title: str, subtitle: str = "", right_content: str = ""):
    """Enterprise page header — title left, optional content right."""
    st.markdown(f"""
    <div style="display:flex;justify-content:space-between;align-items:flex-start;
                padding:32px 0 24px;border-bottom:1px solid rgba(255,255,255,0.06);
                margin-bottom:28px;">
        <div>
            <h1>{title}</h1>
            {'<p style="margin:6px 0 0;font-size:14px;color:#475569;line-height:1.5;">'+subtitle+'</p>' if subtitle else ''}
        </div>
        {'<div style="padding-top:4px;">'+right_content+'</div>' if right_content else ''}
    </div>
    """, unsafe_allow_html=True)


def section_header(title: str, subtitle: str = ""):
    """Section title with optional description."""
    st.markdown(f"""
    <div style="margin:32px 0 16px;">
        <h2>{title}</h2>
        {'<p style="font-size:13px;color:#475569;margin:4px 0 0;">'+subtitle+'</p>' if subtitle else ''}
    </div>
    """, unsafe_allow_html=True)


def kpi_card(label: str, value: str, delta: str = "",
             delta_positive: bool = True, sublabel: str = ""):
    """
    Enterprise KPI card.
    Use inside st.columns() for a proper grid.
    """
    delta_color = C["success"] if delta_positive else C["danger"]
    delta_bg    = C["success_dim"] if delta_positive else C["danger_dim"]
    delta_html  = f"""
        <div style="display:inline-flex;align-items:center;gap:4px;
                    background:{delta_bg};border-radius:6px;
                    padding:2px 8px;margin-top:8px;">
            <span style="font-size:11px;font-weight:600;color:{delta_color};">
                {'↑' if delta_positive else '↓'} {delta}
            </span>
        </div>""" if delta else ""

    sublabel_html = f'<div style="font-size:12px;color:{C["text3"]};margin-top:6px;">{sublabel}</div>' if sublabel else ""

    st.markdown(f"""
    <div style="background:{C['card']};border:1px solid {C['border']};
                border-radius:12px;padding:20px 22px;height:100%;
                transition:border-color 0.15s;">
        <div style="font-size:11px;font-weight:600;letter-spacing:0.08em;
                    color:{C['text2']};text-transform:uppercase;margin-bottom:10px;">
            {label}
        </div>
        <div style="font-size:28px;font-weight:700;color:{C['text']};
                    letter-spacing:-0.03em;line-height:1.1;">
            {value}
        </div>
        {delta_html}
        {sublabel_html}
    </div>
    """, unsafe_allow_html=True)


def insight_card(priority: str, title: str, reason: str,
                 action: str, confidence: int = 0, impact: str = ""):
    """
    AI recommendation card. priority: HIGH | MEDIUM | LOW
    """
    colors = {
        "HIGH":   (C["danger"],   C["danger_dim"]),
        "MEDIUM": (C["warning"],  C["warning_dim"]),
        "LOW":    (C["accent"],   C["accent_dim"]),
    }
    c, bg = colors.get(priority, colors["MEDIUM"])

    conf_html = ""
    if confidence:
        conf_html = f"""
        <div style="display:flex;align-items:center;gap:8px;margin-top:12px;">
            <div style="flex:1;height:3px;background:rgba(255,255,255,0.06);border-radius:99px;">
                <div style="width:{confidence}%;height:100%;background:{c};border-radius:99px;"></div>
            </div>
            <span style="font-size:11px;color:{C['text2']};white-space:nowrap;">
                {confidence}% confidence
            </span>
        </div>"""

    impact_html = f'<div style="font-size:12px;color:{C["text2"]};margin-top:8px;padding-top:8px;border-top:1px solid {C["border"]};">Impact: {impact}</div>' if impact else ""

    st.markdown(f"""
    <div style="background:{C['card']};border:1px solid {C['border']};
                border-left:3px solid {c};border-radius:12px;
                padding:18px 20px;margin-bottom:10px;">
        <div style="display:flex;align-items:center;gap:8px;margin-bottom:10px;">
            <span style="background:{bg};color:{c};font-size:10px;font-weight:700;
                         letter-spacing:0.08em;border-radius:4px;padding:2px 8px;">
                {priority}
            </span>
            <span style="font-size:14px;font-weight:600;color:{C['text']};">
                {title}
            </span>
        </div>
        <p style="font-size:13px;color:{C['text2']};margin:0 0 10px;line-height:1.55;">
            {reason}
        </p>
        <div style="background:rgba(255,255,255,0.03);border-radius:8px;
                    padding:10px 14px;border-left:2px solid {c};">
            <div style="font-size:10px;font-weight:700;letter-spacing:0.08em;
                        color:{C['text3']};margin-bottom:4px;">SUGGESTED ACTION</div>
            <div style="font-size:13px;color:{C['text']};line-height:1.5;">{action}</div>
        </div>
        {conf_html}
        {impact_html}
    </div>
    """, unsafe_allow_html=True)


def alert_card(message: str, type: str = "info"):
    """Inline alert — type: info | warning | success | danger"""
    colors = {
        "info":    (C["accent"],  C["accent_dim"],  "ℹ"),
        "warning": (C["warning"], C["warning_dim"], "⚠"),
        "success": (C["success"], C["success_dim"], "✓"),
        "danger":  (C["danger"],  C["danger_dim"],  "!"),
    }
    c, bg, icon = colors.get(type, colors["info"])
    st.markdown(f"""
    <div style="background:{bg};border:1px solid {c}22;border-radius:10px;
                padding:12px 16px;display:flex;align-items:flex-start;gap:10px;
                margin-bottom:12px;">
        <span style="color:{c};font-weight:700;font-size:13px;flex-shrink:0;">{icon}</span>
        <span style="color:{C['text']};font-size:13px;line-height:1.5;">{message}</span>
    </div>
    """, unsafe_allow_html=True)


def empty_state(message: str, icon: str = "—"):
    """Empty / no-data state."""
    st.markdown(f"""
    <div style="text-align:center;padding:56px 24px;
                background:{C['card']};border:1px dashed {C['border']};
                border-radius:12px;">
        <div style="font-size:28px;margin-bottom:12px;opacity:0.4;">{icon}</div>
        <div style="font-size:14px;color:{C['text3']};font-weight:500;">{message}</div>
    </div>
    """, unsafe_allow_html=True)


def divider():
    st.markdown(
        '<hr style="border:none;border-top:1px solid rgba(255,255,255,0.06);margin:28px 0;"/>',
        unsafe_allow_html=True)


def badge(text: str, color: str = "accent") -> str:
    """Inline badge HTML string."""
    c  = C.get(color, C["accent"])
    bg = C.get(f"{color}_dim", C["accent_dim"])
    return (f'<span style="background:{bg};color:{c};border-radius:4px;'
            f'padding:2px 8px;font-size:10px;font-weight:700;'
            f'letter-spacing:0.06em;">{text}</span>')


def plotly_defaults(height: int = 320) -> dict:
    """Standard Plotly layout. Pass height per chart."""
    return dict(
        template="plotly_dark",
        paper_bgcolor=C["chart_bg"],
        plot_bgcolor=C["chart_bg"],
        font=dict(family="Inter, sans-serif", color=C["text2"], size=11),
        title_font=dict(family="Inter, sans-serif", color=C["text"], size=13),
        margin=dict(l=0, r=8, t=36, b=0),
        height=height,
        xaxis=dict(gridcolor="rgba(255,255,255,0.04)",
                   linecolor="rgba(255,255,255,0.04)",
                   tickfont=dict(size=11), showgrid=True),
        yaxis=dict(gridcolor="rgba(255,255,255,0.04)",
                   linecolor="rgba(255,255,255,0.04)",
                   tickfont=dict(size=11), showgrid=False),
    )
