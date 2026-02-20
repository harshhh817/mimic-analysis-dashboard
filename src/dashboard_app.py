import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os

# -----------------------------------------------------------------------------
# 1. PAGE CONFIG
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="MIMIC-III Analytics",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -----------------------------------------------------------------------------
# 2. DATA LOADING
# -----------------------------------------------------------------------------
@st.cache_data
def load_data():
    try:
        current_dir = os.path.dirname(os.path.abspath(__file__))
        processed_path = os.path.join(current_dir, '../data/processed_admissions.csv')
        
        if not os.path.exists(processed_path): 
            return None, f"File not found at: {processed_path}"
            
        df = pd.read_csv(processed_path)
        df['admittime'] = pd.to_datetime(df['admittime'], errors='coerce')
        df['Outcome'] = df['hospital_expire_flag'].map({0: 'Survivor', 1: 'Deceased'})
        return df, None
    except Exception as e:
        import traceback
        return None, traceback.format_exc()

df, err_msg = load_data()
if df is None:
    st.error(f"Error loading data: {err_msg}")
    st.stop()


# -----------------------------------------------------------------------------
# 3. SIDEBAR
# -----------------------------------------------------------------------------
with st.sidebar:
    st.title("🏥 Settings")
    
    # Simple Filters
    gender = st.multiselect("Gender", options=df['gender'].unique(), default=df['gender'].unique())
    age_range = st.slider("Age Range", int(df['age'].min()), int(df['age'].max()), (20, 90))
    diagnoses_filter = st.multiselect("Specific Diagnosis", options=sorted(df['diagnosis'].unique()))
    
    # Apply Filters
    mask = (df['gender'].isin(gender)) & (df['age'].between(age_range[0], age_range[1]))
    if diagnoses_filter:
        mask = mask & (df['diagnosis'].isin(diagnoses_filter))
    
    df_filtered = df[mask]
    
    st.markdown("---")
    st.metric("Total Patients", len(df_filtered))

# -----------------------------------------------------------------------------
# 4. MAIN DASHBOARD
# -----------------------------------------------------------------------------
st.title("MIMIC-III Clinical Dashboard")
st.markdown(f"Analysis of **{len(df_filtered)}** ICU admissions.")

# KPI Row
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Admissions", len(df_filtered))
col2.metric("Avg Length of Stay", f"{df_filtered['total_icu_los'].mean():.1f} days")
col3.metric("Mortality Rate", f"{df_filtered['hospital_expire_flag'].mean():.1%}")
col4.metric("Avg Age", f"{df_filtered['age'].mean():.0f} years")

st.markdown("---")

# TABS
tab1, tab2, tab3 = st.tabs(["📊 Overview", "🩺 Clinical Analysis", "🧪 Labs"])

# TAB 1: OVERVIEW
with tab1:
    c1, c2 = st.columns(2)
    
    with c1:
        st.subheader("Length of Stay vs Age")
        # Scatter Plot - Use seaborn template for clean look
        fig_scatter = px.scatter(
            df_filtered, x="age", y="total_icu_los", color="Outcome", 
            size="total_icu_los", hover_data=['diagnosis'],
            title="LOS Distribution by Age",
            template="seaborn"
        )
        st.plotly_chart(fig_scatter, use_container_width=True)
        
    with c2:
        st.subheader("Gender Distribution")
        fig_pie = px.pie(
            df_filtered, names="gender", title="Gender Split",
            template="seaborn", hole=0.4
        )
        st.plotly_chart(fig_pie, use_container_width=True)

# TAB 2: CLINICAL
with tab2:
    st.subheader("Top Diagnoses")
    
    # Aggregation
    top_diag = df_filtered['diagnosis'].value_counts().head(10).reset_index()
    top_diag.columns = ['Diagnosis', 'Count']
    
    fig_bar = px.bar(
        top_diag, x='Count', y='Diagnosis', orientation='h',
        title="Top 10 Admission Diagnoses",
        text='Count', color='Count',
        template="seaborn"
    )
    fig_bar.update_layout(yaxis={'categoryorder':'total ascending'})
    st.plotly_chart(fig_bar, use_container_width=True)
    
    st.subheader("Mortality by Diagnosis (Top 10 Volume)")
    
    # Calculate mortality for top diagnoses
    top_diag_list = top_diag['Diagnosis'].tolist()
    mort_data = df_filtered[df_filtered['diagnosis'].isin(top_diag_list)].groupby('diagnosis')['hospital_expire_flag'].mean().reset_index()
    
    fig_mort = px.bar(
        mort_data, x='diagnosis', y='hospital_expire_flag',
        title="Mortality Rate by Condition",
        labels={'hospital_expire_flag': 'Mortality Rate'},
        template="seaborn", color='hospital_expire_flag'
    )
    st.plotly_chart(fig_mort, use_container_width=True)

# TAB 3: LABS
with tab3:
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Glucose Levels")
        fig_box = px.box(
            df_filtered, x="Outcome", y="first_glucose", color="Outcome",
            title="Glucose Distribution by Outcome",
            template="seaborn"
        )
        st.plotly_chart(fig_box, use_container_width=True)
        
    with col2:
        st.subheader("Creatinine Levels")
        fig_hist = px.histogram(
            df_filtered, x="first_creatinine", color="Outcome", barmode="overlay",
            title="Creatinine Distribution",
            template="seaborn"
        )
        st.plotly_chart(fig_hist, use_container_width=True)
