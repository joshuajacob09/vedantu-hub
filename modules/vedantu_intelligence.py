# modules/vedantu_intelligence.py
# ─────────────────────────────────────────────────────
# Vedantu Network Intelligence — full rebuild.
#
# Two views:
#   1. Network Overview — all 19 channels at once,
#      health scores, upload cadence, shorts mix.
#   2. Channel vs Competitor — deep 1v1 comparison
#      with views/video benchmark and title patterns.
# ─────────────────────────────────────────────────────

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from collections import Counter
from datetime import date

from config import VEDANTU_CHANNELS, COMPETITOR_CHANNELS
from utils.ui import C, T, page_header, section_header, kpi_card, divider, empty_state, plotly_defaults
from utils.youtube_helpers import get_channel_info, get_recent_uploads


def _is_short(duration_sec: int) -> bool:
    return 0 < duration_sec <= 60


def _avg(lst):
    return sum(lst) / len(lst) if lst else 0


# Common title keywords to detect format patterns
FORMAT_KEYWORDS = [
    "one shot", "1 shot", "crash course", "revision",
    "previous year", "pyq", "mcq", "short", "live",
    "lecture", "class", "full chapter", "tips", "tricks",
    "formula", "important questions", "doubt",
]


def _extract_patterns(titles: list[str]) -> dict:
    """Count how many titles match each format keyword."""
    counts = {}
    titles_lower = [t.lower() for t in titles]
    for kw in FORMAT_KEYWORDS:
        c = sum(1 for t in titles_lower if kw in t)
        if c > 0:
            counts[kw.title()] = c
    return dict(sorted(counts.items(), key=lambda x: x[1], reverse=True))


def render():
    page_header('Vedantu Intelligence', 'Full network health overview + deep channel benchmarking.', '🏫')

    view = st.radio(
        "View",
        ["📡 Network Overview (all 19 channels)",
         "⚔️ Channel vs Competitor"],
        horizontal=True,
    )

    if view == "📡 Network Overview (all 19 channels)":
        _network_overview()
    else:
        _channel_vs_competitor()


# ─────────────────────────────────────────────────────
# VIEW 1: Full network overview
# ─────────────────────────────────────────────────────
def _network_overview():
    st.subheader("Vedantu Network — All Channels")

    with st.spinner("Loading all 19 Vedantu channels..."):
        rows = []
        today = date.today()
        for name, cid in VEDANTU_CHANNELS.items():
            info    = get_channel_info(cid)
            uploads = get_recent_uploads(cid)
            if not info or not uploads:
                continue

            shorts   = [v for v in uploads if _is_short(v["duration_sec"])]
            longform = [v for v in uploads if not _is_short(v["duration_sec"])]
            uploads_7d = [
                v for v in uploads
                if (today - date.fromisoformat(v["published"])).days <= 7
            ]
            avg_vpd = _avg([v["views_per_day"] for v in uploads])
            avg_vpv = _avg([v["views"] for v in uploads])
            last_up = uploads[0]["published"] if uploads else "—"
            days_since = (today - date.fromisoformat(last_up)).days if last_up != "—" else 99

            rows.append({
                "Channel":        name,
                "Subscribers":    info["subscribers"],
                "Avg Views/Video": int(avg_vpv),
                "Avg Views/Day":  int(avg_vpd),
                "Uploads (7d)":   len(uploads_7d),
                "Shorts":         len(shorts),
                "Long-form":      len(longform),
                "Shorts %":       int(len(shorts) / len(uploads) * 100),
                "Last Upload":    last_up,
                "Days Since":     days_since,
                "Health":         min(100, int(avg_vpd / 500)),
            })

    if not rows:
        st.error("Could not load channel data.")
        return

    df = pd.DataFrame(rows).sort_values("Avg Views/Day", ascending=False)

    # ── Network KPI summary ───────────────────────────
    total_subs   = df["Subscribers"].sum()
    best_channel = df.iloc[0]["Channel"]
    best_vpd     = df.iloc[0]["Avg Views/Day"]
    inactive     = df[df["Days Since"] > 5]

    k1, k2, k3, k4 = st.columns(4)
    k1.metric("Total Network Subscribers", f"{total_subs:,}")
    k2.metric("Best Performing Channel",   best_channel)
    k3.metric("Best Avg Views/Day",        f"{best_vpd:,}")
    k4.metric("Channels Not Uploaded 5d+", len(inactive))

    if len(inactive) > 0:
        st.warning(
            f"⚠️ {len(inactive)} channel(s) haven't uploaded in 5+ days: "
            + ", ".join(inactive["Channel"].tolist())
        )

    st.divider()

    # ── Health score table ────────────────────────────
    st.markdown("**Channel Health Scores**")
    st.dataframe(
        df[[
            "Channel", "Subscribers", "Avg Views/Video",
            "Avg Views/Day", "Uploads (7d)", "Shorts %",
            "Days Since", "Health"
        ]],
        use_container_width=True,
        hide_index=True,
        column_config={
            "Subscribers":      st.column_config.NumberColumn(format="%d"),
            "Avg Views/Video":  st.column_config.NumberColumn(format="%d"),
            "Avg Views/Day":    st.column_config.NumberColumn(format="%d"),
            "Shorts %":         st.column_config.NumberColumn(format="%d%%"),
            "Health":           st.column_config.ProgressColumn(
                "Health Score", min_value=0, max_value=100, format="%d"
            ),
        }
    )

    st.divider()

    # ── Avg Views/Video chart ─────────────────────────
    st.markdown("**Views per Video — Who Gets the Most Eyeballs Per Upload?**")
    fig = px.bar(
        df.sort_values("Avg Views/Video", ascending=True),
        x="Avg Views/Video", y="Channel",
        orientation="h",
        color="Avg Views/Video",
        color_continuous_scale=[[0, "#2d2f3e"], [0.5, "#6366f1"], [1, "#22c55e"]],
        template="plotly_dark",
        text="Avg Views/Video",
    )
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        showlegend=False,
        height=500,
        coloraxis_showscale=False,
    )
    fig.update_traces(texttemplate="%{text:,}", textposition="outside")
    st.plotly_chart(fig, use_container_width=True)

    st.divider()

    # ── Upload cadence heatmap ────────────────────────
    st.markdown("**Upload Cadence — Last 10 Videos per Channel**")
    today_str = str(date.today())
    heatmap_data = []
    for name, cid in VEDANTU_CHANNELS.items():
        uploads = get_recent_uploads(cid)
        for v in uploads:
            days_ago = (date.today() - date.fromisoformat(v["published"])).days
            heatmap_data.append({
                "Channel":  name,
                "Days Ago": days_ago,
                "Views":    v["views"],
            })

    if heatmap_data:
        df_heat = pd.DataFrame(heatmap_data)
        fig_h = px.scatter(
            df_heat, x="Days Ago", y="Channel",
            size="Views", color="Views",
            color_continuous_scale="blues",
            template="plotly_dark",
            title="Upload Activity (bubble size = views)",
        )
        fig_h.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            height=500,
            xaxis=dict(autorange="reversed", title="Days Ago"),
        )
        st.plotly_chart(fig_h, use_container_width=True)


# ─────────────────────────────────────────────────────
# VIEW 2: Deep 1v1 comparison
# ─────────────────────────────────────────────────────
def _channel_vs_competitor():
    col1, col2 = st.columns(2)
    with col1:
        v_name = st.selectbox("Vedantu channel", list(VEDANTU_CHANNELS.keys()))
    with col2:
        c_name = st.selectbox("Competitor", list(COMPETITOR_CHANNELS.keys()))

    if st.button("⚡ Run Deep Comparison", type="primary"):
        _run_deep_comparison(
            v_name, VEDANTU_CHANNELS[v_name],
            c_name, COMPETITOR_CHANNELS[c_name],
        )


def _run_deep_comparison(v_name, v_id, c_name, c_id):
    with st.spinner("Fetching data..."):
        v_info    = get_channel_info(v_id)
        c_info    = get_channel_info(c_id)
        v_uploads = get_recent_uploads(v_id)
        c_uploads = get_recent_uploads(c_id)

    if not v_uploads or not c_uploads:
        st.error("Could not fetch uploads for one or both channels.")
        return

    # ── Core metrics ──────────────────────────────────
    st.subheader("📊 Head-to-Head Metrics")

    def _channel_stats(info, uploads):
        shorts   = [v for v in uploads if _is_short(v["duration_sec"])]
        avg_vpv  = _avg([v["views"] for v in uploads])
        avg_vpd  = _avg([v["views_per_day"] for v in uploads])
        return {
            "Subscribers":      info.get("subscribers", 0),
            "Total Views":      info.get("total_views", 0),
            "Avg Views/Video":  int(avg_vpv),
            "Avg Views/Day":    int(avg_vpd),
            "Shorts Mix":       f"{int(len(shorts)/len(uploads)*100)}%",
            "Top Video Views":  max(v["views"] for v in uploads),
        }

    v_stats = _channel_stats(v_info, v_uploads)
    c_stats = _channel_stats(c_info, c_uploads)

    m_cols = st.columns(len(v_stats))
    for col, (metric, v_val) in zip(m_cols, v_stats.items()):
        c_val = c_stats[metric]
        if isinstance(v_val, int):
            delta = f"{v_val - c_val:+,}" if isinstance(c_val, int) else None
            col.metric(
                metric,
                f"{v_val:,}",
                delta=delta,
                help=f"{c_name}: {c_val:,}" if isinstance(c_val, int) else c_val,
            )
        else:
            col.metric(metric, v_val, help=f"{c_name}: {c_val}")

    st.divider()

    # ── Views/day grouped bar ─────────────────────────
    st.subheader("🚀 Views/Day — Video by Video")
    vd_rows = []
    for v in v_uploads:
        vd_rows.append({"Channel": v_name, "Title": v["title"][:40], "Views/Day": int(v["views_per_day"])})
    for v in c_uploads:
        vd_rows.append({"Channel": c_name, "Title": v["title"][:40], "Views/Day": int(v["views_per_day"])})

    df_vd = pd.DataFrame(vd_rows)
    fig_vd = px.box(
        df_vd, x="Channel", y="Views/Day",
        color="Channel",
        color_discrete_map={v_name: "#6366f1", c_name: "#ef4444"},
        template="plotly_dark",
        title="Views/Day Distribution (box = spread, dot = outlier)",
        points="all",
    )
    fig_vd.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        showlegend=False,
    )
    st.plotly_chart(fig_vd, use_container_width=True)

    st.divider()

    # ── Title pattern analysis ────────────────────────
    st.subheader("🔤 Title Pattern Analysis")
    st.caption("Which content formats are each channel using in their titles?")

    v_patterns = _extract_patterns([v["title"] for v in v_uploads])
    c_patterns = _extract_patterns([v["title"] for v in c_uploads])

    p1, p2 = st.columns(2)
    with p1:
        st.markdown(f"**{v_name}**")
        if v_patterns:
            df_vp = pd.DataFrame(list(v_patterns.items()), columns=["Format", "Count"])
            fig_vp = px.bar(df_vp, x="Count", y="Format", orientation="h",
                            color_discrete_sequence=["#6366f1"],
                            template="plotly_dark")
            fig_vp.update_layout(paper_bgcolor="rgba(0,0,0,0)",
                                  plot_bgcolor="rgba(0,0,0,0)", height=250)
            st.plotly_chart(fig_vp, use_container_width=True)
        else:
            st.info("No common format keywords found.")

    with p2:
        st.markdown(f"**{c_name}**")
        if c_patterns:
            df_cp = pd.DataFrame(list(c_patterns.items()), columns=["Format", "Count"])
            fig_cp = px.bar(df_cp, x="Count", y="Format", orientation="h",
                            color_discrete_sequence=["#ef4444"],
                            template="plotly_dark")
            fig_cp.update_layout(paper_bgcolor="rgba(0,0,0,0)",
                                  plot_bgcolor="rgba(0,0,0,0)", height=250)
            st.plotly_chart(fig_cp, use_container_width=True)
        else:
            st.info("No common format keywords found.")

    st.divider()

    # ── Video tables side by side ─────────────────────
    st.subheader("📹 Recent Uploads")
    tab1, tab2 = st.tabs([f"{v_name}", f"{c_name}"])

    def _vtable(uploads):
        df = pd.DataFrame(uploads)[["title", "published", "views", "views_per_day", "url"]]
        df.columns = ["Title", "Published", "Views", "Views/Day", "URL"]
        df["Views/Day"] = df["Views/Day"].astype(int)
        df["Format"] = ["Short" if _is_short(v["duration_sec"]) else "Long" for v in uploads]
        st.dataframe(df, use_container_width=True, hide_index=True,
                     column_config={
                         "URL": st.column_config.LinkColumn("Watch", display_text="▶"),
                         "Views": st.column_config.NumberColumn(format="%d"),
                         "Views/Day": st.column_config.NumberColumn(format="%d"),
                     })

    with tab1: _vtable(v_uploads)
    with tab2: _vtable(c_uploads)
