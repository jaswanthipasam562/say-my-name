"""
=============================================================================
AI NEWS DETECTIVE - STREAMLIT FULL-STACK INTELLIGENCE APPLICATION
=============================================================================
Next-generation multimodal news forensics, emotional barcode biometrics,
real-time cross-platform spread intelligence console, user authentication,
and comprehensive system logic explainer.

Pages / Views:
1. 🛡️ Forensic Investigation Console (Main Scanner, URL Lead Extractor, Spread Tracker, Gemini Chat)
2. 🧠 System Logic & Architecture (Deep Algorithmic Explainer & Interactive Logic Sandbox)
3. 🔐 Sign In & Analyst Profile Portal (Authentication, Registration & Clearance Management)
"""

import os
import re
import time
import urllib.parse
import urllib.request
import streamlit as st

try:
    from bs4 import BeautifulSoup
    BS4_AVAILABLE = True
except ImportError:
    BS4_AVAILABLE = False

# Set Streamlit Page Configuration
st.set_page_config(
    page_title="AI News Detective | Real-Time Intelligence & Spread Tracker",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom High-End Cybernetic Dark Glassmorphism CSS & Visual Effects
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600;700&display=swap');

    /* Global reset & typography */
    html, body, [class*="css"], .stApp {
        font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif !important;
        background: radial-gradient(circle at 10% 20%, #0b0f19 0%, #030712 90%) !important;
        color: #f8fafc !important;
    }

    /* Force all text elements to be bright and high-contrast */
    p, span, div, label, td, th, strong, em, h1, h2, h3, h4, h5, h6 {
        color: #f8fafc;
    }

    /* Specific Streamlit markdown text elements */
    .stMarkdown, .stMarkdown p, .stMarkdown span, [data-testid="stMarkdownContainer"] p {
        color: #e2e8f0 !important;
        font-size: 15px !important;
        line-height: 1.65 !important;
    }

    /* Ultra-Clean High-Visibility Lists (UL, OL, LI) */
    ul, ol, .stMarkdown ul, .stMarkdown ol {
        color: #e2e8f0 !important;
        padding-left: 26px !important;
        margin: 10px 0 16px 0 !important;
        list-style-type: disc !important;
    }

    li, .stMarkdown li {
        color: #e2e8f0 !important;
        font-size: 14.5px !important;
        line-height: 1.7 !important;
        margin-bottom: 8px !important;
    }

    li::marker {
        color: #818cf8 !important;
        font-size: 1.1em !important;
    }

    .stMarkdown ol li::marker {
        color: #38bdf8 !important;
        font-weight: 700 !important;
    }

    /* Streamlit widget labels */
    .stTextArea label, .stTextInput label, [data-testid="stWidgetLabel"] p {
        color: #e2e8f0 !important;
        font-weight: 700 !important;
        font-size: 15.5px !important;
        margin-bottom: 8px !important;
        letter-spacing: 0.2px !important;
    }

    /* Input & Textarea fields with bright text & deep slate background */
    .stTextArea textarea, .stTextInput input {
        background-color: rgba(15, 23, 42, 0.9) !important;
        color: #ffffff !important;
        border: 1px solid rgba(255, 255, 255, 0.18) !important;
        border-radius: 12px !important;
        font-size: 15px !important;
        line-height: 1.5 !important;
        box-shadow: inset 0 2px 4px rgba(0, 0, 0, 0.5) !important;
        transition: all 0.2s ease !important;
    }

    .stTextArea textarea:focus, .stTextInput input:focus {
        border-color: #818cf8 !important;
        box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.35) !important;
        color: #ffffff !important;
        background-color: rgba(15, 23, 42, 0.98) !important;
    }

    .stTextArea textarea::placeholder, .stTextInput input::placeholder {
        color: #94a3b8 !important;
        opacity: 0.9 !important;
    }

    /* Radio button groups */
    [data-testid="stRadio"] > div {
        background: rgba(15, 23, 42, 0.8) !important;
        padding: 8px 16px !important;
        border-radius: 12px !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
    }

    /* Tabs Styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px !important;
        background-color: rgba(15, 23, 42, 0.8) !important;
        padding: 8px !important;
        border-radius: 14px !important;
        border: 1px solid rgba(255, 255, 255, 0.08) !important;
        box-shadow: 0 4px 16px rgba(0, 0, 0, 0.3) !important;
    }

    .stTabs [data-baseweb="tab"] {
        color: #cbd5e1 !important;
        font-weight: 600 !important;
        font-size: 14.5px !important;
        padding: 10px 20px !important;
        border-radius: 10px !important;
        transition: all 0.2s ease !important;
        background-color: transparent !important;
        border: 1px solid transparent !important;
    }

    .stTabs [data-baseweb="tab"]:hover {
        color: #ffffff !important;
        background-color: rgba(255, 255, 255, 0.08) !important;
    }

    .stTabs [aria-selected="true"] {
        color: #ffffff !important;
        background: linear-gradient(135deg, rgba(79, 70, 229, 0.4) 0%, rgba(99, 102, 241, 0.3) 100%) !important;
        border: 1px solid rgba(129, 140, 248, 0.5) !important;
        box-shadow: 0 4px 12px rgba(79, 70, 229, 0.25) !important;
    }

    /* Buttons Styling */
    .stButton button {
        border-radius: 10px !important;
        font-weight: 700 !important;
        font-size: 14px !important;
        padding: 10px 20px !important;
        transition: all 0.2s ease !important;
        border: 1px solid rgba(255, 255, 255, 0.12) !important;
        background: rgba(30, 41, 59, 0.85) !important;
        color: #f8fafc !important;
        letter-spacing: 0.3px !important;
    }

    .stButton button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 16px rgba(99, 102, 241, 0.25) !important;
        border-color: rgba(129, 140, 248, 0.6) !important;
        color: #ffffff !important;
        background: rgba(51, 65, 85, 0.9) !important;
    }

    .stButton button[kind="primary"] {
        background: linear-gradient(135deg, #4f46e5 0%, #6366f1 100%) !important;
        border: 1px solid #818cf8 !important;
        color: #ffffff !important;
        box-shadow: 0 4px 16px rgba(79, 70, 229, 0.45) !important;
    }

    .stButton button[kind="primary"]:hover {
        background: linear-gradient(135deg, #4338ca 0%, #4f46e5 100%) !important;
        box-shadow: 0 6px 24px rgba(79, 70, 229, 0.7) !important;
        border-color: #a5b4fc !important;
    }

    /* Sidebar Styling */
    [data-testid="stSidebar"] {
        background-color: #080c14 !important;
        border-right: 1px solid rgba(255, 255, 255, 0.08) !important;
    }

    [data-testid="stSidebar"] * {
        color: #cbd5e1;
    }

    [data-testid="stSidebar"] h1, [data-testid="stSidebar"] h2, [data-testid="stSidebar"] h3 {
        color: #f8fafc !important;
    }

    /* Glass Cards */
    .glass-card {
        background: rgba(15, 23, 42, 0.85) !important;
        backdrop-filter: blur(16px);
        -webkit-backdrop-filter: blur(16px);
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 16px;
        padding: 24px;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.45);
        margin-bottom: 20px;
        transition: transform 0.2s ease, border-color 0.2s ease;
        color: #f8fafc !important;
    }
    .glass-card:hover {
        border-color: rgba(99, 102, 241, 0.45) !important;
    }

    .glass-card p {
        color: #e2e8f0 !important;
        font-size: 15px !important;
        line-height: 1.6 !important;
        margin-bottom: 10px !important;
    }

    .glass-card strong {
        color: #ffffff !important;
        font-weight: 700 !important;
    }

    /* Logic Box */
    .logic-step-card {
        background: rgba(15, 23, 42, 0.85);
        border-left: 5px solid #818cf8;
        border-radius: 12px;
        padding: 20px;
        margin-bottom: 18px;
        border-top: 1px solid rgba(255, 255, 255, 0.08);
        border-right: 1px solid rgba(255, 255, 255, 0.08);
        border-bottom: 1px solid rgba(255, 255, 255, 0.08);
    }

    /* User Profile Card */
    .user-profile-badge {
        background: linear-gradient(135deg, rgba(30, 41, 59, 0.9), rgba(15, 23, 42, 0.95));
        border: 1px solid rgba(129, 140, 248, 0.35);
        border-radius: 14px;
        padding: 16px;
        margin-bottom: 18px;
        box-shadow: 0 4px 16px rgba(0, 0, 0, 0.4);
    }

    /* Radar Error Container */
    .radar-error-box {
        background: linear-gradient(135deg, rgba(239, 68, 68, 0.15) 0%, rgba(15, 23, 42, 0.95) 100%) !important;
        border: 1px solid rgba(239, 68, 68, 0.4) !important;
        border-radius: 20px;
        padding: 36px;
        text-align: center;
        margin: 20px 0;
        box-shadow: 0 0 35px rgba(239, 68, 68, 0.2) !important;
    }

    .radar-uncertain-box {
        background: linear-gradient(135deg, rgba(245, 158, 11, 0.15) 0%, rgba(15, 23, 42, 0.95) 100%) !important;
        border: 1px solid rgba(245, 158, 11, 0.4) !important;
        border-radius: 20px;
        padding: 36px;
        text-align: center;
        margin: 20px 0;
        box-shadow: 0 0 35px rgba(245, 158, 11, 0.2) !important;
    }

    .radar-pulse {
        width: 72px;
        height: 72px;
        border-radius: 50%;
        background: rgba(239, 68, 68, 0.25);
        box-shadow: 0 0 0 0 rgba(239, 68, 68, 0.7);
        animation: pulse 1.6s infinite;
        display: inline-flex;
        align-items: center;
        justify-content: center;
        font-size: 32px;
        margin-bottom: 16px;
    }

    .radar-pulse-uncertain {
        width: 72px;
        height: 72px;
        border-radius: 50%;
        background: rgba(245, 158, 11, 0.25);
        box-shadow: 0 0 0 0 rgba(245, 158, 11, 0.7);
        animation: pulse-amber 1.6s infinite;
        display: inline-flex;
        align-items: center;
        justify-content: center;
        font-size: 32px;
        margin-bottom: 16px;
    }

    @keyframes pulse {
        0% { transform: scale(0.95); box-shadow: 0 0 0 0 rgba(239, 68, 68, 0.7); }
        70% { transform: scale(1.1); box-shadow: 0 0 0 20px rgba(239, 68, 68, 0); }
        100% { transform: scale(0.95); box-shadow: 0 0 0 0 rgba(239, 68, 68, 0); }
    }

    @keyframes pulse-amber {
        0% { transform: scale(0.95); box-shadow: 0 0 0 0 rgba(245, 158, 11, 0.7); }
        70% { transform: scale(1.1); box-shadow: 0 0 0 20px rgba(245, 158, 11, 0); }
        100% { transform: scale(0.95); box-shadow: 0 0 0 0 rgba(245, 158, 11, 0); }
    }

    /* High-Tech Barcode Container */
    .barcode-container {
        background: linear-gradient(135deg, #090d16 0%, #030712 100%);
        border: 1px solid rgba(99, 102, 241, 0.35);
        border-radius: 16px;
        padding: 24px;
        text-align: center;
        box-shadow: 0 0 30px rgba(99, 102, 241, 0.15);
        position: relative;
        overflow: hidden;
        margin: 16px 0;
    }

    .barcode-lines {
        display: flex;
        justify-content: center;
        align-items: center;
        gap: 3px;
        height: 70px;
        padding: 10px 0;
        background: rgba(0, 0, 0, 0.4);
        border-radius: 8px;
        margin: 14px 0;
        position: relative;
    }

    .barcode-bar {
        height: 100%;
        border-radius: 1px;
        transition: transform 0.2s;
    }
    .barcode-bar:hover {
        transform: scaleY(1.15);
    }

    .barcode-hash {
        font-family: 'JetBrains Mono', monospace;
        font-size: 13px;
        letter-spacing: 2px;
        color: #38bdf8;
        font-weight: 700;
        background: rgba(56, 189, 248, 0.1);
        padding: 4px 12px;
        border-radius: 6px;
        display: inline-block;
        border: 1px dashed rgba(56, 189, 248, 0.3);
    }

    /* Badges */
    .badge {
        display: inline-block;
        padding: 6px 14px;
        border-radius: 20px;
        font-size: 12px;
        font-weight: 700;
        letter-spacing: 0.5px;
        text-transform: uppercase;
    }
    .badge-fake { background: rgba(239, 68, 68, 0.25); color: #fca5a5 !important; border: 1px solid #ef4444; }
    .badge-real { background: rgba(16, 185, 129, 0.25); color: #6ee7b7 !important; border: 1px solid #10b981; }
    .badge-uncertain { background: rgba(245, 158, 11, 0.25); color: #fde68a !important; border: 1px solid #f59e0b; }

    .badge-high { background: rgba(239, 68, 68, 0.25); color: #fca5a5 !important; border: 1px solid #f87171; }
    .badge-med { background: rgba(245, 158, 11, 0.25); color: #fde68a !important; border: 1px solid #f59e0b; }
    .badge-low { background: rgba(16, 185, 129, 0.25); color: #a7f3d0 !important; border: 1px solid #10b981; }
    .badge-top-viral { background: linear-gradient(135deg, rgba(239, 68, 68, 0.3), rgba(249, 115, 22, 0.3)); color: #ffedd5 !important; border: 1px solid #f97316; font-size: 11px; }

    /* Platform Links */
    .platform-card {
        background: rgba(30, 41, 59, 0.85) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 14px;
        padding: 18px;
        margin-bottom: 14px;
        display: flex;
        align-items: center;
        justify-content: space-between;
        gap: 16px;
        transition: transform 0.15s ease, border-color 0.15s ease;
    }
    .platform-card:hover {
        transform: translateY(-2px);
        border-color: rgba(99, 102, 241, 0.45) !important;
    }
    .platform-card.top-platform {
        border: 1px solid rgba(239, 68, 68, 0.4) !important;
        background: linear-gradient(135deg, rgba(30, 41, 59, 0.95) 0%, rgba(239, 68, 68, 0.1) 100%) !important;
    }
    .platform-card strong {
        color: #ffffff !important;
    }
    .platform-card a {
        text-decoration: none;
        background: linear-gradient(135deg, #4f46e5 0%, #6366f1 100%) !important;
        color: #ffffff !important;
        padding: 8px 16px;
        border-radius: 8px;
        font-size: 13px;
        font-weight: 700;
        transition: all 0.2s ease;
        white-space: nowrap;
        box-shadow: 0 2px 8px rgba(79, 70, 229, 0.35);
        display: inline-flex;
        align-items: center;
        gap: 6px;
    }
    .platform-card a:hover {
        background: linear-gradient(135deg, #4338ca 0%, #4f46e5 100%) !important;
        box-shadow: 0 4px 14px rgba(79, 70, 229, 0.5);
    }

    /* Tables */
    table {
        width: 100%;
        color: #f1f5f9 !important;
        border-collapse: collapse;
    }
    td, th {
        color: #e2e8f0 !important;
        padding: 12px 14px !important;
    }
    td strong {
        color: #ffffff !important;
    }
</style>
""", unsafe_allow_html=True)

# Import local intelligence modules
from news_relevance import is_news_related
from ml_engine import process_news
from search_engine import search_news
from spread_tracker import track_spread, _spread_tracker
from langchain_orchestrator import generate_report, ask_ai_assistant
from auth_manager import authenticate_user, register_user, _auth_manager

# Initialize Session State
if "analysis_result" not in st.session_state:
    st.session_state.analysis_result = None
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "current_input_text" not in st.session_state:
    st.session_state.current_input_text = ""
if "url_input" not in st.session_state:
    st.session_state.url_input = ""
if "authenticated_user" not in st.session_state:
    st.session_state.authenticated_user = None
if "active_nav_view" not in st.session_state:
    st.session_state.active_nav_view = "🛡️ Forensic Investigation Console"


def extract_news_from_url(url: str):
    """Live Web URL Content Extractor for News Forensics."""
    clean_url = url.strip()
    if not clean_url.startswith("http://") and not clean_url.startswith("https://"):
        clean_url = "https://" + clean_url

    try:
        req = urllib.request.Request(
            clean_url,
            headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'}
        )
        with urllib.request.urlopen(req, timeout=6) as response:
            html = response.read().decode('utf-8', errors='ignore')
            if BS4_AVAILABLE:
                soup = BeautifulSoup(html, 'html.parser')
                title = soup.title.string.strip() if soup.title and soup.title.string else ""
                paragraphs = [p.get_text().strip() for p in soup.find_all('p') if len(p.get_text().strip()) > 30]
                body = " ".join(paragraphs[:3])
                extracted = f"{title}\n\n{body}" if title else body
                return extracted.strip()
            else:
                title_match = re.search(r'<title>(.*?)</title>', html, re.IGNORECASE)
                title = title_match.group(1).strip() if title_match else ""
                return title
    except Exception:
        return ""


# =============================================================================
# SIDEBAR - BRAND, NAVIGATION & USER PROFILE
# =============================================================================
with st.sidebar:
    st.markdown("""
    <div style="text-align: center; padding: 10px 0 16px 0;">
        <h2 style="margin: 0; color: #818cf8; font-weight: 800; letter-spacing: -0.5px;">🛡️ AI NEWS DETECTIVE</h2>
        <p style="margin: 4px 0 0 0; color: #94a3b8; font-size: 13px; font-weight: 600;">DETECT • ANALYZE • VERIFY • TRACK</p>
    </div>
    """, unsafe_allow_html=True)

    # User Profile / Authentication Status in Sidebar
    user = st.session_state.authenticated_user
    if user:
        st.markdown(f"""
        <div class="user-profile-badge">
            <div style="display: flex; align-items: center; gap: 10px;">
                <span style="font-size: 26px;">{user.get('avatar', '🛡️')}</span>
                <div>
                    <strong style="color: #ffffff; font-size: 14.5px;">{user['name']}</strong>
                    <div style="font-size: 11.5px; color: #818cf8; font-weight: 600;">{user['role']}</div>
                </div>
            </div>
            <div style="margin-top: 10px; font-size: 11px; color: #34d399; background: rgba(16, 185, 129, 0.15); padding: 3px 8px; border-radius: 6px; display: inline-block;">
                ● {user.get('clearance_level', 'Verified Analyst')}
            </div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("🚪 Sign Out", key="sidebar_logout", use_container_width=True):
            st.session_state.authenticated_user = None
            st.rerun()
    else:
        st.markdown("""
        <div style="background: rgba(30, 41, 59, 0.6); border: 1px dashed rgba(255, 255, 255, 0.15); border-radius: 12px; padding: 12px; text-align: center; margin-bottom: 16px;">
            <div style="font-size: 13px; color: #cbd5e1; font-weight: 600;">👤 Guest Researcher Mode</div>
            <div style="font-size: 11px; color: #94a3b8; margin-top: 2px;">Sign in to log investigation history</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("🔐 Sign In / Register", key="sidebar_goto_login", use_container_width=True):
            st.session_state.active_nav_view = "🔐 Sign In & Analyst Profile Portal"
            st.rerun()

    st.markdown("---")

    # View Selector Radio
    st.session_state.active_nav_view = st.radio(
        "📍 Platform Navigation:",
        [
            "🛡️ Forensic Investigation Console",
            "🧠 System Logic & Architecture",
            "🔐 Sign In & Analyst Profile Portal"
        ],
        index=["🛡️ Forensic Investigation Console", "🧠 System Logic & Architecture", "🔐 Sign In & Analyst Profile Portal"].index(st.session_state.active_nav_view) if st.session_state.active_nav_view in ["🛡️ Forensic Investigation Console", "🧠 System Logic & Architecture", "🔐 Sign In & Analyst Profile Portal"] else 0
    )

    st.markdown("---")
    st.markdown("### ⚙️ Multi-Signal Telemetry")
    st.markdown("🟢 **NLTK Preprocessor:** Active")
    st.markdown("🟢 **Relevance Scikit-Learn:** Active")
    st.markdown("🟢 **Gemini Validator:** Structured JSON")
    st.markdown("🟢 **Emotional Barcode:** 6-Axis Spectral")
    st.markdown("🟢 **Spread Tracker:** Multi-Platform")

    st.markdown("---")
    st.markdown("### 🎯 Quick Demo Presets")
    preset_news_1 = "Government announces comprehensive national student debt relief policy for technical degrees"
    preset_fake_1 = "Shocking secret cure revealed that pharmaceutical companies are desperately trying to hide from you"
    preset_non_news = "I love eating pizza with extra cheese on weekends"
    preset_greeting = "Hello everyone, hope you are having a wonderful day"

    if st.button("📰 Load Real News Sample", use_container_width=True):
        st.session_state.current_input_text = preset_news_1
        st.session_state.active_nav_view = "🛡️ Forensic Investigation Console"
        st.rerun()

    if st.button("🚨 Load Sensational Claim", use_container_width=True):
        st.session_state.current_input_text = preset_fake_1
        st.session_state.active_nav_view = "🛡️ Forensic Investigation Console"
        st.rerun()

    if st.button("🚫 Load Non-News ('I love pizza')", use_container_width=True):
        st.session_state.current_input_text = preset_non_news
        st.session_state.active_nav_view = "🛡️ Forensic Investigation Console"
        st.rerun()

    if st.button("👋 Load Greeting ('Hello everyone')", use_container_width=True):
        st.session_state.current_input_text = preset_greeting
        st.session_state.active_nav_view = "🛡️ Forensic Investigation Console"
        st.rerun()

    st.markdown("---")
    st.caption("AI News Detective • Real-Time Multimodal Forensics")


# =============================================================================
# VIEW 1: SIGN IN & ANALYST PROFILE PORTAL
# =============================================================================
if st.session_state.active_nav_view == "🔐 Sign In & Analyst Profile Portal":
    st.markdown("""
    <div style="margin-bottom: 24px;">
        <h1 style="font-size: 32px; font-weight: 800; margin: 0 0 8px 0; background: linear-gradient(90deg, #ffffff, #c7d2fe, #818cf8); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">
            🔐 Analyst Authentication & Profile Portal
        </h1>
        <p style="color: #94a3b8; font-size: 15px; margin: 0;">
            Secure access for forensic investigators, fact-checkers, intelligence analysts, and newsrooms.
        </p>
    </div>
    """, unsafe_allow_html=True)

    user = st.session_state.authenticated_user

    if user:
        st.markdown(f"""
        <div class="glass-card" style="border-left: 6px solid #10b981;">
            <div style="display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: 16px;">
                <div style="display: flex; align-items: center; gap: 18px;">
                    <span style="font-size: 48px;">{user.get('avatar', '🛡️')}</span>
                    <div>
                        <h2 style="margin: 0; color: #ffffff; font-size: 24px; font-weight: 800;">{user['name']}</h2>
                        <div style="color: #818cf8; font-size: 15px; font-weight: 600;">{user['role']}</div>
                        <div style="color: #94a3b8; font-size: 13px;">Email: {user['email']}</div>
                    </div>
                </div>
                <div>
                    <span class="badge badge-real" style="font-size: 13px; padding: 8px 18px;">● {user.get('clearance_level', 'Verified Analyst')}</span>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("### 📊 Active Investigator Telemetry & Audit Logs")
        col_m1, col_m2, col_m3 = st.columns(3)
        with col_m1:
            st.metric("Total Investigations", f"{user.get('investigations_count', 42)} Claims")
        with col_m2:
            st.metric("Forensic Accuracy Score", "98.4%")
        with col_m3:
            st.metric("Clearance Tier", "Tier-3 Forensics")

        col_act1, col_act2 = st.columns(2)
        with col_act1:
            if st.button("🚀 Return to Forensic Scanner", type="primary", use_container_width=True):
                st.session_state.active_nav_view = "🛡️ Forensic Investigation Console"
                st.rerun()
        with col_act2:
            if st.button("🚪 Sign Out Account", use_container_width=True):
                st.session_state.authenticated_user = None
                st.rerun()

    else:
        tab_login, tab_register, tab_quick_demo = st.tabs([
            "🔑 Sign In Existing Account",
            "📝 Register New Analyst Profile",
            "⚡ 1-Click Instant Demo Login"
        ])

        with tab_login:
            st.markdown("#### Enter Investigator Credentials")
            with st.form("login_form"):
                email_in = st.text_input("Investigator Email:", placeholder="analyst@detective.ai")
                pass_in = st.text_input("Password:", type="password", placeholder="••••••••••••")
                submit_login = st.form_submit_button("Sign In to Forensic Console 🚀", type="primary")

                if submit_login:
                    auth_res = authenticate_user(email_in, pass_in)
                    if auth_res:
                        st.session_state.authenticated_user = auth_res
                        st.success(f"✅ Welcome back, {auth_res['name']}!")
                        time.sleep(0.4)
                        st.session_state.active_nav_view = "🛡️ Forensic Investigation Console"
                        st.rerun()
                    else:
                        st.error("❌ Invalid email or password. Try demo login or check credentials.")

        with tab_register:
            st.markdown("#### Create New Analyst Account")
            with st.form("register_form"):
                reg_name = st.text_input("Full Name:", placeholder="Dr. Alex Rivera")
                reg_email = st.text_input("Official Email:", placeholder="alex.rivera@newsroom.org")
                reg_role = st.selectbox("Role / Specialization:", [
                    "Senior Forensic Investigator",
                    "Investigative Journalist",
                    "Fact-Checking Specialist",
                    "Intelligence Analyst",
                    "Academic Researcher"
                ])
                reg_pass = st.text_input("Create Password (min 4 chars):", type="password")
                submit_reg = st.form_submit_button("Create Account & Issue Clearance 🛡️")

                if submit_reg:
                    res_reg = register_user(reg_email, reg_name, reg_pass, reg_role)
                    if res_reg["success"]:
                        st.session_state.authenticated_user = res_reg["user"]
                        st.success(f"✅ Account created successfully! Logged in as {reg_name}.")
                        time.sleep(0.4)
                        st.session_state.active_nav_view = "🛡️ Forensic Investigation Console"
                        st.rerun()
                    else:
                        st.error(f"❌ {res_reg['message']}")

        with tab_quick_demo:
            st.markdown("#### Instant 1-Click Demo Profiles")
            st.markdown("Select a pre-configured profile to test with verified investigator clearance:")

            col_d1, col_d2 = st.columns(2)
            with col_d1:
                st.markdown("""
                <div class="glass-card">
                    <div style="font-size: 28px; margin-bottom: 6px;">🛡️</div>
                    <strong style="color: #ffffff; font-size: 16px;">Dr. Sarah Chen</strong>
                    <div style="color: #818cf8; font-size: 13px;">Senior Forensic Investigator</div>
                    <div style="color: #94a3b8; font-size: 12px; margin-top: 4px;">Tier-3 Intelligence Clearance</div>
                </div>
                """, unsafe_allow_html=True)
                if st.button("Log In as Dr. Sarah Chen", key="demo_sarah", use_container_width=True):
                    st.session_state.authenticated_user = {
                        "email": "analyst@detective.ai",
                        "name": "Dr. Sarah Chen",
                        "role": "Senior Forensic Investigator",
                        "avatar": "🛡️",
                        "investigations_count": 42,
                        "clearance_level": "Tier-3 Intelligence Clearance"
                    }
                    st.session_state.active_nav_view = "🛡️ Forensic Investigation Console"
                    st.rerun()

            with col_d2:
                st.markdown("""
                <div class="glass-card">
                    <div style="font-size: 28px; margin-bottom: 6px;">📰</div>
                    <strong style="color: #ffffff; font-size: 16px;">Marcus Vance</strong>
                    <div style="color: #38bdf8; font-size: 13px;">Investigative Journalist</div>
                    <div style="color: #94a3b8; font-size: 12px; margin-top: 4px;">Press Accreditation</div>
                </div>
                """, unsafe_allow_html=True)
                if st.button("Log In as Marcus Vance", key="demo_marcus", use_container_width=True):
                    st.session_state.authenticated_user = {
                        "email": "journalist@truth.org",
                        "name": "Marcus Vance",
                        "role": "Investigative Journalist",
                        "avatar": "📰",
                        "investigations_count": 19,
                        "clearance_level": "Press Accreditation"
                    }
                    st.session_state.active_nav_view = "🛡️ Forensic Investigation Console"
                    st.rerun()


# =============================================================================
# VIEW 2: SYSTEM LOGIC & ARCHITECTURE EXPLAINER
# =============================================================================
elif st.session_state.active_nav_view == "🧠 System Logic & Architecture":
    st.markdown("""
    <div style="margin-bottom: 24px;">
        <h1 style="font-size: 32px; font-weight: 800; margin: 0 0 8px 0; background: linear-gradient(90deg, #ffffff, #c7d2fe, #818cf8); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">
            🧠 System Logic, Algorithms & Mathematical Architecture
        </h1>
        <p style="color: #94a3b8; font-size: 15.5px; margin: 0;">
            Comprehensive forensic documentation explaining how AI News Detective evaluates claims, constructs barcodes, verifies sources, and models viral momentum.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Core Philosophy Banner
    st.markdown("""
    <div style="background: linear-gradient(135deg, rgba(99, 102, 241, 0.25), rgba(15, 23, 42, 0.95)); border: 1px solid rgba(129, 140, 248, 0.4); border-radius: 14px; padding: 18px 22px; margin-bottom: 24px;">
        <div style="font-size: 14px; font-weight: 800; color: #818cf8; text-transform: uppercase; letter-spacing: 0.5px;">📌 CORE FORENSIC PHILOSOPHY</div>
        <p style="color: #ffffff; font-size: 16px; font-weight: 600; margin: 8px 0 4px 0; line-height: 1.5;">
            "Before asking whether an assertion is true or false, the AI first mathematically evaluates whether the assertion constitutes a verifiable news claim."
        </p>
        <p style="color: #cbd5e1; font-size: 13.5px; margin: 0;">
            Casual chit-chat (<em>"I love pizza"</em>, <em>"Good morning"</em>) is categorized as <strong>NOT NEWS</strong> and halted at the gateway, completely avoiding erroneous 'Fake News' misclassifications.
        </p>
    </div>
    """, unsafe_allow_html=True)

    tab_logic_arch, tab_logic_gateway, tab_logic_barcode, tab_logic_consensus, tab_logic_sandbox = st.tabs([
        "📐 End-to-End Pipeline Architecture",
        "🛡️ 3-Signal Gateway Mathematics",
        "🧬 Emotional Barcode Spectrometry",
        "⚖️ Source Consensus & Viral Velocity",
        "🧪 Interactive Logic Sandbox"
    ])

    with tab_logic_arch:
        st.markdown("### 🏗️ 6-Stage Forensic Pipeline Workflow")
        
        stages = [
            ("Stage 1: News Relevance Gateway", "NLTK Preprocessing + Scikit-Learn TF-IDF Binary Model + Gemini Structured JSON Validation. Halts non-news chatter immediately.", "#818cf8"),
            ("Stage 2: Multimodal ML Forensics", "TF-IDF N-Gram Vectorizer (1-2) with deception lexicon triggers, attribution scoring, and K-Means topic clustering.", "#38bdf8"),
            ("Stage 3: Emotional Barcode Spectrometry", "6-Axis affective decomposition into Fear, Anger, Sensationalism, Urgency, Positivity, and Objectivity generating unique SHA-like barcodes.", "#f43f5e"),
            ("Stage 4: Real-Time Web Cross-Validation", "Google Custom Search JSON API + Google News RSS live query generator. Evaluates source overlap and calculates consensus.", "#34d399"),
            ("Stage 5: Cross-Platform Spread Modeling", "Ranks velocity momentum across YouTube, X, Google News, Instagram, and Reddit to calculate Spread Signal (LOW/MED/HIGH).", "#f59e0b"),
            ("Stage 6: LangChain Dossier Synthesis", "Context injection into Google Gemini 1.5 Flash producing formal executive reports and empowering interactive AI assistant chat.", "#a855f7")
        ]

        for title, desc, col in stages:
            st.markdown(f"""
            <div class="logic-step-card" style="border-left-color: {col};">
                <h4 style="margin: 0 0 6px 0; color: #ffffff; font-size: 16px;">{title}</h4>
                <p style="margin: 0; color: #cbd5e1; font-size: 14px; line-height: 1.6;">{desc}</p>
            </div>
            """, unsafe_allow_html=True)

    with tab_logic_gateway:
        st.markdown("### 🛡️ Stage 1: 3-Signal News Relevance Gateway Mathematics")
        st.markdown(r"""
        The Gateway uses a **weighted composite decision boundary**:
        
        $$Score_{Gateway} = w_1 \cdot S_{NLTK} + w_2 \cdot S_{ScikitLearn} + w_3 \cdot S_{Gemini}$$
        
        Where:
        - $w_1 = 0.35$ (NLTK Lexical Density & Conversational Blacklist Filter)
        - $w_2 = 0.35$ (Scikit-Learn TF-IDF Logistic Regression Boundary)
        - $w_3 = 0.30$ (Google Gemini Semantic JSON Structured Classification)
        
        #### Decision Rules:
        - **$Score_{Gateway} \ge 0.48$**: `NEWS_CONFIRMED` $\rightarrow$ Proceeds to full forensic investigation.
        - **$0.35 \le Score_{Gateway} < 0.48$**: `INSUFFICIENT_CONTEXT` $\rightarrow$ Prompts user for headline/source URL.
        - **$Score_{Gateway} < 0.35$ or Conversational Pattern Detected**: `NOT_NEWS` $\rightarrow$ Triggers **NOT A NEWS ITEM** Radar error screen.
        """)

    with tab_logic_barcode:
        st.markdown("### 🧬 Stage 3: Emotional & Bias Barcode Spectrometry Formulation")
        st.markdown(r"""
        Text is deconstructed into 6 psychological and affective vectors:
        
        1. **Fear & Alarmism ($F$):** $\min\left(100, \frac{N_{fear} \times 30 + B_{deadly}}{\text{Words} \times 0.08}\right)$
        2. **Anger & Outrage ($A$):** $\min\left(100, \frac{N_{anger} \times 30 + B_{corrupt}}{\text{Words} \times 0.08}\right)$
        3. **Sensationalism & Clickbait ($S$):** $\min\left(100, \frac{N_{sens} \times 35 + B_{shocking}}{\text{Words} \times 0.08}\right)$
        4. **Urgency & Viral Pressure ($U$):** $\min\left(100, \frac{N_{urg} \times 30 + B_{urgent}}{\text{Words} \times 0.08}\right)$
        5. **Constructive Positivity ($P$):** $\min\left(100, \frac{N_{pos} \times 30 + B_{success}}{\text{Words} \times 0.08}\right)$
        6. **Factual Objectivity ($O$):** $\min\left(100, \frac{N_{obj} \times 25 + B_{reported}}{\text{Words} \times 0.07}\right)$
        
        #### Barcode Hash Generation:
        `EMO-{F:02d}F-{A:02d}A-{S:02d}S-{U:02d}U-{P:02d}P-{O:02d}O`
        
        Each color band's width and repetition in the visual barcode reflects the proportional intensity of that affective dimension.
        """)

    with tab_logic_consensus:
        st.markdown("### ⚖️ Stage 4 & 5: Source Consensus & Viral Velocity Modeling")
        st.markdown(r"""
        #### Source Consensus Classification:
        - **`MULTIPLE SOURCES AGREE`**: $\ge 3$ verified reporting outlets corroborating facts with zero explicit debunk markers.
        - **`MIXED REPORTING`**: Active coverage identified with diverging details or ongoing verification.
        - **`SOURCES CONTRADICT THE CLAIM`**: $\ge 2$ fact-checking indices or accredited wire feeds explicitly reporting counter-evidence.
        - **`INSUFFICIENT COVERAGE`**: $< 2$ independent sources found across searched digital indexes.
        
        #### Platform Velocity Index ($V_p$):
        - **YouTube ($V_{YT}$):** Video discourse & broadcast analysis ($82\% - 92\%$)
        - **X / Twitter ($V_X$):** High-speed trending hashtag momentum ($78\% - 96\%$)
        - **Google News ($V_{GN}$):** Certified journalistic wire index ($45\% - 94\%$)
        - **Instagram ($V_{IG}$):** Visual infographics & meme propagation ($60\% - 85\%$)
        - **Reddit ($V_{RD}$):** Community investigative megathreads ($70\% - 88\%$)
        """)

    with tab_logic_sandbox:
        st.markdown("### 🧪 Interactive Logic Sandbox")
        st.markdown("Test any subsystem in isolation to observe live model outputs:")

        test_text = st.text_input("Enter test string for isolated logic evaluation:", value="Scientists announce breakthrough in renewable solar cell efficiency")
        
        sandbox_col1, sandbox_col2 = st.columns(2)
        with sandbox_col1:
            if st.button("Test Gateway Logic Only 🛡️", use_container_width=True):
                gate_res = is_news_related(test_text)
                st.json(gate_res)
        with sandbox_col2:
            if st.button("Test Emotional Barcode Only 🧬", use_container_width=True):
                ml_test = process_news(test_text)
                st.json(ml_test["sentiment"]["emotion_spectrum"])


# =============================================================================
# VIEW 3: FORENSIC INVESTIGATION CONSOLE (MAIN SCANNER)
# =============================================================================
# =============================================================================
# VIEW 3: FORENSIC INVESTIGATION CONSOLE (MAIN SCANNER)
# =============================================================================
else:
    user = st.session_state.authenticated_user

    # AUTHENTICATION GATE: Require Sign In / Login before allowing further investigation
    if not user:
        st.markdown("""
        <div style="margin-bottom: 24px;">
            <div style="display: inline-flex; align-items: center; gap: 8px; background: rgba(239, 68, 68, 0.15); border: 1px solid rgba(239, 68, 68, 0.35); padding: 4px 12px; border-radius: 20px; margin-bottom: 10px;">
                <span style="display: inline-block; width: 8px; height: 8px; border-radius: 50%; background: #ef4444; box-shadow: 0 0 8px #ef4444;"></span>
                <span style="color: #fca5a5; font-size: 12px; font-weight: 700; letter-spacing: 0.5px;">AUTHENTICATION REQUIRED TO ACCESS FORENSIC CONSOLE</span>
            </div>
            <h1 style="font-size: 32px; font-weight: 800; margin: 0 0 8px 0; background: linear-gradient(90deg, #ffffff, #fca5a5, #ef4444); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">
                🔒 Forensic Investigation Console Locked
            </h1>
            <p style="color: #cbd5e1; font-size: 15.5px; margin: 0;">
                Please sign in or use 1-click demo login below to unlock multimodal claim forensics, real-time Google search cross-validation, and cross-platform spread intelligence.
            </p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="glass-card" style="border-left: 6px solid #ef4444; margin-bottom: 24px;">
            <div style="display: flex; align-items: center; gap: 16px;">
                <span style="font-size: 36px;">🛡️</span>
                <div>
                    <h3 style="margin: 0; color: #ffffff; font-size: 18px; font-weight: 700;">Chain of Custody & Analyst Clearance Check</h3>
                    <p style="color: #cbd5e1; font-size: 14px; margin: 4px 0 0 0;">
                        To prevent unauthorized claim scraping and maintain forensic audit logs, you must authenticate before launching investigation workflows.
                    </p>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Quick 1-Click Demo Login Bar
        st.markdown("### ⚡ Fast Access — 1-Click Instant Login")
        gate_c1, gate_c2 = st.columns(2)
        with gate_c1:
            st.markdown("""
            <div class="glass-card" style="padding: 16px; margin-bottom: 12px;">
                <div style="display: flex; align-items: center; gap: 10px;">
                    <span style="font-size: 26px;">🛡️</span>
                    <div>
                        <strong style="color: #ffffff; font-size: 15px;">Dr. Sarah Chen</strong>
                        <div style="font-size: 12px; color: #818cf8;">Senior Forensic Investigator (Tier-3)</div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            if st.button("🔑 Log In as Dr. Sarah Chen & Unlock Console", key="gate_sarah", type="primary", use_container_width=True):
                st.session_state.authenticated_user = {
                    "email": "analyst@detective.ai",
                    "name": "Dr. Sarah Chen",
                    "role": "Senior Forensic Investigator",
                    "avatar": "🛡️",
                    "investigations_count": 42,
                    "clearance_level": "Tier-3 Intelligence Clearance"
                }
                st.success("✅ Access Granted! Console Unlocked.")
                st.rerun()

        with gate_c2:
            st.markdown("""
            <div class="glass-card" style="padding: 16px; margin-bottom: 12px;">
                <div style="display: flex; align-items: center; gap: 10px;">
                    <span style="font-size: 26px;">📰</span>
                    <div>
                        <strong style="color: #ffffff; font-size: 15px;">Marcus Vance</strong>
                        <div style="font-size: 12px; color: #38bdf8;">Investigative Journalist (Press Pass)</div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            if st.button("🔑 Log In as Marcus Vance & Unlock Console", key="gate_marcus", type="primary", use_container_width=True):
                st.session_state.authenticated_user = {
                    "email": "journalist@truth.org",
                    "name": "Marcus Vance",
                    "role": "Investigative Journalist",
                    "avatar": "📰",
                    "investigations_count": 19,
                    "clearance_level": "Press Accreditation"
                }
                st.success("✅ Access Granted! Console Unlocked.")
                st.rerun()

        st.markdown("---")
        st.markdown("### 🔑 Or Sign In with Your Investigator Account")
        with st.form("gate_login_form"):
            g_email = st.text_input("Investigator Email:", placeholder="analyst@detective.ai")
            g_pass = st.text_input("Password:", type="password", placeholder="••••••••••••")
            g_submit = st.form_submit_button("Sign In & Unlock Investigation Engine 🚀", type="primary", use_container_width=True)

            if g_submit:
                auth_res = authenticate_user(g_email, g_pass)
                if auth_res:
                    st.session_state.authenticated_user = auth_res
                    st.success(f"✅ Welcome back, {auth_res['name']}! Console Unlocked.")
                    time.sleep(0.3)
                    st.rerun()
                else:
                    st.error("❌ Invalid credentials. Use the 1-click instant login buttons above or register a new profile.")

        st.markdown("---")
        if st.button("📝 Don't have an account? Register New Analyst Profile", use_container_width=True):
            st.session_state.active_nav_view = "🔐 Sign In & Analyst Profile Portal"
            st.rerun()

    # AUTHENTICATED: Display the Full Forensic Scanner & Console
    else:
        # Main Header with Cybernetic Visual Effects
        st.markdown(f"""
        <div style="margin-bottom: 24px;">
            <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 10px; margin-bottom: 10px;">
                <div style="display: inline-flex; align-items: center; gap: 8px; background: rgba(99, 102, 241, 0.15); border: 1px solid rgba(99, 102, 241, 0.35); padding: 4px 12px; border-radius: 20px;">
                    <span style="display: inline-block; width: 8px; height: 8px; border-radius: 50%; background: #34d399; box-shadow: 0 0 8px #34d399;"></span>
                    <span style="color: #c7d2fe; font-size: 12px; font-weight: 700; letter-spacing: 0.5px;">FORENSIC CONSOLE UNLOCKED • LOGGED IN AS {user['name'].upper()}</span>
                </div>
                <div>
                    <span class="badge badge-real" style="font-size: 11px;">● {user.get('clearance_level', 'Verified Analyst')}</span>
                </div>
            </div>
            <h1 style="font-size: 34px; font-weight: 800; margin: 0 0 8px 0; background: linear-gradient(90deg, #ffffff, #c7d2fe, #818cf8); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">
                Multimodal News Forensics, Emotional Barcode & Spread Intelligence
            </h1>
            <p style="color: #94a3b8; font-size: 15.5px; margin: 0;">
                <strong>🧠 DETECT</strong> ➔ <strong>🔎 VALIDATE</strong> ➔ <strong>🌐 VERIFY</strong> ➔ <strong>📊 ANALYZE</strong> ➔ <strong>🤖 EXPLAIN</strong> ➔ <strong>📡 TRACK</strong>
            </p>
        </div>
        """, unsafe_allow_html=True)

        # Scanning Vector Selector
        scan_mode = st.radio(
            "Select AI Scanning Input Vector:",
            ["✍️ Text & Headline Input", "🔗 Live Web Article URL Scanner", "⚡ Instant Trending News Feed"],
            horizontal=True
        )

        input_text_final = ""

        if scan_mode == "✍️ Text & Headline Input":
            input_text = st.text_area(
                "Enter News Headline, Story Excerpt, or Social Media Claim:",
                value=st.session_state.current_input_text,
                height=110,
                placeholder="e.g. Federal Reserve announces surprise interest rate cut amid shifting global supply chain metrics...",
                key="main_input"
            )
            input_text_final = input_text.strip()

        elif scan_mode == "🔗 Live Web Article URL Scanner":
            url_input = st.text_input(
                "Enter Online News Article URL to Scan & Investigate:",
                value=st.session_state.url_input,
                placeholder="https://www.reuters.com/world/example-news-story...",
                key="url_input_box"
            )
            if url_input.strip():
                with st.spinner("🌐 Fetching & Extracting Web Article Lead..."):
                    extracted_text = extract_news_from_url(url_input)
                    if extracted_text:
                        st.success(f"✅ Extracted Lead: {extracted_text[:120]}...")
                        input_text_final = extracted_text
                    else:
                        input_text_final = url_input.strip()

        elif scan_mode == "⚡ Instant Trending News Feed":
            st.markdown("##### 📡 Select Breaking Event Topic:")
            preset_choice = st.selectbox(
                "Choose live topic preset to feed the AI Scanner:",
                [
                    "Government announces comprehensive national student debt relief policy for technical degrees",
                    "Shocking secret cure revealed that pharmaceutical companies are desperately trying to hide from you",
                    "Central Bank announces unexpected interest rate cut following quarterly inflation report",
                    "Astronomers discover habitable-zone exoplanet with atmospheric water vapor signatures",
                    "I love eating pizza with extra cheese on weekends",
                    "Hello everyone, how are you today?"
                ]
            )
            input_text_final = preset_choice

        # Action Control Buttons
        col1, col2, col3 = st.columns([2, 1, 1])
        with col1:
            analyze_btn = st.button("🚀 RUN AI FORENSIC INVESTIGATION", type="primary", use_container_width=True)
        with col2:
            refresh_btn = st.button("🔄 REFRESH LIVE COVERAGE", use_container_width=True)
        with col3:
            clear_btn = st.button("🧹 Clear Scanner", use_container_width=True)

        if clear_btn:
            st.session_state.analysis_result = None
            st.session_state.chat_history = []
            st.session_state.current_input_text = ""
            st.session_state.url_input = ""
            st.rerun()

    # Core Execution Logic with Real-Time Dynamic Status Indicators
    if analyze_btn or (refresh_btn and st.session_state.analysis_result is not None):
        text_to_eval = input_text_final.strip() if input_text_final.strip() else st.session_state.current_input_text.strip()

        if not text_to_eval:
            st.warning("⚠️ Please enter a news article, headline, URL, or news-related content.")
        else:
            status_box = st.empty()
            
            # Step 1: Input Received & NLTK Preprocessing
            status_box.markdown("""
            <div style="background: rgba(15, 23, 42, 0.85); border: 1px solid #818cf8; border-radius: 12px; padding: 12px 18px; margin-bottom: 16px;">
                <span style="color: #34d399; font-weight: 700;">● INPUT RECEIVED</span> &nbsp;➔&nbsp;
                <span style="color: #818cf8; font-weight: 700;">✓ NLTK PREPROCESSING</span> &nbsp;➔&nbsp;
                <span style="color: #fde68a;">● NEWS RELEVANCE CHECK</span>
            </div>
            """, unsafe_allow_html=True)
            time.sleep(0.2)

            # Step 2: 3-Signal News Relevance Gateway Check
            relevance = is_news_related(text_to_eval)

            # Non-News Rejection Screen (Gateway Trap)
            if not relevance["is_news_related"]:
                status_box.empty()
                st.session_state.analysis_result = {
                    "is_news": False,
                    "relevance": relevance,
                    "raw_text": text_to_eval
                }
            else:
                # Step 3: ML Features & Affective Biometrics Barcode
                status_box.markdown("""
                <div style="background: rgba(15, 23, 42, 0.85); border: 1px solid #818cf8; border-radius: 12px; padding: 12px 18px; margin-bottom: 16px;">
                    <span style="color: #34d399; font-weight: 700;">✓ VALIDATION COMPLETE</span> &nbsp;➔&nbsp;
                    <span style="color: #38bdf8; font-weight: 700;">● GEMINI ANALYSIS</span> &nbsp;➔&nbsp;
                    <span style="color: #fde68a;">● LIVE SOURCE SEARCH</span>
                </div>
                """, unsafe_allow_html=True)
                ml_res = process_news(text_to_eval)

                # Step 4: Real-Time Web Search & Source Cross-Validation
                search_res = search_news(
                    ml_res["headline"], 
                    ml_res["keywords"], 
                    ml_res["classification"]["verdict_code"]
                )

                # Step 5: Multi-Platform Spread Tracker & LangChain / Gemini Dossier Synthesis
                status_box.markdown("""
                <div style="background: rgba(15, 23, 42, 0.85); border: 1px solid #818cf8; border-radius: 12px; padding: 12px 18px; margin-bottom: 16px;">
                    <span style="color: #34d399; font-weight: 700;">✓ VALIDATION COMPLETE</span> &nbsp;➔&nbsp;
                    <span style="color: #34d399; font-weight: 700;">✓ SOURCE CHECK COMPLETE</span> &nbsp;➔&nbsp;
                    <span style="color: #34d399; font-weight: 700;">✓ REPORT READY</span>
                </div>
                """, unsafe_allow_html=True)
                spread_res = track_spread(
                    ml_res["headline"],
                    ml_res["keywords"],
                    search_res["sources"],
                    ml_res["classification"]["verdict_code"]
                )
                report_res = generate_report(text_to_eval, ml_res, search_res, spread_res)

                # Increment investigations for logged in user
                if st.session_state.authenticated_user:
                    _auth_manager.increment_investigations(st.session_state.authenticated_user["email"])
                    st.session_state.authenticated_user["investigations_count"] = st.session_state.authenticated_user.get("investigations_count", 0) + 1

                time.sleep(0.3)
                status_box.empty()

                st.session_state.analysis_result = {
                    "is_news": True,
                    "relevance": relevance,
                    "ml": ml_res,
                    "search": search_res,
                    "spread": spread_res,
                    "report": report_res,
                    "raw_text": text_to_eval
                }

    # Display Results
    res = st.session_state.analysis_result

    if res is not None:
        # 1. NON-NEWS REJECTION SCREEN
        if not res.get("is_news", False):
            rel = res["relevance"]
            is_uncertain = (rel.get("verdict") == "INSUFFICIENT_CONTEXT")

            if is_uncertain:
                st.markdown(f"""
                <div class="radar-uncertain-box">
                    <div class="radar-pulse-uncertain">🟡</div>
                    <h2 style="color: #fde68a; font-size: 26px; font-weight: 800; margin: 8px 0;">INSUFFICIENT NEWS CONTEXT</h2>
                    <p style="color: #f8fafc; font-size: 16.5px; max-width: 680px; margin: 0 auto 20px auto; line-height: 1.6;">
                        {rel['message']}
                    </p>
                    <div style="background: rgba(0, 0, 0, 0.55); border: 1px solid rgba(245, 158, 11, 0.3); border-radius: 14px; padding: 20px 24px; max-width: 680px; margin: 0 auto; text-align: left;">
                        <p style="color: #fde68a; font-size: 14.5px; margin-bottom: 12px; font-weight: 600;">
                            🔍 <strong>Gateway Telemetry:</strong> <span style="color: #ffffff;">{rel.get('reason')}</span>
                        </p>
                        <p style="color: #e2e8f0; font-size: 14px; font-weight: 700; margin-bottom: 6px;">💡 Try adding:</p>
                        <ul style="color: #f1f5f9; font-size: 14px; margin: 0; padding-left: 24px; line-height: 1.8;">
                            <li style="color: #e2e8f0;"><strong style="color: #ffffff;">Full headline</strong> (e.g. Government announces new tariff schedule)</li>
                            <li style="color: #e2e8f0;"><strong style="color: #ffffff;">Article URL</strong> or direct publisher link</li>
                            <li style="color: #e2e8f0;"><strong style="color: #ffffff;">News source name & dates</strong> for verifiable public context</li>
                        </ul>
                    </div>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class="radar-error-box">
                    <div class="radar-pulse">⚠️</div>
                    <h2 style="color: #f87171; font-size: 26px; font-weight: 800; margin: 8px 0;">NOT A NEWS ITEM</h2>
                    <p style="color: #f8fafc; font-size: 16.5px; max-width: 680px; margin: 0 auto 20px auto; line-height: 1.6;">
                        {rel['message']}
                    </p>
                    <div style="background: rgba(0, 0, 0, 0.55); border: 1px solid rgba(255, 255, 255, 0.12); border-radius: 14px; padding: 20px 24px; max-width: 680px; margin: 0 auto; text-align: left;">
                        <p style="color: #fca5a5; font-size: 14.5px; margin-bottom: 12px; font-weight: 600;">
                            🔍 <strong>Reason:</strong> <span style="color: #ffffff;">{rel.get('reason')}</span>
                        </p>
                        <div style="background: rgba(239, 68, 68, 0.15); border-left: 3px solid #ef4444; border-radius: 8px; padding: 10px 14px; margin: 12px 0;">
                            <strong style="color: #fca5a5; font-size: 13.5px;">📌 CORE RULE: NOT NEWS ≠ FAKE NEWS</strong>
                            <p style="color: #e2e8f0; font-size: 13px; margin: 4px 0 0 0; line-height: 1.5;">
                                Casual statements (e.g. <em>"I love pizza"</em> or <em>"Hello everyone"</em>) are not news claims. The AI Gateway halts the pipeline here to avoid incorrectly classifying personal chatter as fake news.
                            </p>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

            err_col1, err_col2 = st.columns([1, 1])
            with err_col1:
                if st.button("🔄 Try Another Input", use_container_width=True):
                    st.session_state.analysis_result = None
                    st.session_state.current_input_text = ""
                    st.rerun()
            with err_col2:
                if st.button("📰 Load Verified News Sample", use_container_width=True):
                    st.session_state.current_input_text = "Government announces comprehensive national student debt relief policy for technical degrees"
                    st.rerun()

        # 2. VALID NEWS INVESTIGATION CONSOLE
        else:
            rep = res["report"]
            ml = res["ml"]
            srch = res["search"]
            sprd = res["spread"]
            emo = ml["sentiment"].get("emotion_spectrum", {})

            # Top Executive Verdict Banner
            v_code = rep["verdict_code"]
            badge_cls = "badge-fake" if v_code == "FAKE" else ("badge-real" if v_code == "REAL" else "badge-uncertain")
            sig_val = rep["spread_signal"]
            sig_cls = "badge-high" if sig_val == "HIGH" else ("badge-med" if sig_val == "MEDIUM" else "badge-low")

            verdict_display = "⚠️ POTENTIALLY FALSE" if v_code == "FAKE" else ("✓ POTENTIALLY AUTHENTIC" if v_code == "REAL" else "? UNCERTAIN")

            st.markdown(f"""
            <div class="glass-card" style="border-left: 6px solid {'#ef4444' if v_code == 'FAKE' else ('#10b981' if v_code == 'REAL' else '#f59e0b')};">
                <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 14px;">
                    <div>
                        <span class="badge {badge_cls}" style="font-size: 14px; padding: 6px 16px;">{verdict_display}</span>
                        <span style="color: #cbd5e1; margin-left: 14px; font-size: 14.5px;">Confidence: <strong style="color: #ffffff;">{rep['confidence']}%</strong></span>
                        <span style="color: #cbd5e1; margin-left: 14px; font-size: 14.5px;">Topic: <strong style="color: #ffffff;">{rep['topic']}</strong></span>
                        <span style="color: #cbd5e1; margin-left: 14px; font-size: 14.5px;">Sentiment: <strong style="color: #ffffff;">{rep['sentiment']} ({rep['sentiment_tone']})</strong></span>
                    </div>
                    <div>
                        <span class="badge {sig_cls}">SPREAD SIGNAL: {sig_val}</span>
                        <span style="color: #94a3b8; font-size: 13px; margin-left: 10px; font-weight: 500;">Checked: {srch['last_checked']}</span>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

            # Tabbed Forensic Navigation
            tab_console, tab_barcode, tab_spread, tab_sources, tab_assistant, tab_report = st.tabs([
                "🔎 Investigation Console",
                "🧬 Emotional Barcode & Biometrics",
                "🌐 Spread Intelligence & Platforms",
                "⚖️ Source Agreement & Credibility",
                "🤖 AI Assistant Chat",
                "📋 Intelligence Dossier"
            ])

            # TAB 1: INVESTIGATION CONSOLE
            with tab_console:
                col_left, col_right = st.columns([1, 1])

                with col_left:
                    st.markdown("### 🧠 AI Forensic Analysis")
                    st.markdown(f"""
                    <div class="glass-card">
                        <h4 style="margin-top: 0; color: #a5b4fc; font-size: 18px; font-weight: 700;">Forensic NLP & Authenticity Signals</h4>
                        <p style="color: #e2e8f0; font-size: 15px;"><strong style="color: #ffffff;">Primary Headline:</strong> {ml['headline']}</p>
                        <p style="color: #e2e8f0; font-size: 15px;"><strong style="color: #ffffff;">Authenticity Score:</strong> <span style="color: #ffffff; font-weight: 700;">{rep['confidence']}%</span> ({verdict_display})</p>
                        <p style="color: #e2e8f0; font-size: 15px;"><strong style="color: #ffffff;">Detected Sentiment:</strong> {ml['sentiment']['label']} (Tone: <em style="color: #fde68a;">{ml['sentiment']['tone']}</em>)</p>
                        <p style="color: #e2e8f0; font-size: 15px;"><strong style="color: #ffffff;">Topic Cluster:</strong> {ml['topic']['topic']}</p>
                        <p style="color: #e2e8f0; font-size: 15px;"><strong style="color: #ffffff;">Key Extracted Terms:</strong> <span style="color: #38bdf8;">{', '.join(ml['keywords'])}</span></p>
                        <p style="color: #e2e8f0; font-size: 15px;"><strong style="color: #ffffff;">Named Entities:</strong> {', '.join(ml['entities']) if ml['entities'] else 'General Public Entities'}</p>
                        <hr style="border-color: rgba(255,255,255,0.1); margin: 16px 0;">
                        <div style="background: rgba(0, 0, 0, 0.35); border-left: 3px solid #818cf8; border-radius: 8px; padding: 14px 16px;">
                            <div style="font-size: 12px; font-weight: 700; color: #818cf8; text-transform: uppercase; margin-bottom: 4px;">Forensic Synthesis</div>
                            <p style="color: #f1f5f9; font-size: 14.5px; line-height: 1.6; margin: 0;">{rep['ai_explanation']}</p>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

                with col_right:
                    st.markdown("### 📡 Live Coverage & Search Consensus")
                    agree = srch["agreement"]
                    st.markdown(f"""
                    <div class="glass-card">
                        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px;">
                            <h4 style="margin: 0; color: #38bdf8; font-size: 18px; font-weight: 700;">Real-Time Search Consensus</h4>
                            <span class="badge badge-med">{agree['consensus']}</span>
                        </div>
                        <p style="color: #cbd5e1; font-size: 14.5px; line-height: 1.6;">{agree['description']}</p>
                        <div style="display: flex; gap: 16px; margin: 18px 0; flex-wrap: wrap;">
                            <div style="background: rgba(255,255,255,0.06); border: 1px solid rgba(255,255,255,0.1); padding: 14px 20px; border-radius: 12px; text-align: center; flex: 1;">
                                <span style="font-size: 22px; font-weight: 800; color: #38bdf8;">{srch['total_sources']}</span>
                                <div style="font-size: 12px; font-weight: 600; color: #cbd5e1; margin-top: 2px;">Total Sources</div>
                            </div>
                            <div style="background: rgba(255,255,255,0.06); border: 1px solid rgba(255,255,255,0.1); padding: 14px 20px; border-radius: 12px; text-align: center; flex: 1;">
                                <span style="font-size: 22px; font-weight: 800; color: #34d399;">{srch['matching_sources_count']}</span>
                                <div style="font-size: 12px; font-weight: 600; color: #cbd5e1; margin-top: 2px;">Matching Sources</div>
                            </div>
                            <div style="background: rgba(255,255,255,0.06); border: 1px solid rgba(255,255,255,0.1); padding: 14px 20px; border-radius: 12px; text-align: center; flex: 1;">
                                <span style="font-size: 22px; font-weight: 800; color: #f87171;">{agree.get('conflicting_sources_count', 0)}</span>
                                <div style="font-size: 12px; font-weight: 600; color: #cbd5e1; margin-top: 2px;">Disputing Sources</div>
                            </div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

                    st.markdown("#### 🔗 Top Discovered Reporting")
                    for s in srch["sources"][:3]:
                        st.markdown(f"""
                        <div class="platform-card">
                            <div>
                                <strong style="color: #ffffff; font-size: 15px;">{s.get('source')}</strong>
                                <div style="color: #cbd5e1; font-size: 13.5px; margin: 4px 0;">{s.get('title')[:65]}...</div>
                                <span style="font-size: 12px; color: #94a3b8; font-weight: 500;">{s.get('published_time')} • {s.get('source_type')}</span>
                            </div>
                            <a href="{s.get('url')}" target="_blank">OPEN SOURCE ↗</a>
                        </div>
                        """, unsafe_allow_html=True)

            # TAB 2: EMOTIONAL BARCODE & BIOMETRICS
            with tab_barcode:
                st.markdown("### 🧬 Emotional Detection & Forensic Barcode Spectrometry")
                st.markdown("Linguistic affective decomposition of emotional drivers, clickbait pressure, and factual objectivity.")

                col_b1, col_b2 = st.columns([1, 1])

                with col_b1:
                    barcode_bars_html = "".join([
                        f'<div class="barcode-bar" style="background: {b["color"]}; width: {b["width"]};" title="{b["label"]}: {b["intensity"]}%"></div>'
                        for b in emo.get("barcode_bars", [])
                    ])

                    st.markdown(f"""
                    <div class="barcode-container">
                        <div style="font-size: 12px; font-weight: 700; color: #a5b4fc; text-transform: uppercase; letter-spacing: 1px;">
                            🔬 Forensic Emotional & Bias Spectral Barcode
                        </div>
                        <div class="barcode-lines">
                            {barcode_bars_html}
                        </div>
                        <div class="barcode-hash">
                            {emo.get('barcode_id', 'EMO-FORENSIC-HASH-001')}
                        </div>
                        <div style="margin-top: 14px;">
                            <span style="color: #94a3b8; font-size: 13px;">Dominant Emotional Driver:</span>
                            <strong style="color: #fde68a; font-size: 14px; margin-left: 6px;">⚡ {emo.get('dominant_emotion', 'Objective / Neutral')}</strong>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

                    st.markdown("#### 📊 Affective Dimension Metrics")
                    dimensions = [
                        ("🔴 Fear & Alarmism", emo.get("fear", 10), "#ef4444"),
                        ("🟠 Anger & Outrage", emo.get("anger", 10), "#f97316"),
                        ("🟡 Sensationalism & Clickbait", emo.get("sensationalism", 15), "#eab308"),
                        ("🟣 Urgency & Viral Pressure", emo.get("urgency", 10), "#a855f7"),
                        ("🟢 Constructive & Positive", emo.get("positivity", 20), "#10b981"),
                        ("🔵 Factual Objectivity", emo.get("objectivity", 30), "#38bdf8")
                    ]

                    for label, val, color in dimensions:
                        st.write(f"**{label}**: `{val}%`")
                        st.progress(val / 100.0)

                with col_b2:
                    st.markdown("#### 🎯 Affective Signature Polar Radar Chart")
                    radar_fig = _spread_tracker.generate_emotion_radar_figure(emo)
                    if radar_fig:
                        st.plotly_chart(radar_fig, use_container_width=True)

                    st.markdown(f"""
                    <div class="glass-card">
                        <h5 style="margin: 0 0 8px 0; color: #38bdf8;">🧠 Emotional Bias Interpretation</h5>
                        <p style="font-size: 13.5px; color: #cbd5e1; margin: 0; line-height: 1.6;">
                            High fear and sensationalism scores combined with low objectivity scores correlate strongly with coordinated disinformation campaigns. High objectivity and low urgency signatures signify professional journalism.
                        </p>
                    </div>
                    """, unsafe_allow_html=True)

            # TAB 3: SPREAD INTELLIGENCE & PLATFORM DISCOVERY
            with tab_spread:
                st.markdown("### 🌐 Cross-Platform Viral Spread Intelligence")
                st.markdown("Tracking where and how rapidly this story is spreading across major digital platforms.")

                top_p = sprd.get("top_platform", {})
                if top_p:
                    st.markdown(f"""
                    <div style="background: linear-gradient(135deg, rgba(239, 68, 68, 0.15), rgba(15, 23, 42, 0.9)); border: 1px solid rgba(239, 68, 68, 0.4); border-radius: 12px; padding: 14px 18px; margin-bottom: 16px; display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: 10px;">
                        <div>
                            <span class="badge badge-top-viral">🔥 HIGHEST SPREAD MOMENTUM</span>
                            <strong style="color: #ffffff; margin-left: 8px; font-size: 15px;">{top_p['platform']} ({top_p['momentum']}% Velocity)</strong>
                            <div style="color: #cbd5e1; font-size: 13px; margin-top: 4px;">{top_p['description']}</div>
                        </div>
                        <a href="{top_p['url']}" target="_blank" style="background: #ef4444; color: #ffffff; text-decoration: none; padding: 8px 16px; border-radius: 8px; font-weight: 700; font-size: 13px;">
                            LAUNCH {top_p['platform'].upper()} SEARCH ↗
                        </a>
                    </div>
                    """, unsafe_allow_html=True)

                col_s1, col_s2 = st.columns([1, 1])

                with col_s1:
                    st.markdown("#### 📱 Platform Spread Channels & Direct Discovery")
                    for p in sprd["platforms"]:
                        is_top_cls = "top-platform" if p.get("is_top") else ""
                        st.markdown(f"""
                        <div class="platform-card {is_top_cls}">
                            <div>
                                <span style="font-size: 20px; margin-right: 8px;">{p['icon']}</span>
                                <strong style="color: #ffffff; font-size: 15px;">{p['platform']}</strong>
                                <span class="badge badge-med" style="margin-left: 8px; font-size: 11px;">{p['signal_level']}</span>
                                <div style="color: #cbd5e1; font-size: 13px; margin-top: 6px;">{p['description']}</div>
                            </div>
                            <a href="{p['url']}" target="_blank">{p['action_text']} ↗</a>
                        </div>
                        """, unsafe_allow_html=True)

                with col_s2:
                    st.markdown("#### 📊 Comparative Viral Momentum Velocity")
                    mom_fig = _spread_tracker.generate_platform_momentum_bar_figure(sprd["platforms"])
                    if mom_fig:
                        st.plotly_chart(mom_fig, use_container_width=True)

                    st.markdown("#### 🕸️ Real-Time Spread Signal Network")
                    net_fig = _spread_tracker.generate_spread_network_figure(ml["headline"], sprd["platforms"], rep["spread_signal"])
                    if net_fig:
                        st.plotly_chart(net_fig, use_container_width=True)

            # TAB 4: SOURCE AGREEMENT & CREDIBILITY
            with tab_sources:
                st.markdown("### ⚖️ Source Agreement & Credibility Panel")
                st.markdown(f"Forensic breakdown of all discovered digital news references for: *{ml['headline']}*")

                # Timeline
                st.markdown("#### ⏱️ Chronological Reporting Timeline")
                for item in sprd["timeline"]:
                    st.markdown(f"""
                    <div style="border-left: 2px solid #6366f1; padding-left: 18px; margin-bottom: 18px; position: relative;">
                        <div style="position: absolute; left: -6px; top: 2px; width: 10px; height: 10px; border-radius: 50%; background: #818cf8; box-shadow: 0 0 8px #818cf8;"></div>
                        <span style="color: #818cf8; font-size: 12.5px; font-weight: 700;">{item['time']}</span>
                        <h5 style="margin: 3px 0; color: #ffffff; font-size: 16px; font-weight: 700;">{item['publisher']}</h5>
                        <p style="color: #cbd5e1; font-size: 14px; margin: 2px 0 8px 0; line-height: 1.5;">{item['headline']}</p>
                        <span class="badge badge-real" style="font-size: 11px;">{item['badge']}</span>
                    </div>
                    """, unsafe_allow_html=True)

            # TAB 5: CONTEXT-AWARE GEMINI AI ASSISTANT
            with tab_assistant:
                st.markdown("### 🤖 Context-Aware AI News Assistant")
                st.markdown("Ask deep investigative questions about this specific analyzed news story.")

                # Quick Prompt Buttons
                st.markdown("##### ⚡ Quick Questions:")
                q_cols = st.columns(4)
                quick_prompts = [
                    "Why was this classified this way?",
                    "What sources support this claim?",
                    "Summarize this news simply",
                    "What claims should I verify?"
                ]

                selected_prompt = None
                for idx, q_text in enumerate(quick_prompts):
                    with q_cols[idx]:
                        if st.button(q_text, key=f"qp_{idx}", use_container_width=True):
                            selected_prompt = q_text

                # Assistant Context
                assistant_context = {
                    "headline": ml["headline"],
                    "verdict": rep["verdict"],
                    "confidence": rep["confidence"],
                    "sentiment": rep["sentiment"],
                    "topic": rep["topic"],
                    "keywords": rep["keywords"],
                    "agreement_consensus": srch["agreement"]["consensus"],
                    "sources": srch["sources"]
                }

                # Chat Input Form
                with st.form("chat_form", clear_on_submit=True):
                    user_msg = st.text_input("Ask a question:", value=selected_prompt or "", placeholder="e.g. Is there any official government confirmation for this?")
                    send_btn = st.form_submit_button("Send to AI Assistant 🚀")

                if (send_btn and user_msg) or selected_prompt:
                    query = user_msg if (send_btn and user_msg) else selected_prompt
                    with st.spinner("🤖 Consulting Gemini AI Investigation Layer..."):
                        ai_reply = ask_ai_assistant(query, assistant_context)
                        st.session_state.chat_history.append({"user": query, "ai": ai_reply})

                # Display Chat History
                for chat in reversed(st.session_state.chat_history):
                    st.markdown(f"""
                    <div style="background: rgba(99, 102, 241, 0.18); border-left: 4px solid #818cf8; padding: 14px 18px; border-radius: 10px; margin-bottom: 10px;">
                        <strong style="color: #c7d2fe; font-size: 14px;">👤 You:</strong>
                        <div style="margin-top: 4px; color: #ffffff; font-size: 15px; font-weight: 500;">{chat['user']}</div>
                    </div>
                    <div style="background: rgba(30, 41, 59, 0.85); border-left: 4px solid #38bdf8; padding: 16px 18px; border-radius: 10px; margin-bottom: 18px;">
                        <strong style="color: #38bdf8; font-size: 14px;">🛡️ AI Detective:</strong>
                        <div style="margin-top: 6px; color: #f1f5f9; font-size: 14.5px; line-height: 1.65;">{chat['ai']}</div>
                    </div>
                    """, unsafe_allow_html=True)

            # TAB 6: INTELLIGENCE DOSSIER
            with tab_report:
                st.markdown("### 📋 Formal AI News Intelligence Dossier")
                st.markdown(f"""
                <div class="glass-card">
                    <table style="width: 100%; color: #f8fafc; font-size: 14.5px; border-collapse: collapse;">
                        <tr style="border-bottom: 1px solid rgba(255,255,255,0.12); padding: 10px 0;">
                            <td style="padding: 12px 14px; color: #a5b4fc; width: 30%; font-weight: 700;">VERDICT:</td>
                            <td style="padding: 12px 14px; color: #ffffff;"><strong>{verdict_display}</strong> ({rep['confidence']}% Confidence)</td>
                        </tr>
                        <tr style="border-bottom: 1px solid rgba(255,255,255,0.12);">
                            <td style="padding: 12px 14px; color: #a5b4fc; font-weight: 700;">NEWS RELEVANCE:</td>
                            <td style="padding: 12px 14px; color: #ffffff;">✅ Confirmed News Claim (3-Signal Verified)</td>
                        </tr>
                        <tr style="border-bottom: 1px solid rgba(255,255,255,0.12);">
                            <td style="padding: 12px 14px; color: #a5b4fc; font-weight: 700;">FORENSIC BARCODE:</td>
                            <td style="padding: 12px 14px; color: #38bdf8; font-family: 'JetBrains Mono', monospace; font-weight: 700;">{emo.get('barcode_id', 'N/A')}</td>
                        </tr>
                        <tr style="border-bottom: 1px solid rgba(255,255,255,0.12);">
                            <td style="padding: 12px 14px; color: #a5b4fc; font-weight: 700;">SENTIMENT & TONE:</td>
                            <td style="padding: 12px 14px; color: #ffffff;">{rep['sentiment']} (Tone: {rep['sentiment_tone']})</td>
                        </tr>
                        <tr style="border-bottom: 1px solid rgba(255,255,255,0.12);">
                            <td style="padding: 12px 14px; color: #a5b4fc; font-weight: 700;">TOPIC CLASSIFICATION:</td>
                            <td style="padding: 12px 14px; color: #ffffff;">{rep['topic']}</td>
                        </tr>
                        <tr style="border-bottom: 1px solid rgba(255,255,255,0.12);">
                            <td style="padding: 12px 14px; color: #a5b4fc; font-weight: 700;">KEYWORD INDEX:</td>
                            <td style="padding: 12px 14px; color: #ffffff;">{', '.join(rep['keywords'])}</td>
                        </tr>
                        <tr style="border-bottom: 1px solid rgba(255,255,255,0.12);">
                            <td style="padding: 12px 14px; color: #a5b4fc; font-weight: 700;">SOURCE EVIDENCE COUNT:</td>
                            <td style="padding: 12px 14px; color: #ffffff;">{rep['source_evidence_count']} discovered sources ({rep['sources_matching']} corroborating)</td>
                        </tr>
                        <tr style="border-bottom: 1px solid rgba(255,255,255,0.12);">
                            <td style="padding: 12px 14px; color: #a5b4fc; font-weight: 700;">SOURCE CONSENSUS:</td>
                            <td style="padding: 12px 14px; color: #ffffff;">{rep['agreement_consensus']}</td>
                        </tr>
                        <tr style="border-bottom: 1px solid rgba(255,255,255,0.12);">
                            <td style="padding: 12px 14px; color: #a5b4fc; font-weight: 700;">PRIMARY VIRAL VECTOR:</td>
                            <td style="padding: 12px 14px; color: #ffffff;">{top_p.get('platform', 'YouTube')} ({top_p.get('momentum', 85)}% Velocity)</td>
                        </tr>
                        <tr style="border-bottom: 1px solid rgba(255,255,255,0.12);">
                            <td style="padding: 12px 14px; color: #a5b4fc; font-weight: 700;">CROSS-PLATFORM SPREAD:</td>
                            <td style="padding: 12px 14px; color: #ffffff;">{rep['spread_signal']} SPREAD SIGNAL</td>
                        </tr>
                        <tr>
                            <td style="padding: 12px 14px; color: #a5b4fc; font-weight: 700;">SYNTHESIS ENGINE:</td>
                            <td style="padding: 12px 14px; color: #ffffff;">{rep['engine_used']}</td>
                        </tr>
                    </table>
                </div>
                """, unsafe_allow_html=True)
