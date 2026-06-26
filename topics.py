"""
DATA FORCES — Topic Configuration
Maps thematic topics to indicator codes, descriptions, and display config.
"""

TOPICS = {
    "economy": {
        "label": "Economy",
        "label_es": "Economia",
        "icon": "chart_with_upwards_trend",
        "color": "#2563eb",
        "subtopics": {
            "macro": {
                "label": "Macroeconomics",
                "label_es": "Macroeconomia",
                "indicators": [
                    ("NY.GDP.MKTP.CD", "GDP (current US$)"),
                    ("NY.GDP.PCAP.CD", "GDP per capita (current US$)"),
                    ("NY.GDP.MKTP.KD.ZG", "GDP growth (annual %)"),
                    ("NE.GDI.FTOT.ZS", "Gross fixed capital formation (% GDP)"),
                    ("FP.CPI.TOTL.ZG", "Inflation, consumer prices (annual %)"),
                    ("GC.DOD.TOTL.GD.ZS", "Central government debt (% GDP)"),
                    ("BN.CAB.XOKA.GD.ZS", "Current account balance (% GDP)"),
                    ("FI.RES.TOTL.CD", "Total reserves (current US$)"),
                ],
            },
            "trade": {
                "label": "Trade",
                "label_es": "Comercio",
                "indicators": [
                    ("NE.EXP.GNFS.ZS", "Exports of goods and services (% GDP)"),
                    ("NE.IMP.GNFS.ZS", "Imports of goods and services (% GDP)"),
                    ("TM.VAL.MRCH.CD.WT", "Merchandise imports (current US$)"),
                    ("TX.VAL.MRCH.CD.WT", "Merchandise exports (current US$)"),
                ],
            },
            "finance": {
                "label": "Finance",
                "label_es": "Finanzas",
                "indicators": [
                    ("BX.KLT.DINV.WD.GD.ZS", "Foreign direct investment, net inflows (% GDP)"),
                    ("DT.DOD.DECT.GN.ZS", "External debt stocks (% GNI)"),
                ],
            },
        },
    },
    "agriculture": {
        "label": "Agriculture & Food Sovereignty",
        "label_es": "Agricultura y Soberania Alimentaria",
        "icon": "seedling",
        "color": "#16a34a",
        "subtopics": {
            "production": {
                "label": "Production",
                "label_es": "Produccion",
                "catalog_topic": "agriculture",
            },
            "food_security": {
                "label": "Food Security",
                "label_es": "Seguridad Alimentaria",
                "indicators": [
                    ("SN.ITK.DEFC.ZS", "Prevalence of undernourishment (%)"),
                    ("AG.LND.FRST.ZS", "Forest area (% of land)"),
                    ("AG.LND.ARBL.ZS", "Arable land (% of land)"),
                ],
            },
        },
    },
    "energy": {
        "label": "Energy",
        "label_es": "Energia",
        "icon": "zap",
        "color": "#f59e0b",
        "subtopics": {
            "generation": {
                "label": "Generation & Capacity",
                "label_es": "Generacion y Capacidad",
                "indicators": [
                    ("EG.ELC.RNEW.ZS", "Renewable electricity output (% total)"),
                    ("EG.EGY.PRIM.PP.KD", "Energy intensity (MJ/$2021 PPP GDP)"),
                ],
            },
            "access": {
                "label": "Access & Transition",
                "label_es": "Acceso y Transicion",
                "indicators": [
                    ("EG.ELC.ACCS.ZS", "Access to electricity (%)"),
                    ("EG.IMP.CONS.ZS", "Energy imports, net (% energy use)"),
                ],
            },
            "emissions": {
                "label": "Emissions",
                "label_es": "Emisiones",
                "indicators": [
                    ("EN.ATM.CO2E.PC", "CO2 emissions (metric tons per capita)"),
                ],
            },
        },
    },
    "education": {
        "label": "Education",
        "label_es": "Educacion",
        "icon": "book",
        "color": "#8b5cf6",
        "subtopics": {
            "access": {
                "label": "Access & Enrollment",
                "label_es": "Acceso y Matricula",
                "indicators": [
                    ("SE.SEC.ENRR", "School enrollment, secondary (% gross)"),
                    ("SE.TER.ENRR", "School enrollment, tertiary (% gross)"),
                ],
            },
            "expenditure": {
                "label": "Public Expenditure",
                "label_es": "Gasto Publico",
                "indicators": [
                    ("SE.XPD.TOTL.GD.ZS", "Government expenditure on education (% GDP)"),
                ],
            },
        },
    },
    "health": {
        "label": "Health",
        "label_es": "Salud",
        "icon": "heart",
        "color": "#ef4444",
        "subtopics": {
            "mortality": {
                "label": "Mortality",
                "label_es": "Mortalidad",
                "indicators": [
                    ("SH.STA.MMRT", "Maternal mortality ratio (per 100,000)"),
                    ("SH.DYN.MORT", "Under-5 mortality rate (per 1,000)"),
                    ("SP.DYN.LE00.IN", "Life expectancy at birth (years)"),
                ],
            },
            "systems": {
                "label": "Health Systems",
                "label_es": "Sistemas de Salud",
                "indicators": [
                    ("SH.XPD.GHED.GD.ZS", "Domestic govt health expenditure (% GDP)"),
                ],
            },
        },
    },
    "politics": {
        "label": "Political Analysis",
        "label_es": "Analisis Politico",
        "icon": "landmark",
        "color": "#6366f1",
        "subtopics": {
            "governance": {
                "label": "Governance",
                "label_es": "Gobernanza",
                "indicators": [
                    ("CC.EST", "Control of Corruption: Estimate"),
                    ("GE.EST", "Government Effectiveness: Estimate"),
                    ("RL.EST", "Rule of Law: Estimate"),
                    ("VA.EST", "Voice and Accountability: Estimate"),
                ],
            },
        },
    },
    "labor": {
        "label": "Labor",
        "label_es": "Trabajo",
        "icon": "hard_hat",
        "color": "#0891b2",
        "subtopics": {
            "employment": {
                "label": "Employment",
                "label_es": "Empleo",
                "indicators": [
                    ("SL.UEM.TOTL.ZS", "Unemployment (% total labor force)"),
                    ("SL.TLF.CACT.ZS", "Labor force participation rate (%)"),
                    ("SL.EMP.VULN.ZS", "Vulnerable employment (% total)"),
                ],
            },
            "gender": {
                "label": "Gender Gap",
                "label_es": "Brecha de Genero",
                "indicators": [
                    ("SL.TLF.CACT.FE.ZS", "Female labor force participation (%)"),
                    ("SG.GEN.PARL.ZS", "Women in parliament (%)"),
                    ("SG.LAW.INDX", "Women, Business and the Law index"),
                ],
            },
        },
    },
    "geopolitics": {
        "label": "Geopolitics",
        "label_es": "Geopolitica",
        "icon": "globe",
        "color": "#475569",
        "subtopics": {
            "military": {
                "label": "Military",
                "label_es": "Militar",
                "indicators": [
                    ("MS.MIL.XPND.GD.ZS", "Military expenditure (% GDP)"),
                ],
            },
            "population": {
                "label": "Population & Migration",
                "label_es": "Poblacion y Migracion",
                "indicators": [
                    ("SP.POP.TOTL", "Population, total"),
                    ("SP.POP.GROW", "Population growth (annual %)"),
                    ("SP.URB.TOTL.IN.ZS", "Urban population (%)"),
                ],
            },
        },
    },
}

# Flat list of all indicator codes across all topics
def get_all_indicator_codes():
    codes = []
    for topic in TOPICS.values():
        for sub in topic["subtopics"].values():
            for code, name in sub.get("indicators", []):
                codes.append(code)
    return codes

# Get indicators for a specific topic
def get_topic_indicators(topic_key):
    topic = TOPICS.get(topic_key, {})
    indicators = []
    for sub in topic.get("subtopics", {}).values():
        indicators.extend(sub.get("indicators", []))
    return indicators

# Country presets
COUNTRY_PRESETS = {
    "BRICS+": ["BRA", "RUS", "IND", "CHN", "ZAF", "ARG", "EGY", "ETH"],
    "Latin America": ["ARG", "BRA", "CHL", "COL", "MEX", "PER", "BOL", "ECU", "URY"],
    "Sub-Saharan Africa": ["NGA", "ETH", "GHA", "KEN", "ZAF", "TZA", "UGA", "SEN", "MOZ"],
    "East & South Asia": ["CHN", "IND", "IDN", "VNM", "THA", "MYS", "BGD", "PHL", "KOR"],
    "Core economies": ["USA", "DEU", "JPN", "GBR", "FRA", "CAN", "AUS", "SWE"],
    "Periphery": ["MOZ", "ETH", "COD", "NGA", "BGD", "MMR", "LAO", "NPL"],
    "Core vs Periphery": ["USA", "DEU", "JPN", "SWE", "NGA", "ETH", "MOZ", "COD"],
}
