"""
DATA FORCES — Explorer v2
Productive Data Infrastructure for Global South Research
Dependency Lab — Tricontinental / IdIHCS-UNLP/CONICET
"""
import streamlit as st
from supabase import create_client
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import base64
import os
from topics import TOPICS, COUNTRY_PRESETS, get_topic_indicators

# =====================================================================
# CONFIG
# =====================================================================
SUPABASE_URL = "https://gpndcspvuewxrkefqewc.supabase.co"
SUPABASE_KEY = "sb_secret_2boRe6vDplEzl0eQFphz4w_28p1GmhT"

# Color palette from Sur Global Hero image
PALETTE = {
    "bg_dark": "#0a0e1a",
    "bg_sidebar": "#0f172a",
    "accent": "#00d4aa",
    "accent2": "#1e88e5",
    "gold": "#f0c040",
    "text": "#e2e8f0",
    "text_muted": "#94a3b8",
    "card_bg": "#1e293b",
    "border": "#334155",
    "core": "#2563eb",
    "semi": "#f59e0b",
    "periphery": "#dc2626",
}

PLOTLY_TEMPLATE = {
    "layout": {
        "paper_bgcolor": "rgba(0,0,0,0)",
        "plot_bgcolor": "rgba(0,0,0,0)",
        "font": {"color": "#e2e8f0", "family": "Inter, system-ui, sans-serif"},
        "xaxis": {"gridcolor": "#1e293b", "zerolinecolor": "#334155"},
        "yaxis": {"gridcolor": "#1e293b", "zerolinecolor": "#334155"},
        "colorway": ["#00d4aa", "#1e88e5", "#f59e0b", "#ef4444", "#8b5cf6",
                      "#06b6d4", "#f97316", "#22c55e", "#ec4899", "#a855f7"],
    }
}

st.set_page_config(
    page_title="DATA FORCES",
    page_icon="",
    layout="wide",
    initial_sidebar_state="expanded",
)

# =====================================================================
# CSS — Sur Global Hero aesthetic
# =====================================================================
st.markdown(f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

    .stApp {{
        background-color: {PALETTE["bg_dark"]};
        color: {PALETTE["text"]};
        font-family: 'Inter', system-ui, sans-serif;
    }}

    .block-container {{
        padding-top: 1rem;
        padding-bottom: 1rem;
        max-width: 1400px;
    }}

    h1 {{
        font-size: 2rem !important;
        font-weight: 700 !important;
        color: {PALETTE["accent"]} !important;
        letter-spacing: -0.5px;
    }}

    h2 {{
        font-size: 1.3rem !important;
        font-weight: 600 !important;
        color: {PALETTE["text"]} !important;
        border-bottom: 1px solid {PALETTE["border"]};
        padding-bottom: 0.4rem;
    }}

    h3 {{
        font-size: 1.05rem !important;
        font-weight: 600 !important;
        color: {PALETTE["accent"]} !important;
    }}

    /* Sidebar */
    section[data-testid="stSidebar"] {{
        background-color: {PALETTE["bg_sidebar"]};
        border-right: 1px solid {PALETTE["border"]};
    }}
    section[data-testid="stSidebar"] * {{
        color: {PALETTE["text"]} !important;
    }}
    section[data-testid="stSidebar"] .stRadio label:hover {{
        color: {PALETTE["accent"]} !important;
    }}

    /* Metrics */
    div[data-testid="stMetric"] {{
        background: {PALETTE["card_bg"]};
        border: 1px solid {PALETTE["border"]};
        border-radius: 10px;
        padding: 14px 18px;
    }}
    div[data-testid="stMetric"] label {{
        color: {PALETTE["text_muted"]} !important;
        font-size: 0.8rem !important;
    }}
    div[data-testid="stMetric"] div[data-testid="stMetricValue"] {{
        color: {PALETTE["accent"]} !important;
        font-weight: 700 !important;
    }}

    /* Expanders */
    details {{
        background: {PALETTE["card_bg"]} !important;
        border: 1px solid {PALETTE["border"]} !important;
        border-radius: 8px !important;
    }}
    details summary {{
        color: {PALETTE["text"]} !important;
    }}

    /* Dataframes */
    .stDataFrame {{
        border: 1px solid {PALETTE["border"]};
        border-radius: 8px;
    }}

    /* Selectbox, inputs */
    div[data-baseweb="select"] {{
        background: {PALETTE["card_bg"]};
    }}

    /* Tabs */
    .stTabs [data-baseweb="tab"] {{
        color: {PALETTE["text_muted"]};
    }}
    .stTabs [data-baseweb="tab"][aria-selected="true"] {{
        color: {PALETTE["accent"]};
        border-bottom-color: {PALETTE["accent"]};
    }}

    /* Topic cards */
    .topic-card {{
        background: {PALETTE["card_bg"]};
        border: 1px solid {PALETTE["border"]};
        border-radius: 12px;
        padding: 20px;
        margin: 8px 0;
        transition: border-color 0.2s;
    }}
    .topic-card:hover {{
        border-color: {PALETTE["accent"]};
    }}
    .topic-card h4 {{
        margin: 0 0 4px 0;
        color: {PALETTE["text"]};
        font-size: 1.1rem;
    }}
    .topic-card p {{
        margin: 0;
        color: {PALETTE["text_muted"]};
        font-size: 0.85rem;
    }}

    /* Hero section */
    .hero-container {{
        position: relative;
        border-radius: 12px;
        overflow: hidden;
        margin-bottom: 1.5rem;
    }}
    .hero-overlay {{
        position: absolute;
        bottom: 0;
        left: 0;
        right: 0;
        padding: 30px;
        background: linear-gradient(transparent, rgba(10,14,26,0.95));
    }}
    .hero-title {{
        font-size: 2.5rem;
        font-weight: 700;
        color: {PALETTE["accent"]};
        margin: 0;
        text-shadow: 0 2px 8px rgba(0,0,0,0.5);
    }}
    .hero-subtitle {{
        font-size: 1rem;
        color: {PALETTE["text_muted"]};
        margin: 4px 0 0 0;
    }}

    /* Source badge */
    .badge {{
        display: inline-block;
        background: {PALETTE["border"]};
        color: {PALETTE["text"]};
        padding: 2px 10px;
        border-radius: 12px;
        font-size: 0.75rem;
        margin: 2px;
    }}
    .badge-accent {{
        background: rgba(0,212,170,0.15);
        color: {PALETTE["accent"]};
        border: 1px solid rgba(0,212,170,0.3);
    }}
</style>
""", unsafe_allow_html=True)


# =====================================================================
# SUPABASE CONNECTION
# =====================================================================
@st.cache_resource
def get_sb():
    return create_client(SUPABASE_URL, SUPABASE_KEY)

sb = get_sb()

@st.cache_data(ttl=3600)
def load_countries():
    r = sb.table("countries").select("*").order("country_name").execute()
    return pd.DataFrame(r.data)

@st.cache_data(ttl=3600)
def load_taxonomy():
    r = sb.table("topic_taxonomy").select("*").order("id").execute()
    return pd.DataFrame(r.data)

@st.cache_data(ttl=3600)
def load_sources():
    r = sb.table("sources").select("*").order("source_id").execute()
    return pd.DataFrame(r.data)

@st.cache_data(ttl=600)
def search_catalog(term):
    r = sb.table("indicator_catalog").select("*").ilike("indicator_name", f"%{term}%").order("country_count", desc=True).limit(100).execute()
    return pd.DataFrame(r.data)

@st.cache_data(ttl=300)
def get_data(iso3_list, codes, yr_min=1995, yr_max=2024):
    q = sb.table("indicators").select("iso3,year,indicator_code,indicator_name,value,source_id,value_type")
    if len(iso3_list) == 1:
        q = q.eq("iso3", iso3_list[0])
    else:
        q = q.in_("iso3", iso3_list)
    if len(codes) == 1:
        q = q.eq("indicator_code", codes[0])
    else:
        q = q.in_("indicator_code", codes)
    q = q.gte("year", yr_min).lte("year", yr_max).order("year").limit(10000)
    return pd.DataFrame(q.execute().data)


# =====================================================================
# SIDEBAR
# =====================================================================
with st.sidebar:
    # Logo area
    st.markdown(f"""
    <div style="text-align:center; padding: 10px 0 5px 0;">
        <span style="font-size:1.6rem; font-weight:700; color:{PALETTE['accent']};">DATA FORCES</span><br>
        <span style="font-size:0.7rem; color:{PALETTE['text_muted']};">Productive Data Infrastructure<br>for Global South Research</span>
    </div>
    """, unsafe_allow_html=True)

    border_color = PALETTE["border"]
    st.markdown(f"<hr style='border-color:{border_color}; margin:10px 0;'>", unsafe_allow_html=True)

    page = st.radio("", [
        "Home",
        "Economy",
        "Agriculture",
        "Energy",
        "Education",
        "Health",
        "Political Analysis",
        "Labor",
        "Geopolitics",
        "---",
        "Indicator Dictionary",
        "Country Profile",
        "Cross-Country",
        "Sources",
        "About",
    ], label_visibility="collapsed")

    border_color = PALETTE["border"]
    st.markdown(f"<hr style='border-color:{border_color}; margin:10px 0;'>", unsafe_allow_html=True)
    st.markdown(f"""
    <div style="font-size:0.65rem; color:{PALETTE['text_muted']}; line-height:1.5; text-align:center;">
    98,651,403 observations<br>
    39 sources | 22,576 indicators<br>
    217 countries | 16 themes<br><br>
    Lopez, E. (2026)<br>
    Tricontinental / IdIHCS-UNLP/CONICET
    </div>
    """, unsafe_allow_html=True)


# =====================================================================
# HELPER: Topic Dashboard
# =====================================================================
def render_topic_dashboard(topic_key):
    """Render a thematic dashboard for a given topic."""
    topic = TOPICS[topic_key]
    st.title(topic["label"])
    st.caption(topic["label_es"])

    countries = load_countries()
    lab70 = countries[countries["in_lab70"] == True]

    # Country filter
    col1, col2, col3 = st.columns([2, 1, 1])
    with col1:
        preset = st.selectbox("Country group", ["Lab70 (all)"] + list(COUNTRY_PRESETS.keys()), key=f"{topic_key}_preset")
    with col2:
        yr_min = st.number_input("From", 1995, 2024, 2000, key=f"{topic_key}_yr_min")
    with col3:
        yr_max = st.number_input("To", 1995, 2024, 2022, key=f"{topic_key}_yr_max")

    if preset == "Lab70 (all)":
        sel_countries = lab70["iso3"].tolist()
    else:
        sel_countries = [c for c in COUNTRY_PRESETS.get(preset, []) if c in lab70["iso3"].tolist()]

    st.markdown("---")

    # Subtopics as tabs
    subtopic_keys = list(topic["subtopics"].keys())
    subtopic_labels = [topic["subtopics"][k]["label"] for k in subtopic_keys]
    tabs = st.tabs(subtopic_labels)

    for tab, sk in zip(tabs, subtopic_keys):
        sub = topic["subtopics"][sk]
        indicators = sub.get("indicators", [])

        with tab:
            if not indicators:
                st.info(f"Indicators for {sub['label']} are available in the local database. Browse via Indicator Dictionary.")
                continue

            codes = [c for c, n in indicators]
            with st.spinner("Loading data..."):
                data = get_data(sel_countries, codes, yr_min, yr_max)

            if len(data) == 0:
                st.warning("No data found for this selection.")
                continue

            data = data.merge(countries[["iso3", "country_name", "structural_pos"]], on="iso3", how="left")

            # One chart per indicator
            for code, name in indicators:
                subset = data[data["indicator_code"] == code]
                if len(subset) == 0:
                    continue

                st.markdown(f"### {name}")

                col_chart, col_rank = st.columns([3, 1])

                with col_chart:
                    fig = px.line(
                        subset, x="year", y="value", color="iso3",
                        hover_data=["country_name"],
                        color_discrete_sequence=PLOTLY_TEMPLATE["layout"]["colorway"],
                    )
                    fig.update_layout(
                        height=350,
                        margin=dict(t=10, b=30, l=50, r=10),
                        legend=dict(orientation="h", y=-0.15, font=dict(size=9)),
                        xaxis_title="", yaxis_title="",
                        **{k: v for k, v in PLOTLY_TEMPLATE["layout"].items() if k not in ["colorway"]},
                    )
                    st.plotly_chart(fig, use_container_width=True)

                with col_rank:
                    latest = subset.sort_values("year", ascending=False).drop_duplicates("iso3")
                    latest = latest.sort_values("value", ascending=False).head(10)
                    st.markdown("**Top 10 (latest)**")
                    for i, (_, row) in enumerate(latest.iterrows()):
                        val = row["value"]
                        val_str = f"{val:,.1f}" if abs(val) < 10000 else f"{val:,.0f}"
                        pos = row.get("structural_pos", "")
                        color = PALETTE.get(pos, PALETTE["text_muted"])
                        st.markdown(f"<span style='color:{color}'>{i+1}. {row['iso3']}</span> {val_str}", unsafe_allow_html=True)


# =====================================================================
# PAGES
# =====================================================================

if page == "Home":
    # Hero image
    hero_path = os.path.join(os.path.dirname(__file__), "assets", "hero.png")
    if os.path.exists(hero_path):
        with open(hero_path, "rb") as f:
            hero_b64 = base64.b64encode(f.read()).decode()
        st.markdown(f"""
        <div class="hero-container">
            <img src="data:image/png;base64,{hero_b64}" style="width:100%; display:block;">
        </div>
        """, unsafe_allow_html=True)

    # Metrics
    c1, c2, c3, c4, c5 = st.columns(5)
    c1.metric("Observations", "98.6M")
    c2.metric("Sources", "39")
    c3.metric("Indicators", "22,576")
    c4.metric("Countries", "217")
    c5.metric("Themes", "16")

    st.markdown("---")

    # Topic cards
    st.markdown("## Explore by Topic")

    cols = st.columns(4)
    for i, (key, topic) in enumerate(TOPICS.items()):
        with cols[i % 4]:
            n_indicators = sum(len(s.get("indicators", [])) for s in topic["subtopics"].values())
            n_subtopics = len(topic["subtopics"])
            st.markdown(f"""
            <div class="topic-card">
                <h4 style="color:{topic['color']}">{topic['label']}</h4>
                <p>{topic['label_es']}</p>
                <p style="margin-top:8px;">
                    <span class="badge">{n_subtopics} areas</span>
                    <span class="badge badge-accent">{n_indicators} indicators</span>
                </p>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("---")

    # Structural position
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("## Data Quality")
        st.markdown(f"""
        | Type | Observations | Share |
        |---|---|---|
        | Observed | 67,212,946 | 96.4% |
        | Projected | 2,499,072 | 3.6% |
        | Estimated | 15,082 | 0.02% |

        Every observation carries a `value_type` flag.
        """)

    with col2:
        st.markdown("## Structural Position (Lab70)")
        countries = load_countries()
        lab70 = countries[countries["in_lab70"] == True]
        struct = lab70["structural_pos"].value_counts()

        fig = go.Figure(data=[go.Pie(
            labels=["Core", "Semi-periphery", "Periphery"],
            values=[struct.get("core", 0), struct.get("semi_periphery", 0), struct.get("periphery", 0)],
            marker_colors=[PALETTE["core"], PALETTE["semi"], PALETTE["periphery"]],
            hole=0.5,
            textinfo="label+value",
            textfont=dict(color="white"),
        )])
        fig.update_layout(
            height=250, margin=dict(t=5, b=5, l=5, r=5),
            showlegend=False,
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        )
        st.plotly_chart(fig, use_container_width=True)

elif page == "---":
    st.markdown("---")

elif page in ["Economy", "Agriculture", "Energy", "Education", "Health", "Political Analysis", "Labor", "Geopolitics"]:
    topic_map = {
        "Economy": "economy", "Agriculture": "agriculture", "Energy": "energy",
        "Education": "education", "Health": "health", "Political Analysis": "politics",
        "Labor": "labor", "Geopolitics": "geopolitics",
    }
    render_topic_dashboard(topic_map[page])

elif page == "Indicator Dictionary":
    st.title("Indicator Dictionary")
    st.caption("22,576 indicators from 39 sources, classified into 16 thematic domains")

    search = st.text_input("Search by name", placeholder="GDP, mortality, electricity, poverty...")

    if search and len(search) >= 2:
        results = search_catalog(search)
        if len(results) > 0:
            st.success(f"{len(results)} indicators found")
            display = results[["indicator_code", "indicator_name", "source_id", "topic",
                               "country_count", "coverage_start", "coverage_end"]].copy()
            display.columns = ["Code", "Name", "Source", "Theme", "Countries", "From", "To"]
            st.dataframe(display, use_container_width=True, hide_index=True, height=400)

            selected = st.selectbox("Explore indicator", results["indicator_code"].tolist(),
                format_func=lambda x: f"{x} - {results[results['indicator_code']==x]['indicator_name'].values[0][:60]}")

            if selected:
                info = results[results["indicator_code"] == selected].iloc[0]
                c1, c2, c3, c4 = st.columns(4)
                c1.markdown(f"**Code:** `{info['indicator_code']}`")
                c2.markdown(f"**Source:** `{info['source_id']}`")
                c3.markdown(f"**Theme:** `{info['topic']}`")
                c4.markdown(f"**Countries:** {info.get('country_count', '?')}")

                countries = load_countries()
                lab70 = countries[countries["in_lab70"] == True]
                data = get_data(lab70["iso3"].tolist(), [selected])

                if len(data) > 0:
                    data = data.merge(countries[["iso3", "country_name", "structural_pos"]], on="iso3", how="left")
                    fig = px.line(data, x="year", y="value", color="iso3",
                        hover_data=["country_name"],
                        color_discrete_sequence=PLOTLY_TEMPLATE["layout"]["colorway"])
                    fig.update_layout(height=400, margin=dict(t=10, b=40),
                        legend=dict(orientation="h", y=-0.15, font=dict(size=9)),
                        xaxis_title="", yaxis_title="",
                        **{k: v for k, v in PLOTLY_TEMPLATE["layout"].items() if k not in ["colorway"]})
                    st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning("No indicators found.")

elif page == "Country Profile":
    st.title("Country Profile")
    countries = load_countries()
    lab70 = countries[countries["in_lab70"] == True]

    selected = st.selectbox("Select country", lab70["iso3"].tolist(),
        format_func=lambda x: f"{lab70[lab70['iso3']==x]['country_name'].values[0]} ({x})")

    if selected:
        c = lab70[lab70["iso3"] == selected].iloc[0]
        pos = c.get("structural_pos", "")
        color = PALETTE.get(pos, PALETTE["text_muted"])

        st.markdown(f"## {c['country_name']} <span style='color:{color}; font-size:0.9rem;'>{pos.replace('_',' ').title()}</span>",
                    unsafe_allow_html=True)
        st.caption(f"Region: {c['region']} | Income: {c['income_group']}")

        profiles = [
            ("NY.GDP.PCAP.CD", "GDP per capita"), ("SP.DYN.LE00.IN", "Life expectancy"),
            ("SH.STA.MMRT", "Maternal mortality"), ("EG.ELC.ACCS.ZS", "Electricity access"),
            ("SL.UEM.TOTL.ZS", "Unemployment"), ("FP.CPI.TOTL.ZG", "Inflation"),
            ("SE.SEC.ENRR", "Secondary enrollment"), ("MS.MIL.XPND.GD.ZS", "Military (% GDP)"),
        ]
        codes = [p[0] for p in profiles]
        data = get_data([selected], codes, 1990, 2024)

        if len(data) > 0:
            for row_start in range(0, len(profiles), 4):
                cols = st.columns(4)
                for j, (code, label) in enumerate(profiles[row_start:row_start + 4]):
                    with cols[j]:
                        subset = data[data["indicator_code"] == code].sort_values("year")
                        if len(subset) > 0:
                            latest = subset.iloc[-1]
                            val = latest["value"]
                            val_str = f"{val:,.0f}" if abs(val) > 100 else f"{val:.1f}"
                            st.metric(label, val_str, help=f"Year: {int(latest['year'])}")
                            fig = px.area(subset, x="year", y="value")
                            fig.update_layout(height=100, margin=dict(t=0, b=0, l=0, r=0),
                                xaxis=dict(visible=False), yaxis=dict(visible=False), showlegend=False,
                                paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
                            fig.update_traces(fillcolor="rgba(0,212,170,0.15)", line_color=PALETTE["accent"])
                            st.plotly_chart(fig, use_container_width=True)
                        else:
                            st.metric(label, "N/A")

elif page == "Cross-Country":
    st.title("Cross-Country Analysis")
    countries = load_countries()
    lab70 = countries[countries["in_lab70"] == True]

    c1, c2 = st.columns([1, 2])
    with c1:
        preset = st.selectbox("Preset", ["Custom"] + list(COUNTRY_PRESETS.keys()))
    with c2:
        default = COUNTRY_PRESETS.get(preset, ["ARG", "BRA", "CHN", "USA", "NGA"])
        sel = st.multiselect("Countries", lab70["iso3"].tolist(),
            default=[c for c in default if c in lab70["iso3"].tolist()],
            format_func=lambda x: f"{x} - {lab70[lab70['iso3']==x]['country_name'].values[0]}")

    popular = [("NY.GDP.PCAP.CD", "GDP per capita"), ("SP.DYN.LE00.IN", "Life expectancy"),
               ("EG.ELC.ACCS.ZS", "Electricity access"), ("SL.UEM.TOTL.ZS", "Unemployment"),
               ("FP.CPI.TOTL.ZG", "Inflation"), ("SI.POV.GINI", "Gini index"),
               ("MS.MIL.XPND.GD.ZS", "Military (% GDP)"), ("IT.NET.USER.ZS", "Internet users")]

    ind = st.selectbox("Indicator", [p[0] for p in popular],
        format_func=lambda x: [p[1] for p in popular if p[0] == x][0])

    yr = st.slider("Period", 1995, 2024, (2000, 2022))

    if sel and ind:
        data = get_data(sel, [ind], yr[0], yr[1])
        if len(data) > 0:
            data = data.merge(countries[["iso3", "country_name", "structural_pos"]], on="iso3", how="left")
            name = data["indicator_name"].iloc[0] or ind

            fig = px.line(data, x="year", y="value", color="iso3",
                hover_data=["country_name"],
                color_discrete_sequence=PLOTLY_TEMPLATE["layout"]["colorway"])
            fig.update_layout(height=450, margin=dict(t=30, b=40),
                title=name, legend=dict(orientation="h", y=-0.12, font=dict(size=10)),
                xaxis_title="", yaxis_title="",
                **{k: v for k, v in PLOTLY_TEMPLATE["layout"].items() if k not in ["colorway"]})
            st.plotly_chart(fig, use_container_width=True)

            # Bar chart latest
            latest = data.sort_values("year", ascending=False).drop_duplicates("iso3").sort_values("value", ascending=False)
            fig2 = px.bar(latest, x="country_name", y="value", color="structural_pos",
                color_discrete_map=PALETTE, title="Latest values")
            fig2.update_layout(height=300, margin=dict(t=40, b=40),
                xaxis_title="", showlegend=True, legend_title="",
                **{k: v for k, v in PLOTLY_TEMPLATE["layout"].items() if k not in ["colorway"]})
            st.plotly_chart(fig2, use_container_width=True)

elif page == "Sources":
    st.title("Source Registry")
    st.caption("48 sources cataloged, 39 loaded with data")
    sources = load_sources()

    for inst in sorted(sources["institution"].dropna().unique()):
        inst_src = sources[sources["institution"] == inst]
        with st.expander(f"**{inst}** ({len(inst_src)} sources)"):
            for _, s in inst_src.iterrows():
                topics = (s.get("topics") or "").split(",")
                badges = " ".join([f'<span class="badge">{t.strip()}</span>' for t in topics if t.strip()])
                st.markdown(f"**`{s['source_id']}`** {s['source_name']}<br>{badges}",
                    unsafe_allow_html=True)

elif page == "About":
    st.title("About DATA FORCES")
    st.markdown(f"""
    **DATA FORCES** is an open, SQL-native research data infrastructure containing
    **98,651,403 observations** from **39 international data sources**, covering
    **217 countries** across **22,576 indicators classified into 16 thematic domains**.

    Every observation carries a `value_type` flag distinguishing observed data (96.4%),
    projections (3.6%), and historical estimates (0.02%).

    The system implements the **DDI Variable Cascade**: 15,543 concepts linked to
    22,576 represented variables and instance variables, all organized under the
    **GSI taxonomy** (11 Level-1 categories, 64 Level-2 subcategories).

    ---

    **Citation:** Lopez, E. (2026). *DATA FORCES: Productive Data Infrastructure
    for Global South Research.* Dependency Lab, Tricontinental Institute for Social
    Research / IdIHCS-UNLP/CONICET.

    **Links:**
    - [Full dataset (HuggingFace)](https://huggingface.co/datasets/emilop1982/dataforces)
    - [Cloud database (Supabase)](https://gpndcspvuewxrkefqewc.supabase.co)
    - Technical documentation: DF_Documentation_v2.md
    """)
