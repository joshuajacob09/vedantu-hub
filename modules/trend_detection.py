# modules/trend_detection.py
# ─────────────────────────────────────────────────────
# Trend Detection — full rebuild.
#
# Old: dumped all titles into Gemini → generic output.
# New:
#   1. Quantitative title pattern frequency chart
#      (no AI needed, instant, zero quota)
#   2. Format trend breakdown (Shorts vs long-form
#      split by category — uses duration_sec)
#   3. Top videos by velocity (views/day leaderboard)
#   4. AI deep analysis (on-demand, Gemini)
# ─────────────────────────────────────────────────────

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from collections import Counter

from utils.registry import get_competitors_by_priority, get_competitors_by_category
from utils.ui import C, T, page_header, section_header, kpi_card, divider, empty_state, plotly_defaults
from utils.youtube_helpers import get_recent_uploads
from utils.api_clients import get_gemini_model


# Subject keywords for edtech topic extraction
SUBJECT_KEYWORDS = {
    "Physics":       ["physics", "mechanics", "optics", "thermodynamics", "electrostatics",
                      "waves", "modern physics", "current electricity"],
    "Chemistry":     ["chemistry", "organic", "inorganic", "physical chemistry",
                      "mole concept", "equilibrium", "electrochemistry"],
    "Mathematics":   ["maths", "math", "calculus", "algebra", "trigonometry",
                      "coordinate geometry", "vectors", "matrices"],
    "Biology":       ["biology", "botany", "zoology", "genetics", "ecology",
                      "cell biology", "human physiology", "ncert"],
    "JEE Strategy":  ["jee mains", "jee advanced", "iit", "rank", "percentile",
                      "jee 2025", "jee 2026", "cutoff"],
    "NEET Strategy": ["neet", "aiims", "medical", "neet 2025", "neet 2026",
                      "neet ug", "mbbs"],
    "Revision":      ["revision", "one shot", "1 shot", "crash course", "quick revision",
                      "last minute", "short notes"],
    "PYQ":           ["previous year", "pyq", "past paper", "2024 paper",
                      "2023 paper", "solved paper"],
}


def _is_short(duration_sec: int) -> bool:
    return 0 < duration_sec <= 60


def _tag_subjects(title: str) -> list[str]:
    title_lower = title.lower()
    tags = []
    for subject, keywords in SUBJECT_KEYWORDS.items():
        if any(kw in title_lower for kw in keywords):
            tags.append(subject)
    return tags if tags else ["Other"]


def render():
    page_header('Trend Detection', 'What the market is doing right now — data-first, AI on demand.', '📈')

    # Scope selector
    col1, col2 = st.columns([2, 1])
    with col1:
        scope = st.radio(
            "Competitor scope",
            ["Tier 1 (12 channels — fast)", "Tier 1 + 2 (38 channels — thorough)"],
            horizontal=True,
        )
    with col2:
        category_filter = st.selectbox(
            "Category focus",
            ["All", "JEE", "NEET", "Class 8-12", "Boards"]
        )

    if st.button("🔍 Analyse Trends Now", type="primary", use_container_width=True):
        max_tier = 1 if "Tier 1" in scope else 2
        _run_analysis(max_tier, category_filter)


def _run_analysis(max_tier: int, category_filter: str):
    # ── Fetch data ────────────────────────────────────
    if category_filter != "All":
        competitors = [
            c for c in get_competitors_by_category(category_filter)
            if c["priority"] <= max_tier
        ]
    else:
        competitors = [
            c for c in
            (get_competitors_by_priority(1) +
             (get_competitors_by_priority(2) if max_tier == 2 else []))
        ]

    all_videos = []
    progress = st.progress(0, text="Fetching data...")
    for i, c in enumerate(competitors):
        progress.progress((i + 1) / len(competitors), text=f"Scanning {c['name']}...")
        uploads = get_recent_uploads(c["id"])
        for v in uploads:
            v["channel_name"] = c["name"]
            v["tier"]         = c["priority"]
            v["is_short"]     = _is_short(v["duration_sec"])
            v["subjects"]     = _tag_subjects(v["title"])
            all_videos.append(v)
    progress.empty()

    if not all_videos:
        st.error("No data fetched.")
        return

    st.success(f"Analysed **{len(all_videos)} videos** across **{len(competitors)} channels**")

    # ── SECTION 1: Velocity Leaderboard ───────────────
    st.subheader("🏆 Velocity Leaderboard — Top 10 Videos This Week")
    st.caption("Ranked by views/day. These are the formats students are watching most right now.")

    df = pd.DataFrame(all_videos)
    top10 = df.nlargest(10, "views_per_day")[
        ["channel_name", "title", "views", "views_per_day", "is_short", "url"]
    ].copy()
    top10["Format"]      = top10["is_short"].apply(lambda x: "Short" if x else "Long-form")
    top10["Views/Day"]   = top10["views_per_day"].astype(int)
    top10.columns        = ["Channel", "Title", "Views", "views_per_day",
                             "is_short", "URL", "Format", "Views/Day"]

    st.dataframe(
        top10[["Channel", "Title", "Format", "Views", "Views/Day", "URL"]],
        use_container_width=True,
        hide_index=True,
        column_config={
            "URL":       st.column_config.LinkColumn("Watch", display_text="▶"),
            "Views":     st.column_config.NumberColumn(format="%d"),
            "Views/Day": st.column_config.NumberColumn(format="%d"),
        }
    )

    st.divider()

    # ── SECTION 2: Subject demand breakdown ───────────
    st.subheader("📚 Subject Demand — What Are Students Watching?")

    subject_counts  = Counter()
    subject_views   = Counter()
    for v in all_videos:
        for subj in v["subjects"]:
            subject_counts[subj]  += 1
            subject_views[subj]   += v["views"]

    df_subj = pd.DataFrame([
        {"Subject": s, "Videos": subject_counts[s], "Total Views": subject_views[s]}
        for s in subject_counts
    ]).sort_values("Total Views", ascending=False)

    col1, col2 = st.columns(2)
    with col1:
        fig_s1 = px.bar(
            df_subj, x="Subject", y="Videos",
            title="Upload Volume by Subject",
            color="Videos",
            color_continuous_scale="blues",
            template="plotly_dark",
        )
        fig_s1.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            showlegend=False, xaxis_tickangle=-20,
        )
        st.plotly_chart(fig_s1, use_container_width=True)

    with col2:
        fig_s2 = px.bar(
            df_subj, x="Subject", y="Total Views",
            title="Total Views by Subject",
            color="Total Views",
            color_continuous_scale="reds",
            template="plotly_dark",
        )
        fig_s2.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            showlegend=False, xaxis_tickangle=-20,
        )
        st.plotly_chart(fig_s2, use_container_width=True)

    st.divider()

    # ── SECTION 3: Shorts vs Long-form performance ────
    st.subheader("🎬 Format War — Shorts vs Long-form")

    shorts_vids   = [v for v in all_videos if v["is_short"]]
    long_vids     = [v for v in all_videos if not v["is_short"]]

    s_avg_vpd = sum(v["views_per_day"] for v in shorts_vids)  / len(shorts_vids)  if shorts_vids  else 0
    l_avg_vpd = sum(v["views_per_day"] for v in long_vids)    / len(long_vids)    if long_vids    else 0
    s_avg_views = sum(v["views"] for v in shorts_vids) / len(shorts_vids) if shorts_vids else 0
    l_avg_views = sum(v["views"] for v in long_vids)   / len(long_vids)   if long_vids   else 0

    f1, f2, f3, f4 = st.columns(4)
    f1.metric("Shorts Count",          len(shorts_vids))
    f2.metric("Shorts Avg Views/Day",  f"{int(s_avg_vpd):,}")
    f3.metric("Long-form Count",       len(long_vids))
    f4.metric("Long-form Avg Views/Day", f"{int(l_avg_vpd):,}")

    # Per-channel format mix
    channel_format = {}
    for v in all_videos:
        ch = v["channel_name"]
        if ch not in channel_format:
            channel_format[ch] = {"Shorts": 0, "Long": 0}
        if v["is_short"]:
            channel_format[ch]["Shorts"] += 1
        else:
            channel_format[ch]["Long"]   += 1

    df_fmt = pd.DataFrame([
        {"Channel": ch, "Shorts": d["Shorts"], "Long-form": d["Long"]}
        for ch, d in channel_format.items()
    ])
    df_fmt["Total"]    = df_fmt["Shorts"] + df_fmt["Long-form"]
    df_fmt["Shorts %"] = (df_fmt["Shorts"] / df_fmt["Total"] * 100).round(0)
    df_fmt = df_fmt.sort_values("Shorts %", ascending=False)

    fig_fmt = go.Figure()
    fig_fmt.add_trace(go.Bar(
        name="Shorts", x=df_fmt["Channel"], y=df_fmt["Shorts"],
        marker_color="#f59e0b",
    ))
    fig_fmt.add_trace(go.Bar(
        name="Long-form", x=df_fmt["Channel"], y=df_fmt["Long-form"],
        marker_color="#6366f1",
    ))
    fig_fmt.update_layout(
        barmode="stack", template="plotly_dark",
        title="Format Mix per Competitor Channel",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        xaxis_tickangle=-30,
        height=340,
        legend=dict(orientation="h", y=1.1),
    )
    st.plotly_chart(fig_fmt, use_container_width=True)

    st.divider()

    # ── SECTION 4: AI Deep Analysis (on-demand) ───────
    st.subheader("🤖 AI Deep Analysis")
    st.caption("Gemini reads all the data above and gives strategic recommendations. "
               "Only run when you need narrative insight.")

    if st.button("✨ Run AI Analysis", type="secondary"):
        top_titles = [
            f"[{v['channel_name']}] {v['title']} ({int(v['views_per_day']):,}/day)"
            for v in sorted(all_videos, key=lambda x: x["views_per_day"], reverse=True)[:40]
        ]
        subj_summary = ", ".join([f"{r['Subject']}: {r['Videos']} videos" for _, r in df_subj.iterrows()])

        prompt = f"""
You are a senior YouTube growth strategist for Vedantu, an Indian edtech platform.

Data from {len(competitors)} competitor channels — {len(all_videos)} videos analysed:

TOP PERFORMING VIDEOS (by views/day):
{chr(10).join(top_titles)}

SUBJECT DEMAND:
{subj_summary}

FORMAT SPLIT: {len(shorts_vids)} Shorts (avg {int(s_avg_vpd):,} views/day) vs {len(long_vids)} Long-form (avg {int(l_avg_vpd):,} views/day)

Based on this live market data, provide:
1. **3 Emerging Trends** — topics gaining velocity that Vedantu should act on THIS week
2. **Format Recommendation** — should Vedantu push more Shorts or Long-form right now, and why?
3. **The #1 Topic to Cover** — the single most important video Vedantu should make this week
4. **One Insight That Isn't Obvious** — something in the data that most teams would miss

Be specific. Reference actual channel names and video titles from the data. 4 paragraphs max.
        """
        with st.spinner("Gemini is reading the market..."):
            response = get_gemini_model().generate_content(prompt)
        st.markdown(response.text)
