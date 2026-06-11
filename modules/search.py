# modules/search.py
# Search across all 78 channels by keyword.
# Searches cached video titles — no extra API calls.

import streamlit as st
import pandas as pd
from config import ALL_CHANNELS, VEDANTU_CHANNELS
from utils.youtube_helpers import get_recent_uploads


def render():
    st.header("🔎 Search")
    st.caption("Search across all channels by keyword. Searches video titles from recent uploads.")

    query = st.text_input(
        "Enter a keyword or topic",
        placeholder="e.g. JEE Main 2025, NEET revision, organic chemistry"
    )

    scope = st.radio(
        "Search scope",
        ["All channels (78)", "Vedantu only", "Competitors only"],
        horizontal=True,
    )

    if st.button("🔍 Search", type="primary"):
        if not query.strip():
            st.warning("Please enter a keyword.")
            return
        _run_search(query.strip(), scope)


def _run_search(query: str, scope: str):
    # Decide which channel dict to use
    if scope == "Vedantu only":
        channels = VEDANTU_CHANNELS
    elif scope == "Competitors only":
        from config import COMPETITOR_CHANNELS
        channels = COMPETITOR_CHANNELS
    else:
        channels = ALL_CHANNELS

    results = []
    progress = st.progress(0, text="Searching channels...")
    channel_list = list(channels.items())

    for i, (name, cid) in enumerate(channel_list):
        progress.progress((i + 1) / len(channel_list), text=f"Searching {name}...")
        videos = get_recent_uploads(cid)
        for v in videos:
            if query.lower() in v["title"].lower():
                results.append({
                    "Channel":    name,
                    "Title":      v["title"],
                    "Published":  v["published"],
                    "Views":      v["views"],
                    "Views/Day":  int(v["views_per_day"]),
                    "URL":        v["url"],
                })

    progress.empty()

    if not results:
        st.info(f"No videos found matching **'{query}'** in recent uploads.")
        return

    st.success(f"Found **{len(results)} videos** matching '{query}'")

    df = pd.DataFrame(results).sort_values("Views", ascending=False)

    # Clickable URLs
    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True,
        column_config={
            "URL": st.column_config.LinkColumn("URL", display_text="▶ Watch"),
            "Views": st.column_config.NumberColumn("Views", format="%d"),
            "Views/Day": st.column_config.NumberColumn("Views/Day", format="%d"),
        }
    )

    # Download results
    st.download_button(
        label="⬇️ Download Search Results as CSV",
        data=df.to_csv(index=False),
        file_name=f"search_{query.replace(' ', '_')}.csv",
        mime="text/csv",
    )
