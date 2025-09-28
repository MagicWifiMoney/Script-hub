"""
Premium UI Components for Marketing Agency Script Hub
Modern, trendy design with dark theme and gradient aesthetics
"""

import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime
import time

def apply_premium_theme():
    """Apply premium dark theme with modern gradients and styling"""

    st.markdown("""
    <style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

    /* Root variables for consistent theming */
    :root {
        --primary-gradient: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        --success-gradient: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
        --warning-gradient: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        --dark-bg: #0f1419;
        --card-bg: #1a1d24;
        --accent-purple: #8b5cf6;
        --accent-cyan: #06b6d4;
        --text-primary: #ffffff;
        --text-secondary: #94a3b8;
        --border-color: #2d3748;
    }

    /* Main app container */
    .stApp {
        background: linear-gradient(135deg, #0f1419 0%, #1a1d24 50%, #2d3748 100%);
        font-family: 'Inter', sans-serif;
    }

    /* Hide default Streamlit styling */
    #MainMenu, .stDeployButton, footer, header {
        visibility: hidden !important;
        height: 0 !important;
    }

    /* Custom header */
    .premium-header {
        background: var(--primary-gradient);
        padding: 2rem 3rem;
        border-radius: 20px;
        margin: 1rem 0 2rem 0;
        border: 1px solid rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        box-shadow: 0 20px 40px rgba(0, 0, 0, 0.3);
    }

    .premium-title {
        font-size: 3rem;
        font-weight: 800;
        background: linear-gradient(45deg, #ffffff, #f1f5f9);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        text-align: center;
        margin: 0;
        text-shadow: 0 0 30px rgba(255, 255, 255, 0.5);
    }

    .premium-subtitle {
        font-size: 1.2rem;
        color: rgba(255, 255, 255, 0.8);
        text-align: center;
        margin: 0.5rem 0 0 0;
        font-weight: 400;
    }

    /* Tool cards */
    .tool-card {
        background: linear-gradient(135deg, rgba(255, 255, 255, 0.1), rgba(255, 255, 255, 0.05));
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 16px;
        padding: 2rem;
        margin: 1rem 0;
        backdrop-filter: blur(10px);
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    }

    .tool-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 25px 50px rgba(139, 92, 246, 0.25);
        border-color: var(--accent-purple);
    }

    .tool-card::before {
        content: '';
        position: absolute;
        top: -2px;
        left: -2px;
        right: -2px;
        bottom: -2px;
        background: var(--primary-gradient);
        border-radius: 16px;
        z-index: -1;
        opacity: 0;
        transition: opacity 0.3s ease;
    }

    .tool-card:hover::before {
        opacity: 0.3;
    }

    /* Status indicators */
    .status-premium {
        display: inline-block;
        padding: 0.5rem 1rem;
        border-radius: 25px;
        font-size: 0.9rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }

    .status-active {
        background: var(--success-gradient);
        color: white;
        box-shadow: 0 4px 15px rgba(17, 153, 142, 0.4);
    }

    .status-enhanced {
        background: var(--warning-gradient);
        color: white;
        box-shadow: 0 4px 15px rgba(240, 147, 251, 0.4);
    }

    /* Buttons */
    .stButton > button {
        background: var(--primary-gradient) !important;
        color: white !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 0.75rem 2rem !important;
        font-weight: 600 !important;
        font-family: 'Inter', sans-serif !important;
        text-transform: uppercase !important;
        letter-spacing: 0.5px !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.3) !important;
    }

    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 12px 35px rgba(102, 126, 234, 0.5) !important;
    }

    /* Input fields */
    .stTextInput > div > div > input,
    .stSelectbox > div > div > select,
    .stTextArea > div > div > textarea {
        background: rgba(255, 255, 255, 0.1) !important;
        color: white !important;
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
        border-radius: 8px !important;
        backdrop-filter: blur(5px) !important;
        font-family: 'Inter', sans-serif !important;
    }

    .stTextInput > div > div > input:focus,
    .stSelectbox > div > div > select:focus,
    .stTextArea > div > div > textarea:focus {
        border-color: var(--accent-purple) !important;
        box-shadow: 0 0 20px rgba(139, 92, 246, 0.3) !important;
    }

    /* Expanders */
    .streamlit-expanderHeader {
        background: linear-gradient(90deg, rgba(255, 255, 255, 0.1), rgba(255, 255, 255, 0.05)) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 12px !important;
        color: white !important;
        font-weight: 600 !important;
        font-family: 'Inter', sans-serif !important;
    }

    .streamlit-expanderContent {
        background: rgba(26, 29, 36, 0.8) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 0 0 12px 12px !important;
        backdrop-filter: blur(10px) !important;
    }

    /* Metrics */
    .metric-card {
        background: linear-gradient(135deg, rgba(6, 182, 212, 0.1), rgba(139, 92, 246, 0.1));
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 12px;
        padding: 1.5rem;
        text-align: center;
        margin: 0.5rem;
    }

    .metric-value {
        font-size: 2.5rem;
        font-weight: 700;
        background: linear-gradient(45deg, var(--accent-cyan), var(--accent-purple));
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }

    .metric-label {
        color: var(--text-secondary);
        font-size: 0.9rem;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-top: 0.5rem;
    }

    /* Loading animations */
    @keyframes pulse-glow {
        0%, 100% { box-shadow: 0 0 20px rgba(139, 92, 246, 0.5); }
        50% { box-shadow: 0 0 40px rgba(139, 92, 246, 0.8); }
    }

    .loading-premium {
        animation: pulse-glow 2s infinite;
        border-radius: 12px;
        background: linear-gradient(45deg, rgba(139, 92, 246, 0.1), rgba(6, 182, 212, 0.1));
    }

    /* Success/Error alerts */
    .stSuccess, .stError, .stWarning, .stInfo {
        border-radius: 12px !important;
        border: none !important;
        backdrop-filter: blur(10px) !important;
    }

    .stSuccess {
        background: linear-gradient(135deg, rgba(17, 153, 142, 0.2), rgba(56, 239, 125, 0.2)) !important;
        border-left: 4px solid #38ef7d !important;
    }

    .stError {
        background: linear-gradient(135deg, rgba(240, 147, 251, 0.2), rgba(245, 87, 108, 0.2)) !important;
        border-left: 4px solid #f5576c !important;
    }

    /* Sidebar styling */
    .css-1d391kg {
        background: linear-gradient(180deg, var(--dark-bg), var(--card-bg)) !important;
    }

    /* Code blocks */
    .stCode {
        background: rgba(15, 20, 25, 0.8) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 12px !important;
        backdrop-filter: blur(10px) !important;
    }

    /* Progress bars */
    .stProgress > div > div > div > div {
        background: var(--primary-gradient) !important;
        border-radius: 10px !important;
    }
    </style>
    """, unsafe_allow_html=True)

def premium_header():
    """Display premium header with modern styling"""
    st.markdown("""
    <div class="premium-header">
        <h1 class="premium-title">⚡ FERMAT AI MARKETING HUB</h1>
        <p class="premium-subtitle">Autonomous Marketing Intelligence • Real-Time Analysis • Premium Results</p>
    </div>
    """, unsafe_allow_html=True)

def premium_metrics_row(metrics_data):
    """Display metrics in premium card layout"""
    cols = st.columns(len(metrics_data))

    for i, (label, value, icon) in enumerate(metrics_data):
        with cols[i]:
            st.markdown(f"""
            <div class="metric-card">
                <div style="font-size: 2rem; margin-bottom: 0.5rem;">{icon}</div>
                <div class="metric-value">{value}</div>
                <div class="metric-label">{label}</div>
            </div>
            """, unsafe_allow_html=True)

def premium_tool_card(tool_name, description, status, icon, category):
    """Display tool in premium card format"""

    status_class = "status-active" if "✅" in status else "status-enhanced"

    st.markdown(f"""
    <div class="tool-card">
        <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 1rem;">
            <div style="display: flex; align-items: center; gap: 1rem;">
                <div style="font-size: 2.5rem;">{icon}</div>
                <div>
                    <h3 style="margin: 0; color: white; font-size: 1.5rem; font-weight: 700;">{tool_name}</h3>
                    <p style="margin: 0.5rem 0 0 0; color: #94a3b8; font-size: 0.9rem; text-transform: uppercase; letter-spacing: 1px;">{category}</p>
                </div>
            </div>
            <span class="status-premium {status_class}">{status}</span>
        </div>
        <p style="color: #e2e8f0; line-height: 1.6; margin: 0;">{description}</p>
    </div>
    """, unsafe_allow_html=True)

def premium_loading_animation(message="Processing your request..."):
    """Show premium loading animation"""
    st.markdown(f"""
    <div class="loading-premium" style="padding: 2rem; text-align: center; margin: 2rem 0;">
        <div style="font-size: 3rem; margin-bottom: 1rem;">⚡</div>
        <h3 style="color: white; margin: 0;">{message}</h3>
        <p style="color: #94a3b8; margin: 0.5rem 0;">This may take 30-60 seconds for real-time analysis</p>
    </div>
    """, unsafe_allow_html=True)

    # Add progress bar
    progress_bar = st.progress(0)
    for i in range(100):
        time.sleep(0.01)
        progress_bar.progress(i + 1)
    progress_bar.empty()

def premium_success_banner(title, message):
    """Display premium success banner"""
    st.markdown(f"""
    <div style="background: var(--success-gradient); padding: 2rem; border-radius: 16px; margin: 2rem 0; text-align: center; color: white;">
        <div style="font-size: 3rem; margin-bottom: 1rem;">🎯</div>
        <h2 style="margin: 0 0 0.5rem 0; font-weight: 700;">{title}</h2>
        <p style="margin: 0; font-size: 1.1rem; opacity: 0.9;">{message}</p>
    </div>
    """, unsafe_allow_html=True)

def premium_dashboard_stats():
    """Display premium dashboard statistics"""

    # System health metrics
    import psutil

    cpu_usage = psutil.cpu_percent()
    memory = psutil.virtual_memory()

    metrics = [
        ("CPU Usage", f"{cpu_usage}%", "🚀"),
        ("Memory", f"{memory.percent}%", "💾"),
        ("Active Tools", "8", "⚡"),
        ("API Status", "Connected", "🌐")
    ]

    premium_metrics_row(metrics)

def premium_feature_spotlight():
    """Highlight premium features"""
    st.markdown("""
    <div style="background: linear-gradient(135deg, rgba(139, 92, 246, 0.1), rgba(6, 182, 212, 0.1));
         border: 1px solid rgba(255, 255, 255, 0.1); border-radius: 16px; padding: 2rem; margin: 2rem 0;">
        <h3 style="color: white; margin: 0 0 1rem 0; font-size: 1.5rem;">✨ Premium Features Active</h3>
        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 1rem;">
            <div style="color: #e2e8f0;">🎯 <strong>Real-Time SEO Analysis</strong><br><small>Live website auditing with 15+ data sources</small></div>
            <div style="color: #e2e8f0;">🤖 <strong>Autonomous AI Generation</strong><br><small>Zero-prompt content creation and strategy</small></div>
            <div style="color: #e2e8f0;">⚡ <strong>Lightning-Fast Processing</strong><br><small>Results in under 60 seconds</small></div>
            <div style="color: #e2e8f0;">💎 <strong>Premium API Integration</strong><br><small>Claude, DataForSEO, Keywords Everywhere</small></div>
        </div>
    </div>
    """, unsafe_allow_html=True)

def create_premium_visualization(title, data_type="seo_score"):
    """Create premium data visualization"""

    if data_type == "seo_score":
        # Create a premium gauge chart
        fig = go.Figure(go.Indicator(
            mode = "gauge+number+delta",
            value = 85,
            domain = {'x': [0, 1], 'y': [0, 1]},
            title = {'text': title, 'font': {'color': 'white'}},
            delta = {'reference': 70},
            gauge = {
                'axis': {'range': [None, 100], 'tickcolor': 'white'},
                'bar': {'color': "#8b5cf6"},
                'steps': [
                    {'range': [0, 50], 'color': "#f5576c"},
                    {'range': [50, 80], 'color': "#f093fb"},
                    {'range': [80, 100], 'color': "#38ef7d"}
                ],
                'threshold': {
                    'line': {'color': "white", 'width': 4},
                    'thickness': 0.75,
                    'value': 85
                }
            }
        ))

        fig.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font={'color': 'white'},
            height=300
        )

        return fig

    return None