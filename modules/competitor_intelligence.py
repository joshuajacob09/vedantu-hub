# modules/competitor_intelligence.py — Enterprise UI. Logic unchanged.

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from utils.registry import (get_all_competitors, get_competitors_by_category,
                             get_competitors_by_priority, get_categories_available,
                             get_registry_stats, as_name_id_dict)
from utils.youtube_helpers import get_channel_info, get_recent_uploads, get_recent_livestreams
from utils.ui import C, page_header, section_header, kpi_card, divider, empty_state, plotly_defaults, badge

TIER_COLOR = {1: C["danger"], 2: C["warning"], 3: C["text3"]}


def render():
    page_header("Competitor Intelligence",
                "Analyse uploads, livestreams, and performance across 59 tracked channels.")

    stats = get_registry_stats()
    k1, k2, k3, k4, k5 = st.columns(5)
    with k1: kpi_card("Total Tracked", str(stats["total"]))
    with k2: kpi_card("Tier 1", str(stats["tier1"]), sublabel="Direct competitors")
    with k3: kpi_card("Tier 2", str(stats["tier2"]), sublabel="Significant players")
    with k4: kpi_card("Tier 3", str(stats["tier3"]), sublabel="Niche / specialist")
    with k5: kpi_card("Active", str(stats["active"]))

    divider()

    view = st.radio("", ["Single Channel", "Category Overview", "Compare Channels"],
                    horizontal=True, label_visibility="collapsed")

    if   view == "Single Channel":      _single()
    elif view == "Category Overview":   _category()
    else:                                _compare()


def _single():
    section_header("Single Channel Analysis")
    c1, c2, c3 = st.columns(3)
    with c1: cat_f  = st.selectbox("Category", ["All"] + get_categories_available(), key="si_cat")
    with c2: tier_f = st.selectbox("Tier",     ["All","Tier 1","Tier 2","Tier 3"],   key="si_tier")
    with c3: lang_f = st.selectbox("Language", ["All","Hindi","English","Tamil","Telugu"], key="si_lang")

    pool = get_all_competitors()
    if cat_f  != "All": pool = [c for c in pool if cat_f in c["category"]]
    if tier_f != "All": pool = [c for c in pool if c["priority"] == int(tier_f.split()[1])]
    if lang_f != "All": pool = [c for c in pool if c["language"] == lang_f]

    if not pool:
        empty_state("No channels match these filters.")
        return

    sel_name = st.selectbox(f"Channel ({len(pool)} matching)",
                             [c["name"] for c in pool], key="si_ch")
    sel = next(c for c in pool if c["name"] == sel_name)

    tc = TIER_COLOR[sel["priority"]]
    meta_cols = st.columns(4)
    for col, txt in zip(meta_cols, [
        f"Tier {sel['priority']}",
        ", ".join(sel["category"]),
        sel["language"],
        "Active" if sel["active"] else "Inactive",
    ]):
        col.markdown(f"""
        <div style="background:{C['card']};border:1px solid {C['border']};
                    border-radius:8px;padding:8px 14px;font-size:12px;
                    font-weight:500;color:{C['text2']};">{txt}</div>
        """, unsafe_allow_html=True)

    st.markdown("<div style='margin:16px 0'/>", unsafe_allow_html=True)

    with st.spinner("Loading..."):
        info    = get_channel_info(sel["id"])
        uploads = get_recent_uploads(sel["id"])
        streams = get_recent_livestreams(sel["id"])

    if not info:
        st.error("Could not fetch channel data.")
        return

    avg_vpd = round(sum(v["views_per_day"] for v in uploads)/len(uploads)) if uploads else 0
    k1, k2, k3, k4 = st.columns(4)
    with k1: kpi_card("Subscribers",    f"{info['subscribers']:,}")
    with k2: kpi_card("Total Views",    f"{info['total_views']:,}")
    with k3: kpi_card("Videos",         f"{info['video_count']:,}")
    with k4: kpi_card("Avg Views/Day",  f"{int(avg_vpd):,}", sublabel="recent uploads")

    divider()
    tab1, tab2 = st.tabs(["Uploads", "Livestreams"])
    with tab1: _vtable(uploads)
    with tab2: _vtable(streams)


def _category():
    section_header("Category Overview")
    cat = st.selectbox("", get_categories_available(), label_visibility="collapsed", key="cat_sel")
    pool = get_competitors_by_category(cat)
    if not pool:
        empty_state("No channels in this category.")
        return

    with st.spinner(f"Loading {len(pool)} channels..."):
        rows = []
        for c in pool:
            info = get_channel_info(c["id"])
            if info:
                rows.append({
                    "Channel":     c["name"],
                    "Tier":        c["priority"],
                    "Language":    c["language"],
                    "Subscribers": info["subscribers"],
                    "Total Views": info["total_views"],
                })

    if not rows:
        empty_state("No data available.")
        return

    df = pd.DataFrame(rows).sort_values("Subscribers", ascending=True).tail(10)
    fig = px.bar(df, x="Subscribers", y="Channel", orientation="h",
                 color="Tier",
                 color_discrete_map={1: C["danger"], 2: C["warning"], 3: C["text3"]})
    fig.update_traces(marker_line_width=0)
    fig.update_layout(**plotly_defaults(height=max(280, len(df)*30)))
    fig.update_layout(legend=dict(orientation="h", y=1.05, bgcolor="rgba(0,0,0,0)"))
    st.plotly_chart(fig, use_container_width=True)

    df_disp = df.sort_values("Subscribers", ascending=False).copy()
    df_disp["Subscribers"] = df_disp["Subscribers"].apply(lambda x: f"{x:,}")
    df_disp["Total Views"]  = df_disp["Total Views"].apply(lambda x: f"{x:,}")
    df_disp["Tier"] = df_disp["Tier"].apply(lambda x: f"Tier {x}")
    st.dataframe(df_disp, use_container_width=True, hide_index=True)


def _compare():
    section_header("Compare Channels", "Select up to 6 channels")
    all_c    = get_all_competitors()
    defaults = [c["name"] for c in all_c if c["priority"] == 1][:3]
    names    = st.multiselect("", [c["name"] for c in all_c],
                               default=defaults, max_selections=6,
                               label_visibility="collapsed")
    if len(names) < 2:
        empty_state("Select at least 2 channels to compare.")
        return

    selected = [c for c in all_c if c["name"] in names]
    with st.spinner("Fetching..."):
        rows = []; vdata = {}
        for c in selected:
            info = get_channel_info(c["id"])
            ups  = get_recent_uploads(c["id"])
            if not info or not ups: continue
            avg_vpd = sum(v["views_per_day"] for v in ups)/len(ups)
            rows.append({
                "Channel":       c["name"],
                "Subscribers":   info["subscribers"],
                "Avg Views/Day": int(avg_vpd),
            })
            vdata[c["name"]] = ups

    if not rows:
        empty_state("No data returned.")
        return

    df = pd.DataFrame(rows).sort_values("Avg Views/Day", ascending=True)
    fig = go.Figure()
    fig.add_trace(go.Bar(name="Subscribers",   x=df["Subscribers"],   y=df["Channel"],
                         orientation="h", marker_color=C["accent"],    marker_line_width=0))
    fig.add_trace(go.Bar(name="Avg Views/Day", x=df["Avg Views/Day"], y=df["Channel"],
                         orientation="h", marker_color=C["warning"],   marker_line_width=0))
    fig.update_layout(**plotly_defaults(height=max(260, len(df)*36)))
    fig.update_layout(barmode="group",
                      legend=dict(orientation="h", y=1.05, bgcolor="rgba(0,0,0,0)"))
    st.plotly_chart(fig, use_container_width=True)

    for name, videos in vdata.items():
        with st.expander(f"{name} — recent uploads"):
            _vtable(videos)


def _vtable(videos):
    if not videos:
        empty_state("No data.")
        return
    df = pd.DataFrame(videos)
    for col in ["title","published","views","views_per_day","url"]:
        if col not in df.columns: df[col] = ""
    df = df[["title","published","views","views_per_day","url"]].copy()
    df.columns = ["Title","Published","Views","Views/Day","URL"]
    df["Views/Day"] = pd.to_numeric(df["Views/Day"], errors="coerce").fillna(0).astype(int)
    st.dataframe(df, use_container_width=True, hide_index=True,
                 column_config={
                     "URL":       st.column_config.LinkColumn("Watch", display_text="▶"),
                     "Views":     st.column_config.NumberColumn(format="%d"),
                     "Views/Day": st.column_config.NumberColumn(format="%d"),
                 })
