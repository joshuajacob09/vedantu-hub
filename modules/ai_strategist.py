# modules/ai_strategist.py — Enterprise UI. Logic unchanged.

import json, streamlit as st, plotly.graph_objects as go

from config import VEDANTU_CHANNELS
from utils.registry import get_competitors_by_priority
from utils.youtube_helpers import get_channel_info, get_recent_uploads, get_recent_livestreams
from utils.api_clients import get_gemini_model
from utils.ui import C, page_header, section_header, kpi_card, insight_card, divider, empty_state, plotly_defaults, badge


def render():
    page_header("AI Strategist",
                "AI-powered growth strategy built from live competitor and Vedantu data.")

    c1, c2 = st.columns(2)
    with c1: v_name   = st.selectbox("Vedantu channel", list(VEDANTU_CHANNELS.keys()))
    with c2: audience = st.selectbox("Target audience", [
        "JEE Mains & Advanced","NEET","Class 11-12 (CBSE)",
        "Class 9-10 (CBSE)","Class 6-8 (Foundation)","Boards + Entrance Combined",
    ])

    goal = st.text_input("Growth goal this week",
        placeholder="e.g. Dominate NEET Biology, grow JEE Advanced watch time, launch PYQ series")

    with st.expander("Options"):
        include_ls = st.checkbox("Include livestream data", value=True)
        tier_scope = st.radio("Competitor scope",
            ["Tier 1 only","Tier 1 + 2"], horizontal=True)

    if st.button("Generate Strategy", type="primary", use_container_width=True):
        if not goal.strip():
            st.warning("Enter a growth goal first.")
            return
        _run(v_name, VEDANTU_CHANNELS[v_name], audience, goal.strip(),
             include_ls, max_tier=1 if "Tier 1 only" in tier_scope else 2)


def _run(v_name, v_id, audience, goal, inc_ls, max_tier):
    with st.spinner("Fetching Vedantu data..."):
        v_info = get_channel_info(v_id)
        v_ups  = get_recent_uploads(v_id)
        v_str  = get_recent_livestreams(v_id) if inc_ls else []

    comps = []
    for t in range(1, max_tier+1): comps += get_competitors_by_priority(t)

    comp_data = []
    prog = st.progress(0, text="Scanning competitors...")
    for i, c in enumerate(comps):
        prog.progress((i+1)/len(comps), text=f"Scanning {c['name']}...")
        ups  = get_recent_uploads(c["id"])
        strs = get_recent_livestreams(c["id"]) if inc_ls else []
        info = get_channel_info(c["id"])
        if ups:
            comp_data.append({
                "name":        c["name"],
                "tier":        c["priority"],
                "subscribers": info.get("subscribers",0) if info else 0,
                "avg_vpd":     round(sum(v["views_per_day"] for v in ups)/len(ups),0),
                "uploads":     ups, "streams": strs,
            })
    prog.empty()

    if not comp_data:
        empty_state("No competitor data.")
        return

    v_lines = [f'"{v["title"]}" | {v["views"]:,} views | {int(v["views_per_day"]):,}/day' for v in v_ups]
    c_lines = []
    for c in comp_data:
        c_lines.append(f'\n[{c["name"]} | T{c["tier"]} | {c["subscribers"]:,} subs | {int(c["avg_vpd"]):,}/day]')
        for v in c["uploads"][:5]: c_lines.append(f'  "{v["title"]}" — {int(v["views_per_day"]):,}/day')

    prompt = f"""Senior YouTube growth strategist. Vedantu edtech. Sharp and specific.

CHANNEL: {v_name} | {v_info.get('subscribers',0):,} subs
AUDIENCE: {audience} | GOAL: {goal}
VEDANTU UPLOADS: {chr(10).join(v_lines)}
COMPETITORS: {chr(10).join(c_lines)}

Return ONLY valid JSON:
{{"executive_summary":"3 sentences. Brutal honesty about the biggest opportunity this week.",
"opportunities":[{{"rank":1,"title":"","why":"","action":"","format":"","momentum_score":0,"confidence_score":0,"priority":"HIGH"}}],
"content_gaps":[{{"topic":"","evidence":"","vedantu_status":"","urgency":"HIGH"}}],
"weekly_priorities":[{{"day":"Monday","action":"","channel":"","format":"","title_idea":""}}],
"livestream_recommendations":[{{"topic":"","timing":"","duration":"","hook":"","why_now":""}}],
"fastest_growing_topics":[{{"topic":"","momentum_score":0,"evidence":"","vedantu_coverage":"None"}}],
"bold_experiment":{{"idea":"","rationale":"","risk":"MEDIUM","potential_upside":""}}}}

5 opportunities, 5 gaps, 5 priorities Mon-Fri, 3 livestreams, 5 topics. Scores 0-100."""

    with st.spinner("Generating strategy..."):
        try:
            raw = get_gemini_model().generate_content(prompt).text.strip()
            if raw.startswith("```"):
                raw = raw.split("```")[1]
                if raw.startswith("json"): raw = raw[4:]
            data = json.loads(raw.strip())
        except json.JSONDecodeError:
            st.error("Gemini returned unexpected format. Try again.")
            return
        except Exception as e:
            st.error(f"Error: {e}")
            return

    _render(data, v_name, audience, v_info, comp_data)


def _render(data, v_name, audience, v_info, comp_data):
    # Executive summary
    st.markdown(f"""
    <div style="background:{C['card']};border:1px solid {C['border']};
                border-left:3px solid {C['accent']};border-radius:12px;
                padding:20px 24px;margin-bottom:28px;">
        <div style="font-size:10px;font-weight:700;letter-spacing:.1em;
                    color:{C['accent']};margin-bottom:10px;">EXECUTIVE SUMMARY</div>
        <p style="font-size:15px;color:{C['text']};margin:0;line-height:1.65;">
            {data.get('executive_summary','')}
        </p>
    </div>
    """, unsafe_allow_html=True)

    k1, k2, k3, k4 = st.columns(4)
    with k1: kpi_card("Channel",     v_name[:20])
    with k2: kpi_card("Subscribers", f"{v_info.get('subscribers',0):,}")
    with k3: kpi_card("Audience",    audience[:20])
    with k4: kpi_card("Competitors", str(len(comp_data)), sublabel="analysed")

    divider()

    # Opportunities as insight cards
    section_header("Top Opportunities")
    for opp in data.get("opportunities", []):
        insight_card(
            priority   = opp.get("priority","MEDIUM"),
            title      = f"#{opp.get('rank','')} {opp.get('title','')}",
            reason     = opp.get("why",""),
            action     = opp.get("action",""),
            confidence = opp.get("confidence_score",0),
            impact     = opp.get("format",""),
        )

    divider()

    # Fastest growing topics — single horizontal bar chart
    section_header("Topic Momentum")
    topics = data.get("fastest_growing_topics",[])
    if topics:
        names  = [t.get("topic","")[:30] for t in topics]
        scores = [t.get("momentum_score",0) for t in topics]
        fig = go.Figure(go.Bar(
            x=scores, y=names, orientation="h",
            marker_color=C["accent"], marker_line_width=0,
            text=[str(s) for s in scores], textposition="outside",
            textfont=dict(color=C["text2"], size=11),
        ))
        fig.update_layout(**plotly_defaults(height=220))
        fig.update_layout(xaxis=dict(visible=False, range=[0,115]))
        st.plotly_chart(fig, use_container_width=True)

        for t in topics:
            cov = t.get("vedantu_coverage","None")
            cov_c = C["success"] if cov=="Strong" else C["warning"] if cov=="Weak" else C["danger"]
            st.markdown(f"""
            <div style="display:flex;align-items:center;gap:12px;padding:10px 0;
                        border-bottom:1px solid {C['border']};">
                <div style="font-size:17px;font-weight:700;color:{C['warning']};
                            min-width:36px;text-align:center;">
                    {t.get('momentum_score',0)}</div>
                <div style="flex:1;">
                    <div style="font-size:13px;font-weight:600;color:{C['text']};">
                        {t.get('topic','')}</div>
                    <div style="font-size:12px;color:{C['text2']};margin-top:2px;">
                        {t.get('evidence','')}</div>
                </div>
                <span style="background:{cov_c}18;color:{cov_c};border-radius:4px;
                             padding:2px 8px;font-size:10px;font-weight:700;
                             white-space:nowrap;">
                    {cov}</span>
            </div>
            """, unsafe_allow_html=True)

    divider()

    # Content gaps
    section_header("Content Gaps")
    gaps = data.get("content_gaps",[])
    if gaps:
        cols = st.columns(min(len(gaps), 3))
        for i, gap in enumerate(gaps):
            urg = gap.get("urgency","LOW")
            c   = {
                "HIGH": C["danger"], "MEDIUM": C["warning"], "LOW": C["accent"]
            }.get(urg, C["accent"])
            cols[i%3].markdown(f"""
            <div style="background:{C['card']};border:1px solid {C['border']};
                        border-top:2px solid {c};border-radius:12px;
                        padding:16px;margin-bottom:12px;height:100%;">
                <div style="font-size:10px;font-weight:700;letter-spacing:.08em;
                            color:{c};margin-bottom:8px;">{urg}</div>
                <div style="font-size:13px;font-weight:600;color:{C['text']};
                            margin-bottom:6px;">{gap.get('topic','')}</div>
                <div style="font-size:12px;color:{C['text2']};line-height:1.5;
                            margin-bottom:6px;">{gap.get('evidence','')}</div>
                <div style="font-size:11px;color:{C['text3']};font-style:italic;">
                    {gap.get('vedantu_status','')}</div>
            </div>
            """, unsafe_allow_html=True)

    divider()

    # Weekly calendar
    section_header("Weekly Calendar")
    for p in data.get("weekly_priorities",[]):
        st.markdown(f"""
        <div style="display:flex;gap:16px;background:{C['card']};
                    border:1px solid {C['border']};border-radius:10px;
                    padding:14px 18px;margin-bottom:8px;align-items:flex-start;">
            <div style="min-width:72px;">
                <div style="font-size:12px;font-weight:700;color:{C['accent']};">
                    {p.get('day','')}</div>
                <div style="font-size:10px;color:{C['text3']};margin-top:2px;">
                    {p.get('format','')}</div>
            </div>
            <div style="flex:1;">
                <div style="font-size:13px;font-weight:600;color:{C['text']};">
                    {p.get('title_idea','')}</div>
                <div style="font-size:12px;color:{C['text2']};margin-top:3px;">
                    {p.get('action','')}</div>
                <div style="font-size:11px;color:{C['accent']};margin-top:3px;">
                    {p.get('channel','')}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    divider()

    # Livestream recs
    section_header("Livestream Recommendations")
    streams = data.get("livestream_recommendations",[])
    if streams:
        cols = st.columns(len(streams))
        for col, s in zip(cols, streams):
            col.markdown(f"""
            <div style="background:{C['card']};border:1px solid {C['border']};
                        border-top:2px solid {C['success']};border-radius:12px;
                        padding:16px;height:100%;">
                <div style="font-size:10px;font-weight:700;color:{C['success']};
                            letter-spacing:.08em;margin-bottom:8px;">LIVE</div>
                <div style="font-size:13px;font-weight:600;color:{C['text']};
                            margin-bottom:6px;">{s.get('topic','')}</div>
                <div style="font-size:11px;color:{C['text2']};margin-bottom:4px;">
                    {s.get('timing','')} · {s.get('duration','')}</div>
                <div style="font-size:11px;color:{C['text3']};line-height:1.5;
                            margin-bottom:6px;">{s.get('hook','')}</div>
                <div style="font-size:11px;color:{C['success']};font-style:italic;">
                    {s.get('why_now','')}</div>
            </div>
            """, unsafe_allow_html=True)

    divider()

    # Bold experiment
    bold = data.get("bold_experiment",{})
    if bold:
        rc = {"LOW":C["success"],"MEDIUM":C["warning"],"HIGH":C["danger"]}.get(
             bold.get("risk","MEDIUM"), C["warning"])
        st.markdown(f"""
        <div style="background:{C['card']};border:1px solid {C['border']};
                    border-left:3px solid #A855F7;border-radius:12px;padding:20px 24px;">
            <div style="font-size:10px;font-weight:700;letter-spacing:.1em;
                        color:#A855F7;margin-bottom:10px;">BOLD EXPERIMENT</div>
            <div style="font-size:15px;font-weight:600;color:{C['text']};
                        margin-bottom:8px;">{bold.get('idea','')}</div>
            <p style="font-size:13px;color:{C['text2']};margin:0 0 14px;line-height:1.6;">
                {bold.get('rationale','')}</p>
            <div style="display:flex;gap:10px;flex-wrap:wrap;">
                <span style="background:{rc}18;color:{rc};border-radius:4px;
                             padding:3px 10px;font-size:11px;font-weight:700;">
                    Risk: {bold.get('risk','')}</span>
                <span style="background:{C['accent_dim']};color:{C['accent']};
                             border-radius:4px;padding:3px 10px;font-size:11px;">
                    {bold.get('potential_upside','')}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
