"""
Lead Scoring Prediction App - Professional UI
Upload CSV files to predict lead conversion probability
"""

import streamlit as st
import pandas as pd
import joblib
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

# Page configuration
st.set_page_config(
    page_title="Lead Scoring App",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for professional look
st.markdown("""
    <style>
    .main {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    .stApp {
        background: linear-gradient(to bottom, #f8f9fa 0%, #e9ecef 100%);
    }
    .css-1d391kg {
        background-color: #ffffff;
    }
    h1 {
        color: #2c3e50;
        font-weight: 700;
        text-align: center;
        padding: 20px;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    h2, h3 {
        color: #34495e;
    }
    .stButton>button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 12px 24px;
        font-weight: 600;
        transition: all 0.3s;
    }
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 12px rgba(102, 126, 234, 0.4);
    }
    .upload-box {
        border: 2px dashed #667eea;
        border-radius: 10px;
        padding: 30px;
        text-align: center;
        background-color: #f8f9fa;
        margin: 20px 0;
    }
    .metric-card {
        background: white;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        text-align: center;
    }
    .info-box {
        background: linear-gradient(135deg, #e3f2fd 0%, #bbdefb 100%);
        padding: 20px;
        border-radius: 10px;
        border-left: 4px solid #2196f3;
        margin: 20px 0;
    }
    .success-box {
        background: linear-gradient(135deg, #e8f5e9 0%, #c8e6c9 100%);
        padding: 20px;
        border-radius: 10px;
        border-left: 4px solid #4caf50;
        margin: 20px 0;
    }
    .stDataFrame {
        border-radius: 10px;
        overflow: hidden;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    }
    </style>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.image("https://img.icons8.com/fluency/96/000000/target.png", width=80)
    st.title("🎯 Lead Scorer")
    st.markdown("---")
    
    st.markdown("""
    ### 📊 About
    This AI-powered tool predicts lead conversion probability using machine learning.
    
    ### 🚀 Features
    - **Smart Predictions**: ML-based scoring
    - **Instant Results**: Real-time analysis
    - **Visual Insights**: Interactive charts
    - **Export Data**: Download results
    
    ### 📈 Score Ranges
    - 🟢 **70-100%**: High Priority
    - 🟡 **40-70%**: Medium Priority  
    - 🔴 **0-40%**: Low Priority
    """)
    
    st.markdown("---")
    st.markdown("**Made with ❤️ using Streamlit**")

# Main content
st.markdown("<h1>🎯 Lead Scoring Intelligence Platform</h1>", unsafe_allow_html=True)

# Load saved models and preprocessors
@st.cache_resource
def load_models():
    try:
        model = joblib.load('best_model.pkl')
        scaler = joblib.load('scaler.pkl')
        label_encoders = joblib.load('label_encoders.pkl')
        return model, scaler, label_encoders
    except FileNotFoundError as e:
        st.error(f"⚠️ Model files not found: {e}")
        st.info("Please ensure 'best_model.pkl', 'scaler.pkl', and 'label_encoders.pkl' are in the same directory as app.py")
        st.stop()
    except Exception as e:
        st.error(f"⚠️ Error loading models: {e}")
        st.stop()

# Load models with progress
with st.spinner("🔄 Loading AI models..."):
    best_model, scaler, label_encoders = load_models()

st.markdown("""
<div class="success-box">
    <h3>✅ System Ready</h3>
    <p>AI models loaded successfully. Upload your lead data to begin scoring.</p>
</div>
""", unsafe_allow_html=True)

# Instructions in expandable section
with st.expander("📖 How to Use This Tool", expanded=False):
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        #### 📥 Step 1: Prepare Your Data
        - Format as CSV file
        - Include required columns
        - Clean data recommended
        
        #### 🎯 Step 2: Upload & Analyze
        - Click upload button
        - Select your CSV file
        - Wait for processing
        """)
    with col2:
        st.markdown("""
        #### 📊 Step 3: Review Results
        - Check conversion scores
        - Analyze distribution
        - Identify priorities
        
        #### 💾 Step 4: Export Results
        - Download scored leads
        - Share with team
        - Track performance
        """)

st.markdown("---")

# File uploader with custom styling
st.markdown("## 📁 Upload Lead Data")

col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    uploaded_file = st.file_uploader(
        "Drop your CSV file here or click to browse",
        type=["csv"],
        help="Upload a CSV file containing lead information"
    )

# Sample data download
st.markdown("### 📥 Need a Sample File?")
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    sample_data = pd.DataFrame({
        'Email_Source': ['Google', 'Facebook', 'Direct', 'Referral', 'LinkedIn'],
        'Contacted': ['Yes', 'No', 'Yes', 'No', 'Yes'],
        'Location': ['Mumbai', 'Delhi', 'Bangalore', 'Chennai', 'Pune'],
        'Profession': ['Student', 'Working Professional', 'Unemployed', 'Freelancer', 'Student'],
        'Course_Interest': ['Data Science', 'Web Development', 'AI/ML', 'Digital Marketing', 'Cloud Computing']
    })
    csv_sample = sample_data.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Download Sample CSV Template",
        data=csv_sample,
        file_name="sample_leads_template.csv",
        mime="text/csv",
        use_container_width=True
    )

st.markdown("---")

if uploaded_file is not None:
    try:
        # Read uploaded file
        new_leads = pd.read_csv(uploaded_file)
        
        # Header with animation effect
        st.markdown("## 📊 Data Analysis Dashboard")
        
        # Quick stats
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.markdown("""
            <div class="metric-card">
                <h2 style="color: #667eea; margin: 0;">📋</h2>
                <h3 style="margin: 10px 0;">{}</h3>
                <p style="color: #7f8c8d; margin: 0;">Total Leads</p>
            </div>
            """.format(len(new_leads)), unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div class="metric-card">
                <h2 style="color: #667eea; margin: 0;">📁</h2>
                <h3 style="margin: 10px 0;">{}</h3>
                <p style="color: #7f8c8d; margin: 0;">Columns</p>
            </div>
            """.format(len(new_leads.columns)), unsafe_allow_html=True)
        
        with col3:
            st.markdown("""
            <div class="metric-card">
                <h2 style="color: #667eea; margin: 0;">✓</h2>
                <h3 style="margin: 10px 0;">Ready</h3>
                <p style="color: #7f8c8d; margin: 0;">Status</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            st.markdown("""
            <div class="metric-card">
                <h2 style="color: #667eea; margin: 0;">🤖</h2>
                <h3 style="margin: 10px 0;">AI</h3>
                <p style="color: #7f8c8d; margin: 0;">Processing</p>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Display uploaded data
        with st.expander("👁️ View Uploaded Data", expanded=True):
            st.dataframe(new_leads.head(10), use_container_width=True)
        
        # Get expected columns from label encoders
        expected_cols = list(label_encoders.keys())
        
        # Check if all required columns are present
        missing_cols = [col for col in expected_cols if col not in new_leads.columns]
        if missing_cols:
            st.error(f"❌ Missing required columns: {missing_cols}")
            st.info(f"Your CSV must have these columns: {expected_cols}")
            st.stop()
        
        # Make a copy for processing
        df_processed = new_leads.copy()
        
        # Remove target column if present
        if 'Converted' in df_processed.columns:
            st.info("ℹ️ Note: 'Converted' column found and will be ignored for prediction")
            df_processed = df_processed.drop(columns=['Converted'])
        
        # Processing section
        st.markdown("## ⚙️ AI Processing Pipeline")
        
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        # Encode categorical columns using saved encoders
        status_text.text("🔄 Encoding categorical variables...")
        progress_bar.progress(33)
        
        for col in expected_cols:
            if col in df_processed.columns:
                try:
                    df_processed[col] = label_encoders[col].transform(df_processed[col].astype(str))
                except ValueError as e:
                    st.error(f"❌ Error encoding column '{col}': {e}")
                    st.info(f"Make sure all values in '{col}' match the training data categories")
                    st.stop()
        
        # Scale features
        status_text.text("📏 Scaling features...")
        progress_bar.progress(66)
        features_scaled = scaler.transform(df_processed)
        
        # Predict scores
        status_text.text("🎯 Generating predictions...")
        progress_bar.progress(100)
        scores = best_model.predict_proba(features_scaled)[:, 1]
        predictions = best_model.predict(features_scaled)
        
        status_text.text("✅ Processing complete!")
        
        # Add predictions to original dataframe
        new_leads['Lead_Score'] = scores
        new_leads['Lead_Score_%'] = (scores * 100).round(2)
        new_leads['Priority'] = pd.cut(
            scores,
            bins=[0, 0.4, 0.7, 1.0],
            labels=['🔴 Low', '🟡 Medium', '🟢 High']
        )
        new_leads['Prediction'] = ['✓ Likely to Convert' if p == 1 else '✗ Unlikely to Convert' for p in predictions]
        
        # Sort by lead score
        new_leads_sorted = new_leads.sort_values(by='Lead_Score', ascending=False).reset_index(drop=True)
        
        st.markdown("---")
        
        # Results Dashboard
        st.markdown("## 🎯 Prediction Results Dashboard")
        
        # Key Metrics with better styling
        col1, col2, col3, col4 = st.columns(4)
        
        high_score = (new_leads_sorted['Lead_Score'] > 0.7).sum()
        medium_score = ((new_leads_sorted['Lead_Score'] > 0.4) & (new_leads_sorted['Lead_Score'] <= 0.7)).sum()
        low_score = (new_leads_sorted['Lead_Score'] <= 0.4).sum()
        avg_score = new_leads_sorted['Lead_Score_%'].mean()
        
        with col1:
            st.metric(
                label="🟢 High Priority Leads",
                value=high_score,
                delta=f"{(high_score/len(new_leads_sorted)*100):.1f}% of total"
            )
        
        with col2:
            st.metric(
                label="🟡 Medium Priority Leads",
                value=medium_score,
                delta=f"{(medium_score/len(new_leads_sorted)*100):.1f}% of total"
            )
        
        with col3:
            st.metric(
                label="🔴 Low Priority Leads",
                value=low_score,
                delta=f"{(low_score/len(new_leads_sorted)*100):.1f}% of total"
            )
        
        with col4:
            st.metric(
                label="📊 Average Score",
                value=f"{avg_score:.1f}%",
                delta="Mean conversion probability"
            )
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Visualizations
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 📊 Score Distribution")
            
            # Create histogram with Plotly
            fig = px.histogram(
                new_leads_sorted,
                x='Lead_Score_%',
                nbins=20,
                color_discrete_sequence=['#667eea'],
                labels={'Lead_Score_%': 'Lead Score (%)'},
            )
            fig.update_layout(
                showlegend=False,
                height=400,
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font=dict(size=12)
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.markdown("### 🎯 Priority Breakdown")
            
            # Create pie chart
            priority_counts = new_leads_sorted['Priority'].value_counts()
            fig = go.Figure(data=[go.Pie(
                labels=priority_counts.index,
                values=priority_counts.values,
                hole=.4,
                marker_colors=['#ef5350', '#ffa726', '#66bb6a']
            )])
            fig.update_layout(
                height=400,
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(size=12)
            )
            st.plotly_chart(fig, use_container_width=True)
        
        # Results Table
        st.markdown("### 📋 Detailed Lead Scores")
        
        # Style the dataframe
        def highlight_priority(row):
            if row['Lead_Score_%'] > 70:
                return ['background-color: #e8f5e9'] * len(row)
            elif row['Lead_Score_%'] > 40:
                return ['background-color: #fff9c4'] * len(row)
            else:
                return ['background-color: #ffebee'] * len(row)
        
        styled_df = new_leads_sorted.style.apply(highlight_priority, axis=1)
        st.dataframe(styled_df, use_container_width=True, height=400)
        
        # Download section
        st.markdown("---")
        st.markdown("## 💾 Export Results")
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            csv = new_leads_sorted.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="📥 Download Complete Report (CSV)",
                data=csv,
                file_name=f"Lead_Scoring_Results_{pd.Timestamp.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv",
                use_container_width=True
            )
        
        # Top leads section
        st.markdown("---")
        st.markdown("## 🏆 Top 10 High-Priority Leads")
        
        top_leads = new_leads_sorted.head(10)[['Lead_Score_%', 'Priority', 'Prediction'] + [col for col in new_leads_sorted.columns if col not in ['Lead_Score', 'Lead_Score_%', 'Priority', 'Prediction']]]
        st.dataframe(top_leads, use_container_width=True)
        
    except Exception as e:
        st.error(f"❌ Error processing file: {str(e)}")
        st.info("Please check your CSV file format and try again")
        with st.expander("🔍 Debug Information"):
            st.code(str(e))

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; padding: 20px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border-radius: 10px; color: white;'>
    <h3 style='color: white; margin: 0;'>🎯 Lead Scoring Intelligence Platform</h3>
    <p style='margin: 10px 0 0 0;'>Powered by Machine Learning | Built with Streamlit & Python</p>
</div>
""", unsafe_allow_html=True)