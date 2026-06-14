# modules/dashboard.py — Morning Briefing. Fixes 5, 6, 7, 14, 20.

import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime, date

from config import VEDANTU_CHANNELS
from utils.registry import get_competitors_by_priority
from utils.youtube_helpers import get_recent_uploads
from utils.ui import C, page_header, section_header, kpi_card, alert_card, divider, empty_state, plotly_defaults, data_timestamp

EXAM_CALENDAR = [
    {"name": "JEE Mains S1",  "date": date(2026, 1, 22)},
    {"name": "JEE Mains S2",  "date": date(2026, 4,  2)},
    {"name": "NEET UG",       "date": date(2026, 5,  3)},
    {"name": "JEE Advanced",  "date": date(2026, 5, 24)},
    {"name": "CBSE Boards",   "date": date(2026, 2, 15)},
]

def _days(d): return (d - date.today()).days
def _is_short(s): return 0 < s <= 60


# Fix #5: don't cache `today` — compute it outside cache
@st.cache_data(ttl=3600)
def _fetch_channels():
    """Only cache the API data, not the date."""
    tier1 = get_competitors_by_priority(1)
    vedantu_sample = {
        "Vedantu JEE":  VEDANTU_CHANNELS["Vedantu JEE Made Ejee"],
        "Vedantu NEET": VEDANTU_CHANNELS["Vedantu NEET Made Ejee"],
        "V CBSE 10":    VEDANTU_CHANNELS["Vedantu CBSE 10th"],
    }
    all_ch = []
    for name, cid in vedantu_sample.items():
        ups = get_recent_uploads(cid)
        if ups: all_ch.append({"name": name, "team": "Vedantu", "uploads": ups})
    for c in tier1[:8]:
        ups = get_recent_uploads(c["id"])
        if ups: all_ch.append({"name": c["name"], "team": "Competitor", "uploads": ups})
    return all_ch


def render():
    page_header("Morning Briefing", "What happened while you were away.")

    # Fix #7: show loading state with label before data appears
    with st.spinner("Loading channel data — this may take a few seconds on first load..."):
        all_ch = _fetch_channels()

    today = date.today()  # Fix #5: computed fresh every render

    # Fix #14: only show exams with non-negative days
    upcoming = sorted(
        [e for e in EXAM_CALENDAR if _days(e["date"]) > 0],
        key=lambda e: e["date"]
    )[:5]

    if upcoming:
        cols = st.columns(len(upcoming))
        for col, exam in zip(cols, upcoming):
            days = _days(exam["date"])
            c = C["danger"] if days <= 14 else C["warning"] if days <= 30 else C["accent"]
            col.markdown(f"""
            <div style="background:{C['card']};border:1px solid {C['border']};
                        border-top:2px solid {c};border-radius:12px;
                        padding:14px 16px;text-align:center;">
                <div style="font-size:26px;font-weight:700;color:{c};
                            letter-spacing:-0.04em;line-height:1;">{days}</div>
                <div style="font-size:9px;font-weight:700;color:{C['text3']};
                            letter-spacing:.1em;margin:3px 0 6px;">DAYS</div>
                <div style="font-size:11px;font-weight:600;color:{C['text']};
                            line-height:1.3;">{exam['name']}</div>
            </div>
            """, unsafe_allow_html=True)
        st.markdown("<div style='margin-top:20px'/>", unsafe_allow_html=True)

    # Signals
    vedantu_7d = sum(
        1 for ch in all_ch if ch["team"] == "Vedantu"
        for v in ch["uploads"]
        if (today - date.fromisoformat(v["published"])).days <= 7
    )
    comp_7d = sum(
        1 for ch in all_ch if ch["team"] == "Competitor"
        for v in ch["uploads"]
        if (today - date.fromisoformat(v["published"])).days <= 7
    )
    all_vids = [v for ch in all_ch for v in ch["uploads"]]
    viral = max(all_vids, key=lambda v: v["views_per_day"], default=None)
    inactive = [
        ch["name"] for ch in all_ch
        if ch["team"] == "Vedantu"
        and ch["uploads"]
        and (today - date.fromisoformat(ch["uploads"][0]["published"])).days > 5
    ]

    if inactive:
        alert_card(f"Inactive 5+ days: {', '.join(inactive)}", "warning")
    if viral:
        alert_card(
            f'Trending: "{viral["title"][:65]}" — {int(viral["views_per_day"]):,} views/day',
            "info"
        )
    if comp_7d > vedantu_7d * 2:
        alert_card(
            f"Competitors uploaded {comp_7d} videos this week vs Vedantu's {vedantu_7d}.",
            "danger"
        )

    divider()
    section_header("This Week at a Glance")

    # Fix #6: all 4 KPI cards always render
    k1, k2, k3, k4 = st.columns(4)
    shorts = sum(1 for ch in all_ch for v in ch["uploads"] if _is_short(v["duration_sec"]))
    total  = sum(len(ch["uploads"]) for ch in all_ch)
    with k1: kpi_card("Vedantu Uploads",    str(vedantu_7d),                                    sublabel="last 7 days")
    with k2: kpi_card("Competitor Uploads", str(comp_7d),                                       sublabel="last 7 days")
    with k3: kpi_card("Top Velocity",       f"{int(viral['views_per_day']):,}" if viral else "—", sublabel="views/day")
    with k4: kpi_card("Shorts Mix",         f"{int(shorts/total*100)}%" if total else "—",       sublabel="all channels")

    divider()
    section_header("Upload Cadence", "Videos published in the last 7 days")
    data_timestamp()  # Fix #20

    cad_rows = []
    for ch in all_ch:
        u7 = [v for v in ch["uploads"]
              if (today - date.fromisoformat(v["published"])).days <= 7]
        if u7 or ch["team"] == "Vedantu":
            cad_rows.append({"Channel": ch["name"], "Team": ch["team"], "Uploads": len(u7)})

    if cad_rows:
        df  = pd.DataFrame(cad_rows).sort_values("Uploads", ascending=True)
        fig = px.bar(df, x="Uploads", y="Channel", orientation="h", color="Team",
                     color_discrete_map={"Vedantu": C["accent"], "Competitor": C["text3"]})
        fig.update_traces(marker_line_width=0)
        fig.update_layout(**plotly_defaults(height=max(260, len(cad_rows) * 28)))
        fig.update_layout(showlegend=True,
                          legend=dict(orientation="h", y=1.06, x=0,
                                      bgcolor="rgba(0,0,0,0)", font=dict(size=11)))
        st.plotly_chart(fig, use_container_width=True)

    divider()
    section_header("Viral This Week", "Top 10 videos by views/day")
    data_timestamp()  # Fix #20

    viral_rows = [
        {
            "Channel":   ch["name"],
            "Title":     v["title"],
            "Views/Day": int(v["views_per_day"]),
            "Views":     v["views"],
            "Format":    "Short" if _is_short(v["duration_sec"]) else "Long",
            "URL":       v["url"],
        }
        for ch in all_ch
        for v in ch["uploads"]
        if (today - date.fromisoformat(v["published"])).days <= 7
    ]

    if viral_rows:
        df_v = pd.DataFrame(viral_rows).sort_values("Views/Day", ascending=False).head(10)
        st.dataframe(df_v, use_container_width=True, hide_index=True,
                     column_config={
                         "URL":       st.column_config.LinkColumn("Watch", display_text="▶"),
                         "Views":     st.column_config.NumberColumn(format="%d"),
                         "Views/Day": st.column_config.NumberColumn(format="%d"),
                     })
    else:
        empty_state("No videos published in the last 7 days.")
