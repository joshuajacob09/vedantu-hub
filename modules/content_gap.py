# modules/content_gap.py
# ─────────────────────────────────────────────────────
# Content Gap Analysis — full rebuild.
#
# Old: 1 Vedantu channel vs 1 competitor.
# New: Vedantu's full network vs full competitor landscape.
#
# Two modes:
#   1. Network Gap Map — all subjects, who covers what
#   2. Deep Gap — Vedantu channel vs multiple competitors
# ─────────────────────────────────────────────────────

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from collections import defaultdict

from config import VEDANTU_CHANNELS, COMPETITOR_CHANNELS
from utils.registry import get_competitors_by_priority, get_competitors_by_category
from utils.ui import C, T, page_header, section_header, kpi_card, divider, empty_state, plotly_defaults
from utils.youtube_helpers import get_recent_uploads
from utils.api_clients import get_gemini_model


SUBJECT_KEYWORDS = {
    "Physics":        ["physics", "mechanics", "optics", "thermodynamics",
                       "electrostatics", "waves", "modern physics"],
    "Chemistry":      ["chemistry", "organic", "inorganic", "mole concept",
                       "equilibrium", "electrochemistry"],
    "Mathematics":    ["maths", "math", "calculus", "algebra", "trigonometry",
                       "coordinate geometry", "vectors", "matrices"],
    "Biology":        ["biology", "botany", "zoology", "genetics",
                       "cell biology", "physiology", "ncert bio"],
    "JEE Prep":       ["jee mains", "jee advanced", "iit", "jee 2025", "jee 2026"],
    "NEET Prep":      ["neet", "aiims", "neet 2025", "neet 2026", "neet ug"],
    "Revision":       ["revision", "one shot", "1 shot", "crash course",
                       "quick revision", "last minute"],
    "PYQ / Papers":   ["previous year", "pyq", "past paper", "2024 paper",
                       "solved paper", "question paper"],
    "Motivation":     ["motivation", "success", "rank", "topper", "strategy",
                       "how to study", "study plan"],
    "Shorts Content": ["#shorts", "short", "60 seconds", "quick"],
}


def _tag(title: str) -> list[str]:
    t = title.lower()
    return [s for s, kws in SUBJECT_KEYWORDS.items() if any(k in t for k in kws)] or ["General"]


def render():
    page_header('Content Gap Analysis', 'See the full picture of what the market covers vs what Vedantu covers.', '🔍')

    mode = st.radio(
        "Analysis mode",
        ["🗺️ Network Gap Map (all channels)",
         "🎯 Deep Gap — Pick Channels"],
        horizontal=True,
    )

    if mode == "🗺️ Network Gap Map (all channels)":
        _network_gap_map()
    else:
        _deep_gap()


# ─────────────────────────────────────────────────────
# MODE 1: Full network gap map
# ─────────────────────────────────────────────────────
def _network_gap_map():
    st.subheader("Network Gap Map")
    st.caption(
        "Each subject row shows how many videos Vedantu posted vs the competitor average. "
        "Red = Vedantu is behind. Green = Vedantu is leading."
    )

    col1, col2 = st.columns(2)
    with col1:
        tier = st.radio("Competitor scope", ["Tier 1 only", "Tier 1 + 2"], horizontal=True)
    with col2:
        vedantu_scope = st.multiselect(
            "Vedantu channels to include",
            list(VEDANTU_CHANNELS.keys()),
            default=list(VEDANTU_CHANNELS.keys())[:5],
        )

    if st.button("📊 Build Gap Map", type="primary"):
        _build_gap_map(tier, vedantu_scope)


def _build_gap_map(tier: str, vedantu_scope: list):
    max_tier = 1 if "Tier 1 only" in tier else 2
    competitors = [c for c in
                   (get_competitors_by_priority(1) +
                    (get_competitors_by_priority(2) if max_tier == 2 else []))]

    # Fetch Vedantu data
    with st.spinner("Fetching Vedantu network data..."):
        vedantu_subject_counts = defaultdict(int)
        for name in vedantu_scope:
            cid = VEDANTU_CHANNELS[name]
            uploads = get_recent_uploads(cid)
            for v in uploads:
                for subj in _tag(v["title"]):
                    vedantu_subject_counts[subj] += 1

    # Fetch competitor data
    comp_subject_counts = defaultdict(lambda: defaultdict(int))
    progress = st.progress(0, text="Fetching competitor data...")
    for i, c in enumerate(competitors):
        progress.progress((i + 1) / len(competitors), text=f"Scanning {c['name']}...")
        uploads = get_recent_uploads(c["id"])
        for v in uploads:
            for subj in _tag(v["title"]):
                comp_subject_counts[c["name"]][subj] += 1
    progress.empty()

    # Build comparison table
    all_subjects = list(SUBJECT_KEYWORDS.keys()) + ["General"]
    rows = []
    for subj in all_subjects:
        v_count    = vedantu_subject_counts.get(subj, 0)
        comp_avg   = sum(
            comp_subject_counts[c["name"]].get(subj, 0)
            for c in competitors
        ) / len(competitors) if competitors else 0
        comp_max   = max(
            (comp_subject_counts[c["name"]].get(subj, 0) for c in competitors),
            default=0
        )
        gap        = round(v_count - comp_avg, 1)
        rows.append({
            "Subject":       subj,
            "Vedantu Videos": v_count,
            "Comp Avg":      round(comp_avg, 1),
            "Comp Max":      comp_max,
            "Gap":           gap,
            "Status":        "✅ Leading" if gap >= 0 else "⚠️ Behind" if gap >= -2 else "🔴 Gap",
        })

    df = pd.DataFrame(rows).sort_values("Gap")

    # Gap bar chart
    fig = go.Figure()
    colors = ["#22c55e" if g >= 0 else "#f59e0b" if g >= -2 else "#ef4444"
              for g in df["Gap"]]
    fig.add_trace(go.Bar(
        x=df["Gap"],
        y=df["Subject"],
        orientation="h",
        marker_color=colors,
        text=df["Gap"].apply(lambda x: f"{x:+.1f}"),
        textposition="outside",
    ))
    fig.add_vline(x=0, line_width=1, line_color="#4b5563")
    fig.update_layout(
        title="Content Gap: Vedantu uploads minus competitor average",
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        height=420,
        xaxis_title="Gap (positive = Vedantu leads, negative = Vedantu behind)",
    )
    st.plotly_chart(fig, use_container_width=True)

    # Full table
    st.dataframe(df, use_container_width=True, hide_index=True,
                 column_config={
                     "Vedantu Videos": st.column_config.NumberColumn(format="%d"),
                     "Comp Avg":       st.column_config.NumberColumn(format="%.1f"),
                     "Comp Max":       st.column_config.NumberColumn(format="%d"),
                     "Gap":            st.column_config.NumberColumn(format="%.1f"),
                 })

    # ── Critical gaps summary ─────────────────────────
    critical = df[df["Gap"] < -2]
    if not critical.empty:
        st.error(f"🔴 **{len(critical)} critical gaps** — Vedantu is significantly behind competitors:")
        for _, row in critical.iterrows():
            st.markdown(
                f"- **{row['Subject']}**: Vedantu has {int(row['Vedantu Videos'])} videos, "
                f"competitors average {row['Comp Avg']:.1f}, max {int(row['Comp Max'])}"
            )


# ─────────────────────────────────────────────────────
# MODE 2: Deep gap with AI
# ─────────────────────────────────────────────────────
def _deep_gap():
    st.subheader("Deep Gap Analysis")

    col1, col2 = st.columns(2)
    with col1:
        v_name = st.selectbox("Vedantu channel", list(VEDANTU_CHANNELS.keys()))
    with col2:
        comp_names = st.multiselect(
            "Competitors to compare against (select up to 5)",
            list(COMPETITOR_CHANNELS.keys()),
            default=list(COMPETITOR_CHANNELS.keys())[:3],
            max_selections=5,
        )

    if st.button("🧠 Find Deep Gaps", type="primary"):
        if not comp_names:
            st.warning("Select at least one competitor.")
            return
        _run_deep_gap(v_name, VEDANTU_CHANNELS[v_name], comp_names)


def _run_deep_gap(v_name, v_id, comp_names):
    with st.spinner("Fetching video data..."):
        v_uploads = get_recent_uploads(v_id)
        v_titles  = [v["title"] for v in v_uploads]
        v_subjs   = defaultdict(int)
        for v in v_uploads:
            for s in _tag(v["title"]):
                v_subjs[s] += 1

        comp_data = {}
        for cname in comp_names:
            cid      = COMPETITOR_CHANNELS[cname]
            uploads  = get_recent_uploads(cid)
            c_subjs  = defaultdict(int)
            for v in uploads:
                for s in _tag(v["title"]):
                    c_subjs[s] += 1
            comp_data[cname] = {
                "titles":   [v["title"] for v in uploads],
                "subjects": dict(c_subjs),
                "top_vpd":  max((v["views_per_day"] for v in uploads), default=0),
            }

    # ── Subject coverage heatmap ──────────────────────
    st.subheader("📊 Subject Coverage Heatmap")
    all_subjects = list(SUBJECT_KEYWORDS.keys())
    heatmap_data = {"Subject": all_subjects}
    heatmap_data[v_name] = [v_subjs.get(s, 0) for s in all_subjects]
    for cname in comp_names:
        heatmap_data[cname] = [comp_data[cname]["subjects"].get(s, 0) for s in all_subjects]

    df_heat = pd.DataFrame(heatmap_data).set_index("Subject")
    fig_h = px.imshow(
        df_heat.T,
        color_continuous_scale=[[0, "#0f1117"], [0.3, "#1a1d2e"],
                                 [0.7, "#6366f1"], [1, "#22c55e"]],
        template="plotly_dark",
        title="Videos per subject per channel (brighter = more coverage)",
        text_auto=True,
    )
    fig_h.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        height=300,
    )
    st.plotly_chart(fig_h, use_container_width=True)

    st.divider()

    # ── AI gap report ─────────────────────────────────
    st.subheader("🤖 AI Gap Report")
    comp_context = []
    for cname, data in comp_data.items():
        comp_context.append(
            f"\n{cname} (top video: {int(data['top_vpd']):,} views/day):\n"
            + "\n".join(f"  - {t}" for t in data["titles"][:8])
        )

    prompt = f"""
You are a senior YouTube content strategist for Vedantu.

VEDANTU CHANNEL: {v_name}
Recent uploads:
{chr(10).join(f'  - {t}' for t in v_titles)}

COMPETITOR UPLOADS:
{''.join(comp_context)}

Perform a precise content gap analysis:

1. **Critical Gaps** (3 topics competitors cover heavily that {v_name} is missing entirely)
2. **Quality Gaps** (2 topics both cover but competitors do it better — cite specific title styles)
3. **Immediate Actions** (3 specific video titles {v_name} should publish this week)
4. **Format Gap** (are competitors using a format — Shorts, series, live — that {v_name} isn't?)
5. **One Opportunity Nobody Has Claimed Yet** (a gap in the entire market, not just Vedantu)

Be specific. Name subjects, topics, and title patterns.
Write as if presenting to a content VP who needs to make decisions today.
    """
    with st.spinner("Gemini is analysing gaps..."):
        try:
            response = get_gemini_model().generate_content(prompt)
            report_text = response.text
        except Exception:
            st.warning(
                "Gemini quota is unavailable right now, so the heatmap remains available but the AI gap report is skipped."
            )
            return
    st.markdown(report_text)
