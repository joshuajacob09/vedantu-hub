# modules/weekly_report.py
# Weekly Report Generator.
# QUOTA FIX: uses TOP_COMPETITORS (5 channels) instead of
# all 60 competitors, keeping daily quota impact low.

import streamlit as st
from datetime import date
from config import VEDANTU_CHANNELS, TOP_COMPETITORS
from utils.ui import C, T, page_header, divider
from utils.youtube_helpers import get_channel_info, get_recent_uploads
from utils.api_clients import get_gemini_model


def _format_subscribers(info: dict) -> str:
    subscribers = info.get("subscribers") if info else None
    return f"{subscribers:,}" if isinstance(subscribers, int) else "N/A"


def render():
    page_header('Weekly Report Generator', 'One-click intelligence report. Uses top 5 competitors to stay within API quota.', '📄')

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
- Subscribers: {_format_subscribers(v_info)}
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
        try:
            response = get_gemini_model().generate_content(prompt)
            report_text = response.text
        except Exception:
            st.warning(
                "Gemini quota is unavailable right now, so showing a data-only report instead."
            )
            top_uploads = "\n".join(
                f"- {v['title']} ({v['views']:,} views, {int(v['views_per_day']):,}/day)"
                for v in v_videos[:5]
            ) or "- No recent uploads found"
            competitor_lines = "\n".join(comp_summary) or "- No competitor data available"
            report_text = f"""## Weekly Intelligence Report — {today}

### Executive Summary
- {v_name} has {len(v_videos)} recent uploads in the current sample.
- Top competitor channels continue to be tracked from the quota-safe shortlist.

### Vedantu Performance This Week
{top_uploads}

### Competitor Watch
{competitor_lines}

### Recommended Actions for Next Week
1. Double down on the formats already appearing in the strongest recent uploads.
2. Prioritise topics where competitors are publishing consistently but Vedantu is lighter.
3. Re-run this report once Gemini quota is available for a fuller narrative.

### One Risk to Watch
- If quota remains exhausted, AI-generated commentary will be temporarily unavailable.

Report prepared by the Content Intelligence Hub | {today}"""

    st.markdown(f"## Weekly Intelligence Report — {today}")
    st.markdown(report_text)

    st.download_button(
        label="⬇️ Download as .txt",
        data=report_text,
        file_name=f"vedantu_report_{date.today().isoformat()}.txt",
        mime="text/plain",
    )
