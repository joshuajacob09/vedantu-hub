# modules/dashboard.py — Morning Briefing
# UI refactored to use design system. Logic unchanged.

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, date

from config import VEDANTU_CHANNELS, COMPETITOR_CHANNELS
from utils.registry import get_competitors_by_priority
from utils.youtube_helpers import get_channel_info, get_recent_uploads
from utils.ui import T, page_header, section_header, kpi_card, divider, empty_state, plotly_defaults

EXAM_CALENDAR = [
    {"name": "JEE Mains S1",    "date": date(2026, 1, 22)},
    {"name": "JEE Mains S2",    "date": date(2026, 4, 2)},
    {"name": "NEET UG",         "date": date(2026, 5, 3)},
    {"name": "JEE Advanced",    "date": date(2026, 5, 24)},
    {"name": "CBSE Boards",     "date": date(2026, 2, 15)},
]

def _days(d): return (d - date.today()).days
def _is_short(sec): return 0 < sec <= 60


def render():
    now_str = datetime.now().strftime("%A, %d %b %Y  •  %I:%M %p")

    # Page header
    st.markdown(f"""
    <div style="display:flex;justify-content:space-between;
                align-items:flex-end;padding-bottom:16px;">
        <div>
            <h1 style="margin:0;font-size:26px;font-weight:700;
                       color:{T['text_primary']};letter-spacing:-0.03em;">
                🌅 Morning Briefing
            </h1>
            <p style="margin:4px 0 0 0;font-size:13px;color:{T['text_muted']};">
                What you need to know before your first meeting.
            </p>
        </div>
        <div style="font-size:11px;color:{T['text_muted']};
                    text-align:right;padding-bottom:4px;">
            {now_str}
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── Exam countdowns ───────────────────────────────
    upcoming = sorted(
        [e for e in EXAM_CALENDAR if _days(e["date"]) >= 0],
        key=lambda e: e["date"]
    )[:5]

    if upcoming:
        cols = st.columns(len(upcoming))
        for col, exam in zip(cols, upcoming):
            days = _days(exam["date"])
            c = T["red"] if days <= 14 else T["amber"] if days <= 30 else T["indigo"]
            col.markdown(f"""
            <div style="background:linear-gradient(145deg,{T['bg_elevated']},{T['bg_surface']});
                        border:1px solid {T['border_default']};border-top:2px solid {c};
                        border-radius:14px;padding:16px;text-align:center;">
                <div style="font-size:30px;font-weight:700;color:{c};
                            letter-spacing:-0.04em;line-height:1;">{days}</div>
                <div style="font-size:9px;font-weight:700;color:{T['text_muted']};
                            letter-spacing:.12em;margin:4px 0 8px;">DAYS</div>
                <div style="font-size:11px;font-weight:600;color:{T['text_primary']};
                            line-height:1.3;">{exam['name']}</div>
            </div>
            """, unsafe_allow_html=True)

    divider()

    if not st.button("📅 Load Morning Briefing", type="primary"):
        st.info("Click the button above to fetch live channel data.")
        return

    # ── Fetch data ────────────────────────────────────
    with st.spinner("Loading channel data..."):
        tier1 = get_competitors_by_priority(1)
        vedantu_sample = {
            "Vedantu JEE Made Ejee":  VEDANTU_CHANNELS["Vedantu JEE Made Ejee"],
            "Vedantu NEET Made Ejee": VEDANTU_CHANNELS["Vedantu NEET Made Ejee"],
            "Vedantu CBSE 10th":      VEDANTU_CHANNELS["Vedantu CBSE 10th"],
            "Vedantu JEE English":    VEDANTU_CHANNELS["Vedantu JEE English"],
            "Vedantu NEET English":   VEDANTU_CHANNELS["Vedantu NEET English"],
        }
        all_ch = []
        for name, cid in vedantu_sample.items():
            ups = get_recent_uploads(cid)
            if ups: all_ch.append({"name": name, "id": cid, "team": "Vedantu", "uploads": ups})
        for c in tier1:
            ups = get_recent_uploads(c["id"])
            if ups: all_ch.append({"name": c["name"], "id": c["id"], "team": "Competitor", "uploads": ups})

    today = date.today()

    # ── Upload cadence ────────────────────────────────
    section_header("📅 Upload Cadence — Last 7 Days",
                   "How many videos each channel published this week")

    cad_rows = []
    for ch in all_ch:
        u7 = [v for v in ch["uploads"] if (today - date.fromisoformat(v["published"])).days <= 7]
        shorts = [v for v in u7 if _is_short(v["duration_sec"])]
        cad_rows.append({
            "Channel":   ch["name"],
            "Team":      ch["team"],
            "Total":     len(u7),
            "Shorts":    len(shorts),
            "Long-form": len(u7) - len(shorts),
        })

    df_cad = pd.DataFrame(cad_rows).sort_values("Total", ascending=False)
    fig_cad = px.bar(
        df_cad, x="Channel", y="Total", color="Team",
        color_discrete_map={"Vedantu": T["indigo"], "Competitor": T["red"]},
        text="Total",
    )
    fig_cad.update_layout(**plotly_defaults(), height=320, xaxis_tickangle=-30)
    fig_cad.update_traces(textposition="outside", marker_line_width=0)
    st.plotly_chart(fig_cad, use_container_width=True)

    st.dataframe(df_cad, use_container_width=True, hide_index=True,
                 column_config={
                     "Total":     st.column_config.NumberColumn(format="%d"),
                     "Shorts":    st.column_config.NumberColumn(format="%d"),
                     "Long-form": st.column_config.NumberColumn(format="%d"),
                 })

    divider()

    # ── Shorts vs Long-form ───────────────────────────
    section_header("🎬 Format Mix — Shorts vs Long-form",
                   "Recent 10 uploads per channel")

    fmt_rows = []
    for ch in all_ch:
        total  = len(ch["uploads"])
        shorts = sum(1 for v in ch["uploads"] if _is_short(v["duration_sec"]))
        if total:
            fmt_rows.append({
                "Channel":     ch["name"],
                "Team":        ch["team"],
                "Shorts %":    round(shorts / total * 100),
                "Long-form %": round((total - shorts) / total * 100),
            })

    df_fmt = pd.DataFrame(fmt_rows).sort_values("Shorts %", ascending=False)
    fig_fmt = go.Figure()
    fig_fmt.add_trace(go.Bar(name="Shorts",    x=df_fmt["Channel"],
                             y=df_fmt["Shorts %"],    marker_color=T["amber"],
                             text=df_fmt["Shorts %"].apply(lambda x: f"{x}%"),
                             textposition="inside"))
    fig_fmt.add_trace(go.Bar(name="Long-form", x=df_fmt["Channel"],
                             y=df_fmt["Long-form %"], marker_color=T["indigo"],
                             text=df_fmt["Long-form %"].apply(lambda x: f"{x}%"),
                             textposition="inside"))
    fig_fmt.update_layout(**plotly_defaults(), barmode="stack", height=320,
                          xaxis_tickangle=-30)
    fig_fmt.update_layout(legend=dict(orientation="h", y=1.08, bgcolor="rgba(0,0,0,0)"))
    fig_fmt.update_traces(marker_line_width=0)
    st.plotly_chart(fig_fmt, use_container_width=True)

    divider()

    # ── Viral this week ───────────────────────────────
    section_header("🔥 Viral This Week",
                   "Videos from the last 7 days ranked by views/day velocity")

    viral = []
    for ch in all_ch:
        for v in ch["uploads"]:
            if (today - date.fromisoformat(v["published"])).days <= 7:
                viral.append({
                    "Channel":   ch["name"],
                    "Team":      ch["team"],
                    "Title":     v["title"],
                    "Published": v["published"],
                    "Views":     v["views"],
                    "Views/Day": int(v["views_per_day"]),
                    "Format":    "Short" if _is_short(v["duration_sec"]) else "Long",
                    "URL":       v["url"],
                })

    if viral:
        df_v = pd.DataFrame(viral).sort_values("Views/Day", ascending=False).head(15)
        st.dataframe(df_v.drop(columns=["Team"]), use_container_width=True,
                     hide_index=True,
                     column_config={
                         "URL":       st.column_config.LinkColumn("Watch", display_text="▶"),
                         "Views":     st.column_config.NumberColumn(format="%d"),
                         "Views/Day": st.column_config.NumberColumn(format="%d"),
                     })
    else:
        empty_state("No videos found from the last 7 days.", "📭")

    divider()

    # ── Channel health ────────────────────────────────
    section_header("💚 Vedantu Channel Health",
                   "Score based on avg views/day of recent uploads")

    health = []
    for name, cid in VEDANTU_CHANNELS.items():
        ups = get_recent_uploads(cid)
        if ups:
            avg_vpd = sum(v["views_per_day"] for v in ups) / len(ups)
            shorts_pct = sum(1 for v in ups if _is_short(v["duration_sec"])) / len(ups) * 100
            days_since = (today - date.fromisoformat(ups[0]["published"])).days
            health.append({
                "Channel":       name,
                "Avg Views/Day": int(avg_vpd),
                "Shorts Mix":    f"{int(shorts_pct)}%",
                "Last Upload":   ups[0]["published"],
                "Days Since":    days_since,
                "Score":         min(100, int(avg_vpd / 500)),
            })

    if health:
        df_h = pd.DataFrame(health).sort_values("Avg Views/Day", ascending=False)
        inactive = df_h[df_h["Days Since"] > 5]
        if not inactive.empty:
            st.warning(f"⚠️ {len(inactive)} channel(s) silent for 5+ days: "
                       + ", ".join(inactive["Channel"].tolist()))
        st.dataframe(df_h, use_container_width=True, hide_index=True,
                     column_config={
                         "Avg Views/Day": st.column_config.NumberColumn(format="%d"),
                         "Score": st.column_config.ProgressColumn(
                             "Health Score", min_value=0, max_value=100, format="%d"),
                     })
