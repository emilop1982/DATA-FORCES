"""
DATA FORCES — Data Catalog & Explorer v5
Organized metadata navigation. Charts only in Analysis tab.
Connected to local DuckDB (98.6M observations).
"""
import streamlit as st
import duckdb
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os

DB_PATH = os.path.join(os.path.dirname(__file__), '..', 'db', 'dataforces.duckdb')
P = {"bg":"#0a0e1a","sidebar":"#0f172a","accent":"#00d4aa","text":"#e2e8f0",
     "muted":"#94a3b8","card":"#1e293b","border":"#334155",
     "core":"#2563eb","semi":"#f59e0b","periphery":"#dc2626"}
COLORS = ["#00d4aa","#1e88e5","#f59e0b","#ef4444","#8b5cf6","#06b6d4",
          "#f97316","#22c55e","#ec4899","#a855f7"]

st.set_page_config(page_title="DATA FORCES — Catalog", layout="wide", initial_sidebar_state="expanded")

st.markdown(f"""<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
.stApp{{background:{P["bg"]};color:{P["text"]};font-family:'Inter',sans-serif}}
.block-container{{padding-top:.8rem;max-width:1400px}}
h1{{font-size:1.7rem!important;font-weight:700!important;color:{P["accent"]}!important}}
h2{{font-size:1.15rem!important;font-weight:600!important;border-bottom:1px solid {P["border"]};padding-bottom:.25rem;margin-top:1rem}}
h3{{font-size:.95rem!important;color:{P["accent"]}!important}}
section[data-testid="stSidebar"]{{background:{P["sidebar"]}}}
section[data-testid="stSidebar"] *{{color:{P["text"]}!important}}
div[data-testid="stMetric"]{{background:{P["card"]};border:1px solid {P["border"]};border-radius:8px;padding:8px 12px}}
div[data-testid="stMetric"] label{{color:{P["muted"]}!important;font-size:.7rem!important}}
div[data-testid="stMetric"] div[data-testid="stMetricValue"]{{color:{P["accent"]}!important;font-size:1.1rem!important}}
details{{background:{P["card"]}!important;border:1px solid {P["border"]}!important;border-radius:6px!important;margin-bottom:4px!important}}
.stDataFrame{{font-size:.85rem}}
</style>""", unsafe_allow_html=True)

# =====================================================================
# DB CONNECTION
# =====================================================================
@st.cache_resource
def get_db():
    return duckdb.connect(DB_PATH, read_only=True)

db = get_db()

def q(sql):
    return db.execute(sql).fetchdf()

def q1(sql):
    return db.execute(sql).fetchone()[0]

# =====================================================================
# SIDEBAR
# =====================================================================
with st.sidebar:
    total = q1("SELECT count(*) FROM indicators") + q1("SELECT count(*) FROM bilateral") + q1("SELECT count(*) FROM commodities")
    st.markdown(f"<div style='text-align:center;padding:6px 0'>"
        f"<span style='font-size:1.3rem;font-weight:700;color:{P['accent']}'>DATA FORCES</span><br>"
        f"<span style='font-size:.58rem;color:{P['muted']}'>{total:,} observations</span></div>",
        unsafe_allow_html=True)
    st.markdown("---")

    section = st.radio("", [
        "Database Overview",
        "Indicator Dictionary",
        "Browse by Topic",
        "Browse by Source",
        "Browse by Taxonomy",
        "Country Data Availability",
        "Argentina Subnational",
        "Documents & Legislation",
        "---",
        "Analysis: Country Profile",
        "Analysis: Cross-Country",
    ], label_visibility="collapsed")

    st.markdown("---")
    st.caption("Lopez, E. (2026)\nTricontinental / CONICET")

# =====================================================================
# 1. DATABASE OVERVIEW
# =====================================================================
if section == "Database Overview":
    hero = os.path.join(os.path.dirname(__file__), "assets", "hero.png")
    if os.path.exists(hero):
        st.image(hero, use_container_width=True)

    st.title("DATA FORCES")
    st.markdown("**Productive Data Infrastructure for Global South Research**")

    # Core metrics
    ni = q1("SELECT count(*) FROM indicators")
    nb = q1("SELECT count(*) FROM bilateral")
    nc = q1("SELECT count(*) FROM commodities")
    ncat = q1("SELECT count(*) FROM indicator_catalog")
    nsrc = q1("SELECT count(DISTINCT source_id) FROM indicators")
    ncountry = q1("SELECT count(*) FROM countries")

    c1,c2,c3,c4,c5,c6 = st.columns(6)
    c1.metric("Total observations", f"{(ni+nb+nc)/1e6:.1f}M")
    c2.metric("Indicators cataloged", f"{ncat:,}")
    c3.metric("Data sources", nsrc)
    c4.metric("Countries", ncountry)
    c5.metric("Subnational units", f"{q1('SELECT count(*) FROM subnational_units'):,}")
    c6.metric("Documents", q1("SELECT count(*) FROM documents"))

    st.markdown("## Database Tables")
    tables_data = pd.DataFrame({
        "Table": ["indicators", "bilateral", "commodities", "indicator_catalog",
                  "indicators_subnational", "documents", "concept", "represented_variable",
                  "instance_variable", "topic_taxonomy", "countries", "subnational_units", "sources"],
        "Rows": [f"{ni:,}", f"{nb:,}", f"{nc:,}", f"{ncat:,}",
                 f"{q1('SELECT count(*) FROM indicators_subnational'):,}",
                 f"{q1('SELECT count(*) FROM documents'):,}",
                 f"{q1('SELECT count(*) FROM concept'):,}",
                 f"{q1('SELECT count(*) FROM represented_variable'):,}",
                 f"{q1('SELECT count(*) FROM instance_variable'):,}",
                 f"{q1('SELECT count(*) FROM topic_taxonomy'):,}",
                 f"{ncountry:,}",
                 f"{q1('SELECT count(*) FROM subnational_units'):,}",
                 f"{q1('SELECT count(*) FROM sources'):,}"],
        "Description": [
            "Country-year-indicator observations (main fact table)",
            "Bilateral flows: trade, FDI, debt between countries",
            "Annual commodity prices",
            "Indicator dictionary: code, name, short_name, topic, source, coverage",
            "Argentina subnational indicators (province, department, school level)",
            "Legislation and policy documents metadata",
            "DDI concepts (abstract analytical ideas)",
            "DDI represented variables (measurement methods)",
            "DDI instance variables (concrete columns in sources)",
            "GSI taxonomy hierarchy (L1-L2, 75 nodes)",
            "Country registry with classifications",
            "Argentine provinces, departments, establishments",
            "Data source registry",
        ],
    })
    st.dataframe(tables_data, use_container_width=True, hide_index=True)

    st.markdown("## Data Quality")
    vt = q("SELECT value_type, count(*) as n FROM indicators GROUP BY value_type ORDER BY n DESC")
    vt["share"] = (vt["n"] / vt["n"].sum() * 100).round(2).astype(str) + "%"
    st.dataframe(vt.rename(columns={"value_type":"Type","n":"Observations","share":"Share"}),
        use_container_width=True, hide_index=True)

    st.markdown("## Indicator Topics")
    topics = q("SELECT topic, count(*) as indicators FROM indicator_catalog GROUP BY topic ORDER BY indicators DESC")
    st.dataframe(topics.rename(columns={"topic":"Topic","indicators":"Indicators"}),
        use_container_width=True, hide_index=True)

    st.markdown("## Variable Cascade (DDI)")
    cc1,cc2,cc3 = st.columns(3)
    cc1.metric("Concepts", f"{q1('SELECT count(*) FROM concept'):,}")
    cc2.metric("Represented Variables", f"{q1('SELECT count(*) FROM represented_variable'):,}")
    cc3.metric("Instance Variables", f"{q1('SELECT count(*) FROM instance_variable'):,}")
    st.caption("Every indicator traces: instance variable → represented variable → concept → taxonomy position")

# =====================================================================
# 2. INDICATOR DICTIONARY
# =====================================================================
elif section == "Indicator Dictionary":
    st.title("Indicator Dictionary")
    st.caption(f"{q1('SELECT count(*) FROM indicator_catalog'):,} indicators — search by name, code, or keyword")

    search = st.text_input("Search", placeholder="Type: GDP, mortality, electricity, poverty, renewable, education...")

    if search and len(search) >= 2:
        safe = search.replace("'", "''")
        results = q(f"""
            SELECT short_name, indicator_code, indicator_name, source_id, topic, unit,
                   country_count, coverage_start, coverage_end
            FROM indicator_catalog
            WHERE indicator_name ILIKE '%{safe}%' OR indicator_code ILIKE '%{safe}%' OR short_name ILIKE '%{safe}%'
            ORDER BY country_count DESC NULLS LAST
            LIMIT 200
        """)

        if len(results) > 0:
            st.success(f"{len(results)} indicators found")
            st.dataframe(
                results.rename(columns={
                    "short_name":"Short Name", "indicator_code":"Code",
                    "indicator_name":"Full Name", "source_id":"Source",
                    "topic":"Topic", "unit":"Unit",
                    "country_count":"Countries", "coverage_start":"From", "coverage_end":"To"
                }),
                use_container_width=True, hide_index=True, height=500,
                column_config={
                    "Short Name": st.column_config.TextColumn(width="medium"),
                    "Code": st.column_config.TextColumn(width="small"),
                    "Full Name": st.column_config.TextColumn(width="large"),
                    "Source": st.column_config.TextColumn(width="small"),
                    "Topic": st.column_config.TextColumn(width="small"),
                }
            )
        else:
            st.warning("No indicators found for that search.")
    else:
        st.info("Type at least 2 characters. Searches across short name, code, and full name.")

        st.markdown("## Quick stats")
        c1,c2,c3 = st.columns(3)
        c1.metric("Total indicators", f"{q1('SELECT count(*) FROM indicator_catalog'):,}")
        c2.metric("With short_name", f"{q1('SELECT count(*) FROM indicator_catalog WHERE short_name IS NOT NULL'):,}")
        c3.metric("Topics", q1("SELECT count(DISTINCT topic) FROM indicator_catalog"))

# =====================================================================
# 3. BROWSE BY TOPIC
# =====================================================================
elif section == "Browse by Topic":
    st.title("Browse by Topic")

    topics = q("SELECT topic, count(*) as n FROM indicator_catalog GROUP BY topic ORDER BY n DESC")
    selected = st.selectbox("Select topic", topics["topic"].tolist(),
        format_func=lambda x: f"{x.replace('_',' ').title()} — {topics[topics['topic']==x]['n'].values[0]:,} indicators")

    if selected:
        indicators = q(f"""
            SELECT short_name, indicator_code, indicator_name, source_id, unit,
                   country_count, coverage_start, coverage_end
            FROM indicator_catalog
            WHERE topic = '{selected}'
            ORDER BY country_count DESC NULLS LAST
        """)

        st.markdown(f"## {selected.replace('_',' ').title()} — {len(indicators):,} indicators")

        # Filter by source within topic
        sources_in_topic = sorted(indicators["source_id"].unique())
        source_filter = st.multiselect("Filter by source", sources_in_topic, default=sources_in_topic)
        filtered = indicators[indicators["source_id"].isin(source_filter)]

        st.dataframe(
            filtered.rename(columns={
                "short_name":"Short Name", "indicator_code":"Code",
                "indicator_name":"Full Name", "source_id":"Source", "unit":"Unit",
                "country_count":"Countries", "coverage_start":"From", "coverage_end":"To"
            }),
            use_container_width=True, hide_index=True, height=600,
        )

# =====================================================================
# 4. BROWSE BY SOURCE
# =====================================================================
elif section == "Browse by Source":
    st.title("Browse by Source")

    sources = q("""
        SELECT s.source_id, s.source_name, s.institution, s.access_method, s.license, s.topics,
               COALESCE(ic.n, 0) as indicators,
               COALESCE(ir.rows, 0) as observations
        FROM sources s
        LEFT JOIN (SELECT source_id, count(*) as n FROM indicator_catalog GROUP BY source_id) ic ON ic.source_id = s.source_id
        LEFT JOIN (SELECT source_id, count(*) as rows FROM indicators GROUP BY source_id) ir ON ir.source_id = s.source_id
        ORDER BY observations DESC
    """)

    # Summary table
    st.dataframe(
        sources[["source_id","source_name","institution","indicators","observations","access_method","topics"]].rename(columns={
            "source_id":"ID","source_name":"Name","institution":"Institution",
            "indicators":"Indicators","observations":"Observations",
            "access_method":"Access","topics":"Topics"
        }),
        use_container_width=True, hide_index=True, height=400,
    )

    # Drill into a source
    st.markdown("---")
    selected_source = st.selectbox("Select source to browse indicators",
        sources[sources["indicators"]>0]["source_id"].tolist(),
        format_func=lambda x: f"{x} — {sources[sources['source_id']==x]['source_name'].values[0]}")

    if selected_source:
        src_indicators = q(f"""
            SELECT short_name, indicator_code, indicator_name, topic, unit,
                   country_count, coverage_start, coverage_end
            FROM indicator_catalog
            WHERE source_id = '{selected_source}'
            ORDER BY topic, indicator_code
        """)
        info = sources[sources["source_id"]==selected_source].iloc[0]
        st.markdown(f"### {info['source_name']}")
        st.caption(f"Institution: {info['institution']} | Access: {info['access_method']} | License: {info['license']}")
        st.caption(f"Topics: {info['topics']}")

        st.dataframe(
            src_indicators.rename(columns={
                "short_name":"Short Name","indicator_code":"Code","indicator_name":"Full Name",
                "topic":"Topic","unit":"Unit","country_count":"Countries",
                "coverage_start":"From","coverage_end":"To"
            }),
            use_container_width=True, hide_index=True, height=500,
        )

# =====================================================================
# 5. BROWSE BY TAXONOMY
# =====================================================================
elif section == "Browse by Taxonomy":
    st.title("GSI Topic Taxonomy")
    st.caption("Global South Infrastructure taxonomy v30 — navigate the conceptual hierarchy")

    tax = q("SELECT * FROM topic_taxonomy ORDER BY id")
    l1 = tax[tax["level"]==1].sort_values("id")

    topic_map = {'5.1':'macro','5.2':'trade','5.6':'finance','5.7':'labor',
        '6.2':'health','6.3':'education','6.4':'social_protection','6.5':'gender',
        '4.7':'inequality','4.1':'population','7.2':'agriculture','7.5':'environment',
        '8.1':'energy','9.1':'military','3.2':'governance','6.7':'infrastructure','5.12':'commodities'}

    for _, row in l1.iterrows():
        l2 = tax[(tax["level"]==2) & (tax["parent_id"]==row["id"])].sort_values("id")
        with st.expander(f"**{row['code']}. {row['name']}** ({row['name_es'] or ''}) — {len(l2)} subcategories"):
            for _, sub in l2.iterrows():
                topic = topic_map.get(sub["code"], "")
                if topic:
                    n = q1(f"SELECT count(*) FROM indicator_catalog WHERE topic='{topic}'")
                    st.markdown(f"**`{sub['code']}`** {sub['name']} ({sub['name_es'] or ''}) — **{n:,} indicators** `[{topic}]`")
                else:
                    st.markdown(f"`{sub['code']}` {sub['name']} ({sub['name_es'] or ''}) — *pending data*")

    st.markdown("---")
    st.markdown("## Variable Cascade (DDI)")
    st.markdown("""
    Every indicator in DATA FORCES follows a three-tier chain:
    1. **Concept** — abstract idea (e.g., "maternal mortality")
    2. **Represented Variable** — measurement method (e.g., "deaths per 100K live births")
    3. **Instance Variable** — concrete column in a specific source (e.g., `SH.STA.MMRT` in WB_WDI)
    """)
    cc1,cc2,cc3 = st.columns(3)
    cc1.metric("Concepts", f"{q1('SELECT count(*) FROM concept'):,}")
    cc2.metric("Represented Vars", f"{q1('SELECT count(*) FROM represented_variable'):,}")
    cc3.metric("Instance Vars", f"{q1('SELECT count(*) FROM instance_variable'):,}")

# =====================================================================
# 6. COUNTRY DATA AVAILABILITY
# =====================================================================
elif section == "Country Data Availability":
    st.title("Country Data Availability")

    countries = q("SELECT * FROM countries ORDER BY country_name")
    lab70 = countries[countries["in_lab70"]==True]

    col1, col2 = st.columns([3,1])
    with col2:
        only_lab70 = st.checkbox("Lab70 only", True)
    with col1:
        pool = lab70 if only_lab70 else countries
        sel = st.selectbox("Select country", pool["iso3"].tolist(),
            format_func=lambda x: f"{pool[pool['iso3']==x]['country_name'].values[0]} ({x})")

    if sel:
        c = pool[pool["iso3"]==sel].iloc[0]
        pos = c.get("structural_pos","")
        st.markdown(f"### {c['country_name']} ({sel})")
        st.caption(f"Region: {c['region']} | Income: {c['income_group']} | Position: {(pos or '').replace('_',' ').title()}")

        # Data availability by topic
        availability = q(f"""
            SELECT ic.topic,
                   count(DISTINCT i.indicator_code) as indicators_with_data,
                   MIN(i.year) as from_year,
                   MAX(i.year) as to_year,
                   count(*) as total_obs
            FROM indicators i
            JOIN indicator_catalog ic ON i.indicator_code = ic.indicator_code AND i.source_id = ic.source_id
            WHERE i.iso3 = '{sel}'
            GROUP BY ic.topic
            ORDER BY indicators_with_data DESC
        """)

        if len(availability) > 0:
            st.markdown("## Data by topic")
            st.dataframe(
                availability.rename(columns={
                    "topic":"Topic","indicators_with_data":"Indicators",
                    "from_year":"From","to_year":"To","total_obs":"Observations"
                }),
                use_container_width=True, hide_index=True,
            )

            total_ind = availability["indicators_with_data"].sum()
            total_obs = availability["total_obs"].sum()
            st.caption(f"Total: {total_ind:,} unique indicators, {total_obs:,} observations")

        # Data by source
        by_source = q(f"""
            SELECT source_id, count(DISTINCT indicator_code) as indicators, count(*) as obs,
                   MIN(year) as from_year, MAX(year) as to_year
            FROM indicators WHERE iso3 = '{sel}'
            GROUP BY source_id ORDER BY obs DESC
        """)
        if len(by_source) > 0:
            with st.expander(f"Data by source ({len(by_source)} sources)"):
                st.dataframe(
                    by_source.rename(columns={
                        "source_id":"Source","indicators":"Indicators","obs":"Observations",
                        "from_year":"From","to_year":"To"
                    }),
                    use_container_width=True, hide_index=True,
                )

# =====================================================================
# 7. ARGENTINA SUBNATIONAL
# =====================================================================
elif section == "Argentina Subnational":
    st.title("Argentina — Subnational Data")

    c1,c2,c3,c4 = st.columns(4)
    c1.metric("Geographic units", f"{q1('SELECT count(*) FROM subnational_units'):,}")
    c2.metric("Observations", f"{q1('SELECT count(*) FROM indicators_subnational'):,}")
    c3.metric("Sources", q1("SELECT count(DISTINCT source_id) FROM indicators_subnational"))
    c4.metric("Indicators", q1("SELECT count(DISTINCT indicator_code) FROM indicators_subnational"))

    st.markdown("## Geographic Hierarchy")
    hierarchy = q("""SELECT level, count(*) as units FROM subnational_units GROUP BY level
        ORDER BY CASE level WHEN 'national' THEN 1 WHEN 'province' THEN 2
        WHEN 'department' THEN 3 WHEN 'establishment' THEN 4 END""")
    st.dataframe(hierarchy.rename(columns={"level":"Level","units":"Units"}),
        use_container_width=True, hide_index=True)

    st.markdown("## Available Indicators")
    sub_inds = q("""SELECT DISTINCT indicator_code, indicator_name, source_id,
        count(*) as obs, MIN(year) as from_year, MAX(year) as to_year
        FROM indicators_subnational
        GROUP BY indicator_code, indicator_name, source_id
        ORDER BY obs DESC""")
    st.dataframe(
        sub_inds.rename(columns={
            "indicator_code":"Code","indicator_name":"Name","source_id":"Source",
            "obs":"Observations","from_year":"From","to_year":"To"
        }),
        use_container_width=True, hide_index=True, height=400,
    )

    st.markdown("## Provinces")
    provs = q("SELECT unit_id, name, name_short, population FROM subnational_units WHERE level='province' ORDER BY population DESC")
    st.dataframe(
        provs.rename(columns={"unit_id":"Code","name":"Province","name_short":"Short","population":"Population (2022)"}),
        use_container_width=True, hide_index=True,
    )

# =====================================================================
# 8. DOCUMENTS & LEGISLATION
# =====================================================================
elif section == "Documents & Legislation":
    st.title("Documents & Legislation")
    ndocs = q1("SELECT count(*) FROM documents")
    st.caption(f"{ndocs} documents cataloged")

    docs = q("SELECT iso3, year, title, doc_type, tags, topics FROM documents ORDER BY iso3, year DESC")

    if len(docs) > 0:
        # Summary
        by_country = q("SELECT iso3, count(*) as n FROM documents GROUP BY iso3 ORDER BY n DESC")
        st.markdown("## By country")
        st.dataframe(by_country.rename(columns={"iso3":"Country","n":"Documents"}),
            use_container_width=True, hide_index=True)

        # Filter and browse
        st.markdown("## Browse")
        countries_with_docs = sorted(docs["iso3"].dropna().unique())
        sel = st.selectbox("Filter by country", ["All"] + countries_with_docs)
        filtered = docs if sel == "All" else docs[docs["iso3"]==sel]

        st.dataframe(
            filtered.rename(columns={"iso3":"Country","year":"Year","title":"Title",
                "doc_type":"Type","tags":"Tags","topics":"Topics"}),
            use_container_width=True, hide_index=True, height=500,
        )

# =====================================================================
# ANALYSIS: COUNTRY PROFILE
# =====================================================================
elif section == "Analysis: Country Profile":
    st.title("Country Profile")
    countries = q("SELECT * FROM countries WHERE in_lab70 ORDER BY country_name")

    sel = st.selectbox("Country", countries["iso3"].tolist(),
        format_func=lambda x: f"{countries[countries['iso3']==x]['country_name'].values[0]} ({x})")

    if sel:
        c = countries[countries["iso3"]==sel].iloc[0]
        pos = c.get("structural_pos","")
        color = P.get(pos, P["muted"])
        st.markdown(f"### {c['country_name']} <span style='color:{color};font-size:.8rem'>{(pos or '').replace('_',' ').title()}</span>", unsafe_allow_html=True)

        key_codes = ["NY.GDP.PCAP.CD","SP.DYN.LE00.IN","SH.STA.MMRT","EG.ELC.ACCS.ZS",
                     "SL.UEM.TOTL.ZS","FP.CPI.TOTL.ZG","SE.SEC.ENRR","MS.MIL.XPND.GD.ZS"]
        code_str = ",".join([f"'{c}'" for c in key_codes])
        data = q(f"SELECT indicator_code, indicator_name, year, value FROM indicators WHERE iso3='{sel}' AND indicator_code IN ({code_str}) AND value IS NOT NULL ORDER BY year")

        if len(data) > 0:
            for i in range(0, len(key_codes), 4):
                cols = st.columns(4)
                for j, code in enumerate(key_codes[i:i+4]):
                    with cols[j]:
                        sub = data[data["indicator_code"]==code].sort_values("year")
                        if len(sub) > 0:
                            latest = sub.iloc[-1]
                            v = latest["value"]
                            vs = f"{v:,.0f}" if abs(v) > 100 else f"{v:.1f}"
                            name = (latest["indicator_name"] or code)[:25]
                            st.metric(name, vs, help=f"Year: {int(latest['year'])}")
                            fig = px.area(sub, x="year", y="value")
                            fig.update_layout(height=80, margin=dict(t=0,b=0,l=0,r=0),
                                xaxis=dict(visible=False), yaxis=dict(visible=False),
                                showlegend=False, paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
                            fig.update_traces(fillcolor="rgba(0,212,170,0.12)", line_color=P["accent"])
                            st.plotly_chart(fig, use_container_width=True)

# =====================================================================
# ANALYSIS: CROSS-COUNTRY
# =====================================================================
elif section == "Analysis: Cross-Country":
    st.title("Cross-Country Analysis")
    lab70 = q("SELECT * FROM countries WHERE in_lab70 ORDER BY country_name")

    presets = {"BRICS+":["BRA","RUS","IND","CHN","ZAF","ARG","EGY","ETH"],
        "Latin America":["ARG","BRA","CHL","COL","MEX","PER","BOL","ECU"],
        "Sub-Saharan Africa":["NGA","ETH","GHA","KEN","ZAF","TZA","UGA","SEN"],
        "Core vs Periphery":["USA","DEU","JPN","SWE","NGA","ETH","MOZ","COD"]}

    col1,col2 = st.columns([1,3])
    with col1:
        preset = st.selectbox("Preset", ["Custom"]+list(presets.keys()))
    with col2:
        default = presets.get(preset, ["ARG","BRA","CHN","USA","NGA"])
        sel_countries = st.multiselect("Countries", lab70["iso3"].tolist(),
            default=[c for c in default if c in lab70["iso3"].tolist()],
            format_func=lambda x: f"{x} — {lab70[lab70['iso3']==x]['country_name'].values[0]}")

    # Search indicator dynamically
    ind_search = st.text_input("Search indicator", placeholder="GDP, life expectancy, electricity...")
    if ind_search and len(ind_search) >= 2:
        safe = ind_search.replace("'","''")
        found = q(f"SELECT indicator_code, short_name, country_count FROM indicator_catalog WHERE (indicator_name ILIKE '%{safe}%' OR short_name ILIKE '%{safe}%') ORDER BY country_count DESC LIMIT 20")
        if len(found) > 0:
            ind = st.selectbox("Select", found["indicator_code"].tolist(),
                format_func=lambda x: found[found["indicator_code"]==x]["short_name"].values[0])
        else:
            ind = None
            st.warning("No indicator found.")
    else:
        ind = None

    yr = st.slider("Period", 1960, 2030, (2000, 2023))

    if sel_countries and ind:
        iso_str = ",".join([f"'{c}'" for c in sel_countries])
        data = q(f"SELECT iso3,year,indicator_code,indicator_name,value FROM indicators WHERE indicator_code='{ind}' AND iso3 IN ({iso_str}) AND year>={yr[0]} AND year<={yr[1]} AND value IS NOT NULL ORDER BY year")

        if len(data) > 0:
            name = data["indicator_name"].iloc[0] or ind
            fig = px.line(data, x="year", y="value", color="iso3",
                color_discrete_sequence=COLORS)
            fig.update_layout(height=450, title=name, margin=dict(t=40,b=30,l=50,r=10),
                paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                font=dict(color=P["text"],family="Inter"),
                xaxis=dict(gridcolor=P["card"],title=""), yaxis=dict(gridcolor=P["card"],title=""),
                legend=dict(orientation="h",y=-0.12,font=dict(size=10)))
            st.plotly_chart(fig, use_container_width=True)

            with st.expander("Data table"):
                pivot = data.pivot_table(index="year", columns="iso3", values="value")
                st.dataframe(pivot, use_container_width=True)

elif section == "---":
    pass
