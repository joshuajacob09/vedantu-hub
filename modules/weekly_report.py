# modules/weekly_report.py — Fixes 4, 8, 9, 13.

import re, streamlit as st
from datetime import date
from config import VEDANTU_CHANNELS, TOP_COMPETITORS
from utils.ui import C, T, page_header, section_header, divider, report_section
from utils.youtube_helpers import get_channel_info, get_recent_uploads
from utils.api_clients import get_gemini_model


def render():
    # Fix #3/#11: no emoji in page_header
    page_header("Weekly Report", "One-click intelligence report using top 5 competitors.")

    v_name = st.selectbox("Vedantu channel", list(VEDANTU_CHANNELS.keys()))

    if st.button("Generate Report", type="primary"):
        _generate_report(v_name, VEDANTU_CHANNELS[v_name])


def _parse_sections(text: str) -> list[tuple[str,str]]:
    """
    Parse Gemini markdown output into (title, content) pairs.
    Fix #4: render as styled cards, not raw markdown dump.
    """
    # Split on ## or bold **Title** patterns
    parts = re.split(r'\n(?=#{1,3}\s|\*\*\d+\.)', text.strip())
    sections = []
    for part in parts:
        part = part.strip()
        if not part:
            continue
        # Extract heading
        m = re.match(r'^#{1,3}\s*(.+?)[\n\r]', part)
        if not m:
            m = re.match(r'^\*\*(.+?)\*\*', part)
        if m:
            title   = m.group(1).strip().lstrip('0123456789. ')
            content = part[m.end():].strip()
        else:
            title   = "Summary"
            content = part
        # Clean markdown bold from content
        content = re.sub(r'\*\*(.+?)\*\*', r'\1', content)
        content = content.replace('\n', '<br>')
        if content:
            sections.append((title, content))
    return sections if sections else [("Report", text.replace('\n','<br>'))]


def _generate_report(v_name, v_id):
    today = date.today().strftime("%B %d, %Y")

    with st.spinner("Fetching channel data..."):
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
                    f"{c_name}: {c_info.get('subscribers',0):,} subs | "
                    f"Avg views/day: {avg_vpd:,.0f} | "
                    f"Top: '{top_vid['title'][:50]}' ({top_vid['views']:,} views)"
                )

    with st.spinner("Generating report..."):
        prompt = f"""Weekly YouTube intelligence report for Vedantu content team.
Date: {today}

Vedantu channel ({v_name}):
- Subscribers: {v_info.get('subscribers','N/A'):,}
- Recent uploads: {[v['title'] for v in v_videos]}

Competitor summary:
{chr(10).join(comp_summary)}

Write sections:
## Executive Summary
## Vedantu Performance
## Competitor Watch
## Trending Topics
## Recommended Actions
## Risk to Watch

Keep each section to 3-5 bullet points. Be specific and direct."""

        response = get_gemini_model().generate_content(prompt)

    # Fix #13: use section_header, not raw st.markdown heading
    section_header(f"Weekly Intelligence Report — {today}")

    # Fix #4: parse and render as cards
    sections = _parse_sections(response.text)
    for title, content in sections:
        report_section(title, content)

    divider()

    st.download_button(
        label="Download as .txt",
        data=response.text,
        file_name=f"vedantu_report_{date.today().isoformat()}.txt",
        mime="text/plain",
    )
