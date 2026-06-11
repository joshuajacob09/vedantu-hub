# modules/weekly_report.py
# Weekly Report Generator.
# QUOTA FIX: uses TOP_COMPETITORS (5 channels) instead of
# all 60 competitors, keeping daily quota impact low.

import streamlit as st
from datetime import date
from config import VEDANTU_CHANNELS, TOP_COMPETITORS
from utils.youtube_helpers import get_channel_info, get_recent_uploads
from utils.api_clients import get_gemini_model


def render():
    st.header("📄 Weekly Report Generator")
    st.caption("One-click intelligence report. Uses top 5 competitors to stay within API quota.")

    v_name = st.selectbox("Primary Vedantu channel", list(VEDANTU_CHANNELS.keys()))

    if st.button("📊 Generate This Week's Report", type="primary"):
        _generate_report(v_name, VEDANTU_CHANNELS[v_name])


def _generate_report(v_name, v_id):
    today = date.today().strftime("%B %d, %Y")

    with st.spinner("Compiling data..."):
        v_info   = get_channel_info(v_id)
        v_videos = get_recent_uploads(v_id)

        comp_summary = []
        for c_name, c_id in TOP_COMPETITORS.items():
            c_info   = get_channel_info(c_id)
            c_videos = get_recent_uploads(c_id)
            if c_videos:
                avg_vpd = sum(v["views_per_day"] for v in c_videos) / len(c_videos)
                top_vid = max(c_videos, key=lambda v: v["views"])
                comp_summary.append(
                    f"{c_name}: {c_info.get('subscribers', 0):,} subs | "
                    f"Avg views/day: {avg_vpd:,.0f} | "
                    f"Top video: '{top_vid['title']}' ({top_vid['views']:,} views)"
                )

    with st.spinner("Gemini is writing the report..."):
        prompt = f"""
You are writing a weekly YouTube intelligence report for the Vedantu content team.
Date: {today}

Vedantu channel ({v_name}):
- Subscribers: {v_info.get('subscribers', 'N/A'):,}
- Recent uploads: {[v['title'] for v in v_videos]}

Top competitor summary:
{chr(10).join(comp_summary)}

Write a professional weekly report with these sections:
1. **Executive Summary** (3 sentences max)
2. **Vedantu Performance This Week**
3. **Competitor Watch** (who is surging, who is slowing)
4. **Top Trending Topics Across the Industry**
5. **Recommended Actions for Next Week** (numbered, specific)
6. **One Risk to Watch**

Tone: professional but readable. Use bullet points where helpful.
Sign off: "Report prepared by the Content Intelligence Hub | {today}"
        """
        response = get_gemini_model().generate_content(prompt)

    st.markdown(f"## Weekly Intelligence Report — {today}")
    st.markdown(response.text)

    st.download_button(
        label="⬇️ Download as .txt",
        data=response.text,
        file_name=f"vedantu_report_{date.today().isoformat()}.txt",
        mime="text/plain",
    )
