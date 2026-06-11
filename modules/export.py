# modules/export.py
# Export channel data to CSV or JSON.
# Lets managers download raw data for offline analysis.

import streamlit as st
import pandas as pd
import json
from config import ALL_CHANNELS, VEDANTU_CHANNELS, COMPETITOR_CHANNELS
from utils.youtube_helpers import get_recent_uploads, get_channel_info


def render():
    st.header("⬇️ Export Data")
    st.caption("Download raw channel data as CSV or JSON for offline analysis.")

    # ── Options ───────────────────────────────────────
    col1, col2 = st.columns(2)

    with col1:
        scope = st.selectbox("Channel scope", [
            "Vedantu channels only",
            "Competitors only",
            "All channels",
            "Single channel",
        ])

    with col2:
        fmt = st.radio("Format", ["CSV", "JSON"], horizontal=True)

    # Single channel picker
    if scope == "Single channel":
        channel_name = st.selectbox("Pick a channel", list(ALL_CHANNELS.keys()))

    if st.button("📦 Prepare Export", type="primary"):
        _run_export(scope, fmt,
                    channel_name if scope == "Single channel" else None)


def _run_export(scope: str, fmt: str, single_channel: str | None):
    # Decide channels
    if scope == "Vedantu channels only":
        channels = VEDANTU_CHANNELS
    elif scope == "Competitors only":
        channels = COMPETITOR_CHANNELS
    elif scope == "Single channel":
        channels = {single_channel: ALL_CHANNELS[single_channel]}
    else:
        channels = ALL_CHANNELS

    rows = []
    progress = st.progress(0, text="Fetching data...")
    channel_list = list(channels.items())

    for i, (name, cid) in enumerate(channel_list):
        progress.progress((i + 1) / len(channel_list), text=f"Fetching {name}...")
        info   = get_channel_info(cid)
        videos = get_recent_uploads(cid)
        for v in videos:
            rows.append({
                "channel_name":  name,
                "channel_id":    cid,
                "subscribers":   info.get("subscribers", 0) if info else 0,
                "total_views":   info.get("total_views", 0) if info else 0,
                "title":         v["title"],
                "published":     v["published"],
                "views":         v["views"],
                "views_per_day": int(v["views_per_day"]),
                "likes":         v.get("likes", 0),
                "comments":      v.get("comments", 0),
                "url":           v["url"],
            })

    progress.empty()

    if not rows:
        st.error("No data fetched. Check channel IDs in config.py.")
        return

    df = pd.DataFrame(rows)
    st.success(f"Ready — {len(rows)} videos across {len(channels)} channels.")
    st.dataframe(df.head(20), use_container_width=True, hide_index=True)
    st.caption(f"Preview: first 20 of {len(rows)} rows.")

    if fmt == "CSV":
        st.download_button(
            label="⬇️ Download CSV",
            data=df.to_csv(index=False),
            file_name="vedantu_export.csv",
            mime="text/csv",
        )
    else:
        st.download_button(
            label="⬇️ Download JSON",
            data=json.dumps(rows, indent=2),
            file_name="vedantu_export.json",
            mime="application/json",
        )
