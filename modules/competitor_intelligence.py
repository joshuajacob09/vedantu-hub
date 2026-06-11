# modules/competitor_intelligence.py — UI refactored. Logic unchanged.

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from utils.registry import (get_all_competitors, get_competitors_by_category,
                             get_competitors_by_priority, get_categories_available,
                             get_registry_stats, as_name_id_dict)
from utils.youtube_helpers import get_channel_info, get_recent_uploads, get_recent_livestreams
from utils.ui import T, page_header, section_header, kpi_card, divider, empty_state, plotly_defaults, badge, label

TIER_LABEL = {
    1: ("🔴", "Tier 1 — Direct Competitor", T["red"]),
    2: ("🟡", "Tier 2 — Significant Player",  T["amber"]),
    3: ("⚪", "Tier 3 — Niche / Specialist",  T["text_muted"]),
}


def render():
    page_header("Competitor Intelligence",
                "Dynamic competitor registry — filter by category, tier, and language.",
                "🕵️")

    stats = get_registry_stats()
    c1, c2, c3, c4, c5 = st.columns(5)
    with c1: kpi_card("Total Tracked",  str(stats["total"]),  color="indigo")
    with c2: kpi_card("Tier 1",         str(stats["tier1"]),  color="red")
    with c3: kpi_card("Tier 2",         str(stats["tier2"]),  color="amber")
    with c4: kpi_card("Tier 3",         str(stats["tier3"]))
    with c5: kpi_card("Active",         str(stats["active"]), color="green")

    divider()

    view = st.radio("View", [
        "🔍 Single Channel Deep Dive",
        "📊 Category Overview",
        "⚔️ Multi-Channel Compare",
    ], horizontal=True, label_visibility="collapsed")

    if   view == "🔍 Single Channel Deep Dive": _single_channel()
    elif view == "📊 Category Overview":         _category_overview()
    else:                                         _multi_compare()


def _single_channel():
    section_header("Single Channel Deep Dive")
    c1, c2, c3 = st.columns(3)
    with c1: cat_f  = st.selectbox("Category", ["All"] + get_categories_available())
    with c2: tier_f = st.selectbox("Tier",     ["All", "Tier 1", "Tier 2", "Tier 3"])
    with c3: lang_f = st.selectbox("Language", ["All", "Hindi", "English", "Tamil", "Telugu", "Bilingual"])

    pool = get_all_competitors()
    if cat_f  != "All": pool = [c for c in pool if cat_f in c["category"]]
    if tier_f != "All": pool = [c for c in pool if c["priority"] == int(tier_f.split()[1])]
    if lang_f != "All": pool = [c for c in pool if c["language"] == lang_f]

    if not pool:
        empty_state("No channels match these filters. Try broadening your selection.", "🔍")
        return

    selected_name = st.selectbox(f"Select channel ({len(pool)} matching)",
                                  [c["name"] for c in pool])
    selected = next(c for c in pool if c["name"] == selected_name)

    emoji, tier_text, tier_color = TIER_LABEL[selected["priority"]]
    b1, b2, b3, b4 = st.columns(4)
    b1.markdown(f"""
    <div style="background:{T['bg_elevated']};border:1px solid {T['border_default']};
                border-radius:10px;padding:10px 14px;font-size:12px;font-weight:500;
                color:{T['text_secondary']};">
        📂 {', '.join(selected['category'])}
    </div>""", unsafe_allow_html=True)
    b2.markdown(f"""
    <div style="background:{T['bg_elevated']};border:1px solid {T['border_default']};
                border-radius:10px;padding:10px 14px;font-size:12px;font-weight:500;
                color:{T['text_secondary']};">
        🌐 {selected['language']}
    </div>""", unsafe_allow_html=True)
    b3.markdown(f"""
    <div style="background:{T['bg_elevated']};border:1px solid {tier_color}44;
                border-radius:10px;padding:10px 14px;font-size:12px;font-weight:500;
                color:{tier_color};">
        {emoji} {tier_text}
    </div>""", unsafe_allow_html=True)
    b4.markdown(f"""
    <div style="background:{T['green_dim']};border:1px solid {T['green']};
                border-radius:10px;padding:10px 14px;font-size:12px;font-weight:500;
                color:{T['green']};">
        {'✅ Active' if selected['active'] else '⏸ Inactive'}
    </div>""", unsafe_allow_html=True)

    st.markdown("<div style='margin:16px 0'/>", unsafe_allow_html=True)

    with st.spinner(f"Fetching {selected_name}..."):
        info        = get_channel_info(selected["id"])
        uploads     = get_recent_uploads(selected["id"])
        livestreams = get_recent_livestreams(selected["id"])

    if not info:
        st.error("Could not fetch channel data. Check the channel ID in competitors.py")
        return

    avg_vpd = round(sum(v["views_per_day"] for v in uploads) / len(uploads)) if uploads else 0
    k1, k2, k3, k4 = st.columns(4)
    with k1: kpi_card("Subscribers",      f"{info['subscribers']:,}",    color="indigo")
    with k2: kpi_card("Total Views",       f"{info['total_views']:,}")
    with k3: kpi_card("Total Videos",      f"{info['video_count']:,}")
    with k4: kpi_card("Avg Views/Day",     f"{int(avg_vpd):,}",           color="green")

    divider()
    tab1, tab2 = st.tabs(["📹 Latest Uploads", "🔴 Latest Livestreams"])
    with tab1: _video_table(uploads, selected_name, "uploads")
    with tab2: _video_table(livestreams, selected_name, "livestreams")


def _category_overview():
    section_header("Category Overview")
    cat = st.selectbox("Select category", get_categories_available())
    pool = get_competitors_by_category(cat)
    if not pool:
        empty_state("No active competitors in this category.")
        return

    with st.spinner(f"Loading {len(pool)} channels..."):
        rows = []
        for c in pool:
            info = get_channel_info(c["id"])
            if info:
                rows.append({
                    "Channel":     c["name"],
                    "Tier":        f"Tier {c['priority']}",
                    "Language":    c["language"],
                    "Subscribers": info["subscribers"],
                    "Total Views": info["total_views"],
                    "Videos":      info["video_count"],
                })

    if not rows:
        empty_state("Could not load channel data.")
        return

    df = pd.DataFrame(rows).sort_values("Subscribers", ascending=False)
    fig = px.bar(df, x="Channel", y="Subscribers", color="Tier",
                 color_discrete_map={"Tier 1": T["red"], "Tier 2": T["amber"], "Tier 3": T["text_muted"]})
    fig.update_layout(**plotly_defaults(), xaxis_tickangle=-30, height=340)
    fig.update_traces(marker_line_width=0)
    st.plotly_chart(fig, use_container_width=True)

    disp = df.copy()
    disp["Subscribers"] = disp["Subscribers"].apply(lambda x: f"{x:,}")
    disp["Total Views"]  = disp["Total Views"].apply(lambda x: f"{x:,}")
    disp["Videos"]       = disp["Videos"].apply(lambda x: f"{x:,}")
    st.dataframe(disp, use_container_width=True, hide_index=True)


def _multi_compare():
    section_header("Multi-Channel Compare", "Select up to 6 competitors")
    all_comps = get_all_competitors()
    defaults  = [c["name"] for c in all_comps if c["priority"] == 1][:3]
    selected_names = st.multiselect("Select channels (max 6)",
                                    [c["name"] for c in all_comps],
                                    default=defaults, max_selections=6)
    if len(selected_names) < 2:
        empty_state("Select at least 2 channels to compare.", "⚔️")
        return

    selected = [c for c in all_comps if c["name"] in selected_names]
    with st.spinner("Fetching data..."):
        rows = []; vdata = {}
        for c in selected:
            info    = get_channel_info(c["id"])
            uploads = get_recent_uploads(c["id"])
            if not info or not uploads: continue
            avg_vpd = sum(v["views_per_day"] for v in uploads) / len(uploads)
            top_vid = max(uploads, key=lambda v: v["views"])
            rows.append({
                "Channel":         c["name"],
                "Tier":            f"Tier {c['priority']}",
                "Subscribers":     info["subscribers"],
                "Total Views":     info["total_views"],
                "Avg Views/Day":   int(avg_vpd),
                "Top Video Views": top_vid["views"],
                "Top Video":       top_vid["title"][:45] + "...",
            })
            vdata[c["name"]] = uploads

    if not rows:
        empty_state("No data returned.")
        return

    df = pd.DataFrame(rows).sort_values("Avg Views/Day", ascending=False)
    fig = go.Figure()
    fig.add_trace(go.Bar(name="Subscribers",   x=df["Channel"], y=df["Subscribers"],
                         marker_color=T["indigo"], marker_line_width=0))
    fig.add_trace(go.Bar(name="Avg Views/Day", x=df["Channel"], y=df["Avg Views/Day"],
                         marker_color=T["amber"],  marker_line_width=0))
    fig.update_layout(**plotly_defaults(), barmode="group", xaxis_tickangle=-20, height=320)
    st.plotly_chart(fig, use_container_width=True)

    disp = df.copy()
    for col in ["Subscribers", "Total Views", "Avg Views/Day", "Top Video Views"]:
        disp[col] = disp[col].apply(lambda x: f"{x:,}")
    st.dataframe(disp, use_container_width=True, hide_index=True)

    divider()
    for name, videos in vdata.items():
        with st.expander(f"📹 {name} — recent uploads"):
            _video_table(videos, name, "uploads", compact=True)


def _video_table(videos, channel_name, label_text, compact=False):
    if not videos:
        empty_state(f"No {label_text} found for {channel_name}.", "📭")
        return
    df = pd.DataFrame(videos)
    for col in ["title","published","views","views_per_day","url"]:
        if col not in df.columns: df[col] = "" if col in ("title","published","url") else 0
    df = df[["title","published","views","views_per_day","url"]].copy()
    df.columns = ["Title","Published","Views","Views/Day","URL"]
    df["Views/Day"] = df["Views/Day"].astype(int)
    st.dataframe(df, use_container_width=True, hide_index=True,
                 column_config={
                     "URL":       st.column_config.LinkColumn("Watch", display_text="▶"),
                     "Views":     st.column_config.NumberColumn(format="%d"),
                     "Views/Day": st.column_config.NumberColumn(format="%d"),
                 })
    if not compact:
        fig = px.bar(df, x="Title", y="Views/Day", color="Views/Day",
                     color_continuous_scale=[[0,T["bg_overlay"]],[1,T["indigo"]]])
        fig.update_layout(**plotly_defaults(), xaxis_tickangle=-30,
                          showlegend=False, height=280, coloraxis_showscale=False)
        fig.update_traces(marker_line_width=0)
        st.plotly_chart(fig, use_container_width=True)
