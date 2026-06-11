# modules/ai_strategist.py — UI refactored. Logic unchanged.

import json
import streamlit as st
import plotly.graph_objects as go

from config import VEDANTU_CHANNELS
from utils.registry import get_competitors_by_priority
from utils.youtube_helpers import get_channel_info, get_recent_uploads, get_recent_livestreams
from utils.api_clients import get_gemini_model
from utils.ui import T, page_header, section_header, kpi_card, divider, empty_state, plotly_defaults


def render():
    page_header("AI Content Strategist",
                "Senior-level growth strategy powered by Gemini — built from live competitor and Vedantu data.",
                "🤖")

    c1, c2 = st.columns(2)
    with c1: v_name  = st.selectbox("Vedantu channel", list(VEDANTU_CHANNELS.keys()))
    with c2: audience = st.selectbox("Target audience", [
        "JEE Mains & Advanced", "NEET", "Class 11-12 (CBSE)",
        "Class 9-10 (CBSE)", "Class 6-8 (Foundation)", "Boards + Entrance Combined",
    ])

    goal = st.text_input("This week's growth goal",
        placeholder="e.g. Increase watch time on JEE Physics, gain 10K subscribers, dominate NEET Biology shorts")

    with st.expander("⚙️ Advanced options"):
        include_livestreams = st.checkbox("Include livestream analysis", value=True)
        tier_scope = st.radio("Competitor scope",
            ["Tier 1 only (fastest)", "Tier 1 + Tier 2 (thorough)"], horizontal=True)

    if st.button("✨ Generate Strategy Report", type="primary", use_container_width=True):
        if not goal.strip():
            st.warning("Please enter a growth goal.")
            return
        _run(v_name, VEDANTU_CHANNELS[v_name], audience, goal.strip(),
             include_livestreams, max_tier=1 if "Tier 1 only" in tier_scope else 2)


def _run(v_name, v_id, audience, goal, include_ls, max_tier):
    with st.spinner("Fetching Vedantu data..."):
        v_info   = get_channel_info(v_id)
        v_ups    = get_recent_uploads(v_id)
        v_str    = get_recent_livestreams(v_id) if include_ls else []

    competitors = []
    for t in range(1, max_tier + 1): competitors += get_competitors_by_priority(t)

    comp_data = []
    prog = st.progress(0, text="Fetching competitor data...")
    for i, c in enumerate(competitors):
        prog.progress((i+1)/len(competitors), text=f"Scanning {c['name']}...")
        ups  = get_recent_uploads(c["id"])
        strs = get_recent_livestreams(c["id"]) if include_ls else []
        info = get_channel_info(c["id"])
        if ups:
            comp_data.append({
                "name":        c["name"],
                "tier":        c["priority"],
                "subscribers": info.get("subscribers", 0) if info else 0,
                "avg_vpd":     round(sum(v["views_per_day"] for v in ups)/len(ups), 0),
                "uploads":     ups,
                "streams":     strs,
            })
    prog.empty()

    if not comp_data:
        empty_state("No competitor data fetched. Check API key and channel IDs.", "⚠️")
        return

    v_upload_lines = [f'  - "{v["title"]}" | {v["views"]:,} views | {int(v["views_per_day"]):,}/day' for v in v_ups]
    v_stream_lines = [f'  - "{v["title"]}" | {v["views"]:,} views' for v in v_str] if v_str else ["  - No recent livestreams"]
    comp_lines = []
    for c in comp_data:
        comp_lines.append(f'\n[{c["name"]} | Tier {c["tier"]} | {c["subscribers"]:,} subs | Avg {int(c["avg_vpd"]):,}/day]')
        for v in c["uploads"][:5]:  comp_lines.append(f'  UPLOAD: "{v["title"]}" | {v["views"]:,} views | {int(v["views_per_day"]):,}/day')
        for v in c["streams"][:3]:  comp_lines.append(f'  STREAM: "{v["title"]}" | {v["views"]:,} views')

    prompt = f"""You are a senior YouTube growth strategist with 10 years in Indian edtech.
You are advising the Vedantu YouTube operations team.
Think like McKinsey meets MrBeast — sharp, specific, results-obsessed.

VEDANTU: {v_name} | {v_info.get('subscribers',0):,} subs | Audience: {audience} | Goal: {goal}
RECENT UPLOADS:\n{chr(10).join(v_upload_lines)}
RECENT LIVESTREAMS:\n{chr(10).join(v_stream_lines)}
COMPETITORS:\n{chr(10).join(comp_lines)}

Return ONLY valid JSON matching this structure exactly:
{{"executive_summary":"3-4 sentence strategic assessment",
"opportunities":[{{"rank":1,"title":"","why":"","action":"","format":"","momentum_score":0,"confidence_score":0,"priority":"HIGH"}}],
"content_gaps":[{{"topic":"","evidence":"","vedantu_status":"","urgency":"HIGH"}}],
"weekly_priorities":[{{"day":"Monday","action":"","channel":"","format":"","title_idea":""}}],
"livestream_recommendations":[{{"topic":"","timing":"","duration":"","hook":"","why_now":""}}],
"fastest_growing_topics":[{{"topic":"","momentum_score":0,"evidence":"","vedantu_coverage":"None"}}],
"bold_experiment":{{"idea":"","rationale":"","risk":"MEDIUM","potential_upside":""}}}}

Rules: 5 opportunities, 5 gaps, 5 priorities (Mon-Fri), 3 livestream recs, 5 topics. Scores 0-100. Be specific."""

    with st.spinner("Gemini is analysing and building your strategy..."):
        try:
            raw = get_gemini_model().generate_content(prompt).text.strip()
            if raw.startswith("```"):
                raw = raw.split("```")[1]
                if raw.startswith("json"): raw = raw[4:]
            data = json.loads(raw.strip())
        except json.JSONDecodeError:
            st.error("Gemini returned an unexpected format. Try again.")
            return
        except Exception as e:
            st.error(f"Error: {e}")
            return

    _render_report(data, v_name, audience, v_info, comp_data)


def _render_report(data, v_name, audience, v_info, comp_data):
    # Executive summary
    st.markdown(f"""
    <div style="background:linear-gradient(135deg,{T['bg_elevated']},{T['bg_surface']});
                border:1px solid {T['indigo']};border-radius:16px;
                padding:24px 28px;margin-bottom:24px;">
        <div style="font-size:10px;font-weight:700;letter-spacing:.12em;
                    color:{T['indigo']};margin-bottom:12px;">EXECUTIVE SUMMARY</div>
        <div style="color:{T['text_primary']};font-size:15px;line-height:1.75;font-weight:400;">
            {data.get('executive_summary','')}
        </div>
    </div>
    """, unsafe_allow_html=True)

    c1, c2, c3, c4 = st.columns(4)
    with c1: kpi_card("Channel",              v_name[:22],                          color="indigo")
    with c2: kpi_card("Subscribers",          f"{v_info.get('subscribers',0):,}",   color="indigo")
    with c3: kpi_card("Audience",             audience[:22])
    with c4: kpi_card("Competitors Analysed", str(len(comp_data)),                  color="green")

    divider()

    # Opportunities
    section_header("🚀 Top 5 Opportunities")
    for opp in data.get("opportunities", []):
        _opp_card(opp)

    divider()

    # Fastest growing topics
    section_header("📈 Fastest Growing Topics")
    topics = data.get("fastest_growing_topics", [])
    if topics:
        _momentum_chart(topics)
        for t in topics:
            cov_color = {
                "None":   T["red"],
                "Weak":   T["amber"],
                "Strong": T["green"],
            }.get(t.get("vedantu_coverage","None"), T["text_muted"])
            st.markdown(f"""
            <div style="display:flex;align-items:flex-start;gap:16px;
                        padding:12px 0;border-bottom:1px solid {T['border_subtle']};">
                <div style="min-width:48px;text-align:center;">
                    <div style="font-size:20px;font-weight:700;color:{T['amber']};">
                        {t.get('momentum_score',0)}</div>
                    <div style="font-size:9px;color:{T['text_muted']};letter-spacing:.08em;">SCORE</div>
                </div>
                <div style="flex:1;">
                    <div style="color:{T['text_primary']};font-weight:600;font-size:13px;">
                        {t.get('topic','')}</div>
                    <div style="color:{T['text_secondary']};font-size:12px;margin-top:3px;">
                        {t.get('evidence','')}</div>
                </div>
                <div style="background:{cov_color}18;border:1px solid {cov_color};
                            color:{cov_color};border-radius:6px;padding:3px 10px;
                            font-size:11px;font-weight:600;white-space:nowrap;align-self:center;">
                    {t.get('vedantu_coverage','None')}
                </div>
            </div>
            """, unsafe_allow_html=True)

    divider()

    # Content gaps
    section_header("🔍 Content Gaps")
    gaps = data.get("content_gaps", [])
    if gaps:
        cols = st.columns(min(len(gaps), 3))
        for i, gap in enumerate(gaps):
            urg = gap.get("urgency","LOW")
            c   = {
                "HIGH":   T["red"],
                "MEDIUM": T["amber"],
                "LOW":    T["indigo"],
            }.get(urg, T["indigo"])
            cols[i % 3].markdown(f"""
            <div style="background:{c}10;border:1px solid {c}44;
                        border-radius:12px;padding:16px;margin-bottom:12px;">
                <div style="color:{c};font-size:10px;font-weight:700;
                            letter-spacing:.1em;margin-bottom:8px;">
                    {urg} URGENCY</div>
                <div style="color:{T['text_primary']};font-weight:600;
                            font-size:13px;margin-bottom:6px;">{gap.get('topic','')}</div>
                <div style="color:{T['text_secondary']};font-size:11px;
                            line-height:1.5;margin-bottom:8px;">{gap.get('evidence','')}</div>
                <div style="color:{T['text_muted']};font-size:10px;font-style:italic;">
                    Status: {gap.get('vedantu_status','')}</div>
            </div>
            """, unsafe_allow_html=True)

    divider()

    # Weekly calendar
    section_header("📅 Weekly Content Calendar")
    for p in data.get("weekly_priorities", []):
        st.markdown(f"""
        <div style="display:flex;align-items:flex-start;gap:16px;
                    background:{T['bg_elevated']};border:1px solid {T['border_default']};
                    border-radius:12px;padding:14px 18px;margin-bottom:8px;">
            <div style="min-width:80px;">
                <div style="color:{T['indigo']};font-weight:700;font-size:13px;">
                    {p.get('day','')}</div>
                <div style="color:{T['text_muted']};font-size:10px;margin-top:2px;">
                    {p.get('format','')}</div>
            </div>
            <div style="flex:1;">
                <div style="color:{T['text_primary']};font-weight:600;font-size:13px;">
                    {p.get('title_idea','')}</div>
                <div style="color:{T['text_secondary']};font-size:12px;margin-top:4px;">
                    {p.get('action','')}</div>
                <div style="color:{T['indigo']};font-size:11px;margin-top:4px;">
                    → {p.get('channel','')}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    divider()

    # Livestream recs
    section_header("🔴 Livestream Recommendations")
    streams = data.get("livestream_recommendations", [])
    if streams:
        s_cols = st.columns(len(streams))
        for col, s in zip(s_cols, streams):
            col.markdown(f"""
            <div style="background:{T['green_dim']};border:1px solid {T['green']};
                        border-radius:12px;padding:16px;height:100%;">
                <div style="color:{T['green']};font-size:10px;font-weight:700;
                            letter-spacing:.1em;margin-bottom:8px;">🔴 LIVE</div>
                <div style="color:{T['text_primary']};font-weight:600;
                            font-size:13px;margin-bottom:8px;">{s.get('topic','')}</div>
                <div style="color:{T['text_secondary']};font-size:11px;margin-bottom:4px;">
                    🕐 {s.get('timing','')} · {s.get('duration','')}</div>
                <div style="color:{T['text_muted']};font-size:11px;
                            margin-bottom:8px;line-height:1.5;">
                    <b style="color:{T['text_secondary']};">Hook:</b> {s.get('hook','')}</div>
                <div style="color:{T['green']};font-size:11px;font-style:italic;">
                    {s.get('why_now','')}</div>
            </div>
            """, unsafe_allow_html=True)

    divider()

    # Bold experiment
    bold = data.get("bold_experiment", {})
    if bold:
        risk_c = {
            "LOW":    T["green"],
            "MEDIUM": T["amber"],
            "HIGH":   T["red"],
        }.get(bold.get("risk","MEDIUM"), T["amber"])
        st.markdown(f"""
        <div style="background:linear-gradient(135deg,{T['purple_dim']},{T['bg_surface']});
                    border:1px solid {T['purple']};border-radius:16px;padding:24px 28px;">
            <div style="color:{T['purple']};font-size:10px;font-weight:700;
                        letter-spacing:.12em;margin-bottom:12px;">
                ⚡ BOLD EXPERIMENT</div>
            <div style="color:{T['text_primary']};font-size:16px;
                        font-weight:600;margin-bottom:10px;">{bold.get('idea','')}</div>
            <div style="color:{T['text_secondary']};font-size:13px;
                        line-height:1.65;margin-bottom:16px;">{bold.get('rationale','')}</div>
            <div style="display:flex;gap:12px;flex-wrap:wrap;">
                <span style="background:{risk_c}18;border:1px solid {risk_c};
                             color:{risk_c};border-radius:6px;padding:4px 12px;
                             font-size:11px;font-weight:700;">
                    Risk: {bold.get('risk','')}</span>
                <span style="background:{T['indigo_dim']};border:1px solid {T['indigo']};
                             color:{T['indigo']};border-radius:6px;padding:4px 12px;
                             font-size:11px;">
                    Upside: {bold.get('potential_upside','')}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)


def _opp_card(opp):
    p     = opp.get("priority","MEDIUM")
    c     = {
        "HIGH":   T["red"],
        "MEDIUM": T["amber"],
        "LOW":    T["indigo"],
    }.get(p, T["amber"])
    m     = opp.get("momentum_score", 0)
    conf  = opp.get("confidence_score", 0)
    st.markdown(f"""
    <div style="background:{T['bg_elevated']};border:1px solid {T['border_default']};
                border-left:4px solid {c};border-radius:12px;
                padding:20px 24px;margin-bottom:10px;">
        <div style="display:flex;justify-content:space-between;
                    align-items:flex-start;gap:16px;flex-wrap:wrap;">
            <div style="flex:1;min-width:200px;">
                <div style="display:flex;align-items:center;gap:10px;margin-bottom:8px;">
                    <span style="color:{T['text_muted']};font-size:12px;font-weight:700;">
                        #{opp.get('rank','')}</span>
                    <span style="background:{c}18;border:1px solid {c};color:{c};
                                 border-radius:6px;padding:2px 10px;font-size:10px;
                                 font-weight:700;letter-spacing:.06em;">{p}</span>
                    <span style="color:{T['text_muted']};font-size:11px;">
                        {opp.get('format','')}</span>
                </div>
                <div style="color:{T['text_primary']};font-size:15px;
                            font-weight:600;margin-bottom:6px;">{opp.get('title','')}</div>
                <div style="color:{T['text_secondary']};font-size:12px;
                            line-height:1.6;margin-bottom:10px;">
                    <span style="color:{T['text_muted']};">Why now: </span>{opp.get('why','')}</div>
                <div style="background:{T['bg_overlay']};border-radius:8px;
                            padding:10px 14px;border-left:3px solid {c};">
                    <div style="color:{T['text_muted']};font-size:10px;font-weight:700;
                                letter-spacing:.08em;margin-bottom:4px;">ACTION</div>
                    <div style="color:{T['text_primary']};font-size:13px;line-height:1.5;">
                        {opp.get('action','')}</div>
                </div>
            </div>
            <div style="display:flex;flex-direction:column;gap:8px;min-width:100px;">
                <div style="text-align:center;background:{T['bg_overlay']};
                            border-radius:10px;padding:12px 16px;">
                    <div style="font-size:24px;font-weight:700;color:{c};">{m}</div>
                    <div style="font-size:9px;color:{T['text_muted']};
                                letter-spacing:.08em;margin-top:2px;">MOMENTUM</div>
                </div>
                <div style="text-align:center;background:{T['bg_overlay']};
                            border-radius:10px;padding:12px 16px;">
                    <div style="font-size:24px;font-weight:700;color:{T['indigo']};">
                        {conf}</div>
                    <div style="font-size:9px;color:{T['text_muted']};
                                letter-spacing:.08em;margin-top:2px;">CONFIDENCE</div>
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)


def _momentum_chart(topics):
    names  = [t.get("topic","")[:28] for t in topics]
    scores = [t.get("momentum_score", 0) for t in topics]
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=scores, y=names, orientation="h",
        marker=dict(color=scores,
                    colorscale=[[0,T["indigo"]],[0.5,T["amber"]],[1,T["red"]]],
                    showscale=False),
        text=[str(s) for s in scores],
        textposition="outside",
        textfont=dict(color=T["text_primary"], size=12),
    ))
    fig.update_layout(**plotly_defaults(), height=240,
                      xaxis=dict(range=[0,115], visible=False, showgrid=False),
                      yaxis=dict(showgrid=False),
                      margin=dict(l=0, r=50, t=30, b=0))
    st.plotly_chart(fig, use_container_width=True)
