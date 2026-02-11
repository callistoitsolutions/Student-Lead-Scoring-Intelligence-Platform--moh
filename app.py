"""
Student Lead Scoring Intelligence Platform
Complete system with authentication, admin panel, and AI-powered predictions
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import joblib
import hashlib
import sqlite3
from datetime import datetime
import time
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
# DATABASE FUNCTIONS
# ============================================================================

def init_database():
    """Initialize database with migration support"""
    conn = sqlite3.connect('student_lead_scoring.db', check_same_thread=False)
    c = conn.cursor()
    
    # Create users table
    c.execute('''CREATE TABLE IF NOT EXISTS users
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  username TEXT UNIQUE NOT NULL,
                  password_hash TEXT NOT NULL,
                  email TEXT,
                  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                  last_login TIMESTAMP,
                  is_active BOOLEAN DEFAULT 1,
                  role TEXT DEFAULT 'user')''')
    
    # Create usage_logs table
    c.execute('''CREATE TABLE IF NOT EXISTS usage_logs
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  user_id INTEGER,
                  action TEXT,
                  details TEXT,
                  leads_scored INTEGER,
                  timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                  FOREIGN KEY (user_id) REFERENCES users (id))''')
    
    # Create sessions table
    c.execute('''CREATE TABLE IF NOT EXISTS sessions
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  user_id INTEGER,
                  login_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                  logout_time TIMESTAMP,
                  is_active BOOLEAN DEFAULT 1,
                  session_token TEXT,
                  FOREIGN KEY (user_id) REFERENCES users (id))''')
    
    # Migration: Add missing columns
    try:
        c.execute("PRAGMA table_info(sessions)")
        columns = [column[1] for column in c.fetchall()]
        
        if 'is_active' not in columns:
            c.execute("ALTER TABLE sessions ADD COLUMN is_active BOOLEAN DEFAULT 1")
            conn.commit()
            
        if 'session_token' not in columns:
            c.execute("ALTER TABLE sessions ADD COLUMN session_token TEXT")
            conn.commit()
    except Exception as e:
        pass
    
    # Create admin user if not exists
    c.execute("SELECT * FROM users WHERE username = 'admin'")
    if not c.fetchone():
        admin_password = hashlib.sha256('admin123'.encode()).hexdigest()
        c.execute("INSERT INTO users (username, password_hash, email, role) VALUES (?, ?, ?, ?)",
                  ('admin', admin_password, 'admin@studentscore.com', 'admin'))
    
    conn.commit()
    conn.close()

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def verify_user(username, password):
    """Verify and login user"""
    conn = sqlite3.connect('student_lead_scoring.db', check_same_thread=False)
    c = conn.cursor()
    
    try:
        password_hash = hash_password(password)
        c.execute("SELECT id, username, role, is_active FROM users WHERE username = ? AND password_hash = ?",
                  (username, password_hash))
        
        user = c.fetchone()
        
        if user and user[3]:
            c.execute("UPDATE users SET last_login = ? WHERE id = ?", (datetime.now(), user[0]))
            session_token = hashlib.md5(f"{user[0]}{datetime.now()}".encode()).hexdigest()
            
            try:
                c.execute("UPDATE sessions SET is_active = 0, logout_time = ? WHERE user_id = ? AND is_active = 1", 
                          (datetime.now(), user[0]))
            except sqlite3.OperationalError:
                pass
            
            try:
                c.execute("INSERT INTO sessions (user_id, login_time, is_active, session_token) VALUES (?, ?, ?, ?)",
                          (user[0], datetime.now(), 1, session_token))
            except sqlite3.OperationalError:
                c.execute("INSERT INTO sessions (user_id, login_time) VALUES (?, ?)",
                          (user[0], datetime.now()))
            
            conn.commit()
            conn.close()
            
            return {
                'id': user[0], 
                'username': user[1], 
                'role': user[2], 
                'is_active': user[3], 
                'session_token': session_token
            }
        
        conn.close()
        return None
    except Exception as e:
        conn.close()
        return None

def create_user_by_admin(username, password, email):
    """Admin creates user"""
    conn = sqlite3.connect('student_lead_scoring.db', check_same_thread=False)
    c = conn.cursor()
    try:
        password_hash = hash_password(password)
        c.execute("INSERT INTO users (username, password_hash, email, role) VALUES (?, ?, ?, ?)",
                  (username, password_hash, email, 'user'))
        conn.commit()
        conn.close()
        return True
    except sqlite3.IntegrityError:
        conn.close()
        return False

def logout_user(user_id):
    """Logout user"""
    conn = sqlite3.connect('student_lead_scoring.db', check_same_thread=False)
    c = conn.cursor()
    try:
        c.execute("UPDATE sessions SET is_active = 0, logout_time = ? WHERE user_id = ? AND is_active = 1",
                  (datetime.now(), user_id))
    except sqlite3.OperationalError:
        c.execute("UPDATE sessions SET logout_time = ? WHERE user_id = ? AND logout_time IS NULL",
                  (datetime.now(), user_id))
    conn.commit()
    conn.close()

def log_usage(user_id, action, details="", leads_scored=0):
    """Log activity"""
    conn = sqlite3.connect('student_lead_scoring.db', check_same_thread=False)
    c = conn.cursor()
    c.execute("INSERT INTO usage_logs (user_id, action, details, leads_scored) VALUES (?, ?, ?, ?)",
              (user_id, action, details, leads_scored))
    conn.commit()
    conn.close()

def get_user_stats(user_id):
    """Get user stats"""
    conn = sqlite3.connect('student_lead_scoring.db', check_same_thread=False)
    c = conn.cursor()
    c.execute("SELECT COUNT(*) FROM usage_logs WHERE user_id = ? AND action = 'score_leads'", (user_id,))
    total_scorings = c.fetchone()[0]
    c.execute("SELECT SUM(leads_scored) FROM usage_logs WHERE user_id = ? AND action = 'score_leads'", (user_id,))
    total_leads = c.fetchone()[0] or 0
    c.execute("SELECT COUNT(*) FROM sessions WHERE user_id = ?", (user_id,))
    total_logins = c.fetchone()[0]
    conn.close()
    return {'total_scorings': total_scorings, 'total_leads': total_leads, 'total_logins': total_logins}

def get_all_users():
    """Get all users"""
    conn = sqlite3.connect('student_lead_scoring.db', check_same_thread=False)
    c = conn.cursor()
    c.execute("SELECT id, username, email, created_at, last_login, is_active, role FROM users ORDER BY created_at DESC")
    users = c.fetchall()
    conn.close()
    return users

def get_currently_logged_in_users():
    """Get currently logged in users"""
    conn = sqlite3.connect('student_lead_scoring.db', check_same_thread=False)
    c = conn.cursor()
    try:
        c.execute("""
            SELECT u.id, u.username, u.email, s.login_time, u.role
            FROM sessions s
            JOIN users u ON s.user_id = u.id
            WHERE s.is_active = 1
            ORDER BY s.login_time DESC
        """)
        active_users = c.fetchall()
    except sqlite3.OperationalError:
        active_users = []
    conn.close()
    return active_users

def get_user_activity_details(user_id):
    """Get detailed activity for a specific user"""
    conn = sqlite3.connect('student_lead_scoring.db', check_same_thread=False)
    c = conn.cursor()
    c.execute("""
        SELECT action, details, leads_scored, timestamp
        FROM usage_logs
        WHERE user_id = ?
        ORDER BY timestamp DESC
        LIMIT 20
    """, (user_id,))
    activities = c.fetchall()
    conn.close()
    return activities

def get_all_user_activities():
    """Get all activities from all users"""
    conn = sqlite3.connect('student_lead_scoring.db', check_same_thread=False)
    c = conn.cursor()
    c.execute("""
        SELECT u.username, l.action, l.details, l.leads_scored, l.timestamp
        FROM usage_logs l
        JOIN users u ON l.user_id = u.id
        ORDER BY l.timestamp DESC
        LIMIT 100
    """)
    activities = c.fetchall()
    conn.close()
    return activities

def get_system_stats():
    """Get system stats"""
    conn = sqlite3.connect('student_lead_scoring.db', check_same_thread=False)
    c = conn.cursor()
    c.execute("SELECT COUNT(*) FROM users WHERE role = 'user'")
    total_users = c.fetchone()[0]
    try:
        c.execute("SELECT COUNT(*) FROM sessions WHERE is_active = 1")
        currently_online = c.fetchone()[0]
    except sqlite3.OperationalError:
        currently_online = 0
    c.execute("SELECT COUNT(*) FROM usage_logs WHERE action = 'score_leads'")
    total_scorings = c.fetchone()[0]
    c.execute("SELECT SUM(leads_scored) FROM usage_logs WHERE action = 'score_leads'")
    total_leads = c.fetchone()[0] or 0
    c.execute("SELECT COUNT(*) FROM sessions WHERE DATE(login_time) = DATE('now')")
    today_logins = c.fetchone()[0]
    conn.close()
    return {
        'total_users': total_users,
        'currently_online': currently_online,
        'total_scorings': total_scorings,
        'total_leads': total_leads,
        'today_logins': today_logins
    }

def toggle_user_status(user_id, is_active):
    """Enable/disable user"""
    conn = sqlite3.connect('student_lead_scoring.db', check_same_thread=False)
    c = conn.cursor()
    c.execute("UPDATE users SET is_active = ? WHERE id = ?", (is_active, user_id))
    conn.commit()
    conn.close()

def delete_user(user_id):
    """Delete user"""
    conn = sqlite3.connect('student_lead_scoring.db', check_same_thread=False)
    c = conn.cursor()
    c.execute("DELETE FROM users WHERE id = ?", (user_id,))
    conn.commit()
    conn.close()

# ============================================================================
# MODEL LOADING FUNCTIONS
# ============================================================================

@st.cache_resource
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
# PREDICTION FUNCTIONS
# ============================================================================

def process_and_predict(df, best_model, scaler, label_encoders):
    """Process data and generate predictions"""
    
    # Get expected columns from label encoders
    expected_cols = list(label_encoders.keys())
    
    # Check for required columns
    missing_cols = [col for col in expected_cols if col not in df.columns]
    if missing_cols:
        return None, f"Missing required columns: {missing_cols}"
    
    # Make a copy for processing
    df_processed = df.copy()
    
    # Remove target column if present
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
            labels=['🔴 Low', '🟡 Medium', '🟢 High']
        )
        df['Prediction'] = ['✓ Likely' if p == 1 else '✗ Unlikely' for p in predictions]
        
        # Sort by score
        df_sorted = df.sort_values(by='Lead_Score', ascending=False).reset_index(drop=True)
        
        return df_sorted, None
        
    except Exception as e:
        return None, str(e)

# ============================================================================
# LOGIN PAGE
# ============================================================================

def show_login_page():
    """Professional login page with modern design"""
    
    # Creative CSS for login page
    st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700;800&display=swap');
        
        [data-testid="stAppViewContainer"] {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            font-family: 'Poppins', sans-serif;
        }
        
        .login-container {
            max-width: 480px;
            margin: 80px auto;
            padding: 0;
            background: white;
            border-radius: 24px;
            box-shadow: 0 30px 80px rgba(0,0,0,0.3);
            overflow: hidden;
            animation: slideUp 0.6s ease-out;
        }
        
        @keyframes slideUp {
            from {
                opacity: 0;
                transform: translateY(30px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }
        
        .login-header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 40px 30px;
            text-align: center;
            color: white;
            position: relative;
            overflow: hidden;
        }
        
        .login-header::before {
            content: '';
            position: absolute;
            top: -50%;
            left: -50%;
            width: 200%;
            height: 200%;
            background: radial-gradient(circle, rgba(255,255,255,0.1) 0%, transparent 70%);
            animation: pulse 4s ease-in-out infinite;
        }
        
        @keyframes pulse {
            0%, 100% { transform: scale(1); opacity: 0.5; }
            50% { transform: scale(1.1); opacity: 0.3; }
        }
        
        .login-icon {
            font-size: 80px;
            margin-bottom: 15px;
            display: inline-block;
            animation: float 3s ease-in-out infinite;
            position: relative;
            z-index: 1;
        }
        
        @keyframes float {
            0%, 100% { transform: translateY(0px); }
            50% { transform: translateY(-15px); }
        }
        
        .login-title {
            font-size: 2.2rem;
            font-weight: 800;
            margin: 0;
            position: relative;
            z-index: 1;
            letter-spacing: -0.5px;
        }
        
        .login-subtitle {
            font-size: 1rem;
            opacity: 0.95;
            margin-top: 8px;
            font-weight: 400;
            position: relative;
            z-index: 1;
        }
        
        .login-body {
            padding: 40px 35px;
        }
        
        .input-label {
            font-size: 0.9rem;
            font-weight: 600;
            color: #334155;
            margin-bottom: 8px;
            display: block;
        }
        
        .stTextInput > div > div > input {
            border: 2px solid #e2e8f0;
            border-radius: 12px;
            padding: 14px 18px;
            font-size: 1rem;
            transition: all 0.3s ease;
            background: #f8fafc;
        }
        
        .stTextInput > div > div > input:focus {
            border-color: #667eea;
            background: white;
            box-shadow: 0 0 0 4px rgba(102, 126, 234, 0.1);
        }
        
        .feature-card {
            background: linear-gradient(135deg, #f8fafc 0%, #e0e7ff 100%);
            padding: 20px;
            border-radius: 16px;
            margin-top: 30px;
            border: 2px solid #e0e7ff;
        }
        
        .feature-title {
            font-size: 1rem;
            font-weight: 700;
            color: #1e293b;
            margin-bottom: 12px;
            display: flex;
            align-items: center;
            gap: 8px;
        }
        
        .feature-item {
            font-size: 0.9rem;
            color: #475569;
            margin: 8px 0;
            padding-left: 24px;
            position: relative;
        }
        
        .feature-item::before {
            content: '✓';
            position: absolute;
            left: 0;
            color: #10b981;
            font-weight: 800;
            font-size: 1.1rem;
        }
        
        /* Mobile Responsive */
        @media (max-width: 768px) {
            .login-container {
                margin: 20px;
                max-width: 100%;
            }
            
            .login-title {
                font-size: 1.8rem;
            }
            
            .login-icon {
                font-size: 60px;
            }
            
            .login-body {
                padding: 30px 25px;
            }
        }
        </style>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2.5, 1])
    
    with col2:
        st.markdown('<div class="login-container">', unsafe_allow_html=True)
        
        # Header Section
        st.markdown('''
        <div class="login-header">
            <div class="login-icon">🎓</div>
            <h1 class="login-title">Student Lead Scorer</h1>
            <p class="login-subtitle">AI-Powered Student Intelligence Platform</p>
        </div>
        ''', unsafe_allow_html=True)
        
        # Body Section
        st.markdown('<div class="login-body">', unsafe_allow_html=True)
        
        st.markdown('<label class="input-label">👤 Username</label>', unsafe_allow_html=True)
        username = st.text_input("", key="login_username", placeholder="Enter your username", label_visibility="collapsed")
        
        st.markdown('<label class="input-label" style="margin-top: 20px;">🔒 Password</label>', unsafe_allow_html=True)
        password = st.text_input("", type="password", key="login_password", placeholder="Enter your password", label_visibility="collapsed")
        
        col_btn1, col_btn2 = st.columns(2)
        
        with col_btn1:
            if st.button("🚀 Login", use_container_width=True, type="primary", key="login_btn"):
                if username and password:
                    user = verify_user(username, password)
                    if user:
                        st.session_state.logged_in = True
                        st.session_state.user = user
                        log_usage(user['id'], 'login')
                        st.success(f"✅ Welcome back, {username}!")
                        time.sleep(1)
                        st.rerun()
                    else:
                        st.error("❌ Invalid credentials. Please try again.")
                else:
                    st.warning("⚠️ Please enter both username and password")
        
        with col_btn2:
            if st.button("🔑 Demo Access", use_container_width=True, key="demo_btn"):
                with st.expander("📌 Demo Credentials", expanded=True):
                    st.markdown("""
                        **Admin Account:**
                        - Username: `admin`
                        - Password: `admin123`
                        
                        **Features:**
                        - Full system access
                        - User management
                        - Analytics dashboard
                    """)
        
        # Features Section
        st.markdown('''
        <div class="feature-card">
            <div class="feature-title">
                <span>⭐</span>
                <span>Platform Features</span>
            </div>
            <div class="feature-item">AI-powered student lead scoring</div>
            <div class="feature-item">Real-time conversion prediction</div>
            <div class="feature-item">Advanced user management</div>
            <div class="feature-item">Export & reporting tools</div>
        </div>
        ''', unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)  # Close login-body
        st.markdown('</div>', unsafe_allow_html=True)  # Close login-container
        
        # Footer
        st.markdown('''
        <div style="text-align: center; margin-top: 30px; color: white; font-size: 0.9rem; opacity: 0.9;">
            <p>🔒 Secure & Encrypted | ⚡ Fast & Reliable | 📱 Mobile Responsive</p>
            <p style="opacity: 0.7; font-size: 0.85rem;">© 2024 Student Lead Scoring Pro. All rights reserved.</p>
        </div>
        ''', unsafe_allow_html=True)

# ============================================================================
# INITIALIZE
# ============================================================================

init_database()

# Initialize session state
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'user' not in st.session_state:
    st.session_state.user = None

# Check login
if not st.session_state.logged_in:
    show_login_page()
    st.stop()

# ============================================================================
# MAIN APPLICATION CSS (After Login)
# ============================================================================

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');
    
    /* Global Styles */
    * {
        font-family: 'Inter', sans-serif;
    }
    
    /* Main Background */
    [data-testid="stAppViewContainer"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    
    .block-container {
        padding-top: 1rem;
        padding-bottom: 2rem;
        max-width: 100%;
    }
    
    /* Header Styles */
    .main-header {
        font-size: 3.5rem;
        font-weight: 900;
        background: linear-gradient(135deg, #60a5fa 0%, #a78bfa 50%, #ec4899 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        padding: 2rem 0 0.5rem 0;
        margin-bottom: 0;
        letter-spacing: -0.03em;
    }
    
    .sub-header {
        text-align: center;
        color: white;
        font-size: 1.2rem;
        margin-bottom: 2rem;
        font-weight: 400;
        opacity: 0.95;
    }
    
    /* Sidebar Styling */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1e293b 0%, #0f172a 100%);
        padding: 1rem;
    }
    
    [data-testid="stSidebar"] * {
        color: white !important;
    }
    
    [data-testid="stSidebar"] .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 12px;
        padding: 0.75rem 1.5rem;
        font-weight: 700;
        font-size: 1rem;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
        transition: all 0.3s ease;
        width: 100%;
    }
    
    [data-testid="stSidebar"] .stButton > button:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.6);
    }
    
    /* User Info Card */
    .user-info {
        background: linear-gradient(135deg, rgba(102, 126, 234, 0.2) 0%, rgba(118, 75, 162, 0.2) 100%);
        padding: 20px;
        border-radius: 16px;
        margin-bottom: 24px;
        border: 2px solid rgba(102, 126, 234, 0.3);
        backdrop-filter: blur(10px);
    }
    
    /* Metric Cards */
    .metric-card {
        background: white;
        padding: 20px;
        border-radius: 16px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.1);
        transition: all 0.3s ease;
    }
    
    .metric-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 30px rgba(0,0,0,0.15);
    }
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 1rem;
        background: rgba(255, 255, 255, 0.1);
        padding: 0.5rem;
        border-radius: 16px;
        backdrop-filter: blur(10px);
    }
    
    .stTabs [data-baseweb="tab"] {
        background: transparent;
        border-radius: 12px;
        padding: 1rem 2rem;
        font-weight: 700;
        color: rgba(255, 255, 255, 0.7);
        border: none;
        transition: all 0.3s ease;
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        background: rgba(255, 255, 255, 0.1);
        color: white;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white !important;
        box-shadow: 0 4px 20px rgba(102, 126, 234, 0.4);
    }
    
    /* Buttons */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 12px;
        padding: 0.75rem 1.5rem;
        font-weight: 700;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.5);
    }
    
    /* Download Buttons */
    .stDownloadButton > button {
        background: linear-gradient(135deg, #10b981 0%, #059669 100%);
        color: white;
        border: none;
        border-radius: 12px;
        padding: 0.75rem 1.5rem;
        font-weight: 700;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(16, 185, 129, 0.3);
    }
    
    .stDownloadButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(16, 185, 129, 0.5);
    }
    
    /* DataFrames */
    [data-testid="stDataFrame"] {
        border-radius: 16px;
        overflow: hidden;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
    }
    
    .dataframe {
        border: none !important;
    }
    
    .dataframe thead tr th {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        color: white !important;
        font-weight: 700 !important;
        padding: 16px !important;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    .dataframe tbody tr:hover {
        background: rgba(102, 126, 234, 0.1) !important;
        transform: scale(1.005);
    }
    
    /* Info Boxes */
    .info-box {
        background: white;
        padding: 24px;
        border-radius: 16px;
        border-left: 4px solid #667eea;
        margin: 20px 0;
        box-shadow: 0 4px 20px rgba(0,0,0,0.1);
    }
    
    .success-box {
        background: linear-gradient(135deg, #e8f5e9 0%, #c8e6c9 100%);
        padding: 24px;
        border-radius: 16px;
        border-left: 4px solid #4caf50;
        margin: 20px 0;
        box-shadow: 0 4px 20px rgba(0,0,0,0.1);
    }
    
    /* Activity Card */
    .activity-card {
        background: rgba(255, 255, 255, 0.1);
        padding: 16px;
        border-radius: 12px;
        margin: 10px 0;
        border-left: 4px solid #667eea;
        backdrop-filter: blur(10px);
        transition: all 0.3s ease;
    }
    
    .activity-card:hover {
        transform: translateX(5px);
        background: rgba(255, 255, 255, 0.15);
    }
    
    /* Online Indicator */
    .online-indicator {
        display: inline-block;
        width: 10px;
        height: 10px;
        background: #10b981;
        border-radius: 50%;
        margin-right: 8px;
        animation: pulse-green 2s infinite;
        box-shadow: 0 0 10px #10b981;
    }
    
    @keyframes pulse-green {
        0%, 100% { opacity: 1; transform: scale(1); }
        50% { opacity: 0.6; transform: scale(1.1); }
    }
    
    /* Progress Bar */
    .stProgress > div > div > div > div {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        border-radius: 10px;
    }
    
    /* Expanders */
    .streamlit-expanderHeader {
        background: rgba(255, 255, 255, 0.1);
        border-radius: 12px;
        border: 2px solid rgba(255, 255, 255, 0.2);
        font-weight: 700;
        color: white;
        padding: 1rem;
        backdrop-filter: blur(10px);
    }
    
    .streamlit-expanderHeader:hover {
        border-color: rgba(255, 255, 255, 0.4);
        background: rgba(255, 255, 255, 0.15);
    }
    
    /* Mobile Responsive */
    @media (max-width: 768px) {
        .main-header {
            font-size: 2rem;
        }
        
        .sub-header {
            font-size: 1rem;
        }
    }
</style>
""", unsafe_allow_html=True)

# ============================================================================
# LOAD MODELS
# ============================================================================

with st.spinner("🔄 Loading AI models..."):
    best_model, scaler, label_encoders = load_models()

# ============================================================================
# SIDEBAR (Common for both Admin & User)
# ============================================================================

with st.sidebar:
    st.image("https://img.icons8.com/fluency/96/000000/student-male.png", width=80)
    st.title("🎓 Student Scorer")
    
    user_stats = get_user_stats(st.session_state.user['id'])
    
    st.markdown(f"""
    <div class='user-info'>
        <h3 style='color: #60a5fa !important;'>👤 {st.session_state.user['username']}</h3>
        <p style='margin: 8px 0; opacity: 0.9;'>Role: <b style='color: #a78bfa;'>{st.session_state.user['role'].upper()}</b></p>
        <hr style='margin: 12px 0; opacity: 0.3;'>
        <p style='margin: 6px 0;'>📊 Scorings: <b>{user_stats['total_scorings']}</b></p>
        <p style='margin: 6px 0;'>📄 Students: <b>{user_stats['total_leads']:,}</b></p>
        <p style='margin: 6px 0;'>🔑 Logins: <b>{user_stats['total_logins']}</b></p>
    </div>
    """, unsafe_allow_html=True)
    
    if st.button("🚪 LOGOUT", use_container_width=True):
        logout_user(st.session_state.user['id'])
        log_usage(st.session_state.user['id'], 'logout')
        st.session_state.logged_in = False
        st.session_state.user = None
        st.rerun()
    
    st.markdown("---")
    
    st.markdown("""
    ### 📊 About
    AI-powered tool for predicting student lead conversion
    
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

# ============================================================================
# ADMIN DASHBOARD
# ============================================================================

if st.session_state.user['role'] == 'admin':
    
    st.markdown('<div class="main-header">👑 ADMIN COMMAND CENTER</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Complete System Management & Student Lead Scoring</div>', unsafe_allow_html=True)
    
    # System Stats
    sys_stats = get_system_stats()
    
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.metric("👥 Users", sys_stats['total_users'])
    with col2:
        st.metric("🟢 Online", sys_stats['currently_online'])
    with col3:
        st.metric("📊 Scorings", sys_stats['total_scorings'])
    with col4:
        st.metric("📄 Students", f"{sys_stats['total_leads']:,}")
    with col5:
        st.metric("🕒 Today", sys_stats['today_logins'])
    
    st.markdown("---")
    
    # Main Admin Tabs
    admin_main_tab1, admin_main_tab2 = st.tabs([
        "🎯 STUDENT SCORING DASHBOARD",
        "👑 USER MANAGEMENT"
    ])
    
    # ========================================================================
    # ADMIN TAB 1: STUDENT SCORING DASHBOARD
    # ========================================================================
    
    with admin_main_tab1:
        st.markdown("## 🚀 Student Lead Scoring Engine")
        
        # File uploader
        st.markdown("### 📁 Upload Student Lead Data")
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            uploaded_file = st.file_uploader(
                "Drop your CSV file here or click to browse",
                type=["csv"],
                help="Upload CSV file containing student lead information"
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
                "📥 Download Sample CSV Template",
                csv_sample,
                "sample_student_leads.csv",
                "text/csv",
                use_container_width=True
            )
        
        st.markdown("---")
        
        if uploaded_file is not None:
            try:
                new_leads = pd.read_csv(uploaded_file)
                
                # Quick stats
                st.markdown("### 📊 Data Overview")
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    st.markdown(f"""
                    <div class="metric-card">
                        <h2 style="color: #667eea; margin: 0;">📋</h2>
                        <h3 style="margin: 10px 0;">{len(new_leads)}</h3>
                        <p style="color: #7f8c8d; margin: 0;">Total Leads</p>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col2:
                    st.markdown(f"""
                    <div class="metric-card">
                        <h2 style="color: #667eea; margin: 0;">📁</h2>
                        <h3 style="margin: 10px 0;">{len(new_leads.columns)}</h3>
                        <p style="color: #7f8c8d; margin: 0;">Columns</p>
                    </div>
                    """, unsafe_allow_html=True)
                
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
                
                # Display data
                with st.expander("👁️ View Uploaded Data", expanded=True):
                    st.dataframe(new_leads.head(10), use_container_width=True)
                
                # Process and predict
                st.markdown("### ⚙️ AI Processing Pipeline")
                progress_bar = st.progress(0)
                status_text = st.empty()
                
                status_text.text("🔄 Processing data...")
                progress_bar.progress(50)
                
                result_df, error = process_and_predict(new_leads, best_model, scaler, label_encoders)
                
                if error:
                    st.error(f"❌ Error: {error}")
                    st.stop()
                
                progress_bar.progress(100)
                status_text.text("✅ Processing complete!")
                
                log_usage(st.session_state.user['id'], 'score_leads', 'Admin scoring', len(result_df))
                
                st.markdown("---")
                
                # Results Dashboard
                st.markdown("### 🎯 Prediction Results Dashboard")
                
                high_score = (result_df['Lead_Score'] > 0.7).sum()
                medium_score = ((result_df['Lead_Score'] > 0.4) & (result_df['Lead_Score'] <= 0.7)).sum()
                low_score = (result_df['Lead_Score'] <= 0.4).sum()
                avg_score = result_df['Lead_Score_%'].mean()
                
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    st.metric("🟢 High Priority", high_score, f"{(high_score/len(result_df)*100):.1f}%")
                with col2:
                    st.metric("🟡 Medium Priority", medium_score, f"{(medium_score/len(result_df)*100):.1f}%")
                with col3:
                    st.metric("🔴 Low Priority", low_score, f"{(low_score/len(result_df)*100):.1f}%")
                with col4:
                    st.metric("📊 Average Score", f"{avg_score:.1f}%")
                
                st.markdown("---")
                
                # Visualizations
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown("#### 📊 Score Distribution")
                    fig = px.histogram(
                        result_df,
                        x='Lead_Score_%',
                        nbins=20,
                        color_discrete_sequence=['#667eea']
                    )
                    fig.update_layout(
                        showlegend=False,
                        height=400,
                        paper_bgcolor='rgba(0,0,0,0)',
                        plot_bgcolor='rgba(255,255,255,0.9)'
                    )
                    st.plotly_chart(fig, use_container_width=True)
                
                with col2:
                    st.markdown("#### 🎯 Priority Breakdown")
                    priority_counts = result_df['Priority'].value_counts()
                    fig = go.Figure(data=[go.Pie(
                        labels=priority_counts.index,
                        values=priority_counts.values,
                        hole=.4,
                        marker_colors=['#ef5350', '#ffa726', '#66bb6a']
                    )])
                    fig.update_layout(
                        height=400,
                        paper_bgcolor='rgba(0,0,0,0)'
                    )
                    st.plotly_chart(fig, use_container_width=True)
                
                # Results Table
                st.markdown("### 📋 Detailed Lead Scores")
                
                def highlight_priority(row):
                    if row['Lead_Score_%'] > 70:
                        return ['background-color: #e8f5e9'] * len(row)
                    elif row['Lead_Score_%'] > 40:
                        return ['background-color: #fff9c4'] * len(row)
                    else:
                        return ['background-color: #ffebee'] * len(row)
                
                st.dataframe(result_df.style.apply(highlight_priority, axis=1), use_container_width=True, height=400)
                
                # Export section
                st.markdown("---")
                st.markdown("### 💾 Export Results")
                
                col1, col2, col3 = st.columns([1, 2, 1])
                with col2:
                    csv = result_df.to_csv(index=False).encode('utf-8')
                    st.download_button(
                        "📥 Download Complete Report (CSV)",
                        csv,
                        f"Student_Lead_Scoring_{pd.Timestamp.now().strftime('%Y%m%d_%H%M%S')}.csv",
                        "text/csv",
                        use_container_width=True
                    )
                
                # Top leads
                st.markdown("---")
                st.markdown("### 🏆 Top 10 High-Priority Student Leads")
                top_leads = result_df.head(10)
                st.dataframe(top_leads, use_container_width=True)
                
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")
                with st.expander("🔍 Debug Info"):
                    st.code(str(e))
        
        else:
            st.markdown("""
                <div class="success-box">
                    <h3>✅ System Ready</h3>
                    <p>AI models loaded successfully. Upload student lead data to begin scoring.</p>
                </div>
            """, unsafe_allow_html=True)
    
    # ========================================================================
    # ADMIN TAB 2: USER MANAGEMENT
    # ========================================================================
    
    with admin_main_tab2:
        st.markdown("## 👑 User Management System")
        
        user_tab1, user_tab2, user_tab3, user_tab4 = st.tabs([
            "🟢 LIVE DASHBOARD",
            "➕ CREATE USER",
            "👥 MANAGE USERS",
            "📊 ACTIVITY LOG"
        ])
        
        with user_tab1:
            st.markdown("### 🟢 Live User Activity")
            
            if st.button("🔄 Refresh", key="admin_refresh"):
                st.rerun()
            
            active_users = get_currently_logged_in_users()
            
            if active_users:
                st.success(f"**{len(active_users)} user(s) online**")
                
                for user in active_users:
                    user_id, username, email, login_time, role = user
                    user_stats = get_user_stats(user_id)
                    
                    st.markdown(f"""
<div style='background: linear-gradient(135deg, rgba(16, 185, 129, 0.2) 0%, rgba(5, 150, 105, 0.1) 100%);
            padding: 20px; border-radius: 12px; margin: 12px 0; border: 2px solid rgba(16, 185, 129, 0.3);'>
    <span class='online-indicator'></span>
    <b style='color: white; font-size: 1.1rem;'>{username}</b> 
    <span style='color: #a7f3d0; margin-left: 10px;'>({role})</span><br>
    <small style='color: rgba(255,255,255,0.8);'>📧 {email if email else 'N/A'} | 🕒 {login_time}</small><br>
    <small style='color: rgba(255,255,255,0.9);'>📊 {user_stats['total_scorings']} scorings | 📄 {user_stats['total_leads']:,} students</small>
</div>
                    """, unsafe_allow_html=True)
            else:
                st.warning("No users currently online")
        
        with user_tab2:
            st.markdown("### ➕ Create New User")
            
            with st.form("create_user_form"):
                col_a, col_b = st.columns(2)
                with col_a:
                    new_username = st.text_input("Username *")
                    new_email = st.text_input("Email")
                with col_b:
                    new_password = st.text_input("Password *", type="password")
                    confirm_password = st.text_input("Confirm Password *", type="password")
                
                submitted = st.form_submit_button("✅ CREATE USER", type="primary", use_container_width=True)
                
                if submitted:
                    if new_username and new_password == confirm_password and len(new_password) >= 6:
                        if create_user_by_admin(new_username, new_password, new_email):
                            st.success(f"""
✅ User Created Successfully!

**Username:** `{new_username}`
**Password:** `{new_password}`
**Email:** `{new_email if new_email else 'Not provided'}`
                            """)
                        else:
                            st.error("❌ Username already exists!")
                    elif len(new_password) < 6:
                        st.error("❌ Password must be at least 6 characters")
                    else:
                        st.error("❌ Passwords don't match or fields are empty")
        
        with user_tab3:
            st.markdown("### 👥 All Users")
            
            users = get_all_users()
            user_data = []
            for user in users:
                user_data.append({
                    'ID': user[0],
                    'Username': user[1],
                    'Email': user[2] if user[2] else 'N/A',
                    'Created': user[3],
                    'Last Login': user[4] if user[4] else 'Never',
                    'Status': '🟢 Active' if user[5] else '🔴 Inactive',
                    'Role': user[6]
                })
            
            df_users = pd.DataFrame(user_data)
            st.dataframe(df_users, use_container_width=True, height=500)
            
            st.markdown("---")
            st.markdown("### ⚙️ User Actions")
            
            col_m1, col_m2, col_m3 = st.columns(3)
            with col_m1:
                user_id_action = st.number_input("User ID", min_value=1, step=1)
            with col_m2:
                action_type = st.selectbox("Action", ["Enable", "Disable", "Delete"])
            with col_m3:
                st.write("")
                if st.button("▶️ EXECUTE", type="primary"):
                    if user_id_action != 1:
                        if action_type == "Enable":
                            toggle_user_status(user_id_action, 1)
                            st.success("✅ User enabled!")
                            time.sleep(1)
                            st.rerun()
                        elif action_type == "Disable":
                            toggle_user_status(user_id_action, 0)
                            st.warning("⚠️ User disabled!")
                            time.sleep(1)
                            st.rerun()
                        elif action_type == "Delete":
                            delete_user(user_id_action)
                            st.error("🗑️ User deleted!")
                            time.sleep(1)
                            st.rerun()
                    else:
                        st.error("❌ Cannot modify admin account")
        
        with user_tab4:
            st.markdown("### 📊 System Activity Log")
            
            all_activities = get_all_user_activities()
            
            if all_activities:
                activity_data = []
                for activity in all_activities:
                    username, action, details, leads_scored, timestamp = activity
                    activity_data.append({
                        'Username': username,
                        'Action': action,
                        'Details': details if details else '-',
                        'Leads': leads_scored if leads_scored else '-',
                        'Timestamp': timestamp
                    })
                
                df_activities = pd.DataFrame(activity_data)
                st.dataframe(df_activities, use_container_width=True, height=600)
            else:
                st.info("No activities logged yet")

# ============================================================================
# USER DASHBOARD
# ============================================================================

else:
    
    st.markdown('<div class="main-header">🎓 STUDENT LEAD SCORING</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">AI-Powered Student Conversion Prediction Platform</div>', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="success-box">
        <h3>✅ System Ready</h3>
        <p>AI models loaded successfully. Upload your student lead data to begin scoring.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Instructions
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
    
    # File uploader
    st.markdown("## 📁 Upload Student Lead Data")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        uploaded_file = st.file_uploader(
            "Drop your CSV file here or click to browse",
            type=["csv"],
            help="Upload CSV file containing student lead information"
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
            "📥 Download Sample CSV Template",
            csv_sample,
            "sample_student_leads.csv",
            "text/csv",
            use_container_width=True
        )
    
    st.markdown("---")
    
    if uploaded_file is not None:
        try:
            new_leads = pd.read_csv(uploaded_file)
            
            # Quick stats
            st.markdown("## 📊 Data Analysis Dashboard")
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.markdown(f"""
                <div class="metric-card">
                    <h2 style="color: #667eea; margin: 0;">📋</h2>
                    <h3 style="margin: 10px 0;">{len(new_leads)}</h3>
                    <p style="color: #7f8c8d; margin: 0;">Total Leads</p>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                st.markdown(f"""
                <div class="metric-card">
                    <h2 style="color: #667eea; margin: 0;">📁</h2>
                    <h3 style="margin: 10px 0;">{len(new_leads.columns)}</h3>
                    <p style="color: #7f8c8d; margin: 0;">Columns</p>
                </div>
                """, unsafe_allow_html=True)
            
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
            
            # Display data
            with st.expander("👁️ View Uploaded Data", expanded=True):
                st.dataframe(new_leads.head(10), use_container_width=True)
            
            # Process
            st.markdown("## ⚙️ AI Processing Pipeline")
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            status_text.text("🔄 Processing data...")
            progress_bar.progress(50)
            
            result_df, error = process_and_predict(new_leads, best_model, scaler, label_encoders)
            
            if error:
                st.error(f"❌ Error: {error}")
                st.stop()
            
            progress_bar.progress(100)
            status_text.text("✅ Processing complete!")
            
            log_usage(st.session_state.user['id'], 'score_leads', 'User scoring', len(result_df))
            
            st.markdown("---")
            
            # Results
            st.markdown("## 🎯 Prediction Results Dashboard")
            
            high_score = (result_df['Lead_Score'] > 0.7).sum()
            medium_score = ((result_df['Lead_Score'] > 0.4) & (result_df['Lead_Score'] <= 0.7)).sum()
            low_score = (result_df['Lead_Score'] <= 0.4).sum()
            avg_score = result_df['Lead_Score_%'].mean()
            
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("🟢 High Priority", high_score, f"{(high_score/len(result_df)*100):.1f}%")
            with col2:
                st.metric("🟡 Medium Priority", medium_score, f"{(medium_score/len(result_df)*100):.1f}%")
            with col3:
                st.metric("🔴 Low Priority", low_score, f"{(low_score/len(result_df)*100):.1f}%")
            with col4:
                st.metric("📊 Average Score", f"{avg_score:.1f}%")
            
            st.markdown("<br>", unsafe_allow_html=True)
            
            # Visualizations
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("### 📊 Score Distribution")
                fig = px.histogram(
                    result_df,
                    x='Lead_Score_%',
                    nbins=20,
                    color_discrete_sequence=['#667eea']
                )
                fig.update_layout(
                    showlegend=False,
                    height=400,
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(255,255,255,0.9)'
                )
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                st.markdown("### 🎯 Priority Breakdown")
                priority_counts = result_df['Priority'].value_counts()
                fig = go.Figure(data=[go.Pie(
                    labels=priority_counts.index,
                    values=priority_counts.values,
                    hole=.4,
                    marker_colors=['#ef5350', '#ffa726', '#66bb6a']
                )])
                fig.update_layout(
                    height=400,
                    paper_bgcolor='rgba(0,0,0,0)'
                )
                st.plotly_chart(fig, use_container_width=True)
            
            # Results Table
            st.markdown("### 📋 Detailed Lead Scores")
            
            def highlight_priority(row):
                if row['Lead_Score_%'] > 70:
                    return ['background-color: #e8f5e9'] * len(row)
                elif row['Lead_Score_%'] > 40:
                    return ['background-color: #fff9c4'] * len(row)
                else:
                    return ['background-color: #ffebee'] * len(row)
            
            st.dataframe(result_df.style.apply(highlight_priority, axis=1), use_container_width=True, height=400)
            
            # Export
            st.markdown("---")
            st.markdown("## 💾 Export Results")
            
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                csv = result_df.to_csv(index=False).encode('utf-8')
                st.download_button(
                    "📥 Download Complete Report (CSV)",
                    csv,
                    f"Student_Lead_Scoring_{pd.Timestamp.now().strftime('%Y%m%d_%H%M%S')}.csv",
                    "text/csv",
                    use_container_width=True
                )
            
            # Top leads
            st.markdown("---")
            st.markdown("## 🏆 Top 10 High-Priority Student Leads")
            top_leads = result_df.head(10)
            st.dataframe(top_leads, use_container_width=True)
            
        except Exception as e:
            st.error(f"❌ Error: {str(e)}")
            with st.expander("🔍 Debug Info"):
                st.code(str(e))

# Footer
st.markdown("---")
st.markdown(f"""
<div style='text-align: center; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
            padding: 20px; border-radius: 10px; color: white;'>
    <p style='margin: 0;'>🔐 Logged in as: <b>{st.session_state.user['username']}</b> ({st.session_state.user['role']}) | {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}</p>
    <h3 style='color: white; margin: 10px 0 0 0;'>🎓 Student Lead Scoring Intelligence Platform</h3>
    <p style='margin: 5px 0 0 0;'>Powered by Machine Learning | Built with Streamlit & Python | © 2024</p>
</div>
""", unsafe_allow_html=True)
