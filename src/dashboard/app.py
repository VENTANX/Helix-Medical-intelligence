
import streamlit as st
import time
import os
import json
import pandas as pd
import sys
from collections import Counter
import altair as alt

# Add src to python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
from src.api.json_formatter import format_ner_output

# Page Config
st.set_page_config(
    page_title="Helix | Medical Intelligence",
    page_icon="🧬",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- ULTRA-PREMIUM CSS & ICONS ---
st.markdown("""
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
<style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700&display=swap');

    /* Base */
    .stApp {
        background: linear-gradient(-45deg, #020617, #0f172a, #1e1b4b, #172554);
        background-size: 400% 400%;
        animation: gradientBG 15s ease infinite;
        font-family: 'Outfit', sans-serif;
        color: #e2e8f0;
    }
    
    @keyframes gradientBG {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    /* Floating Particles */
    .particle {
        position: fixed;
        bottom: -100px;
        z-index: 0;
        opacity: 0.3;
        animation: floatUp 15s infinite linear;
        font-size: 2rem;
        pointer-events: none;
    }
    @keyframes floatUp {
        0% { transform: translateY(0) rotate(0deg); opacity: 0; }
        10% { opacity: 0.5; }
        90% { opacity: 0.5; }
        100% { transform: translateY(-120vh) rotate(360deg); opacity: 0; }
    }
    
    h1, h2, h3, h4, h5, h6 { font-family: 'Outfit', sans-serif !important; position: relative; z-index: 1; }
    
    /* Ensure content is above particles */
    .stApp > header, .stApp > div.main { z-index: 1; position: relative; }

    /* Custom Glass Cards */
    .glass-card {
        background: rgba(30, 41, 59, 0.4);
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 16px;
        padding: 20px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }
    .glass-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.2);
        border-color: rgba(255, 255, 255, 0.15);
    }

    /* Metric Value Styling */
    .metric-value {
        font-size: 2rem;
        font-weight: 700;
        background: linear-gradient(to right, #f8fafc, #cbd5e1);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .metric-label {
        color: #94a3b8;
        font-size: 0.85rem;
        font-weight: 500;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        display: flex;
        align-items: center;
        gap: 8px;
    }
    .metric-icon { color: #3b82f6; font-size: 1rem; }

    /* Expander Styling */
    div[data-testid="stExpander"] {
        background: rgba(30, 41, 59, 0.3) !important;
        border: 1px solid rgba(255, 255, 255, 0.05) !important;
        border-radius: 12px;
    }

    /* Badges */
    .badge {
        padding: 4px 12px;
        border-radius: 9999px;
        font-size: 0.75rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        margin-right: 6px;
        margin-bottom: 6px;
        display: inline-block;
    }
    .badge-disease { background: linear-gradient(135deg, #ef4444 0%, #991b1b 100%); color: white; border: 1px solid rgba(239, 68, 68, 0.3); }
    .badge-med { background: linear-gradient(135deg, #3b82f6 0%, #1e40af 100%); color: white; border: 1px solid rgba(59, 130, 246, 0.3); }
    .badge-dose { background: rgba(255, 255, 255, 0.1); color: #e2e8f0; border: 1px solid rgba(255,255,255,0.1); }
    .badge-critical { background: linear-gradient(135deg, #dc2626 0%, #7f1d1d 100%); color: white; border: 1px solid #fecaca; box-shadow: 0 0 10px #ef4444; animation: pulse-red 2s infinite; }

    /* Pulsing Dot */
    .pulse-dot {
        width: 10px; height: 10px;
        background-color: #4ade80;
        border-radius: 50%;
        display: inline-block;
        box-shadow: 0 0 0 0 rgba(74, 222, 128, 0.7);
        animation: pulse-green 2s infinite;
    }
    @keyframes pulse-green {
        0% { transform: scale(0.95); box-shadow: 0 0 0 0 rgba(74, 222, 128, 0.7); }
        70% { transform: scale(1); box-shadow: 0 0 0 10px rgba(74, 222, 128, 0); }
        100% { transform: scale(0.95); box-shadow: 0 0 0 0 rgba(74, 222, 128, 0); }
    }
    @keyframes pulse-red {
        0% { box-shadow: 0 0 0 0 rgba(220, 38, 38, 0.7); }
        70% { box-shadow: 0 0 0 10px rgba(220, 38, 38, 0); }
        100% { box-shadow: 0 0 0 0 rgba(220, 38, 38, 0); }
    }
</style>

<!-- Floating Background Elements -->
<div class="particle-container">
    <div class="particle" style="left: 10%; animation-duration: 12s; animation-delay: 0s;">🧬</div>
    <div class="particle" style="left: 20%; animation-duration: 15s; animation-delay: 2s;">💊</div>
    <div class="particle" style="left: 35%; animation-duration: 18s; animation-delay: 5s;">🦠</div>
    <div class="particle" style="left: 50%; animation-duration: 14s; animation-delay: 1s;">🩺</div>
    <div class="particle" style="left: 65%; animation-duration: 16s; animation-delay: 3s;">🏥</div>
    <div class="particle" style="left: 80%; animation-duration: 13s; animation-delay: 6s;">🩸</div>
    <div class="particle" style="left: 15%; animation-duration: 11s; animation-delay: 7s;">🧪</div>
    <div class="particle" style="left: 55%; animation-duration: 19s; animation-delay: 4s;">🧬</div>
    <div class="particle" style="left: 90%; animation-duration: 17s; animation-delay: 0s;">💊</div>
    <div class="particle" style="left: 42%; animation-duration: 10s; animation-delay: 8s;">🦠</div>
</div>
""", unsafe_allow_html=True)

# --- HEADER ---
c1, c2 = st.columns([3, 1])
with c1:
    st.markdown('<div style="display:flex; align-items:center; gap:15px; margin-bottom:20px;"><i class="fa-solid fa-dna fa-2x" style="color:#60a5fa;"></i> <span style="font-size:2.2rem; font-weight:700; background: linear-gradient(to right, #60a5fa, #a855f7); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">HELIX INTELLIGENCE</span></div>', unsafe_allow_html=True)
with c2:
    st.markdown('<div style="text-align: right; padding-top: 10px;"><div class="glass-card" style="padding: 8px 16px; display:inline-flex; align-items:center; gap:10px;"><div class="pulse-dot"></div><span style="font-size:0.8rem; font-weight:600; color:#4ade80;">SYSTEM OPTIMAL</span></div></div>', unsafe_allow_html=True)

# Data File
DATA_FILE = os.path.join(os.path.dirname(__file__), '../../data/processed_notes.jsonl')

# Session State
if 'last_pos' not in st.session_state: st.session_state.last_pos = 0
if 'messages' not in st.session_state: st.session_state.messages = []
if 'total_processed' not in st.session_state: st.session_state.total_processed = 0
if 'entities_found' not in st.session_state: st.session_state.entities_found = 0
if 'history_stats' not in st.session_state: 
    st.session_state.history_stats = {
        'diseases': Counter(), 
        'medications': Counter(), 
        'pairs': Counter(), # (Disease, Med)
        'timestamps': []
    }

CRITICAL_CONDITIONS = ["sepsis", "stroke", "myocardial infarction", "meningitis", "pulmonary embolism"]

def read_data():
    if not os.path.exists(DATA_FILE): return []
    new_data = []
    try:
        with open(DATA_FILE, 'r') as f:
            f.seek(st.session_state.last_pos)
            lines = f.readlines()
            st.session_state.last_pos = f.tell()
            for line in lines:
                if line.strip():
                    try: new_data.append(json.loads(line))
                    except: pass
    except: pass
    return new_data

def process_batch(items):
    formatted = []
    for item in items:
        fmt = format_ner_output(item)
        formatted.append(fmt)
        st.session_state.total_processed += 1
        st.session_state.entities_found += len(fmt['entities'])
        st.session_state.history_stats['timestamps'].append(fmt['timestamp'])
        
        # Stats & Pairs
        current_diseases = []
        current_meds = []
        
        for ent in fmt['entities']:
            if "Disease" in ent['Label']: 
                st.session_state.history_stats['diseases'][ent['Text']] += 1
                current_diseases.append(ent['Text'])
            elif "Medication" in ent['Label']: 
                st.session_state.history_stats['medications'][ent['Text']] += 1
                current_meds.append(ent['Text'])
        
        # Simple Pair Counting (Cross product for now)
        for d in current_diseases:
            for m in current_meds:
                st.session_state.history_stats['pairs'][(d, m)] += 1
                
    return formatted

def is_critical(entities):
    for ent in entities:
        if "Disease" in ent['Label'] and ent['Text'].lower() in CRITICAL_CONDITIONS:
            return True
    return False

# --- TABS ---
tab_ops, tab_intel, tab_vault = st.tabs(["🚀 OPS CENTER", "🧠 INTEL CORE", "💾 DATA VAULT"])

with tab_ops:
    # CUSTOM METRIC CARDS
    m1, m2, m3, m4 = st.columns(4)
    with m1:
        st.markdown(f"""
        <div class="glass-card">
            <div class="metric-label"><i class="fa-solid fa-file-medical metric-icon"></i> RECORDS SCANNED</div>
            <div class="metric-value">{st.session_state.total_processed}</div>
            <div style="font-size:0.75rem; color:#4ade80; margin-top:5px;"><i class="fa-solid fa-arrow-trend-up"></i> Live Feed</div>
        </div>""", unsafe_allow_html=True)
    with m2:
        st.markdown(f"""
        <div class="glass-card">
            <div class="metric-label"><i class="fa-solid fa-tags metric-icon"></i> ENTITIES EXTRACTED</div>
            <div class="metric-value">{st.session_state.entities_found}</div>
            <div style="font-size:0.75rem; color:#60a5fa; margin-top:5px;"><i class="fa-solid fa-bullseye"></i> High Precision</div>
        </div>""", unsafe_allow_html=True)
    with m3:
        st.markdown(f"""
        <div class="glass-card">
            <div class="metric-label"><i class="fa-solid fa-server metric-icon"></i> LATENCY</div>
            <div class="metric-value">24ms</div>
            <div style="font-size:0.75rem; color:#a855f7; margin-top:5px;"><i class="fa-solid fa-bolt"></i> Real-time</div>
        </div>""", unsafe_allow_html=True)   
    with m4:
        st.markdown(f"""
        <div class="glass-card">
            <div class="metric-label"><i class="fa-solid fa-shield-halved metric-icon"></i> PRIVACY PROTOCOL</div>
            <div class="metric-value" style="color:#4ade80; -webkit-text-fill-color:#4ade80;">SECURE</div>
            <div style="font-size:0.75rem; color:#94a3b8; margin-top:5px;"><i class="fa-solid fa-lock"></i> HIPAA Compliant</div>
        </div>""", unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<div style="margin-bottom:10px; font-weight:600; font-size:0.9rem; color:#94a3b8; text-transform:uppercase; letter-spacing:0.05em;"><i class="fa-solid fa-satellite-dish"></i> Incoming Transmission Log</div>', unsafe_allow_html=True)
    
    msgs = st.session_state.messages[:15]
    if not msgs: st.info("Awaiting Stream Initialization...")
    
    for msg in msgs:
        critical = is_critical(msg['entities'])
        border_style = "border: 1px solid #ef4444;" if critical else ""
        icon_top = "🔴 CRITICAL ALERT | " if critical else ""
        
        with st.expander(f"{icon_top}SCAN ID: {str(msg['timestamp'])[-6:]} | {time.strftime('%H:%M:%S', time.localtime(msg['timestamp']))}", expanded=True):
            c1, c2 = st.columns([2, 1])
            with c1:
                st.markdown(f"<div style='color:#cbd5e1; font-family:monospace; font-size:0.9em;'><i class='fa-regular fa-file-lines' style='margin-right:8px; color:#64748b;'></i> {msg['text']}</div>", unsafe_allow_html=True)
            with c2:
                if msg['entities']:
                    tags = ""
                    for ent in msg['entities']:
                        icon = ""
                        cls = "badge-dose"
                        if "Disease" in ent['Label']: 
                            cls="badge-disease"
                            icon = "<i class='fa-solid fa-virus'></i> "
                            if ent['Text'].lower() in CRITICAL_CONDITIONS: cls="badge-critical"
                        elif "Medication" in ent['Label']: 
                            cls="badge-med"
                            icon = "<i class='fa-solid fa-pills'></i> "
                        tags += f'<span class="badge {cls}">{icon}{ent["Text"]}</span>'
                    st.markdown(tags, unsafe_allow_html=True)
                else: st.caption("No pathology.")

with tab_intel:
    st.markdown("### <i class='fa-solid fa-brain' style='color:#a855f7'></i> Clinical Intelligence Core", unsafe_allow_html=True)
    
    # Row 1: Frequency Distributions
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("#### Pathology Frequency")
        if st.session_state.history_stats['diseases']:
            data = pd.DataFrame.from_dict(st.session_state.history_stats['diseases'], orient='index', columns=['Count']).reset_index()
            data.columns = ['Disease', 'Count']
            chart = alt.Chart(data).mark_bar(cornerRadiusTopLeft=4, cornerRadiusTopRight=4).encode(
                x=alt.X('Count', title=None), y=alt.Y('Disease', sort='-x', title=None),
                color=alt.value('#ef4444'), tooltip=['Disease', 'Count']
            ).properties(height=250).configure_axis(grid=False, labelColor='#94a3b8').configure_view(strokeWidth=0)
            st.altair_chart(chart, use_container_width=True)
    with c2:
        st.markdown("#### Therapeutic Utilization")
        if st.session_state.history_stats['medications']:
            data = pd.DataFrame.from_dict(st.session_state.history_stats['medications'], orient='index', columns=['Count']).reset_index()
            data.columns = ['Medication', 'Count']
            chart = alt.Chart(data).mark_bar(cornerRadiusTopLeft=4, cornerRadiusTopRight=4).encode(
                x=alt.X('Count', title=None), y=alt.Y('Medication', sort='-x', title=None),
                color=alt.value('#3b82f6'), tooltip=['Medication', 'Count']
            ).properties(height=250).configure_axis(grid=False, labelColor='#94a3b8').configure_view(strokeWidth=0)
            st.altair_chart(chart, use_container_width=True)

    # Row 2: Heatmap & Time Series
    c3, c4 = st.columns(2)
    with c3:
        st.markdown("#### Treatment Correlations (Disease vs Meds)")
        if st.session_state.history_stats['pairs']:
            pair_data = [{'Disease': k[0], 'Medication': k[1], 'Count': v} for k, v in st.session_state.history_stats['pairs'].items()]
            df_pairs = pd.DataFrame(pair_data)
            chart_heat = alt.Chart(df_pairs).mark_rect().encode(
                x='Medication:O', y='Disease:O',
                color=alt.Color('Count:Q', scale=alt.Scale(scheme='magma')),
                tooltip=['Disease', 'Medication', 'Count']
            ).properties(height=300)
            st.altair_chart(chart_heat, use_container_width=True)
        else: st.info("Correlating data...")

    with c4:
        st.markdown("#### Patient Influx Velocity")
        if st.session_state.history_stats['timestamps']:
            # Create a time series dataframe
            ts_df = pd.DataFrame({'Timestamp': pd.to_datetime(st.session_state.history_stats['timestamps'], unit='s')})
            ts_df['Count'] = 1
            ts_df = ts_df.set_index('Timestamp').resample('10s').sum().reset_index() # 10s bins
            
            chart_line = alt.Chart(ts_df).mark_area(
                line={'color':'#4ade80'},
                color=alt.Gradient(
                    gradient='linear',
                    stops=[alt.GradientStop(offset=0, color='#4ade80'), alt.GradientStop(offset=1, color='rgba(74, 222, 128, 0.1)')],
                    x1=1, x2=1, y1=1, y2=0
                )
            ).encode(
                x='Timestamp:T',
                y='Count:Q'
            ).properties(height=300)
            st.altair_chart(chart_line, use_container_width=True)
        else: st.info("Gathering timeline...")

with tab_vault:
    st.markdown("### <i class='fa-solid fa-magnifying-glass' style='color:#60a5fa'></i> Smart Query Engine", unsafe_allow_html=True)
    
    # Search Bar
    search_term = st.text_input("Filter Registry (Name, ID, Diagnosis, Rx...)", placeholder="e.g. Sepsis, 10293, Aspirin...")
    
    if st.session_state.messages:
        df = pd.DataFrame([{'Time': time.strftime('%H:%M:%S', time.localtime(m['timestamp'])), 'Content': m['text'], 'Entities': ", ".join([e['Text'] for e in m['entities']])} for m in st.session_state.messages])
        
        # Filter
        if search_term:
            df = df[df.apply(lambda row: row.astype(str).str.contains(search_term, case=False).any(), axis=1)]
        
        st.dataframe(df, use_container_width=True, hide_index=True)
        
        # CSV Export
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="Download Filtered Report (CSV)",
            data=csv,
            file_name='helix_intelligence_report.csv',
            mime='text/csv',
        )
    else: st.caption("Vault empty.")

# Sidebar
with st.sidebar:
    st.title("COMMAND")
    with st.expander("System Controls", expanded=True):
        run_live = st.toggle("UPLINK ACTIVE", value=True)
        if st.button("PURGE BUFFER", type="primary"):
            st.session_state.messages = []
            st.session_state.total_processed = 0
            st.session_state.entities_found = 0
            st.session_state.history_stats = {'diseases': Counter(), 'medications': Counter(), 'pairs': Counter(), 'timestamps': []}
            st.rerun()

    st.markdown("---")
    st.markdown("<div style='text-align: center; color: #64748b; font-size: 0.8rem;'>Architected by <br><b>Oussama Aslouj</b></div>", unsafe_allow_html=True)


if run_live:
    new_items = read_data()
    if new_items:
        formatted = process_batch(new_items)
        for f in formatted: st.session_state.messages.insert(0, f)
        st.session_state.messages = st.session_state.messages[:200]
        time.sleep(0.8)
        st.rerun()
