import os
import streamlit as st
import requests
import time

API_BASE_URL = os.getenv("API_BASE_URL", "http://127.0.0.1:8000").rstrip("/")

# ---------- PAGE CONFIG ----------

st.set_page_config(
    page_title="AI Support Autopilot",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------- SESSION ----------

defaults = {
    "logged_in": False,
    "name": "",
    "email": "",
    "chat_history": [],   # list of {question, answer, route, escalated}
    "email_sent": False,
    "session_ended": False
}

for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value

# ---------- MASTER CSS ----------

st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@600;700;800&family=DM+Sans:wght@300;400;500;600&family=JetBrains+Mono:wght@400;500&display=swap');

/* ── ROOT VARIABLES ─────────────────────────────────── */
:root {
    --lav-deep:    #6B4FA3;
    --lav-mid:     #9B7FD4;
    --lav-light:   #C9B8E8;
    --lav-pale:    #EDE5F9;
    --choc-deep:   #2C1503;
    --choc-mid:    #5C3317;
    --choc-warm:   #8B5E3C;
    --choc-light:  #D4A87A;
    --pista-deep:  #4A7C59;
    --pista-mid:   #7DB88A;
    --pista-light: #B8DDB8;
    --pista-pale:  #E4F5E4;
    --cream:       #FAF6F0;
    --white:       #FFFFFF;
}

/* ── GLOBAL RESET ───────────────────────────────────── */
* { box-sizing: border-box; }

html, body, [data-testid="stAppViewContainer"] {
    font-family: 'DM Sans', sans-serif;
    background: var(--cream) !important;
}

.stApp {
    background: linear-gradient(135deg, #FAF6F0 0%, #EDE5F9 40%, #E4F5E4 80%, #FAF6F0 100%) !important;
    background-attachment: fixed !important;
}

/* ── HIDE STREAMLIT CHROME ─────────────────────────── */
#MainMenu, footer, header { visibility: hidden !important; }
[data-testid="stToolbar"] { display: none !important; }
.block-container {
    padding-top: 1.5rem !important;
    padding-bottom: 3rem !important;
    max-width: 1100px !important;
}

/* ── SIDEBAR ────────────────────────────────────────── */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, var(--choc-deep) 0%, var(--choc-mid) 60%, #3D2410 100%) !important;
    border-right: 1px solid var(--choc-warm) !important;
}

section[data-testid="stSidebar"] * {
    color: var(--cream) !important;
    font-family: 'DM Sans', sans-serif !important;
}

section[data-testid="stSidebar"] .stMetric {
    background: rgba(255,255,255,0.06) !important;
    border: 1px solid rgba(201,184,232,0.2) !important;
    border-radius: 12px !important;
    padding: 10px 14px !important;
    margin-bottom: 10px !important;
    backdrop-filter: blur(6px) !important;
}

section[data-testid="stSidebar"] [data-testid="stMetricValue"] {
    color: var(--lav-light) !important;
    font-size: 1.05rem !important;
    font-weight: 600 !important;
}

section[data-testid="stSidebar"] [data-testid="stMetricLabel"] {
    color: var(--choc-light) !important;
    font-size: 0.72rem !important;
    letter-spacing: 0.08em !important;
    text-transform: uppercase !important;
}

section[data-testid="stSidebar"] hr {
    border-color: rgba(201,184,232,0.2) !important;
}

/* ── INPUT FIELDS ───────────────────────────────────── */
input[type="text"], textarea,
[data-testid="stTextInput"] input,
[data-testid="stTextArea"] textarea {
    background: rgba(255,255,255,0.85) !important;
    border: 1.5px solid var(--lav-light) !important;
    border-radius: 14px !important;
    color: var(--choc-deep) !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 0.95rem !important;
    padding: 12px 18px !important;
    transition: border-color 0.25s ease, box-shadow 0.25s ease !important;
}

input[type="text"]:focus, textarea:focus {
    border-color: var(--lav-deep) !important;
    box-shadow: 0 0 0 4px rgba(107,79,163,0.12) !important;
    outline: none !important;
}

[data-testid="stTextInput"] label,
[data-testid="stTextArea"] label {
    font-family: 'DM Sans', sans-serif !important;
    font-size: 0.82rem !important;
    font-weight: 600 !important;
    letter-spacing: 0.06em !important;
    text-transform: uppercase !important;
    color: var(--choc-mid) !important;
}

/* ── BUTTONS ────────────────────────────────────────── */
.stButton > button {
    font-family: 'DM Sans', sans-serif !important;
    font-weight: 600 !important;
    font-size: 0.9rem !important;
    letter-spacing: 0.04em !important;
    border-radius: 50px !important;
    padding: 0.65rem 2rem !important;
    border: none !important;
    cursor: pointer !important;
    transition: all 0.25s ease !important;
    background: linear-gradient(135deg, var(--lav-deep), var(--choc-mid)) !important;
    color: white !important;
    box-shadow: 0 4px 18px rgba(107,79,163,0.3) !important;
}

.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 28px rgba(107,79,163,0.42) !important;
    background: linear-gradient(135deg, var(--choc-mid), var(--lav-deep)) !important;
}

.stButton > button:active {
    transform: translateY(0) !important;
}

/* ── SPINNER ────────────────────────────────────────── */
[data-testid="stSpinner"] {
    color: var(--lav-deep) !important;
}

/* ── ALERTS ─────────────────────────────────────────── */
.stSuccess {
    background: linear-gradient(135deg, var(--pista-pale), rgba(184,221,184,0.5)) !important;
    border: 1px solid var(--pista-mid) !important;
    border-radius: 12px !important;
    color: var(--pista-deep) !important;
}

.stInfo {
    background: linear-gradient(135deg, var(--lav-pale), rgba(201,184,232,0.5)) !important;
    border: 1px solid var(--lav-mid) !important;
    border-radius: 12px !important;
    color: var(--lav-deep) !important;
}

.stError {
    background: linear-gradient(135deg, #FDE8E8, rgba(253,208,208,0.5)) !important;
    border: 1px solid #E57373 !important;
    border-radius: 12px !important;
}

.stWarning {
    background: linear-gradient(135deg, #FFF3E0, rgba(255,224,178,0.5)) !important;
    border: 1px solid var(--choc-light) !important;
    border-radius: 12px !important;
}

/* ── DIVIDERS ───────────────────────────────────────── */
hr {
    border-color: rgba(107,79,163,0.15) !important;
    margin: 1.5rem 0 !important;
}

</style>
""", unsafe_allow_html=True)

# ---------- COMPONENT STYLES ----------

HERO_CSS = """
<style>

/* ── HERO HEADER ────────────────────────────────────── */
.hero-wrap {
    text-align: center;
    padding: 2.5rem 1rem 1.5rem;
    position: relative;
}

.hero-badge {
    display: inline-block;
    background: linear-gradient(135deg, var(--lav-pale), var(--pista-pale));
    border: 1px solid var(--lav-light);
    border-radius: 50px;
    padding: 6px 20px;
    font-size: 0.72rem;
    font-weight: 600;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: var(--lav-deep);
    margin-bottom: 1.2rem;
}

.hero-title {
    font-family: 'Playfair Display', serif;
    font-size: clamp(2.2rem, 5vw, 3.4rem);
    font-weight: 800;
    background: linear-gradient(135deg, var(--choc-deep) 0%, var(--lav-deep) 50%, var(--pista-deep) 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    line-height: 1.15;
    margin-bottom: 0.7rem;
    letter-spacing: -0.02em;
}

.hero-sub {
    font-family: 'DM Sans', sans-serif;
    font-size: 1rem;
    color: var(--choc-warm);
    font-weight: 400;
    letter-spacing: 0.02em;
}

/* ── TECH PILLS ─────────────────────────────────────── */
.pills-row {
    display: flex;
    flex-wrap: wrap;
    gap: 10px;
    justify-content: center;
    margin: 1.4rem 0 0.5rem;
}

.pill {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    padding: 7px 16px;
    border-radius: 50px;
    font-size: 0.78rem;
    font-weight: 600;
    letter-spacing: 0.05em;
    border: 1.5px solid;
}

.pill-lav  { background: var(--lav-pale);   border-color: var(--lav-mid);   color: var(--lav-deep); }
.pill-choc { background: #F5EBE0;           border-color: var(--choc-warm); color: var(--choc-mid); }
.pill-pis  { background: var(--pista-pale); border-color: var(--pista-mid); color: var(--pista-deep); }

/* ── PIPELINE DIAGRAM ───────────────────────────────── */
.pipeline {
    display: flex;
    align-items: center;
    justify-content: center;
    flex-wrap: wrap;
    gap: 0;
    margin: 1.8rem 0 1rem;
    padding: 1.4rem 1rem;
    background: rgba(255,255,255,0.55);
    border: 1px solid rgba(201,184,232,0.35);
    border-radius: 20px;
    backdrop-filter: blur(10px);
}

.pipe-node {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 4px;
}

.pipe-icon {
    width: 46px;
    height: 46px;
    border-radius: 14px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1.3rem;
    font-weight: bold;
    box-shadow: 0 4px 14px rgba(0,0,0,0.1);
}

.pi-lav  { background: linear-gradient(135deg, var(--lav-light), var(--lav-mid)); }
.pi-choc { background: linear-gradient(135deg, var(--choc-light), var(--choc-warm)); }
.pi-pis  { background: linear-gradient(135deg, var(--pista-light), var(--pista-mid)); }

.pipe-label {
    font-size: 0.62rem;
    font-weight: 600;
    letter-spacing: 0.06em;
    text-transform: uppercase;
    color: var(--choc-mid);
    text-align: center;
}

.pipe-arrow {
    font-size: 1.1rem;
    color: var(--lav-light);
    margin: 0 2px;
    padding-bottom: 18px;
}

/* ── LOGIN CARD ─────────────────────────────────────── */
.login-card {
    background: rgba(255,255,255,0.75);
    border: 1px solid rgba(201,184,232,0.4);
    border-radius: 24px;
    padding: 2.5rem 2.8rem;
    max-width: 480px;
    margin: 0 auto;
    backdrop-filter: blur(12px);
    box-shadow: 0 20px 60px rgba(107,79,163,0.12), 0 4px 20px rgba(0,0,0,0.06);
}

.login-title {
    font-family: 'Playfair Display', serif;
    font-size: 1.55rem;
    font-weight: 700;
    color: var(--choc-deep);
    margin-bottom: 0.3rem;
}

.login-sub {
    font-size: 0.87rem;
    color: var(--choc-warm);
    margin-bottom: 1.6rem;
}

/* ── CHAT BUBBLES ───────────────────────────────────── */
.chat-wrap {
    display: flex;
    flex-direction: column;
    gap: 14px;
    margin: 1.6rem 0;
}

.bubble {
    padding: 16px 20px;
    border-radius: 20px;
    font-size: 0.96rem;
    line-height: 1.6;
    max-width: 88%;
    position: relative;
    animation: bubbleIn 0.4s cubic-bezier(0.34,1.56,0.64,1) both;
}

@keyframes bubbleIn {
    from { opacity:0; transform: translateY(16px) scale(0.96); }
    to   { opacity:1; transform: translateY(0)   scale(1); }
}

.bubble-user {
    background: linear-gradient(135deg, var(--lav-pale), rgba(201,184,232,0.6));
    border: 1px solid var(--lav-light);
    color: var(--choc-deep);
    margin-left: auto;
    border-bottom-right-radius: 6px;
}

.bubble-user::before {
    content: "👤  YOU";
    display: block;
    font-size: 0.65rem;
    font-weight: 700;
    letter-spacing: 0.1em;
    color: var(--lav-deep);
    margin-bottom: 6px;
}

.bubble-bot {
    background: linear-gradient(135deg, #FBF6F1, rgba(212,168,122,0.18));
    border: 1px solid rgba(139,94,60,0.25);
    color: var(--choc-deep);
    margin-right: auto;
    border-bottom-left-radius: 6px;
}

.bubble-bot::before {
    content: "🤖  AI AGENT";
    display: block;
    font-size: 0.65rem;
    font-weight: 700;
    letter-spacing: 0.1em;
    color: var(--choc-mid);
    margin-bottom: 6px;
}

/* ── ANALYTICS CARDS ────────────────────────────────── */
.analytics-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 14px;
    margin-top: 1rem;
}

.a-card {
    padding: 18px 20px;
    border-radius: 18px;
    text-align: center;
    border: 1px solid;
    backdrop-filter: blur(8px);
}

.a-card-lav {
    background: linear-gradient(135deg, var(--lav-pale), rgba(201,184,232,0.4));
    border-color: var(--lav-light);
}

.a-card-pis {
    background: linear-gradient(135deg, var(--pista-pale), rgba(184,221,184,0.4));
    border-color: var(--pista-light);
}

.a-card-choc {
    background: linear-gradient(135deg, #F5EBE0, rgba(212,168,122,0.3));
    border-color: var(--choc-light);
}

.a-card-red {
    background: linear-gradient(135deg, #FDE8E8, rgba(253,208,208,0.4));
    border-color: #E57373;
}

.a-icon { font-size: 1.5rem; margin-bottom: 6px; }

.a-label {
    font-size: 0.65rem;
    font-weight: 700;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    margin-bottom: 4px;
    color: var(--choc-warm);
}

.a-value {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.92rem;
    font-weight: 500;
    color: var(--choc-deep);
}

/* ── SECTION HEADER ─────────────────────────────────── */
.section-head {
    display: flex;
    align-items: center;
    gap: 10px;
    margin: 1.8rem 0 1rem;
}

.section-head-line {
    flex: 1;
    height: 1px;
    background: linear-gradient(90deg, rgba(107,79,163,0.3), transparent);
}

.section-head-text {
    font-family: 'DM Sans', sans-serif;
    font-size: 0.72rem;
    font-weight: 700;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: var(--lav-deep);
    white-space: nowrap;
}

/* ── SIDEBAR EXTRAS ─────────────────────────────────── */
.sb-profile {
    background: rgba(255,255,255,0.08);
    border: 1px solid rgba(201,184,232,0.2);
    border-radius: 16px;
    padding: 14px 16px;
    margin-bottom: 14px;
    display: flex;
    align-items: center;
    gap: 12px;
}

.sb-avatar {
    width: 40px;
    height: 40px;
    border-radius: 50%;
    background: linear-gradient(135deg, var(--lav-mid), var(--choc-warm));
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1.1rem;
    flex-shrink: 0;
}

.sb-name {
    font-weight: 600;
    font-size: 0.92rem;
    color: var(--cream);
}

.sb-email {
    font-size: 0.72rem;
    color: var(--choc-light);
    word-break: break-all;
}

.sb-section-label {
    font-size: 0.62rem;
    font-weight: 700;
    letter-spacing: 0.14em;
    text-transform: uppercase;
    color: var(--choc-light) !important;
    margin: 1rem 0 0.6rem;
    opacity: 0.75;
}

.agent-badge {
    display: flex;
    align-items: center;
    gap: 10px;
    background: rgba(255,255,255,0.06);
    border: 1px solid rgba(201,184,232,0.15);
    border-radius: 10px;
    padding: 9px 12px;
    margin-bottom: 7px;
}

.agent-dot {
    width: 8px;
    height: 8px;
    border-radius: 50%;
    flex-shrink: 0;
    animation: pulse 2s infinite;
}

@keyframes pulse {
    0%,100% { opacity:1; transform:scale(1); }
    50%      { opacity:0.5; transform:scale(1.3); }
}

.agent-dot-lav  { background: var(--lav-light); }
.agent-dot-pis  { background: var(--pista-light); }
.agent-dot-choc { background: var(--choc-light); }

.agent-name {
    font-size: 0.78rem;
    font-weight: 500;
    color: var(--cream) !important;
}

/* ── QUESTION INPUT AREA ─────────────────────────────── */
.input-card {
    background: rgba(255,255,255,0.65);
    border: 1px solid rgba(201,184,232,0.4);
    border-radius: 20px;
    padding: 1.8rem 2rem;
    backdrop-filter: blur(10px);
    box-shadow: 0 8px 30px rgba(107,79,163,0.08);
}

/* ── EMAIL SENT BANNER ──────────────────────────────── */
.email-banner {
    background: linear-gradient(135deg, var(--pista-pale), rgba(184,221,184,0.5));
    border: 1px solid var(--pista-mid);
    border-radius: 14px;
    padding: 14px 20px;
    display: flex;
    align-items: center;
    gap: 12px;
    color: var(--pista-deep);
    font-weight: 500;
    font-size: 0.9rem;
    margin-top: 0.5rem;
}

/* ── BOTTOM TICKER BAR ──────────────────────────────── */
.ticker-bar {
    position: fixed;
    bottom: 0;
    left: 0;
    width: 100vw;
    height: 46px;
    background: linear-gradient(90deg, var(--choc-deep) 0%, #3A1A08 40%, var(--choc-mid) 100%);
    border-top: 1px solid rgba(201,184,232,0.25);
    display: flex;
    align-items: center;
    overflow: hidden;
    z-index: 9999;
    box-shadow: 0 -4px 24px rgba(44,21,3,0.35);
}

.ticker-label {
    flex-shrink: 0;
    display: flex;
    align-items: center;
    gap: 8px;
    padding: 0 18px 0 20px;
    border-right: 1px solid rgba(201,184,232,0.2);
    height: 100%;
    font-family: 'DM Sans', sans-serif;
    font-size: 0.65rem;
    font-weight: 700;
    letter-spacing: 0.14em;
    text-transform: uppercase;
    color: var(--lav-light);
    white-space: nowrap;
    background: rgba(0,0,0,0.15);
}

.ticker-dot-live {
    width: 7px;
    height: 7px;
    background: #7DB88A;
    border-radius: 50%;
    animation: livepulse 1.4s ease-in-out infinite;
}

@keyframes livepulse {
    0%,100% { opacity:1; box-shadow: 0 0 0 0 rgba(125,184,138,0.7); }
    50%      { opacity:0.7; box-shadow: 0 0 0 5px rgba(125,184,138,0); }
}

.ticker-track-wrap {
    flex: 1;
    overflow: hidden;
    height: 100%;
    display: flex;
    align-items: center;
    mask-image: linear-gradient(90deg, transparent 0%, black 4%, black 96%, transparent 100%);
    -webkit-mask-image: linear-gradient(90deg, transparent 0%, black 4%, black 96%, transparent 100%);
}

.ticker-track {
    display: flex;
    align-items: center;
    gap: 0;
    animation: tickerScroll 28s linear infinite;
    white-space: nowrap;
}

.ticker-track:hover { animation-play-state: paused; }

@keyframes tickerScroll {
    0%   { transform: translateX(0); }
    100% { transform: translateX(-50%); }
}

.ticker-node {
    display: inline-flex;
    align-items: center;
    gap: 7px;
    padding: 0 6px;
}

.ticker-icon {
    width: 28px;
    height: 28px;
    border-radius: 8px;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    font-size: 0.85rem;
    flex-shrink: 0;
}

.ti-lav  { background: rgba(155,127,212,0.3); border: 1px solid rgba(201,184,232,0.3); }
.ti-choc { background: rgba(139,94,60,0.3);   border: 1px solid rgba(212,168,122,0.3); }
.ti-pis  { background: rgba(125,184,138,0.3); border: 1px solid rgba(184,221,184,0.3); }

.ticker-name {
    font-family: 'DM Sans', sans-serif;
    font-size: 0.7rem;
    font-weight: 600;
    letter-spacing: 0.07em;
    text-transform: uppercase;
    color: rgba(250,246,240,0.85);
}

.ticker-arrow {
    font-size: 0.75rem;
    color: rgba(201,184,232,0.45);
    padding: 0 10px;
}

.ticker-sep {
    width: 1px;
    height: 22px;
    background: rgba(201,184,232,0.15);
    margin: 0 24px;
}

/* Push page content up so ticker doesn't overlap last element */
.block-container { padding-bottom: 5rem !important; }

/* ── STATIC BOTTOM PIPELINE BAR ─────────────────────── */
.pipeline-bar {
    position: fixed;
    bottom: 0;
    left: 0;
    width: 100vw;
    height: 50px;
    background: linear-gradient(90deg, var(--choc-deep) 0%, #3A1A08 50%, var(--choc-mid) 100%);
    border-top: 1px solid rgba(201,184,232,0.25);
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 0;
    z-index: 9999;
    box-shadow: 0 -4px 24px rgba(44,21,3,0.35);
    padding: 0 20px;
    overflow: hidden;
}

.pb-label {
    flex-shrink: 0;
    display: flex;
    align-items: center;
    gap: 7px;
    padding-right: 16px;
    margin-right: 14px;
    border-right: 1px solid rgba(201,184,232,0.2);
    font-family: 'DM Sans', sans-serif;
    font-size: 0.62rem;
    font-weight: 700;
    letter-spacing: 0.13em;
    text-transform: uppercase;
    color: var(--lav-light);
    white-space: nowrap;
}

.pb-dot {
    width: 6px;
    height: 6px;
    background: var(--pista-mid);
    border-radius: 50%;
    animation: livepulse 1.4s ease-in-out infinite;
}

@keyframes livepulse {
    0%,100% { opacity:1; box-shadow: 0 0 0 0 rgba(125,184,138,0.7); }
    50%      { opacity:0.7; box-shadow: 0 0 0 4px rgba(125,184,138,0); }
}

.pb-nodes {
    display: flex;
    align-items: center;
    gap: 0;
    flex: 1;
    justify-content: center;
}

.pb-node {
    display: inline-flex;
    align-items: center;
    gap: 5px;
    padding: 0 4px;
}

.pb-icon {
    width: 26px;
    height: 26px;
    border-radius: 7px;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    font-size: 0.8rem;
    flex-shrink: 0;
}

.pbi-lav  { background: rgba(155,127,212,0.28); border: 1px solid rgba(201,184,232,0.3); }
.pbi-choc { background: rgba(139,94,60,0.28);   border: 1px solid rgba(212,168,122,0.3); }
.pbi-pis  { background: rgba(125,184,138,0.28); border: 1px solid rgba(184,221,184,0.3); }

.pb-name {
    font-family: 'DM Sans', sans-serif;
    font-size: 0.62rem;
    font-weight: 600;
    letter-spacing: 0.05em;
    text-transform: uppercase;
    color: rgba(250,246,240,0.82);
    white-space: nowrap;
}

.pb-arrow {
    font-size: 0.65rem;
    color: rgba(201,184,232,0.4);
    padding: 0 5px;
    flex-shrink: 0;
}

</style>
"""

st.markdown(HERO_CSS, unsafe_allow_html=True)

# ── STATIC BOTTOM PIPELINE BAR (always rendered) ───────
st.markdown("""
<div class="pipeline-bar">
    <div class="pb-label"><div class="pb-dot"></div>Agent Pipeline</div>
    <div class="pb-nodes">
        <div class="pb-node"><div class="pb-icon pbi-lav">👤</div><div class="pb-name">User</div></div>
        <span class="pb-arrow">→</span>
        <div class="pb-node"><div class="pb-icon pbi-choc">🖥️</div><div class="pb-name">Streamlit</div></div>
        <span class="pb-arrow">→</span>
        <div class="pb-node"><div class="pb-icon pbi-lav">⚙️</div><div class="pb-name">FastAPI</div></div>
        <span class="pb-arrow">→</span>
        <div class="pb-node"><div class="pb-icon pbi-pis">🔷</div><div class="pb-name">LangGraph</div></div>
        <span class="pb-arrow">→</span>
        <div class="pb-node"><div class="pb-icon pbi-choc">🗂️</div><div class="pb-name">Router</div></div>
        <span class="pb-arrow">→</span>
        <div class="pb-node"><div class="pb-icon pbi-lav">🔍</div><div class="pb-name">RAG</div></div>
        <span class="pb-arrow">→</span>
        <div class="pb-node"><div class="pb-icon pbi-pis">💬</div><div class="pb-name">Answer</div></div>
        <span class="pb-arrow">→</span>
        <div class="pb-node"><div class="pb-icon pbi-choc">🚨</div><div class="pb-name">Escalation</div></div>
        <span class="pb-arrow">→</span>
        <div class="pb-node"><div class="pb-icon pbi-lav">🔗</div><div class="pb-name">MCP</div></div>
        <span class="pb-arrow">→</span>
        <div class="pb-node"><div class="pb-icon pbi-pis">✅</div><div class="pb-name">Human Loop</div></div>
        <span class="pb-arrow">→</span>
        <div class="pb-node"><div class="pb-icon pbi-choc">⚡</div><div class="pb-name">n8n</div></div>
        <span class="pb-arrow">→</span>
        <div class="pb-node"><div class="pb-icon pbi-pis">📧</div><div class="pb-name">Gmail</div></div>
    </div>
</div>
""", unsafe_allow_html=True)

# ---------- HERO HEADER (shared) ----------

def render_hero():
    st.markdown("""
    <div class="hero-wrap">
        <div class="hero-badge">✦ Human-in-the-Loop AI System</div>
        <div class="hero-title">AI Support Autopilot</div>
        <div class="hero-sub">Intelligent multi-agent support, escalation & automation</div>
        <div class="pills-row">
            <span class="pill pill-lav">🔷 LangGraph</span>
            <span class="pill pill-choc">🍫 RAG + ChromaDB</span>
            <span class="pill pill-pis">🌿 MCP Protocol</span>
            <span class="pill pill-lav">⚡ n8n Automation</span>
            <span class="pill pill-choc">📧 Gmail Integration</span>
        </div>
    </div>
    """, unsafe_allow_html=True)


# ---------- PIPELINE DIAGRAM (shared) ----------

def render_pipeline():
    st.markdown("""
    <div class="pipeline">
        <div class="pipe-node">
            <div class="pipe-icon pi-lav">👤</div>
            <div class="pipe-label">User</div>
        </div>
        <span class="pipe-arrow">→</span>
        <div class="pipe-node">
            <div class="pipe-icon pi-choc">🖥️</div>
            <div class="pipe-label">Streamlit</div>
        </div>
        <span class="pipe-arrow">→</span>
        <div class="pipe-node">
            <div class="pipe-icon pi-lav">⚙️</div>
            <div class="pipe-label">FastAPI</div>
        </div>
        <span class="pipe-arrow">→</span>
        <div class="pipe-node">
            <div class="pipe-icon pi-pis">🔷</div>
            <div class="pipe-label">LangGraph</div>
        </div>
        <span class="pipe-arrow">→</span>
        <div class="pipe-node">
            <div class="pipe-icon pi-choc">🗂️</div>
            <div class="pipe-label">Router</div>
        </div>
        <span class="pipe-arrow">→</span>
        <div class="pipe-node">
            <div class="pipe-icon pi-lav">🔍</div>
            <div class="pipe-label">RAG</div>
        </div>
        <span class="pipe-arrow">→</span>
        <div class="pipe-node">
            <div class="pipe-icon pi-pis">💬</div>
            <div class="pipe-label">Answer</div>
        </div>
        <span class="pipe-arrow">→</span>
        <div class="pipe-node">
            <div class="pipe-icon pi-choc">🚨</div>
            <div class="pipe-label">Escalation</div>
        </div>
        <span class="pipe-arrow">→</span>
        <div class="pipe-node">
            <div class="pipe-icon pi-lav">✅</div>
            <div class="pipe-label">Human Loop</div>
        </div>
        <span class="pipe-arrow">→</span>
        <div class="pipe-node">
            <div class="pipe-icon pi-pis">📧</div>
            <div class="pipe-label">Gmail</div>
        </div>
    </div>
    """, unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════
#  LOGIN PAGE
# ══════════════════════════════════════════════════════════

if not st.session_state.logged_in:

    render_hero()

    st.markdown("<br>", unsafe_allow_html=True)

    # Centered login card
    _, center_col, _ = st.columns([1, 1.6, 1])
    with center_col:
        st.markdown("""
        <div class="login-card">
            <div class="login-title">Welcome Back</div>
            <div class="login-sub">Sign in to access your AI support dashboard</div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<div style='max-width:480px;margin:0 auto;padding:0 0.5rem;'>", unsafe_allow_html=True)

        name  = st.text_input("Your Full Name",  placeholder="e.g. Arjun Sharma")
        email = st.text_input("Your Email Address", placeholder="e.g. arjun@company.com")

        st.markdown("<br>", unsafe_allow_html=True)

        col_btn, _ = st.columns([1, 1])
        with col_btn:
            if st.button("🚀  Launch Dashboard", use_container_width=True):
                if name and email:
                    st.session_state.logged_in    = True
                    st.session_state.name         = name
                    st.session_state.email        = email
                    st.rerun()
                else:
                    st.warning("Please fill in both fields to continue.")

        st.markdown("</div>", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════
#  MAIN DASHBOARD
# ══════════════════════════════════════════════════════════

else:

    # ── SIDEBAR ─────────────────────────────────────────

    with st.sidebar:

        st.markdown(f"""
        <div class="sb-profile">
            <div class="sb-avatar">👤</div>
            <div>
                <div class="sb-name">{st.session_state.name}</div>
                <div class="sb-email">{st.session_state.email}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown('<div class="sb-section-label">System Status</div>', unsafe_allow_html=True)

        st.metric("Active Agents", "4", delta="online")
        st.metric("Vector DB",     "ChromaDB")
        st.metric("Automation",    "n8n")
        st.metric("Messages",      len(st.session_state.chat_history))

        st.markdown('<div class="sb-section-label">Agent Pipeline</div>', unsafe_allow_html=True)

        agents = [
            ("agent-dot-pis",  "Router Agent"),
            ("agent-dot-lav",  "RAG Agent"),
            ("agent-dot-pis",  "Answer Agent"),
            ("agent-dot-choc", "Escalation Agent"),
        ]
        for dot, name_a in agents:
            st.markdown(f"""
            <div class="agent-badge">
                <div class="agent-dot {dot}"></div>
                <div class="agent-name">{name_a}</div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown('<div class="sb-section-label">Integrations</div>', unsafe_allow_html=True)

        for dot, name_a in [("agent-dot-lav","LangGraph Workflow"), ("agent-dot-choc","MCP Protocol"), ("agent-dot-pis","n8n Webhook")]:
            st.markdown(f"""
            <div class="agent-badge">
                <div class="agent-dot {dot}"></div>
                <div class="agent-name">{name_a}</div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("---")

        if st.button("🚪  Sign Out", use_container_width=True):
            for key in defaults:
                st.session_state[key] = defaults[key]
            st.rerun()

    # ── MAIN CONTENT ────────────────────────────────────

    render_hero()

    # ── ASK QUESTION ────────────────────────────────────

    st.markdown("""
    <div class="section-head">
        <div class="section-head-text">💬 Chat with AI Agents</div>
        <div class="section-head-line"></div>
    </div>
    """, unsafe_allow_html=True)

    if not st.session_state.session_ended:

        question = st.text_input(
            "💬  Your support question",
            placeholder="e.g. How do I track my order? What is the refund policy?",
            key="q_input"
        )

        col_send, col_end, col_hint = st.columns([1, 1, 3])
        with col_send:
            send_clicked = st.button("⚡  Send to Agents", use_container_width=True)
        with col_end:
            end_clicked = st.button("🔴  End Session", use_container_width=True)
        with col_hint:
            st.markdown(
                "<p style='color:var(--choc-warm);font-size:0.8rem;padding-top:0.55rem;'>"
                "Keep asking questions — approve & send email whenever you're ready.</p>",
                unsafe_allow_html=True
            )

        # ── SEND ────────────────────────────────────────
        if send_clicked and question:
            with st.spinner("🔄  Routing through LangGraph agents…"):
                try:
                    response = requests.post(
                        f"{API_BASE_URL}/chat",
                        json={
                            "question": question,
                            "email":    st.session_state.email,
                            "name":     st.session_state.name
                        },
                        timeout=60
                    )
                    response.raise_for_status()
                    data = response.json()
                    st.session_state.chat_history.append({
                        "question":  question,
                        "answer":    data["answer"],
                        "route":     data["route"],
                        "escalated": data["escalated"]
                    })
                    st.rerun()
                except Exception as e:
                    st.error(f"Connection error: {e}")

        elif send_clicked and not question:
            st.warning("Please type a question before sending.")

        # ── END SESSION ─────────────────────────────────
        if end_clicked:
            st.session_state.session_ended = True
            st.rerun()

    else:
        st.markdown("""
        <div style="
            background: linear-gradient(135deg, #FBF0E8, rgba(212,168,122,0.2));
            border: 1px solid rgba(139,94,60,0.3);
            border-radius: 14px;
            padding: 14px 20px;
            color: #5C3317;
            font-size: 0.9rem;
            font-weight: 500;
            display: flex;
            align-items: center;
            gap: 10px;
            margin-bottom: 0.5rem;
        ">
            🔴 &nbsp; Session ended. Review the conversation below and approve sending the response via email.
        </div>
        """, unsafe_allow_html=True)

    # ── CONVERSATION HISTORY ─────────────────────────────

    if st.session_state.chat_history:

        st.markdown("""
        <div class="section-head">
            <div class="section-head-text">🗨 Conversation</div>
            <div class="section-head-line"></div>
        </div>
        """, unsafe_allow_html=True)

        bubbles_html = '<div class="chat-wrap">'
        for turn in st.session_state.chat_history:
            route_tag = (
                f'<span style="font-size:0.68rem;opacity:0.6;margin-left:8px;">'
                f'· routed via {turn["route"]}</span>'
            ) if turn.get("route") else ""
            escalated_tag = (
                ' <span style="font-size:0.68rem;color:#E57373;font-weight:700;margin-left:6px;">'
                '⚠ ESCALATED</span>'
            ) if turn.get("escalated") else ""
            bubbles_html += f'<div class="bubble bubble-user">{turn["question"]}</div>'
            bubbles_html += f'<div class="bubble bubble-bot">{turn["answer"]}{route_tag}{escalated_tag}</div>'
        bubbles_html += '</div>'

        st.markdown(bubbles_html, unsafe_allow_html=True)

        # ── HUMAN-IN-LOOP (always visible once chat starts) ──

        st.markdown("""
        <div class="section-head">
            <div class="section-head-text">✅ Human Approval</div>
            <div class="section-head-line"></div>
        </div>
        """, unsafe_allow_html=True)

        last = st.session_state.chat_history[-1]

        col_email, col_info = st.columns([1, 2])
        with col_email:
            if st.button("📧  Approve & Send Email", use_container_width=True):
                with st.spinner("Triggering n8n webhook…"):
                    try:
                        response = requests.post(
                            f"{API_BASE_URL}/send-email",
                            json={
                                "question": last["question"],
                                "answer": last["answer"],
                                "email": st.session_state.email,
                                "name": st.session_state.name
                            },
                            timeout=30
                        )
                        response.raise_for_status()
                        st.session_state.email_sent = True
                        st.rerun()
                    except Exception as e:
                        st.error(f"Email error: {e}")

        with col_info:
            st.markdown(
                "<p style='color:var(--choc-warm);font-size:0.82rem;padding-top:0.55rem;'>"
                "Sends the <b>latest response</b> via n8n → Gmail. "
                "You can keep chatting and approve at any time.</p>",
                unsafe_allow_html=True
            )

        if st.session_state.email_sent:
            st.markdown("""
            <div class="email-banner">
                ✅ &nbsp; Webhook request accepted. Check the n8n workflow to confirm email delivery.
            </div>
            """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)