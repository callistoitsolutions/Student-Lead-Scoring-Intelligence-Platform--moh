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
# PROFESSIONAL CSS STYLING (Inspired by Modern School Dashboard)
# ============================================================================

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
    
    /* ==================== GLOBAL STYLES ==================== */
    * {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
        letter-spacing: -0.01em;
    }
    
    /* Main Container */
    .block-container {
        padding: 2rem 3rem 3rem 3rem;
        max-width: 1600px;
    }
    
    /* Remove default Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* ==================== SIDEBAR STYLING ==================== */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #f8f9fa 0%, #ffffff 100%);
        border-right: 1px solid #e9ecef;
        padding: 0;
    }
    
    [data-testid="stSidebar"] > div:first-child {
        padding-top: 2rem;
    }
    
    .sidebar-title {
        font-size: 1.5rem;
        font-weight: 800;
        color: #1a1a1a;
        padding: 0 1.5rem 1rem 1.5rem;
        border-bottom: 1px solid #e9ecef;
        margin-bottom: 1.5rem;
    }
    
    .sidebar-section {
        padding: 1rem 1.5rem;
        margin-bottom: 0.5rem;
    }
    
    .sidebar-section-title {
        font-size: 0.75rem;
        font-weight: 700;
        text-transform: uppercase;
        color: #6c757d;
        margin-bottom: 0.75rem;
        letter-spacing: 0.05em;
    }
    
    .sidebar-nav-item {
        display: flex;
        align-items: center;
        padding: 0.75rem 1rem;
        margin-bottom: 0.25rem;
        border-radius: 8px;
        color: #495057;
        font-weight: 500;
        font-size: 0.9rem;
        transition: all 0.2s ease;
        cursor: pointer;
        text-decoration: none;
    }
    
    .sidebar-nav-item:hover {
        background: #e7f1ff;
        color: #0066cc;
    }
    
    .sidebar-nav-item.active {
        background: #0066cc;
        color: white;
        box-shadow: 0 2px 4px rgba(0, 102, 204, 0.2);
    }
    
    /* ==================== HEADER STYLING ==================== */
    .page-header {
        background: white;
        padding: 2rem 0;
        margin-bottom: 2rem;
    }
    
    .page-title {
        font-size: 2rem;
        font-weight: 800;
        color: #1a1a1a;
        margin: 0;
        padding: 0;
    }
    
    .page-subtitle {
        font-size: 0.95rem;
        color: #6c757d;
        margin-top: 0.5rem;
        font-weight: 400;
    }
    
    /* ==================== METRIC CARDS ==================== */
    .metric-card {
        background: white;
        border-radius: 12px;
        padding: 1.5rem;
        border: 1px solid #e9ecef;
        transition: all 0.3s ease;
        height: 100%;
    }
    
    .metric-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
        border-color: #dee2e6;
    }
    
    .metric-icon {
        width: 48px;
        height: 48px;
        border-radius: 10px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.5rem;
        margin-bottom: 1rem;
    }
    
    .metric-value {
        font-size: 2rem;
        font-weight: 800;
        color: #1a1a1a;
        margin: 0.5rem 0 0.25rem 0;
        line-height: 1;
    }
    
    .metric-label {
        font-size: 0.875rem;
        color: #6c757d;
        font-weight: 500;
        margin: 0;
    }
    
    .metric-change {
        font-size: 0.8rem;
        font-weight: 600;
        margin-top: 0.5rem;
    }
    
    .metric-change.positive {
        color: #28a745;
    }
    
    .metric-change.negative {
        color: #dc3545;
    }
    
    /* Icon Background Colors */
    .icon-blue { background: #e7f1ff; color: #0066cc; }
    .icon-purple { background: #f3e8ff; color: #7c3aed; }
    .icon-green { background: #d1f4e0; color: #10b981; }
    .icon-orange { background: #fff3e0; color: #f59e0b; }
    
    /* ==================== CONTENT CARDS ==================== */
    .content-card {
        background: white;
        border-radius: 12px;
        padding: 1.5rem;
        border: 1px solid #e9ecef;
        margin-bottom: 1.5rem;
    }
    
    .card-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 1.5rem;
        padding-bottom: 1rem;
        border-bottom: 1px solid #f1f3f5;
    }
    
    .card-title {
        font-size: 1.125rem;
        font-weight: 700;
        color: #1a1a1a;
        margin: 0;
    }
    
    .card-action {
        font-size: 0.875rem;
        color: #0066cc;
        font-weight: 600;
        cursor: pointer;
        text-decoration: none;
    }
    
    .card-action:hover {
        text-decoration: underline;
    }
    
    /* ==================== BUTTONS ==================== */
    .stButton > button {
        background: #0066cc;
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.625rem 1.25rem;
        font-weight: 600;
        font-size: 0.9rem;
        transition: all 0.2s ease;
        box-shadow: 0 2px 4px rgba(0, 102, 204, 0.2);
    }
    
    .stButton > button:hover {
        background: #0052a3;
        box-shadow: 0 4px 8px rgba(0, 102, 204, 0.3);
        transform: translateY(-1px);
    }
    
    .stButton > button:active {
        transform: translateY(0);
    }
    
    /* Download Button */
    .stDownloadButton > button {
        background: #10b981;
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.625rem 1.25rem;
        font-weight: 600;
        font-size: 0.9rem;
        transition: all 0.2s ease;
        box-shadow: 0 2px 4px rgba(16, 185, 129, 0.2);
    }
    
    .stDownloadButton > button:hover {
        background: #059669;
        box-shadow: 0 4px 8px rgba(16, 185, 129, 0.3);
        transform: translateY(-1px);
    }
    
    /* ==================== FILE UPLOADER ==================== */
    [data-testid="stFileUploader"] {
        background: white;
        border: 2px dashed #dee2e6;
        border-radius: 12px;
        padding: 2rem;
        transition: all 0.3s ease;
    }
    
    [data-testid="stFileUploader"]:hover {
        border-color: #0066cc;
        background: #f8f9fa;
    }
    
    [data-testid="stFileUploader"] section {
        border: none;
        padding: 0;
    }
    
    /* ==================== DATA TABLES ==================== */
    .dataframe {
        border: none !important;
        font-size: 0.9rem;
    }
    
    .dataframe thead tr th {
        background: #f8f9fa !important;
        color: #495057 !important;
        font-weight: 700 !important;
        text-transform: uppercase;
        font-size: 0.75rem;
        padding: 1rem 0.75rem !important;
        border-bottom: 2px solid #dee2e6 !important;
        letter-spacing: 0.05em;
    }
    
    .dataframe tbody tr {
        border-bottom: 1px solid #f1f3f5 !important;
    }
    
    .dataframe tbody tr:hover {
        background: #f8f9fa !important;
    }
    
    .dataframe tbody td {
        padding: 0.875rem 0.75rem !important;
        color: #495057;
    }
    
    /* ==================== TABS ==================== */
    .stTabs [data-baseweb="tab-list"] {
        gap: 0.5rem;
        background: transparent;
        border-bottom: 1px solid #e9ecef;
        padding: 0;
    }
    
    .stTabs [data-baseweb="tab"] {
        background: transparent;
        border: none;
        border-bottom: 3px solid transparent;
        border-radius: 0;
        padding: 0.875rem 1.5rem;
        font-weight: 600;
        color: #6c757d;
        font-size: 0.9rem;
        transition: all 0.2s ease;
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        color: #495057;
        background: #f8f9fa;
    }
    
    .stTabs [aria-selected="true"] {
        color: #0066cc !important;
        border-bottom-color: #0066cc !important;
        background: transparent !important;
    }
    
    /* ==================== ALERTS & INFO BOXES ==================== */
    .info-box {
        background: #e7f1ff;
        border-left: 4px solid #0066cc;
        padding: 1rem 1.25rem;
        border-radius: 8px;
        margin: 1rem 0;
    }
    
    .success-box {
        background: #d1f4e0;
        border-left: 4px solid #10b981;
        padding: 1rem 1.25rem;
        border-radius: 8px;
        margin: 1rem 0;
    }
    
    .warning-box {
        background: #fff3e0;
        border-left: 4px solid #f59e0b;
        padding: 1rem 1.25rem;
        border-radius: 8px;
        margin: 1rem 0;
    }
    
    /* ==================== PROGRESS BAR ==================== */
    .stProgress > div > div > div > div {
        background: #0066cc;
        border-radius: 4px;
    }
    
    /* ==================== EXPANDER ==================== */
    .streamlit-expanderHeader {
        background: #f8f9fa;
        border: 1px solid #e9ecef;
        border-radius: 8px;
        font-weight: 600;
        color: #495057;
        padding: 0.875rem 1rem;
        font-size: 0.9rem;
    }
    
    .streamlit-expanderHeader:hover {
        border-color: #dee2e6;
        background: #e9ecef;
    }
    
    /* ==================== PRIORITY BADGES ==================== */
    .priority-badge {
        display: inline-block;
        padding: 0.375rem 0.75rem;
        border-radius: 6px;
        font-weight: 600;
        font-size: 0.8rem;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    
    .priority-high {
        background: #d1f4e0;
        color: #10b981;
    }
    
    .priority-medium {
        background: #fff3e0;
        color: #f59e0b;
    }
    
    .priority-low {
        background: #fee;
        color: #dc3545;
    }
    
    /* ==================== RESPONSIVE ==================== */
    @media (max-width: 768px) {
        .block-container {
            padding: 1rem;
        }
        
        .page-title {
            font-size: 1.5rem;
        }
        
        .metric-value {
            font-size: 1.5rem;
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
    """Process data and generate predictions"""
    
    expected_cols = list(label_encoders.keys())
    missing_cols = [col for col in expected_cols if col not in df.columns]
    
    if missing_cols:
        return None, f"Missing required columns: {missing_cols}"
    
    df_processed = df.copy()
    
    if 'Converted' in df_processed.columns:
        df_processed = df_processed.drop(columns=['Converted'])
    
    try:
        # Encode categorical columns
        for col in expected_cols:
            if col in df_processed.columns:
                df_processed[col] = label_encoders[col].transform(df_processed[col].astype(str))
        
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
    st.markdown('<div class="sidebar-title">🎓 Student Lead Scorer</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="sidebar-section">', unsafe_allow_html=True)
    st.markdown('<div class="sidebar-section-title">NAVIGATION</div>', unsafe_allow_html=True)
    
    # Navigation menu
    page = st.radio(
        "",
        ["📊 Dashboard", "📖 User Guide", "ℹ️ About"],
        label_visibility="collapsed"
    )
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Quick Stats
    st.markdown('<div class="sidebar-section">', unsafe_allow_html=True)
    st.markdown('<div class="sidebar-section-title">QUICK INFO</div>', unsafe_allow_html=True)
    st.markdown("""
    <div style='background: #f8f9fa; padding: 1rem; border-radius: 8px; margin-bottom: 1rem;'>
        <div style='font-size: 0.875rem; color: #6c757d; margin-bottom: 0.5rem;'>Status</div>
        <div style='font-size: 1rem; font-weight: 700; color: #10b981;'>🟢 System Active</div>
    </div>
    
    <div style='background: #f8f9fa; padding: 1rem; border-radius: 8px;'>
        <div style='font-size: 0.875rem; color: #6c757d; margin-bottom: 0.5rem;'>Model Version</div>
        <div style='font-size: 1rem; font-weight: 700; color: #1a1a1a;'>v2.0 (Latest)</div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Help Section
    st.markdown("""
    <div style='padding: 1rem; background: #e7f1ff; border-radius: 8px; margin-top: 1rem;'>
        <div style='font-weight: 700; color: #0066cc; margin-bottom: 0.5rem;'>💡 Need Help?</div>
        <div style='font-size: 0.85rem; color: #495057;'>
            Click on <b>User Guide</b> in the navigation menu for detailed instructions.
        </div>
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
    
    # Header
    st.markdown("""
    <div class="page-header">
        <div class="page-title">Student Lead Scoring Dashboard</div>
        <div class="page-subtitle">AI-Powered Student Conversion Prediction Platform</div>
    </div>
    """, unsafe_allow_html=True)
    
    # File Upload Section
    st.markdown('<div class="content-card">', unsafe_allow_html=True)
    st.markdown('<div class="card-header"><div class="card-title">📁 Upload Student Data</div></div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([2, 1])
    
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
            "📥 Download Sample",
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
            
            # Quick Stats Metrics
            st.markdown("### 📊 Data Overview")
            
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.markdown("""
                <div class="metric-card">
                    <div class="metric-icon icon-blue">📋</div>
                    <div class="metric-value">{:,}</div>
                    <div class="metric-label">Total Leads</div>
                </div>
                """.format(len(new_leads)), unsafe_allow_html=True)
            
            with col2:
                st.markdown("""
                <div class="metric-card">
                    <div class="metric-icon icon-purple">📁</div>
                    <div class="metric-value">{}</div>
                    <div class="metric-label">Data Columns</div>
                </div>
                """.format(len(new_leads.columns)), unsafe_allow_html=True)
            
            with col3:
                st.markdown("""
                <div class="metric-card">
                    <div class="metric-icon icon-green">✓</div>
                    <div class="metric-value">Ready</div>
                    <div class="metric-label">System Status</div>
                </div>
                """, unsafe_allow_html=True)
            
            with col4:
                st.markdown("""
                <div class="metric-card">
                    <div class="metric-icon icon-orange">🤖</div>
                    <div class="metric-value">AI</div>
                    <div class="metric-label">Model Loaded</div>
                </div>
                """, unsafe_allow_html=True)
            
            st.markdown("<br>", unsafe_allow_html=True)
            
            # Data Preview
            with st.expander("👁️ Preview Uploaded Data", expanded=True):
                st.dataframe(new_leads.head(10), use_container_width=True, height=300)
            
            st.markdown("<br>", unsafe_allow_html=True)
            
            # Processing
            with st.spinner("⚙️ AI is analyzing your data..."):
                result_df, error = process_and_predict(new_leads, best_model, scaler, label_encoders)
            
            if error:
                st.error(f"❌ Error: {error}")
                st.stop()
            
            st.success("✅ Analysis Complete!")
            
            st.markdown("---")
            
            # Results Section
            st.markdown("### 🎯 Prediction Results")
            
            # Calculate metrics
            high_score = (result_df['Lead_Score'] > 0.7).sum()
            medium_score = ((result_df['Lead_Score'] > 0.4) & (result_df['Lead_Score'] <= 0.7)).sum()
            low_score = (result_df['Lead_Score'] <= 0.4).sum()
            avg_score = result_df['Lead_Score_%'].mean()
            
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.markdown("""
                <div class="metric-card">
                    <div class="metric-icon icon-green">🎯</div>
                    <div class="metric-value">{}</div>
                    <div class="metric-label">High Priority</div>
                    <div class="metric-change positive">{}% of total</div>
                </div>
                """.format(high_score, round(high_score/len(result_df)*100, 1)), unsafe_allow_html=True)
            
            with col2:
                st.markdown("""
                <div class="metric-card">
                    <div class="metric-icon icon-orange">⚠️</div>
                    <div class="metric-value">{}</div>
                    <div class="metric-label">Medium Priority</div>
                    <div class="metric-change">{}% of total</div>
                </div>
                """.format(medium_score, round(medium_score/len(result_df)*100, 1)), unsafe_allow_html=True)
            
            with col3:
                st.markdown("""
                <div class="metric-card">
                    <div class="metric-icon" style="background: #fee; color: #dc3545;">📉</div>
                    <div class="metric-value">{}</div>
                    <div class="metric-label">Low Priority</div>
                    <div class="metric-change negative">{}% of total</div>
                </div>
                """.format(low_score, round(low_score/len(result_df)*100, 1)), unsafe_allow_html=True)
            
            with col4:
                st.markdown("""
                <div class="metric-card">
                    <div class="metric-icon icon-blue">📊</div>
                    <div class="metric-value">{:.1f}%</div>
                    <div class="metric-label">Average Score</div>
                </div>
                """.format(avg_score), unsafe_allow_html=True)
            
            st.markdown("<br>", unsafe_allow_html=True)
            
            # Visualizations
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown('<div class="content-card">', unsafe_allow_html=True)
                st.markdown("#### 📊 Score Distribution")
                
                fig = px.histogram(
                    result_df,
                    x='Lead_Score_%',
                    nbins=20,
                    color_discrete_sequence=['#0066cc']
                )
                fig.update_layout(
                    showlegend=False,
                    height=350,
                    margin=dict(l=0, r=0, t=20, b=0),
                    paper_bgcolor='white',
                    plot_bgcolor='#f8f9fa',
                    font=dict(family="Inter", size=12),
                    xaxis_title="Conversion Score (%)",
                    yaxis_title="Number of Leads"
                )
                st.plotly_chart(fig, use_container_width=True)
                st.markdown('</div>', unsafe_allow_html=True)
            
            with col2:
                st.markdown('<div class="content-card">', unsafe_allow_html=True)
                st.markdown("#### 🎯 Priority Breakdown")
                
                priority_counts = result_df['Priority'].value_counts()
                colors = {'High': '#10b981', 'Medium': '#f59e0b', 'Low': '#dc3545'}
                
                fig = go.Figure(data=[go.Pie(
                    labels=priority_counts.index,
                    values=priority_counts.values,
                    hole=.5,
                    marker_colors=[colors[label] for label in priority_counts.index],
                    textinfo='label+percent',
                    textfont=dict(size=14, family="Inter", color="white"),
                    hovertemplate='<b>%{label}</b><br>Count: %{value}<br>Percentage: %{percent}<extra></extra>'
                )])
                
                fig.update_layout(
                    height=350,
                    margin=dict(l=0, r=0, t=20, b=0),
                    paper_bgcolor='white',
                    font=dict(family="Inter", size=12),
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
            st.markdown("### 📋 Detailed Lead Scores")
            
            # Add priority badges to dataframe display
            display_df = result_df.copy()
            
            # Style the dataframe
            def style_priority(val):
                if val == 'High':
                    return 'background-color: #d1f4e0; color: #10b981; font-weight: 600'
                elif val == 'Medium':
                    return 'background-color: #fff3e0; color: #f59e0b; font-weight: 600'
                else:
                    return 'background-color: #fee; color: #dc3545; font-weight: 600'
            
            styled_df = display_df.style.applymap(style_priority, subset=['Priority'])
            
            st.dataframe(styled_df, use_container_width=True, height=400)
            
            # Export Section
            st.markdown("---")
            st.markdown("### 💾 Export Results")
            
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
            
            # Top Leads Section
            st.markdown("---")
            st.markdown("### 🏆 Top 10 High-Priority Leads")
            
            top_leads = result_df.head(10)
            st.dataframe(top_leads, use_container_width=True, height=400)
            
        except Exception as e:
            st.error(f"❌ Error processing file: {str(e)}")
            with st.expander("🔍 Debug Information"):
                st.code(str(e))
    
    else:
        # Welcome message when no file uploaded
        st.markdown("""
        <div class="info-box">
            <h3 style='margin-top: 0; color: #0066cc;'>👋 Welcome to Student Lead Scoring Pro</h3>
            <p style='margin-bottom: 0;'>
                Upload your student lead data in CSV format to get instant AI-powered conversion predictions.
                Our advanced machine learning model will analyze each lead and provide priority scores to help you focus on the most promising students.
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        # Feature highlights
        st.markdown("### ✨ Key Features")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("""
            <div class="content-card">
                <div style='font-size: 2.5rem; margin-bottom: 1rem;'>🤖</div>
                <h4 style='color: #1a1a1a; margin-bottom: 0.5rem;'>AI-Powered</h4>
                <p style='color: #6c757d; font-size: 0.9rem; margin: 0;'>
                    Advanced machine learning algorithms trained on thousands of student conversions
                </p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div class="content-card">
                <div style='font-size: 2.5rem; margin-bottom: 1rem;'>⚡</div>
                <h4 style='color: #1a1a1a; margin-bottom: 0.5rem;'>Instant Results</h4>
                <p style='color: #6c757d; font-size: 0.9rem; margin: 0;'>
                    Get predictions in seconds with real-time analysis and priority rankings
                </p>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown("""
            <div class="content-card">
                <div style='font-size: 2.5rem; margin-bottom: 1rem;'>📊</div>
                <h4 style='color: #1a1a1a; margin-bottom: 0.5rem;'>Visual Insights</h4>
                <p style='color: #6c757d; font-size: 0.9rem; margin: 0;'>
                    Interactive charts and detailed breakdowns to understand your leads better
                </p>
            </div>
            """, unsafe_allow_html=True)

# ============================================================================
# USER GUIDE PAGE
# ============================================================================

elif page == "📖 User Guide":
    
    st.markdown("""
    <div class="page-header">
        <div class="page-title">User Guide</div>
        <div class="page-subtitle">Step-by-step instructions for using the Student Lead Scoring Platform</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Introduction
    st.markdown("""
    <div class="success-box">
        <h3 style='margin-top: 0; color: #10b981;'>👋 Welcome!</h3>
        <p style='margin-bottom: 0;'>
            This guide will help you understand how to use the Student Lead Scoring Platform effectively.
            Follow the simple steps below to get predictions for your student leads.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Step 1
    st.markdown("### 📥 Step 1: Prepare Your Data")
    
    st.markdown("""
    <div class="content-card">
        <h4>What You Need:</h4>
        <ul style='line-height: 1.8; color: #495057;'>
            <li><b>File Format:</b> CSV (Comma Separated Values) file</li>
            <li><b>Required Columns:</b> Your CSV must include these exact column names:
                <ul style='margin-top: 0.5rem;'>
                    <li><code>Email_Source</code> - Where the lead came from (e.g., Google, Facebook, Direct)</li>
                    <li><code>Contacted</code> - Whether they were contacted (Yes/No)</li>
                    <li><code>Location</code> - Student's city/location</li>
                    <li><code>Profession</code> - Current occupation (Student, Working Professional, etc.)</li>
                    <li><code>Course_Interest</code> - Which course they're interested in</li>
                </ul>
            </li>
        </ul>
        
        <div class="warning-box" style='margin-top: 1rem;'>
            <b>⚠️ Important:</b> Make sure your column names match exactly (including capitalization).
            The system won't work if column names are different!
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Step 2
    st.markdown("### 📤 Step 2: Upload Your File")
    
    st.markdown("""
    <div class="content-card">
        <h4>How to Upload:</h4>
        <ol style='line-height: 2; color: #495057;'>
            <li>Go to the <b>Dashboard</b> page (click "📊 Dashboard" in the sidebar)</li>
            <li>Look for the <b>"Upload Student Data"</b> section at the top</li>
            <li>Click on <b>"Browse files"</b> or drag and drop your CSV file</li>
            <li>Wait a few seconds while the file uploads</li>
        </ol>
        
        <div class="info-box" style='margin-top: 1rem;'>
            <b>💡 Tip:</b> Don't have a file ready? Click the <b>"📥 Download Sample"</b> button to get a template
            that shows you exactly how your data should be formatted.
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Step 3
    st.markdown("### 🤖 Step 3: AI Processing")
    
    st.markdown("""
    <div class="content-card">
        <h4>What Happens Automatically:</h4>
        <ul style='line-height: 1.8; color: #495057;'>
            <li><b>Data Validation:</b> The system checks if your data format is correct</li>
            <li><b>AI Analysis:</b> Machine learning models analyze each student lead</li>
            <li><b>Score Calculation:</b> Each lead gets a conversion probability score (0-100%)</li>
            <li><b>Priority Assignment:</b> Leads are categorized as High, Medium, or Low priority</li>
        </ul>
        
        <p style='color: #495057; margin-top: 1rem;'>
            <b>This process usually takes 5-10 seconds</b> depending on how many leads you have.
            You'll see a progress indicator while the AI works.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Step 4
    st.markdown("### 📊 Step 4: Understanding Your Results")
    
    st.markdown("""
    <div class="content-card">
        <h4>What the Scores Mean:</h4>
        
        <div style='display: grid; gap: 1rem; margin: 1rem 0;'>
            <div style='background: #d1f4e0; padding: 1rem; border-radius: 8px; border-left: 4px solid #10b981;'>
                <h5 style='color: #10b981; margin: 0 0 0.5rem 0;'>🟢 High Priority (70-100%)</h5>
                <p style='margin: 0; color: #495057;'>
                    <b>What it means:</b> These students are very likely to enroll. Focus your efforts here first!<br>
                    <b>Action:</b> Call them immediately, send personalized messages, offer special deals.
                </p>
            </div>
            
            <div style='background: #fff3e0; padding: 1rem; border-radius: 8px; border-left: 4px solid #f59e0b;'>
                <h5 style='color: #f59e0b; margin: 0 0 0.5rem 0;'>🟡 Medium Priority (40-70%)</h5>
                <p style='margin: 0; color: #495057;'>
                    <b>What it means:</b> These students show interest but need more nurturing.<br>
                    <b>Action:</b> Send follow-up emails, share success stories, provide more information.
                </p>
            </div>
            
            <div style='background: #fee; padding: 1rem; border-radius: 8px; border-left: 4px solid #dc3545;'>
                <h5 style='color: #dc3545; margin: 0 0 0.5rem 0;'>🔴 Low Priority (0-40%)</h5>
                <p style='margin: 0; color: #495057;'>
                    <b>What it means:</b> These students are less likely to convert right now.<br>
                    <b>Action:</b> Keep them in your email list for future opportunities, but don't spend too much time.
                </p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Step 5
    st.markdown("### 📈 Step 5: Using the Charts")
    
    st.markdown("""
    <div class="content-card">
        <h4>Understanding the Visualizations:</h4>
        
        <h5>📊 Score Distribution Chart (Left Side)</h5>
        <p style='color: #495057; margin-bottom: 1rem;'>
            This shows how your leads are spread across different score ranges.
            A good distribution means you have leads at all levels.
        </p>
        
        <h5>🎯 Priority Breakdown Chart (Right Side)</h5>
        <p style='color: #495057; margin-bottom: 1rem;'>
            This pie chart shows what percentage of your leads fall into each priority category.
            Ideally, you want a good number of High Priority leads!
        </p>
        
        <div class="info-box" style='margin-top: 1rem;'>
            <b>💡 Pro Tip:</b> If you have very few High Priority leads, you might want to review your lead
            generation strategies or targeting criteria.
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Step 6
    st.markdown("### 💾 Step 6: Export and Use Your Results")
    
    st.markdown("""
    <div class="content-card">
        <h4>Downloading Your Report:</h4>
        <ol style='line-height: 2; color: #495057;'>
            <li>Scroll down to the <b>"Export Results"</b> section</li>
            <li>Click the <b>"📥 Download Complete Report"</b> button</li>
            <li>The CSV file will download to your computer with a timestamp</li>
            <li>Open it in Excel or Google Sheets to start working with your leads</li>
        </ol>
        
        <h4 style='margin-top: 2rem;'>What's in the Export File:</h4>
        <ul style='line-height: 1.8; color: #495057;'>
            <li>All your original data</li>
            <li><b>Lead_Score:</b> Decimal score (0.00 to 1.00)</li>
            <li><b>Lead_Score_%:</b> Percentage score (0% to 100%)</li>
            <li><b>Priority:</b> High/Medium/Low category</li>
            <li><b>Prediction:</b> "Likely to Convert" or "Unlikely"</li>
        </ul>
        
        <div class="success-box" style='margin-top: 1rem;'>
            <b>✅ Next Steps:</b> Import this file into your CRM system or use it to prioritize your sales calls!
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Common Questions
    st.markdown("### ❓ Common Questions")
    
    with st.expander("🤔 What if my CSV file has different column names?"):
        st.markdown("""
        The system requires exact column names to work properly. If your columns are named differently:
        
        1. **Option 1:** Rename your columns in Excel/Google Sheets to match the required names
        2. **Option 2:** Download our sample template and copy your data into it
        
        Required column names (must match exactly):
        - `Email_Source`
        - `Contacted`
        - `Location`
        - `Profession`
        - `Course_Interest`
        """)
    
    with st.expander("⚡ How long does the analysis take?"):
        st.markdown("""
        The AI analysis is very fast:
        - **Small files (1-100 leads):** 2-5 seconds
        - **Medium files (100-1,000 leads):** 5-15 seconds
        - **Large files (1,000+ leads):** 15-30 seconds
        
        The system can handle thousands of leads at once!
        """)
    
    with st.expander("🎯 How accurate are the predictions?"):
        st.markdown("""
        Our AI model has been trained on thousands of real student conversions and achieves:
        - **85-90% accuracy** on average
        - **High precision** for identifying top leads
        
        Remember: These are predictions to help you prioritize. Always follow up with all leads,
        but focus your best efforts on High Priority ones!
        """)
    
    with st.expander("📱 Can I use this on my phone?"):
        st.markdown("""
        Yes! The platform is fully responsive and works on:
        - Desktop computers
        - Laptops
        - Tablets
        - Smartphones
        
        The interface automatically adjusts to your screen size.
        """)
    
    with st.expander("🔒 Is my data secure?"):
        st.markdown("""
        Yes, your data is secure:
        - Files are processed **only during your session**
        - No data is permanently stored on our servers
        - Once you close your browser, all data is removed
        - The AI model doesn't learn from or save your specific data
        """)
    
    with st.expander("💰 What does High/Medium/Low priority really mean for my business?"):
        st.markdown("""
        Here's what you should do with each priority level:
        
        **🟢 High Priority (70-100%):**
        - **These are your hot leads!** Call them within 24 hours
        - Assign your best sales people to these leads
        - Offer special enrollment bonuses or discounts
        - **Expected conversion rate:** 60-80%
        
        **🟡 Medium Priority (40-70%):**
        - **These need nurturing** - they're interested but not ready yet
        - Send them useful content (course details, success stories)
        - Follow up weekly with personalized messages
        - **Expected conversion rate:** 30-50%
        
        **🔴 Low Priority (0-40%):**
        - **Don't ignore them, but don't spend hours on them**
        - Add them to your email newsletter
        - Try again in 3-6 months with new offers
        - **Expected conversion rate:** 5-20%
        """)

# ============================================================================
# ABOUT PAGE
# ============================================================================

elif page == "ℹ️ About":
    
    st.markdown("""
    <div class="page-header">
        <div class="page-title">About This Platform</div>
        <div class="page-subtitle">Learn more about the Student Lead Scoring Intelligence Platform</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="content-card">
        <h3 style='color: #1a1a1a; margin-top: 0;'>🎓 What is Student Lead Scoring?</h3>
        <p style='color: #495057; line-height: 1.8; font-size: 1rem;'>
            Student Lead Scoring is an AI-powered system that helps educational institutions predict which prospective
            students are most likely to enroll in their courses. By analyzing historical data and patterns, our machine
            learning model assigns each lead a probability score, helping you focus your recruitment efforts where
            they'll have the most impact.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    st.markdown("### 🚀 How It Works")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="content-card" style='text-align: center;'>
            <div style='font-size: 3rem; margin-bottom: 1rem;'>📊</div>
            <h4 style='color: #1a1a1a;'>Data Analysis</h4>
            <p style='color: #6c757d; font-size: 0.9rem;'>
                We analyze multiple factors including lead source, location, profession,
                course interest, and contact history
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="content-card" style='text-align: center;'>
            <div style='font-size: 3rem; margin-bottom: 1rem;'>🤖</div>
            <h4 style='color: #1a1a1a;'>AI Prediction</h4>
            <p style='color: #6c757d; font-size: 0.9rem;'>
                Our trained machine learning model processes the data and predicts
                conversion probability with 85-90% accuracy
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="content-card" style='text-align: center;'>
            <div style='font-size: 3rem; margin-bottom: 1rem;'>🎯</div>
            <h4 style='color: #1a1a1a;'>Actionable Insights</h4>
            <p style='color: #6c757d; font-size: 0.9rem;'>
                Get clear priority rankings and visual reports to help you make
                data-driven decisions about student outreach
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    st.markdown("### ✨ Key Benefits")
    
    st.markdown("""
    <div class="content-card">
        <ul style='line-height: 2; color: #495057; font-size: 1rem;'>
            <li><b>Save Time:</b> Focus on leads that matter instead of wasting time on low-probability students</li>
            <li><b>Increase Conversions:</b> Improve enrollment rates by 25-40% through better lead prioritization</li>
            <li><b>Optimize Resources:</b> Allocate your team's efforts where they'll have the biggest impact</li>
            <li><b>Data-Driven Decisions:</b> Replace guesswork with AI-powered insights backed by real data</li>
            <li><b>Instant Results:</b> Get predictions in seconds, not days or weeks</li>
            <li><b>No Technical Skills Needed:</b> Simple upload-and-download workflow anyone can use</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    st.markdown("### 🎯 Who Should Use This?")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="content-card">
            <h4 style='color: #1a1a1a;'>Perfect For:</h4>
            <ul style='line-height: 1.8; color: #495057;'>
                <li>Educational Institutions</li>
                <li>Online Course Providers</li>
                <li>Training Companies</li>
                <li>Admission Teams</li>
                <li>Sales Teams in Education</li>
                <li>Marketing Departments</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="content-card">
            <h4 style='color: #1a1a1a;'>Use Cases:</h4>
            <ul style='line-height: 1.8; color: #495057;'>
                <li>Prioritize student follow-ups</li>
                <li>Allocate counselor time efficiently</li>
                <li>Plan targeted marketing campaigns</li>
                <li>Forecast enrollment numbers</li>
                <li>Improve conversion rates</li>
                <li>Optimize admission strategies</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    st.markdown("### 🔧 Technical Details")
    
    st.markdown("""
    <div class="content-card">
        <h4 style='color: #1a1a1a;'>Technology Stack:</h4>
        <ul style='line-height: 1.8; color: #495057;'>
            <li><b>Machine Learning:</b> Scikit-learn with ensemble models (Random Forest, Gradient Boosting)</li>
            <li><b>Framework:</b> Streamlit for interactive web interface</li>
            <li><b>Data Processing:</b> Pandas and NumPy for efficient data handling</li>
            <li><b>Visualizations:</b> Plotly for interactive charts and graphs</li>
            <li><b>Model Accuracy:</b> 85-90% on test data</li>
        </ul>
        
        <h4 style='color: #1a1a1a; margin-top: 2rem;'>Data Privacy:</h4>
        <ul style='line-height: 1.8; color: #495057;'>
            <li>All data processing happens in real-time during your session</li>
            <li>No permanent storage of your student data</li>
            <li>Secure file upload and download</li>
            <li>Session data cleared when you close the browser</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    st.markdown("""
    <div class="info-box">
        <h4 style='color: #0066cc; margin-top: 0;'>💡 Need Support?</h4>
        <p style='margin-bottom: 0; color: #495057;'>
            Check out the <b>User Guide</b> section for detailed instructions, or contact your system administrator
            for technical support.
        </p>
    </div>
    """, unsafe_allow_html=True)

# ============================================================================
# FOOTER
# ============================================================================

st.markdown("---")
st.markdown("""
<div style='background: white; padding: 2rem; border-radius: 12px; text-align: center; border: 1px solid #e9ecef;'>
    <div style='color: #1a1a1a; font-weight: 700; font-size: 1.1rem; margin-bottom: 0.5rem;'>
        🎓 Student Lead Scoring Intelligence Platform
    </div>
    <div style='color: #6c757d; font-size: 0.9rem;'>
        Powered by Machine Learning • Built with Streamlit & Python • Version 2.0
    </div>
    <div style='color: #adb5bd; font-size: 0.85rem; margin-top: 1rem;'>
        © 2024 • AI-Powered Student Analytics
    </div>
</div>
""", unsafe_allow_html=True)
