import streamlit as st
import pandas as pd
import numpy as np

# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="HR Placement Intelligence",
    page_icon="💼",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================
# PREMIUM DASHBOARD STYLING
# ============================================================

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

.stApp {
    background:
        radial-gradient(circle at 10% 0%, rgba(99,102,241,.12), transparent 25%),
        radial-gradient(circle at 90% 10%, rgba(14,165,233,.10), transparent 25%);
}

.block-container {
    max-width: 1450px;
    padding-top: 1.4rem;
    padding-bottom: 3rem;
}

#MainMenu, footer {
    visibility: hidden;
}

/* Hero */
.hero {
    padding: 30px 34px;
    border-radius: 24px;
    background: linear-gradient(120deg, #111827 0%, #312e81 52%, #0369a1 100%);
    box-shadow: 0 18px 45px rgba(15,23,42,.20);
    margin-bottom: 25px;
}

.hero-badge {
    display:inline-block;
    padding:7px 13px;
    border-radius:999px;
    background:rgba(255,255,255,.14);
    color:#e0f2fe;
    font-size:.78rem;
    font-weight:700;
    letter-spacing:.5px;
    margin-bottom:12px;
}

.hero h1 {
    color:white;
    font-size:2.25rem;
    margin:0;
    font-weight:800;
}

.hero p {
    color:#dbeafe;
    margin:10px 0 0 0;
    font-size:1rem;
}

/* Section */
.section-heading {
    font-size:1.25rem;
    font-weight:800;
    margin:22px 0 12px 0;
}

.section-note {
    opacity:.65;
    font-size:.9rem;
    margin-top:-7px;
    margin-bottom:15px;
}

/* Metric cards */
div[data-testid="stMetric"] {
    border:1px solid rgba(148,163,184,.25);
    border-radius:18px;
    padding:18px 18px 16px 18px;
    background:rgba(255,255,255,.04);
    box-shadow:0 7px 25px rgba(15,23,42,.07);
    min-height:130px;
    transition:transform .2s ease, box-shadow .2s ease;
}

div[data-testid="stMetric"]:hover {
    transform:translateY(-3px);
    box-shadow:0 13px 30px rgba(15,23,42,.12);
}

div[data-testid="stMetricLabel"] {
    font-size:.88rem;
    font-weight:650;
}

div[data-testid="stMetricValue"] {
    font-size:1.75rem;
    font-weight:800;
}

/* Insight cards */
.insight-card {
    border:1px solid rgba(148,163,184,.22);
    border-radius:18px;
    padding:20px;
    min-height:165px;
    background:rgba(255,255,255,.035);
    box-shadow:0 7px 25px rgba(15,23,42,.06);
}

.insight-title {
    font-size:.95rem;
    font-weight:800;
    margin-bottom:10px;
}

.insight-value {
    font-size:1.65rem;
    font-weight:800;
    margin-bottom:6px;
}

.insight-text {
    font-size:.88rem;
    opacity:.72;
    line-height:1.55;
}

/* Status pill */
.pill {
    display:inline-block;
    padding:5px 10px;
    border-radius:999px;
    font-size:.76rem;
    font-weight:700;
    background:rgba(99,102,241,.13);
}

/* Sidebar */
section[data-testid="stSidebar"] {
    border-right:1px solid rgba(148,163,184,.18);
}

.sidebar-brand {
    padding:10px 0 6px 0;
}

.sidebar-brand h2 {
    margin:0;
    font-size:1.35rem;
}

.sidebar-brand p {
    opacity:.65;
    font-size:.84rem;
    margin-top:5px;
}

/* Expander */
div[data-testid="stExpander"] {
    border-radius:14px;
    border:1px solid rgba(148,163,184,.22);
}

/* dataframe */
div[data-testid="stDataFrame"] {
    border-radius:14px;
    overflow:hidden;
}
</style>
""", unsafe_allow_html=True)

# ============================================================
# LOAD DATA
# ============================================================

@st.cache_data
def load_data():
    df = pd.read_csv("HR.csv")

    for col in df.select_dtypes(include="object").columns:
        df[col] = df[col].str.strip().str.lower()

    num_cols = df.select_dtypes(include="number").columns
    for col in num_cols:
        df[col] = df[col].fillna(df[col].median())

    cat_cols = df.select_dtypes(include="object").columns
    for col in cat_cols:
        df[col] = df[col].fillna(df[col].mode()[0])

    return df.drop_duplicates().reset_index(drop=True)


try:
    df = load_data()
except FileNotFoundError:
    st.error("⚠️ HR.csv not found. Keep HR.csv in the same folder as this dashboard.")
    st.stop()

# ============================================================
# FEATURE CREATION - ALIGNED WITH PROJECT
# ============================================================

df["interview_score"] = df[
    ["technical_score", "aptitude_score", "communication_score"]
].mean(axis=1)

df["placement"] = df["status"].map({
    "placed": 1,
    "not placed": 0
})

df["academic_score"] = df[
    ["ssc_percentage", "hsc_percentage", "degree_percentage"]
].mean(axis=1)

df["placement_readiness_score"] = (
    df["academic_score"] * 0.25
    + df["skills_match_percentage"] * 0.30
    + df["technical_score"] * 0.20
    + df["aptitude_score"] * 0.10
    + df["communication_score"] * 0.15
).round(2)

# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:
    st.markdown("""
    <div class="sidebar-brand">
        <h2>💼 PlacementIQ</h2>
        <p>HR Placement Intelligence</p>
    </div>
    """, unsafe_allow_html=True)

    st.divider()

    st.markdown("#### ⚙️ Dashboard Controls")

    risk_threshold = st.slider(
        "High-Risk Threshold",
        30, 70, 50, 5,
        help="Readiness scores below this threshold are classified as high risk."
    )

    status_options = ["All"] + sorted(df["status"].dropna().unique().tolist())
    selected_status = st.selectbox("Candidate Status", status_options)

    if "company_tier" in df.columns:
        tier_options = ["All"] + sorted(df["company_tier"].dropna().unique().tolist())
        selected_tier = st.selectbox("Company Tier", tier_options)
    else:
        selected_tier = "All"

    st.divider()
    st.markdown("#### 📦 Dataset Snapshot")
    st.write(f"**{len(df):,}** candidate records")
    st.write(f"**{df.shape[1]}** available features")
    st.caption("Cleaned using the same preprocessing logic as the project notebook.")

# ============================================================
# FILTERS
# ============================================================

filtered_df = df.copy()

if selected_status != "All":
    filtered_df = filtered_df[filtered_df["status"] == selected_status]

if selected_tier != "All":
    filtered_df = filtered_df[filtered_df["company_tier"] == selected_tier]

# ============================================================
# KPIs
# ============================================================

total_candidates = len(filtered_df)

placement_rate = (
    filtered_df["placement"].mean() * 100
    if total_candidates else 0
)

# Current dataset has no separate acceptance field.
job_acceptance_rate = placement_rate

avg_interview = (
    filtered_df["interview_score"].mean()
    if total_candidates else 0
)

avg_skills = (
    filtered_df["skills_match_percentage"].mean()
    if total_candidates else 0
)

# Current project has no explicit offer-dropout field.
offer_dropout_rate = None

filtered_df = filtered_df.copy()
filtered_df["high_risk_candidate"] = (
    filtered_df["placement_readiness_score"] < risk_threshold
)

high_risk_pct = (
    filtered_df["high_risk_candidate"].mean() * 100
    if total_candidates else 0
)

avg_readiness = (
    filtered_df["placement_readiness_score"].mean()
    if total_candidates else 0
)

# ============================================================
# HERO
# ============================================================

st.markdown("""
<div class="hero">
    <div class="hero-badge">HR ANALYTICS • PLACEMENT INTELLIGENCE</div>
    <h1>Candidate Placement Dashboard</h1>
    <p>Executive view of placement outcomes, interview performance,
    skill alignment and candidate readiness.</p>
</div>
""", unsafe_allow_html=True)

# ============================================================
# KPI GRID
# ============================================================

st.markdown('<div class="section-heading">Executive KPIs</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="section-note">A quick view of the most important placement indicators.</div>',
    unsafe_allow_html=True
)

r1c1, r1c2, r1c3, r1c4 = st.columns(4)

with r1c1:
    st.metric("👥 Total Candidates", f"{total_candidates:,}")

with r1c2:
    st.metric("🎯 Placement Rate", f"{placement_rate:.2f}%")

with r1c3:
    st.metric("🤝 Job Acceptance Rate", f"{job_acceptance_rate:.2f}%")

with r1c4:
    st.metric("⭐ Avg Interview Score", f"{avg_interview:.2f}")

r2c1, r2c2, r2c3 = st.columns(3)

with r2c1:
    st.metric("🧩 Avg Skills Match", f"{avg_skills:.2f}%")

with r2c2:
    st.metric("📉 Offer Dropout Rate", "N/A")

with r2c3:
    st.metric("⚠️ High-Risk Candidates", f"{high_risk_pct:.2f}%")

# ============================================================
# MANAGEMENT SNAPSHOT
# ============================================================

st.markdown('<div class="section-heading">Management Snapshot</div>', unsafe_allow_html=True)

a, b, c = st.columns(3)

with a:
    st.markdown(f"""
    <div class="insight-card">
        <div class="insight-title">🏆 PLACEMENT PERFORMANCE</div>
        <div class="insight-value">{placement_rate:.2f}%</div>
        <div class="insight-text">
            Current placement rate for the selected candidate segment.
            Use the sidebar filters to compare candidate groups.
        </div>
    </div>
    """, unsafe_allow_html=True)

with b:
    st.markdown(f"""
    <div class="insight-card">
        <div class="insight-title">🚀 READINESS INDEX</div>
        <div class="insight-value">{avg_readiness:.2f}</div>
        <div class="insight-text">
            Average project-defined placement readiness score combining
            academics, skills, technical, aptitude and communication performance.
        </div>
    </div>
    """, unsafe_allow_html=True)

with c:
    st.markdown(f"""
    <div class="insight-card">
        <div class="insight-title">⚠️ CANDIDATE RISK</div>
        <div class="insight-value">{high_risk_pct:.2f}%</div>
        <div class="insight-text">
            Candidates below the current readiness threshold of
            <b>{risk_threshold}</b>. Adjust the threshold from the sidebar.
        </div>
    </div>
    """, unsafe_allow_html=True)

# ============================================================
# PLACEMENT OVERVIEW
# ============================================================

st.markdown('<div class="section-heading">Placement Overview</div>', unsafe_allow_html=True)

left, right = st.columns([1, 1])

with left:
    placement_counts = (
        filtered_df["status"]
        .value_counts()
        .rename_axis("Status")
        .reset_index(name="Candidates")
    )
    st.markdown("##### Candidate Status")
    st.bar_chart(
        placement_counts.set_index("Status"),
        use_container_width=True
    )

with right:
    st.markdown("##### Performance Summary")

    summary = pd.DataFrame({
        "Indicator": [
            "Average Interview Score",
            "Average Skills Match %",
            "Average Readiness Score",
            "High-Risk Candidate %"
        ],
        "Value": [
            round(avg_interview, 2),
            round(avg_skills, 2),
            round(avg_readiness, 2),
            round(high_risk_pct, 2)
        ]
    })

    st.dataframe(
        summary,
        use_container_width=True,
        hide_index=True
    )

    st.info(
        "Offer Dropout Rate is shown as N/A because the current project "
        "dataset does not contain an explicit offer-dropout field."
    )

# ============================================================
# DETAILS
# ============================================================

st.markdown('<div class="section-heading">Dashboard Details</div>', unsafe_allow_html=True)

with st.expander("📖 KPI Definitions & Business Logic"):
    st.markdown("""
**Total Candidates** — Candidate records remaining after project cleaning and duplicate removal.

**Placement Rate (%)** — Percentage of candidates with `status = placed`.

**Job Acceptance Rate (%)** — Uses placement status as the available proxy because the current project does not include a separate offer-acceptance field.

**Average Interview Score** — Average of technical, aptitude and communication scores.

**Average Skills Match %** — Mean of `skills_match_percentage`.

**Offer Dropout Rate** — Not calculated because an explicit offer-dropout/offer-declined field is not present in the current project dataset.

**High-Risk Candidate Percentage** — Candidates whose project-defined `placement_readiness_score` is below the selected threshold. This is a dashboard business rule and not an ML-predicted probability.
""")

with st.expander("🔎 Explore Candidate Data"):
    st.dataframe(
        filtered_df,
        use_container_width=True,
        hide_index=True
    )

# ============================================================
# FOOTER
# ============================================================

st.markdown("<br>", unsafe_allow_html=True)
st.divider()

f1, f2 = st.columns([3, 1])
with f1:
    st.caption("HR Job Placement Prediction & Candidate Analytics")
with f2:
    st.caption("Built with Streamlit • PlacementIQ")
