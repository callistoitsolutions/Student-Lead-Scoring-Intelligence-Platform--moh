"""
🎓 Student Lead Scoring Intelligence Platform
Professional AI-Powered Student Conversion Prediction System
No Login Required - Direct Access Dashboard
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import joblib
from datetime import datetime
from io import BytesIO

# ============================================================================
# PAGE CONFIGURATION
# ============================================================================
st.set_page_config(
    page_title="Student Lead Scoring Pro",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================================
# PROFESSIONAL CSS STYLING (Matching School Dashboard Design)
# ============================================================================

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700;800&display=swap');
    
    /* ==================== GLOBAL STYLES ==================== */
    * {
        font-family: 'Poppins', -apple-system, BlinkMacSystemFont, sans-serif;
    }
    
    /* Remove default Streamlit elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Main Container */
    .block-container {
        padding: 1.5rem 2rem 2rem 2rem;
        max-width: 100%;
    }
    
    /* ==================== SIDEBAR STYLING ==================== */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #003d82 0%, #00264d 100%);
        padding: 0;
    }
    
    [data-testid="stSidebar"] > div:first-child {
        padding: 0;
    }
    
    /* Sidebar Header */
    .sidebar-header {
        background: #002347;
        padding: 1.5rem 1.25rem;
        border-bottom: 1px solid rgba(255, 255, 255, 0.1);
        display: flex;
        align-items: center;
        gap: 0.75rem;
    }
    
    .sidebar-logo {
        width: 40px;
        height: 40px;
        background: white;
        border-radius: 8px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.5rem;
    }
    
    .sidebar-brand {
        color: white;
        font-weight: 700;
        font-size: 1.1rem;
    }
    
    /* Sidebar Navigation */
    .sidebar-nav {
        padding: 1rem 0;
    }
    
    .nav-section {
        margin-bottom: 0.5rem;
    }
    
    .nav-section-title {
        color: rgba(255, 255, 255, 0.5);
        font-size: 0.7rem;
        font-weight: 600;
        text-transform: uppercase;
        padding: 0.75rem 1.25rem 0.5rem 1.25rem;
        letter-spacing: 0.05em;
    }
    
    .nav-item {
        color: rgba(255, 255, 255, 0.8);
        padding: 0.75rem 1.25rem;
        display: flex;
        align-items: center;
        gap: 0.75rem;
        font-size: 0.9rem;
        font-weight: 500;
        cursor: pointer;
        transition: all 0.2s ease;
        border-left: 3px solid transparent;
    }
    
    .nav-item:hover {
        background: rgba(255, 255, 255, 0.05);
        color: white;
        border-left-color: #4CAF50;
    }
    
    .nav-item.active {
        background: rgba(255, 255, 255, 0.1);
        color: white;
        border-left-color: #4CAF50;
        font-weight: 600;
    }
    
    .nav-icon {
        font-size: 1.1rem;
        width: 20px;
        text-align: center;
    }
    
    /* Override Streamlit radio buttons in sidebar */
    [data-testid="stSidebar"] .stRadio > label {
        display: none;
    }
    
    [data-testid="stSidebar"] .stRadio > div {
        background: transparent;
        gap: 0;
    }
    
    [data-testid="stSidebar"] .stRadio > div > label {
        background: transparent;
        color: rgba(255, 255, 255, 0.8);
        padding: 0.75rem 1.25rem;
        margin: 0;
        border-left: 3px solid transparent;
        border-radius: 0;
        font-weight: 500;
        transition: all 0.2s ease;
    }
    
    [data-testid="stSidebar"] .stRadio > div > label:hover {
        background: rgba(255, 255, 255, 0.05);
        color: white;
        border-left-color: #4CAF50;
    }
    
    [data-testid="stSidebar"] .stRadio > div > label[data-selected="true"] {
        background: rgba(255, 255, 255, 0.1);
        color: white;
        border-left-color: #4CAF50;
        font-weight: 600;
    }
    
    /* ==================== TOP HEADER ==================== */
    .top-header {
        background: white;
        padding: 1.25rem 2rem;
        margin: -1.5rem -2rem 2rem -2rem;
        border-bottom: 1px solid #e0e0e0;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    
    .header-title {
        font-size: 1.5rem;
        font-weight: 700;
        color: #1a1a1a;
        margin: 0;
    }
    
    .header-actions {
        display: flex;
        align-items: center;
        gap: 1rem;
    }
    
    /* ==================== METRIC CARDS (Matching Dashboard) ==================== */
    .metric-row {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
        gap: 1.25rem;
        margin-bottom: 2rem;
    }
    
    .metric-card {
        background: white;
        border-radius: 12px;
        padding: 1.5rem;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    }
    
    .metric-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 6px 20px rgba(0, 0, 0, 0.12);
    }
    
    .metric-card::before {
        content: '';
        position: absolute;
        top: 0;
        right: 0;
        width: 100px;
        height: 100px;
        background: linear-gradient(135deg, rgba(255, 255, 255, 0.1), rgba(255, 255, 255, 0));
        border-radius: 0 12px 0 100%;
    }
    
    .metric-header {
        display: flex;
        justify-content: space-between;
        align-items: flex-start;
        margin-bottom: 1rem;
    }
    
    .metric-label {
        font-size: 0.85rem;
        color: #666;
        font-weight: 500;
        line-height: 1.4;
    }
    
    .metric-icon {
        width: 48px;
        height: 48px;
        border-radius: 10px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.5rem;
        opacity: 0.9;
    }
    
    .metric-value {
        font-size: 2rem;
        font-weight: 700;
        color: #1a1a1a;
        margin: 0.5rem 0 0.25rem 0;
        line-height: 1;
    }
    
    .metric-footer {
        font-size: 0.75rem;
        color: #999;
        margin-top: 0.5rem;
    }
    
    /* Icon Colors */
    .icon-purple { background: linear-gradient(135deg, #9b6dff 0%, #7c4dff 100%); color: white; }
    .icon-green { background: linear-gradient(135deg, #4ade80 0%, #22c55e 100%); color: white; }
    .icon-red { background: linear-gradient(135deg, #f87171 0%, #ef4444 100%); color: white; }
    .icon-yellow { background: linear-gradient(135deg, #fbbf24 0%, #f59e0b 100%); color: white; }
    .icon-blue { background: linear-gradient(135deg, #60a5fa 0%, #3b82f6 100%); color: white; }
    .icon-teal { background: linear-gradient(135deg, #2dd4bf 0%, #14b8a6 100%); color: white; }
    .icon-orange { background: linear-gradient(135deg, #fb923c 0%, #f97316 100%); color: white; }
    .icon-pink { background: linear-gradient(135deg, #f472b6 0%, #ec4899 100%); color: white; }
    
    /* ==================== CONTENT CARDS ==================== */
    .content-card {
        background: white;
        border-radius: 12px;
        padding: 1.5rem;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
        margin-bottom: 1.5rem;
    }
    
    .card-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 1.5rem;
        padding-bottom: 1rem;
        border-bottom: 1px solid #f0f0f0;
    }
    
    .card-title {
        font-size: 1.125rem;
        font-weight: 700;
        color: #1a1a1a;
        margin: 0;
    }
    
    /* ==================== SIDEBAR PANELS (Notice Board, Events) ==================== */
    .sidebar-panel {
        background: white;
        border-radius: 12px;
        padding: 1.25rem;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
        margin-bottom: 1.25rem;
    }
    
    .panel-header {
        font-size: 1rem;
        font-weight: 700;
        color: #1a1a1a;
        margin-bottom: 1rem;
        padding-bottom: 0.75rem;
        border-bottom: 1px solid #f0f0f0;
    }
    
    .notice-item {
        background: #fff9f0;
        border-left: 3px solid #fbbf24;
        padding: 0.75rem;
        border-radius: 6px;
        margin-bottom: 0.75rem;
        font-size: 0.85rem;
    }
    
    .notice-title {
        color: #1a1a1a;
        font-weight: 600;
        margin-bottom: 0.25rem;
    }
    
    .notice-time {
        color: #999;
        font-size: 0.75rem;
    }
    
    .event-item {
        display: flex;
        gap: 0.75rem;
        padding: 0.75rem;
        background: #f8f9fa;
        border-radius: 8px;
        margin-bottom: 0.75rem;
    }
    
    .event-date {
        background: white;
        border-radius: 6px;
        padding: 0.5rem;
        text-align: center;
        min-width: 50px;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
    }
    
    .event-date-day {
        font-size: 1.25rem;
        font-weight: 700;
        color: #1a1a1a;
        line-height: 1;
    }
    
    .event-date-month {
        font-size: 0.7rem;
        color: #999;
        text-transform: uppercase;
    }
    
    .event-details {
        flex: 1;
    }
    
    .event-title {
        color: #1a1a1a;
        font-weight: 600;
        font-size: 0.85rem;
        margin-bottom: 0.25rem;
    }
    
    .event-time {
        color: #666;
        font-size: 0.75rem;
    }
    
    .add-button {
        background: transparent;
        border: 2px dashed #ddd;
        color: #0066cc;
        padding: 0.5rem 1rem;
        border-radius: 8px;
        font-weight: 600;
        font-size: 0.85rem;
        cursor: pointer;
        transition: all 0.2s ease;
        width: 100%;
        text-align: center;
    }
    
    .add-button:hover {
        border-color: #0066cc;
        background: #f0f7ff;
    }
    
    /* ==================== BUTTONS ==================== */
    .stButton > button {
        background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.625rem 1.5rem;
        font-weight: 600;
        font-size: 0.9rem;
        transition: all 0.3s ease;
        box-shadow: 0 4px 12px rgba(59, 130, 246, 0.3);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 16px rgba(59, 130, 246, 0.4);
    }
    
    .stDownloadButton > button {
        background: linear-gradient(135deg, #22c55e 0%, #16a34a 100%);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.625rem 1.5rem;
        font-weight: 600;
        font-size: 0.9rem;
        transition: all 0.3s ease;
        box-shadow: 0 4px 12px rgba(34, 197, 94, 0.3);
    }
    
    .stDownloadButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 16px rgba(34, 197, 94, 0.4);
    }
    
    /* ==================== FILE UPLOADER ==================== */
    [data-testid="stFileUploader"] {
        background: white;
        border: 2px dashed #d1d5db;
        border-radius: 12px;
        padding: 2rem;
        transition: all 0.3s ease;
    }
    
    [data-testid="stFileUploader"]:hover {
        border-color: #3b82f6;
        background: #f8fafc;
    }
    
    /* ==================== TABLES ==================== */
    .dataframe {
        border: none !important;
        font-size: 0.875rem;
    }
    
    .dataframe thead tr th {
        background: #f8f9fa !important;
        color: #495057 !important;
        font-weight: 600 !important;
        text-transform: uppercase;
        font-size: 0.75rem;
        padding: 1rem 0.75rem !important;
        border-bottom: 2px solid #dee2e6 !important;
        letter-spacing: 0.05em;
    }
    
    .dataframe tbody tr {
        border-bottom: 1px solid #f1f3f5 !important;
        transition: background 0.2s ease;
    }
    
    .dataframe tbody tr:hover {
        background: #f8f9fa !important;
    }
    
    .dataframe tbody td {
        padding: 0.875rem 0.75rem !important;
        color: #495057;
    }
    
    /* ==================== PRIORITY BADGES ==================== */
    .priority-badge {
        display: inline-block;
        padding: 0.375rem 0.875rem;
        border-radius: 20px;
        font-weight: 600;
        font-size: 0.75rem;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    
    .priority-high {
        background: linear-gradient(135deg, #22c55e 0%, #16a34a 100%);
        color: white;
    }
    
    .priority-medium {
        background: linear-gradient(135deg, #fbbf24 0%, #f59e0b 100%);
        color: white;
    }
    
    .priority-low {
        background: linear-gradient(135deg, #f87171 0%, #ef4444 100%);
        color: white;
    }
    
    /* ==================== ALERTS ==================== */
    .alert {
        padding: 1rem 1.25rem;
        border-radius: 10px;
        margin: 1rem 0;
        border-left: 4px solid;
    }
    
    .alert-info {
        background: #eff6ff;
        border-color: #3b82f6;
        color: #1e40af;
    }
    
    .alert-success {
        background: #f0fdf4;
        border-color: #22c55e;
        color: #15803d;
    }
    
    .alert-warning {
        background: #fffbeb;
        border-color: #f59e0b;
        color: #92400e;
    }
    
    /* ==================== TABS ==================== */
    .stTabs [data-baseweb="tab-list"] {
        gap: 0.5rem;
        background: transparent;
        border-bottom: 2px solid #e5e7eb;
    }
    
    .stTabs [data-baseweb="tab"] {
        background: transparent;
        border: none;
        border-bottom: 3px solid transparent;
        border-radius: 0;
        padding: 0.875rem 1.5rem;
        font-weight: 600;
        color: #6b7280;
        transition: all 0.2s ease;
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        color: #3b82f6;
    }
    
    .stTabs [aria-selected="true"] {
        color: #3b82f6 !important;
        border-bottom-color: #3b82f6 !important;
    }
    
    /* ==================== EXPANDER ==================== */
    .streamlit-expanderHeader {
        background: #f8f9fa;
        border: 1px solid #e5e7eb;
        border-radius: 10px;
        font-weight: 600;
        color: #374151;
        padding: 1rem 1.25rem;
        transition: all 0.2s ease;
    }
    
    .streamlit-expanderHeader:hover {
        background: #f1f3f5;
        border-color: #d1d5db;
    }
    
    /* ==================== RESPONSIVE ==================== */
    @media (max-width: 768px) {
        .block-container {
            padding: 1rem;
        }
        
        .top-header {
            flex-direction: column;
            gap: 1rem;
        }
        
        .metric-row {
            grid-template-columns: 1fr;
        }
    }
</style>
""", unsafe_allow_html=True)

# ============================================================================
# MODEL LOADING
# ============================================================================

@st.cache_resource(show_spinner=False)
def load_models():
    """Load ML models and preprocessors"""
    try:
        model = joblib.load('best_model.pkl')
        scaler = joblib.load('scaler.pkl')
        label_encoders = joblib.load('label_encoders.pkl')
        return model, scaler, label_encoders
    except FileNotFoundError as e:
        st.error(f"⚠️ Model files not found: {e}")
        st.info("Please ensure 'best_model.pkl', 'scaler.pkl', and 'label_encoders.pkl' are in the same directory")
        st.stop()
    except Exception as e:
        st.error(f"⚠️ Error loading models: {e}")
        st.stop()

# ============================================================================
# PREDICTION FUNCTION
# ============================================================================
def process_and_predict(df, best_model, scaler, label_encoders):
    """Process data and generate predictions with unknown category handling"""
    
    expected_cols = list(label_encoders.keys())
    missing_cols = [col for col in expected_cols if col not in df.columns]
    
    if missing_cols:
        return None, f"Missing required columns: {missing_cols}"
    
    df_processed = df.copy()
    
    if 'Converted' in df_processed.columns:
        df_processed = df_processed.drop(columns=['Converted'])
    
    try:
        # Encode categorical columns with unknown category handling
        for col in expected_cols:
            if col in df_processed.columns:
                # Get the encoder for this column
                encoder = label_encoders[col]
                
                # Convert to string
                col_values = df_processed[col].astype(str)
                
                # Handle unknown categories
                known_categories = set(encoder.classes_)
                
                # Replace unknown categories with the most common category from training
                # (which is typically at index 0 after fitting)
                default_category = encoder.classes_[0]
                
                # Map unknown values to default
                col_values = col_values.apply(
                    lambda x: x if x in known_categories else default_category
                )
                
                # Now transform
                df_processed[col] = encoder.transform(col_values)
        
        # Scale features
        features_scaled = scaler.transform(df_processed)
        
        # Generate predictions
        scores = best_model.predict_proba(features_scaled)[:, 1]
        predictions = best_model.predict(features_scaled)
        
        # Add results to original dataframe
        df['Lead_Score'] = scores
        df['Lead_Score_%'] = (scores * 100).round(2)
        df['Priority'] = pd.cut(
            scores,
            bins=[0, 0.4, 0.7, 1.0],
            labels=['Low', 'Medium', 'High']
        )
        df['Prediction'] = ['Likely to Convert' if p == 1 else 'Unlikely' for p in predictions]
        
        # Sort by score
        df_sorted = df.sort_values(by='Lead_Score', ascending=False).reset_index(drop=True)
        
        return df_sorted, None
        
    except Exception as e:
        return None, str(e)


# ============================================================================
# SIDEBAR
# ============================================================================

with st.sidebar:
    # Sidebar Header
    st.markdown("""
    <div class="sidebar-header">
        <div class="sidebar-logo">🎓</div>
        <div class="sidebar-brand">Lead Scorer</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown('<div class="nav-section-title">MAIN MENU</div>', unsafe_allow_html=True)
    
    # Navigation
    page = st.radio(
        "",
        ["📊 Dashboard", "📖 User Guide", "ℹ️ About"],
        label_visibility="collapsed"
    )
    
    st.markdown("---")
    
    # System Status
    st.markdown("""
    <div style='padding: 1rem; background: rgba(255, 255, 255, 0.05); border-radius: 8px; margin: 1rem 0;'>
        <div style='color: rgba(255, 255, 255, 0.6); font-size: 0.75rem; margin-bottom: 0.5rem;'>SYSTEM STATUS</div>
        <div style='color: #4ade80; font-weight: 600; display: flex; align-items: center; gap: 0.5rem;'>
            <span style='width: 8px; height: 8px; background: #4ade80; border-radius: 50%; display: inline-block;'></span>
            Online & Active
        </div>
    </div>
    
    <div style='padding: 1rem; background: rgba(255, 255, 255, 0.05); border-radius: 8px;'>
        <div style='color: rgba(255, 255, 255, 0.6); font-size: 0.75rem; margin-bottom: 0.5rem;'>MODEL VERSION</div>
        <div style='color: white; font-weight: 600;'>AI v2.0 (Latest)</div>
    </div>
    """, unsafe_allow_html=True)

# ============================================================================
# LOAD MODELS
# ============================================================================

with st.spinner("🔄 Loading AI models..."):
    best_model, scaler, label_encoders = load_models()

# ============================================================================
# MAIN CONTENT - DASHBOARD
# ============================================================================

if page == "📊 Dashboard":
    
    # Top Header
    st.markdown("""
    <div class="top-header">
        <div>
            <div class="header-title">Student Lead Scoring Dashboard</div>
            <div style='color: #666; font-size: 0.9rem; margin-top: 0.25rem;'>AI-Powered Conversion Prediction Platform</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Main Content Area
    col_main, col_sidebar = st.columns([3, 1])
    
    with col_main:
        # File Upload Section
        st.markdown('<div class="content-card">', unsafe_allow_html=True)
        st.markdown('<div class="card-title">📁 Upload Student Data</div>', unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)
        
        col1, col2 = st.columns([3, 1])
        
        with col1:
            uploaded_file = st.file_uploader(
                "Upload your CSV file containing student lead information",
                type=["csv"],
                help="Select a CSV file with student lead data",
                label_visibility="collapsed"
            )
        
        with col2:
            # Sample data download
            sample_data = pd.DataFrame({
                'Email_Source': ['Google', 'Facebook', 'Direct', 'Referral', 'LinkedIn'],
                'Contacted': ['Yes', 'No', 'Yes', 'No', 'Yes'],
                'Location': ['Mumbai', 'Delhi', 'Bangalore', 'Chennai', 'Pune'],
                'Profession': ['Student', 'Working Professional', 'Unemployed', 'Freelancer', 'Student'],
                'Course_Interest': ['Data Science', 'Web Development', 'AI/ML', 'Digital Marketing', 'Cloud Computing']
            })
            csv_sample = sample_data.to_csv(index=False).encode('utf-8')
            st.download_button(
                "📥 Sample Template",
                csv_sample,
                "sample_template.csv",
                "text/csv",
                use_container_width=True
            )
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Process uploaded file
        if uploaded_file is not None:
            try:
                new_leads = pd.read_csv(uploaded_file)
                
                # Metrics Row
                st.markdown('<div class="metric-row">', unsafe_allow_html=True)
                
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    st.markdown(f"""
                    <div class="metric-card">
                        <div class="metric-header">
                            <div class="metric-label">Total Leads<br>Uploaded</div>
                            <div class="metric-icon icon-purple">📋</div>
                        </div>
                        <div class="metric-value">{len(new_leads):,}</div>
                        <div class="metric-footer">Ready for analysis</div>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col2:
                    st.markdown(f"""
                    <div class="metric-card">
                        <div class="metric-header">
                            <div class="metric-label">Data<br>Columns</div>
                            <div class="metric-icon icon-blue">📁</div>
                        </div>
                        <div class="metric-value">{len(new_leads.columns)}</div>
                        <div class="metric-footer">Attributes detected</div>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col3:
                    st.markdown("""
                    <div class="metric-card">
                        <div class="metric-header">
                            <div class="metric-label">System<br>Status</div>
                            <div class="metric-icon icon-green">✓</div>
                        </div>
                        <div class="metric-value">Ready</div>
                        <div class="metric-footer">AI model loaded</div>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col4:
                    st.markdown("""
                    <div class="metric-card">
                        <div class="metric-header">
                            <div class="metric-label">Processing<br>Speed</div>
                            <div class="metric-icon icon-orange">⚡</div>
                        </div>
                        <div class="metric-value">5-10s</div>
                        <div class="metric-footer">Estimated time</div>
                    </div>
                    """, unsafe_allow_html=True)
                
                st.markdown('</div>', unsafe_allow_html=True)
                
                # Data Preview
                with st.expander("👁️ Preview Uploaded Data", expanded=False):
                    st.dataframe(new_leads.head(10), use_container_width=True, height=300)
                
                # Processing
                with st.spinner("⚙️ AI is analyzing your data..."):
                    result_df, error = process_and_predict(new_leads, best_model, scaler, label_encoders)
                
                if error:
                    st.error(f"❌ Error: {error}")
                    st.stop()
                
                st.success("✅ Analysis Complete!")
                
                st.markdown("<br>", unsafe_allow_html=True)
                
                # Results Metrics
                high_score = (result_df['Lead_Score'] > 0.7).sum()
                medium_score = ((result_df['Lead_Score'] > 0.4) & (result_df['Lead_Score'] <= 0.7)).sum()
                low_score = (result_df['Lead_Score'] <= 0.4).sum()
                avg_score = result_df['Lead_Score_%'].mean()
                
                st.markdown("### 🎯 Prediction Results")
                
                st.markdown('<div class="metric-row">', unsafe_allow_html=True)
                
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    st.markdown(f"""
                    <div class="metric-card">
                        <div class="metric-header">
                            <div class="metric-label">High Priority<br>Leads</div>
                            <div class="metric-icon icon-green">🎯</div>
                        </div>
                        <div class="metric-value">{high_score}</div>
                        <div class="metric-footer" style='color: #22c55e;'>↑ {round(high_score/len(result_df)*100, 1)}% of total</div>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col2:
                    st.markdown(f"""
                    <div class="metric-card">
                        <div class="metric-header">
                            <div class="metric-label">Medium Priority<br>Leads</div>
                            <div class="metric-icon icon-yellow">⚠️</div>
                        </div>
                        <div class="metric-value">{medium_score}</div>
                        <div class="metric-footer">{round(medium_score/len(result_df)*100, 1)}% of total</div>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col3:
                    st.markdown(f"""
                    <div class="metric-card">
                        <div class="metric-header">
                            <div class="metric-label">Low Priority<br>Leads</div>
                            <div class="metric-icon icon-red">📉</div>
                        </div>
                        <div class="metric-value">{low_score}</div>
                        <div class="metric-footer" style='color: #ef4444;'>↓ {round(low_score/len(result_df)*100, 1)}% of total</div>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col4:
                    st.markdown(f"""
                    <div class="metric-card">
                        <div class="metric-header">
                            <div class="metric-label">Average<br>Score</div>
                            <div class="metric-icon icon-teal">📊</div>
                        </div>
                        <div class="metric-value">{avg_score:.1f}%</div>
                        <div class="metric-footer">Overall quality</div>
                    </div>
                    """, unsafe_allow_html=True)
                
                st.markdown('</div>', unsafe_allow_html=True)
                
                st.markdown("<br>", unsafe_allow_html=True)
                
                # Visualizations
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown('<div class="content-card">', unsafe_allow_html=True)
                    st.markdown('<div class="card-title">📊 Score Distribution</div>', unsafe_allow_html=True)
                    
                    fig = px.histogram(
                        result_df,
                        x='Lead_Score_%',
                        nbins=20,
                        color_discrete_sequence=['#3b82f6']
                    )
                    fig.update_layout(
                        showlegend=False,
                        height=350,
                        margin=dict(l=0, r=0, t=20, b=0),
                        paper_bgcolor='white',
                        plot_bgcolor='#f8f9fa',
                        font=dict(family="Poppins", size=12),
                        xaxis_title="Conversion Score (%)",
                        yaxis_title="Number of Leads"
                    )
                    st.plotly_chart(fig, use_container_width=True)
                    st.markdown('</div>', unsafe_allow_html=True)
                
                with col2:
                    st.markdown('<div class="content-card">', unsafe_allow_html=True)
                    st.markdown('<div class="card-title">🎯 Priority Breakdown</div>', unsafe_allow_html=True)
                    
                    priority_counts = result_df['Priority'].value_counts()
                    colors = {'High': '#22c55e', 'Medium': '#fbbf24', 'Low': '#ef4444'}
                    
                    fig = go.Figure(data=[go.Pie(
                        labels=priority_counts.index,
                        values=priority_counts.values,
                        hole=.6,
                        marker_colors=[colors[label] for label in priority_counts.index],
                        textinfo='label+percent',
                        textfont=dict(size=14, family="Poppins", color="white", weight=600),
                        hovertemplate='<b>%{label}</b><br>Count: %{value}<br>Percentage: %{percent}<extra></extra>'
                    )])
                    
                    fig.update_layout(
                        height=350,
                        margin=dict(l=0, r=0, t=20, b=0),
                        paper_bgcolor='white',
                        font=dict(family="Poppins", size=12),
                        showlegend=True,
                        legend=dict(
                            orientation="h",
                            yanchor="bottom",
                            y=-0.1,
                            xanchor="center",
                            x=0.5
                        )
                    )
                    st.plotly_chart(fig, use_container_width=True)
                    st.markdown('</div>', unsafe_allow_html=True)
                
                # Results Table
                st.markdown('<div class="content-card">', unsafe_allow_html=True)
                st.markdown('<div class="card-title">📋 Detailed Lead Scores</div>', unsafe_allow_html=True)
                st.markdown("<br>", unsafe_allow_html=True)
                
                # Style the dataframe - FIXED: Using 'map' instead of 'applymap'
                display_df = result_df.copy()
                
                def style_priority(val):
                    if val == 'High':
                        return 'background-color: #d1fae5; color: #065f46; font-weight: 600'
                    elif val == 'Medium':
                        return 'background-color: #fef3c7; color: #92400e; font-weight: 600'
                    else:
                        return 'background-color: #fee2e2; color: #991b1b; font-weight: 600'
                
                # FIXED: Use 'map' instead of 'applymap' for pandas >= 2.1.0
                styled_df = display_df.style.map(style_priority, subset=['Priority'])
                
                st.dataframe(styled_df, use_container_width=True, height=400)
                st.markdown('</div>', unsafe_allow_html=True)
                
                # Export Section
                st.markdown('<div class="content-card">', unsafe_allow_html=True)
                st.markdown('<div class="card-title">💾 Export Results</div>', unsafe_allow_html=True)
                st.markdown("<br>", unsafe_allow_html=True)
                
                col1, col2, col3 = st.columns([1, 2, 1])
                
                with col2:
                    csv = result_df.to_csv(index=False).encode('utf-8')
                    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                    st.download_button(
                        "📥 Download Complete Report (CSV)",
                        csv,
                        f"Lead_Scoring_Report_{timestamp}.csv",
                        "text/csv",
                        use_container_width=True
                    )
                
                st.markdown('</div>', unsafe_allow_html=True)
                
                # Top Leads
                st.markdown('<div class="content-card">', unsafe_allow_html=True)
                st.markdown('<div class="card-title">🏆 Top 10 High-Priority Leads</div>', unsafe_allow_html=True)
                st.markdown("<br>", unsafe_allow_html=True)
                
                top_leads = result_df.head(10)
                st.dataframe(top_leads, use_container_width=True, height=400)
                st.markdown('</div>', unsafe_allow_html=True)
                
            except Exception as e:
                st.error(f"❌ Error processing file: {str(e)}")
                with st.expander("🔍 Debug Information"):
                    st.code(str(e))
        
        else:
            # Welcome message
            st.markdown("""
            <div class="alert alert-info">
                <h3 style='margin-top: 0;'>👋 Welcome to Student Lead Scoring Pro</h3>
                <p style='margin-bottom: 0;'>
                    Upload your student lead data in CSV format to get instant AI-powered conversion predictions.
                    Our advanced machine learning model will analyze each lead and provide priority scores.
                </p>
            </div>
            """, unsafe_allow_html=True)
            
            # Features
            st.markdown("### ✨ Key Features")
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.markdown("""
                <div class="content-card" style='text-align: center;'>
                    <div style='font-size: 3rem; margin-bottom: 1rem;'>🤖</div>
                    <h4 style='color: #1a1a1a;'>AI-Powered</h4>
                    <p style='color: #666; font-size: 0.9rem;'>
                        Advanced ML algorithms trained on real conversion data
                    </p>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                st.markdown("""
                <div class="content-card" style='text-align: center;'>
                    <div style='font-size: 3rem; margin-bottom: 1rem;'>⚡</div>
                    <h4 style='color: #1a1a1a;'>Instant Results</h4>
                    <p style='color: #666; font-size: 0.9rem;'>
                        Get predictions in seconds with real-time analysis
                    </p>
                </div>
                """, unsafe_allow_html=True)
            
            with col3:
                st.markdown("""
                <div class="content-card" style='text-align: center;'>
                    <div style='font-size: 3rem; margin-bottom: 1rem;'>📊</div>
                    <h4 style='color: #1a1a1a;'>Visual Insights</h4>
                    <p style='color: #666; font-size: 0.9rem;'>
                        Interactive charts and detailed analytics dashboard
                    </p>
                </div>
                """, unsafe_allow_html=True)
    
    # Right Sidebar - Notice Board & Events
    with col_sidebar:
        # Notice Board
        st.markdown('<div class="sidebar-panel">', unsafe_allow_html=True)
        st.markdown('<div class="panel-header">📌 System Updates</div>', unsafe_allow_html=True)
        
        st.markdown("""
        <div class="notice-item">
            <div class="notice-title">AI Model Updated</div>
            <div class="notice-time">Today, 10:30 AM</div>
        </div>
        
        <div class="notice-item">
            <div class="notice-title">New Features Added</div>
            <div class="notice-time">Yesterday, 3:45 PM</div>
        </div>
        
        <div class="notice-item">
            <div class="notice-title">Performance Optimized</div>
            <div class="notice-time">2 days ago</div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown('<div class="add-button">+ Add Update</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Upcoming Events
        st.markdown('<div class="sidebar-panel">', unsafe_allow_html=True)
        st.markdown('<div class="panel-header">📅 Quick Actions</div>', unsafe_allow_html=True)
        
        st.markdown("""
        <div class="event-item">
            <div class="event-date">
                <div class="event-date-day">15</div>
                <div class="event-date-month">Apr</div>
            </div>
            <div class="event-details">
                <div class="event-title">Export Analytics</div>
                <div class="event-time">📊 Download reports</div>
            </div>
        </div>
        
        <div class="event-item">
            <div class="event-date">
                <div class="event-date-day">20</div>
                <div class="event-date-month">Apr</div>
            </div>
            <div class="event-details">
                <div class="event-title">Model Training</div>
                <div class="event-time">🤖 Update AI model</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown('<div class="add-button">+ Add Action</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

# ============================================================================
# USER GUIDE PAGE
# ============================================================================

elif page == "📖 User Guide":
    
    st.markdown("""
    <div class="top-header">
        <div>
            <div class="header-title">User Guide</div>
            <div style='color: #666; font-size: 0.9rem; margin-top: 0.25rem;'>Step-by-step instructions for using the platform</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="alert alert-success">
        <h3 style='margin-top: 0;'>👋 Welcome!</h3>
        <p style='margin-bottom: 0;'>
            This guide will help you understand how to use the Student Lead Scoring Platform effectively.
            Follow the simple steps below to get predictions for your student leads.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("### 📥 Step 1: Prepare Your Data")
    
    st.markdown("""
    <div class="content-card">
        <h4>Required CSV Columns:</h4>
        <ul style='line-height: 2;'>
            <li><code>Email_Source</code> - Lead source (Google, Facebook, etc.)</li>
            <li><code>Contacted</code> - Whether contacted (Yes/No)</li>
            <li><code>Location</code> - Student's city</li>
            <li><code>Profession</code> - Occupation type</li>
            <li><code>Course_Interest</code> - Interested course</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("### 📤 Step 2: Upload Your File")
    st.markdown("### 🤖 Step 3: AI Processing")
    st.markdown("### 📊 Step 4: View Results")
    st.markdown("### 💾 Step 5: Export Data")

# ============================================================================
# ABOUT PAGE
# ============================================================================

elif page == "ℹ️ About":
    
    st.markdown("""
    <div class="top-header">
        <div>
            <div class="header-title">About This Platform</div>
            <div style='color: #666; font-size: 0.9rem; margin-top: 0.25rem;'>Learn more about Student Lead Scoring Intelligence</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="content-card">
        <h3>🎓 What is Student Lead Scoring?</h3>
        <p style='line-height: 1.8; color: #495057;'>
            Student Lead Scoring is an AI-powered system that helps educational institutions predict which
            prospective students are most likely to enroll. Our machine learning model assigns probability
            scores to help you focus recruitment efforts effectively.
        </p>
    </div>
    """, unsafe_allow_html=True)

# ============================================================================
# FOOTER
# ============================================================================

st.markdown("---")
st.markdown("""
<div style='background: white; padding: 1.5rem; border-radius: 12px; text-align: center; box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);'>
    <div style='color: #1a1a1a; font-weight: 700; font-size: 1.1rem; margin-bottom: 0.5rem;'>
        🎓 Student Lead Scoring Intelligence Platform
    </div>
    <div style='color: #666; font-size: 0.9rem;'>
        Powered by Machine Learning • Built with Streamlit & Python
    </div>
    <div style='color: #999; font-size: 0.85rem; margin-top: 0.75rem;'>
        © 2024 AI-Powered Student Analytics • Version 2.0
    </div>
</div>
""", unsafe_allow_html=True)
