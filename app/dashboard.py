import os
import time
import json
import textwrap
from datetime import datetime, timezone
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
from dotenv import load_dotenv
from supabase import create_client

# ==========================================
# PAGE CONFIGURATION
# ==========================================
st.set_page_config(
    page_title="RealityDiff AI | Surveillance Command",
    page_icon="👁️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ==========================================
# RETRO-FUTURISTIC AI SURVEILLANCE & COMMAND THEME
# Near-black matte base, graphite panels, amber primary, subdued cyan touch.
# CRT scanlines, monospace system labels, NO purple gradients.
# ==========================================
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@300;400;500;600;700;800&family=Inter:wght@300;400;500;600;700&display=swap');

    /* Global Root & Typography */
    :root {
        --base-black: #08090B;
        --panel-graphite: #0F1217;
        --panel-graphite-light: #161A22;
        --border-graphite: #222834;
        --border-graphite-bright: #313A4B;
        --accent-amber: #FFB000;
        --accent-amber-glow: rgba(255, 176, 0, 0.25);
        --accent-amber-dim: rgba(255, 176, 0, 0.12);
        --accent-cyan: #00D8F6;
        --accent-cyan-dim: rgba(0, 216, 246, 0.12);
        --text-primary: #ECEFF4;
        --text-secondary: #8A94A6;
        --text-muted: #576275;
    }

    html, body, [class*="css"], .stApp {
        background-color: var(--base-black) !important;
        color: var(--text-primary);
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }

    code, pre, .mono, [data-testid="stMarkdownContainer"] code {
        font-family: 'JetBrains Mono', monospace !important;
    }

    /* Subtle CRT Scanlines Layer */
    .crt-scanlines {
        position: fixed;
        top: 0;
        left: 0;
        width: 100vw;
        height: 100vh;
        background: repeating-linear-gradient(
            0deg,
            rgba(0, 0, 0, 0.18) 0px,
            rgba(0, 0, 0, 0.18) 1px,
            transparent 1px,
            transparent 3px
        );
        pointer-events: none;
        z-index: 99999;
        opacity: 0.65;
    }

    /* Block Container Padding */
    .block-container {
        padding-top: 1.25rem;
        padding-bottom: 2rem;
        max-width: 1440px;
    }

    /* Sidebar Matte Styling */
    [data-testid="stSidebar"] {
        background-color: #0B0D11 !important;
        border-right: 1px solid var(--border-graphite) !important;
    }

    [data-testid="stSidebar"] h3, [data-testid="stSidebar"] h4 {
        font-family: 'JetBrains Mono', monospace !important;
        color: var(--accent-amber) !important;
        letter-spacing: 0.08em;
        font-size: 0.88rem;
        text-transform: uppercase;
    }

    /* Buttons: Tactical Industrial */
    .stButton > button {
        background: #12161E !important;
        color: var(--accent-amber) !important;
        border: 1px solid var(--border-graphite-bright) !important;
        border-radius: 4px !important;
        font-family: 'JetBrains Mono', monospace !important;
        font-size: 0.8rem !important;
        letter-spacing: 0.06em !important;
        text-transform: uppercase !important;
        font-weight: 600 !important;
        transition: all 0.15s ease-in-out !important;
    }

    .stButton > button:hover {
        background: var(--accent-amber) !important;
        color: #08090B !important;
        border-color: var(--accent-amber) !important;
        box-shadow: 0 0 12px var(--accent-amber-glow) !important;
    }

    /* Tabs Styling */
    [data-baseweb="tab-list"] {
        background-color: var(--panel-graphite) !important;
        border: 1px solid var(--border-graphite) !important;
        border-radius: 6px !important;
        padding: 4px !important;
        gap: 6px !important;
    }

    [data-baseweb="tab"] {
        font-family: 'JetBrains Mono', monospace !important;
        font-size: 0.8rem !important;
        letter-spacing: 0.06em !important;
        text-transform: uppercase !important;
        color: var(--text-secondary) !important;
        border-radius: 4px !important;
        padding: 8px 16px !important;
        border: 1px solid transparent !important;
    }

    [data-baseweb="tab"][aria-selected="true"] {
        background-color: var(--panel-graphite-light) !important;
        color: var(--accent-amber) !important;
        border: 1px solid var(--border-graphite-bright) !important;
        border-bottom: 2px solid var(--accent-amber) !important;
        font-weight: 700 !important;
        box-shadow: inset 0 1px 0 rgba(255, 176, 0, 0.3) !important;
    }

    /* Command Center Surveillance Header */
    .command-header {
        background: var(--panel-graphite);
        border: 1px solid var(--border-graphite);
        border-top: 2px solid var(--accent-amber);
        border-radius: 8px;
        padding: 20px 24px;
        margin-bottom: 20px;
        box-shadow: 0 8px 30px rgba(0, 0, 0, 0.7), inset 0 1px 0 rgba(255, 176, 0, 0.15);
        display: flex;
        justify-content: space-between;
        align-items: center;
        flex-wrap: wrap;
        gap: 16px;
    }

    .command-title {
        font-family: 'JetBrains Mono', monospace;
        font-size: 1.65rem;
        font-weight: 800;
        letter-spacing: 0.04em;
        color: var(--accent-amber);
        text-shadow: 0 0 16px rgba(255, 176, 0, 0.35);
        margin: 0;
        display: flex;
        align-items: center;
        gap: 12px;
    }

    .command-subtext {
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.76rem;
        letter-spacing: 0.06em;
        color: var(--text-secondary);
        margin-top: 5px;
        text-transform: uppercase;
    }

    /* Monospace Status LED Badges */
    .status-badge-amber {
        display: inline-flex;
        align-items: center;
        gap: 8px;
        background: var(--accent-amber-dim);
        border: 1px solid rgba(255, 176, 0, 0.4);
        color: var(--accent-amber);
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.75rem;
        font-weight: 700;
        padding: 5px 12px;
        border-radius: 4px;
        letter-spacing: 0.08em;
        text-transform: uppercase;
    }

    .status-badge-cyan {
        display: inline-flex;
        align-items: center;
        gap: 8px;
        background: var(--accent-cyan-dim);
        border: 1px solid rgba(0, 216, 246, 0.4);
        color: var(--accent-cyan);
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.75rem;
        font-weight: 700;
        padding: 5px 12px;
        border-radius: 4px;
        letter-spacing: 0.08em;
        text-transform: uppercase;
    }

    .pulse-dot-amber {
        width: 7px;
        height: 7px;
        background-color: var(--accent-amber);
        border-radius: 50%;
        box-shadow: 0 0 8px var(--accent-amber);
        animation: amberPulse 1.8s infinite;
    }

    @keyframes amberPulse {
        0% { transform: scale(0.9); box-shadow: 0 0 0 0 rgba(255, 176, 0, 0.7); }
        70% { transform: scale(1.15); box-shadow: 0 0 0 6px rgba(255, 176, 0, 0); }
        100% { transform: scale(0.9); box-shadow: 0 0 0 0 rgba(255, 176, 0, 0); }
    }

    /* Metric KPI Cards (Graphite + Amber / Cyan) */
    .metric-panel {
        background: var(--panel-graphite);
        border: 1px solid var(--border-graphite);
        border-radius: 6px;
        padding: 16px 18px;
        position: relative;
        transition: border-color 0.2s ease, box-shadow 0.2s ease;
    }

    .metric-panel:hover {
        border-color: var(--accent-amber);
        box-shadow: 0 4px 16px rgba(0, 0, 0, 0.6), 0 0 8px var(--accent-amber-glow);
    }

    .metric-panel-label {
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.72rem;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        color: var(--text-secondary);
        margin-bottom: 6px;
        display: flex;
        align-items: center;
        gap: 6px;
    }

    .metric-panel-value {
        font-family: 'JetBrains Mono', monospace;
        font-size: 1.85rem;
        font-weight: 800;
        letter-spacing: -0.02em;
        color: var(--text-primary);
        line-height: 1.1;
    }

    .metric-panel-sub {
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.72rem;
        color: var(--text-muted);
        margin-top: 6px;
        letter-spacing: 0.02em;
    }

    /* Native Container Bordering Override */
    [data-testid="stVerticalBlockBorderWrapper"] {
        background-color: var(--panel-graphite) !important;
        border-color: var(--border-graphite) !important;
        border-radius: 6px !important;
    }
    </style>
    <div class="crt-scanlines"></div>
    """,
    unsafe_allow_html=True,
)

# ==========================================
# LOAD ENVIRONMENT & INITIALIZE
# ==========================================
load_dotenv()
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

# ==========================================
# SIDEBAR CONTROLS & MONITORING
# ==========================================
with st.sidebar:
    st.markdown("### // COMMAND_CENTER // CONFIG")

    # Connection Status Indicator (Retro Amber/Graphite)
    if SUPABASE_URL and SUPABASE_KEY:
        st.markdown(
            """
            <div style="background: #0E1116; border: 1px solid #28313F; border-left: 3px solid #FFB000; border-radius: 4px; padding: 10px 12px; margin-bottom: 16px;">
                <div style="display: flex; align-items: center; gap: 8px;">
                    <span style="width: 7px; height: 7px; border-radius: 50%; background: #FFB000; display: inline-block; box-shadow: 0 0 6px #FFB000;"></span>
                    <span style="font-family: 'JetBrains Mono', monospace; font-size: 0.78rem; font-weight: 700; color: #FFB000; letter-spacing: 0.06em; text-transform: uppercase;">
                        [ SUPABASE // CONNECTED ]
                    </span>
                </div>
                <div style="font-family: 'JetBrains Mono', monospace; font-size: 0.68rem; color: #8A94A6; margin-top: 4px;">
                    STREAM // ENCRYPTED_SYNC
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    else:
        st.error("[WARN] SUPABASE_CREDENTIALS_MISSING")

    # Auto Refresh Setting
    st.markdown("#### // CHRONO_SYNC")
    auto_refresh = st.selectbox(
        "Auto-Refresh Interval",
        options=["Off", "3 seconds", "5 seconds", "10 seconds", "30 seconds"],
        index=0,
        help="Periodic polling interval for scene differential updates",
    )

    refresh_btn = st.button("⚡ EXECUTE_FORCE_SYNC", width="stretch")

    st.divider()

    # Event Simulation Tool for Testing
    with st.expander("// SIMULATOR // INJECT_EVENT", expanded=False):
        st.caption("Inject synthetic spatial difference event directly to telemetry stream.")
        sim_type = st.selectbox("Event Class", ["ADDED", "MOVED", "REMOVED"])
        sim_obj = st.selectbox("Target Object", ["laptop", "cup", "cell phone", "person", "backpack", "bottle"])
        sim_conf = st.slider("Confidence Index", 0.50, 1.00, 0.92, 0.01)
        sim_dist = st.slider("Displacement Delta (px)", 10, 300, 75) if sim_type == "MOVED" else None

        if st.button("🚀 INJECT_EVENT", width="stretch"):
            if SUPABASE_URL and SUPABASE_KEY:
                try:
                    sb_test = create_client(SUPABASE_URL, SUPABASE_KEY)
                    mock_pos = [round(float(os.urandom(1)[0]) * 3.5, 1), round(float(os.urandom(1)[0]) * 2.5, 1)]
                    sb_test.table("change_events").insert({
                        "event_type": sim_type,
                        "object_name": sim_obj,
                        "track_id": int(os.urandom(1)[0] % 50 + 1),
                        "confidence": sim_conf,
                        "distance": sim_dist,
                        "previous_position": [mock_pos[0] - 50, mock_pos[1] - 40] if sim_type == "MOVED" else None,
                        "current_position": mock_pos,
                    }).execute()
                    st.success("[SYSTEM] INJECTION_SUCCESSFUL")
                    st.rerun()
                except Exception as ex:
                    st.error(f"[ERROR] INJECTION_FAILED: {ex}")

# ==========================================
# DATA FETCHING
# ==========================================
@st.cache_data(ttl=2, show_spinner=False)
def fetch_events_from_supabase(url: str, key: str):
    t_start = time.time()
    sb = create_client(url, key)
    res = sb.table("change_events").select("*").order("created_at", desc=True).limit(500).execute()
    latency_ms = round((time.time() - t_start) * 1000)
    return res.data or [], latency_ms

raw_events = []
query_latency = 0
fetch_error = None

if SUPABASE_URL and SUPABASE_KEY:
    try:
        raw_events, query_latency = fetch_events_from_supabase(SUPABASE_URL, SUPABASE_KEY)
    except Exception as e:
        fetch_error = str(e)
else:
    fetch_error = "SUPABASE_URL or SUPABASE_KEY not configured."

if refresh_btn:
    st.cache_data.clear()
    st.rerun()

# Fallback Demo Data if Supabase is totally empty or errored
is_demo_mode = False
if fetch_error or not raw_events:
    if fetch_error:
        st.sidebar.warning(f"[LINK_WARN] {fetch_error}")
    use_demo = st.sidebar.checkbox("LOAD_SYNTHETIC_TELEMETRY", value=True if not raw_events else False)
    if use_demo:
        is_demo_mode = True
        raw_events = [
            {"id": 101, "event_type": "MOVED", "object_name": "laptop", "track_id": 4, "confidence": 0.94, "previous_position": [320.0, 410.0], "current_position": [410.0, 430.0], "distance": 92.2, "created_at": "2026-09-04T15:02:10Z"},
            {"id": 102, "event_type": "ADDED", "object_name": "bottle", "track_id": 12, "confidence": 0.88, "previous_position": None, "current_position": [620.0, 350.0], "distance": None, "created_at": "2026-09-04T14:58:30Z"},
            {"id": 103, "event_type": "REMOVED", "object_name": "cell phone", "track_id": 7, "confidence": 0.79, "previous_position": [510.0, 290.0], "current_position": None, "distance": None, "created_at": "2026-09-04T14:55:00Z"},
            {"id": 104, "event_type": "MOVED", "object_name": "chair", "track_id": 2, "confidence": 0.91, "previous_position": [200.0, 550.0], "current_position": [280.0, 570.0], "distance": 82.5, "created_at": "2026-09-04T14:50:15Z"},
            {"id": 105, "event_type": "ADDED", "object_name": "person", "track_id": 19, "confidence": 0.97, "previous_position": None, "current_position": [800.0, 300.0], "distance": None, "created_at": "2026-09-04T14:48:00Z"},
        ]

# Format DataFrame
df = pd.DataFrame(raw_events)
if not df.empty:
    if "created_at" in df.columns:
        df["datetime"] = pd.to_datetime(df["created_at"], errors="coerce")
    else:
        df["datetime"] = datetime.now(timezone.utc)
    
    if "confidence" in df.columns:
        df["confidence"] = pd.to_numeric(df["confidence"], errors="coerce").fillna(0.0)
    if "distance" in df.columns:
        df["distance"] = pd.to_numeric(df["distance"], errors="coerce").fillna(0.0)
    if "track_id" in df.columns:
        df["track_id"] = df["track_id"].fillna(0).astype(int)

# ==========================================
# SIDEBAR FILTERS
# ==========================================
with st.sidebar:
    st.markdown("#### // TELEMETRY_FILTERS")
    
    # Event Type Filter
    all_types = ["ADDED", "MOVED", "REMOVED"]
    selected_types = st.multiselect("Event Class Filter", options=all_types, default=all_types)
    
    # Object Class Filter
    available_objects = sorted(df["object_name"].dropna().unique().tolist()) if not df.empty and "object_name" in df.columns else []
    selected_objects = st.multiselect("Object Classes Monitored", options=available_objects, default=available_objects)
    
    # Confidence Slider
    min_confidence = st.slider("Min Confidence Index", min_value=0.0, max_value=1.0, value=0.0, step=0.05)
    
    # Search Query
    search_query = st.text_input("Query Object or Track ID", placeholder="e.g. bottle, 16").strip().lower()

# Apply Filters
filtered_df = df.copy() if not df.empty else pd.DataFrame()

if not filtered_df.empty:
    if selected_types:
        filtered_df = filtered_df[filtered_df["event_type"].isin(selected_types)]
    if selected_objects:
        filtered_df = filtered_df[filtered_df["object_name"].isin(selected_objects)]
    if "confidence" in filtered_df.columns:
        filtered_df = filtered_df[filtered_df["confidence"] >= min_confidence]
    if search_query:
        filtered_df = filtered_df[
            filtered_df["object_name"].astype(str).str.lower().str.contains(search_query)
            | filtered_df["track_id"].astype(str).str.contains(search_query)
        ]

# ==========================================
# COMMAND CENTER SURVEILLANCE HEADER
# ==========================================
total_count = len(df)
filtered_count = len(filtered_df)

st.markdown(
    f"""
    <div class="command-header">
        <div>
            <div style="font-family: 'JetBrains Mono', monospace; font-size: 0.72rem; letter-spacing: 0.12em; color: #8A94A6; margin-bottom: 2px;">
                // TACTICAL_SURVEILLANCE_TERMINAL // SEC-ID: RD-CORE
            </div>
            <h1 class="command-title">
                <span>👁️</span> REALITYDIFF // COMMAND_CENTER
                <span style="font-size: 0.75rem; font-weight: 700; color: #FFB000; background: rgba(255, 176, 0, 0.12); padding: 3px 8px; border-radius: 4px; border: 1px solid rgba(255, 176, 0, 0.35);">REV-2.0</span>
            </h1>
            <div class="command-subtext">
                Autonomous Spatial Differential Intelligence & Real-Time Scene Verification
            </div>
        </div>
        <div style="display: flex; align-items: center; gap: 12px; flex-wrap: wrap;">
            <div class="status-badge-amber">
                <span class="pulse-dot-amber"></span>
                <span>{'SYS_ONLINE // RECON_ACTIVE' if not is_demo_mode else 'SYS_SYNTHETIC // REPLAY_FEED'}</span>
            </div>
            <div class="status-badge-cyan">
                <span>PING // {query_latency}ms</span>
                <span>•</span>
                <span>SYNC // {total_count}_EVENTS</span>
            </div>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

# ==========================================
# TOP KPI METRICS ROW (GRAPHITE + AMBER / CYAN)
# ==========================================
added_count = int((df["event_type"] == "ADDED").sum()) if not df.empty else 0
moved_count = int((df["event_type"] == "MOVED").sum()) if not df.empty else 0
removed_count = int((df["event_type"] == "REMOVED").sum()) if not df.empty else 0
avg_distance = round(float(df[df["event_type"] == "MOVED"]["distance"].mean()), 1) if moved_count > 0 and "distance" in df.columns else 0.0

kpi_col1, kpi_col2, kpi_col3, kpi_col4, kpi_col5 = st.columns(5)

with kpi_col1:
    st.markdown(
        f"""
        <div class="metric-panel" style="border-top: 2px solid #8A94A6;">
            <div class="metric-panel-label">// SYS_LOG: TOTAL_EVENTS</div>
            <div class="metric-panel-value">{total_count}</div>
            <div class="metric-panel-sub">{filtered_count} MATCHING FILTER</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with kpi_col2:
    st.markdown(
        f"""
        <div class="metric-panel" style="border-top: 2px solid #00D8F6;">
            <div class="metric-panel-label" style="color: #00D8F6;">// DELTA: ADDED_TARGETS</div>
            <div class="metric-panel-value" style="color: #00D8F6;">{added_count}</div>
            <div class="metric-panel-sub">{(added_count/total_count*100):.0f}% OF STREAM COMPOSITION</div>
        </div>
        """ if total_count > 0 else """<div class="metric-panel"><div class="metric-panel-label">// ADDED</div><div class="metric-panel-value">0</div></div>""",
        unsafe_allow_html=True,
    )

with kpi_col3:
    st.markdown(
        f"""
        <div class="metric-panel" style="border-top: 2px solid #FFB000;">
            <div class="metric-panel-label" style="color: #FFB000;">// DELTA: DISPLACED_TARGETS</div>
            <div class="metric-panel-value" style="color: #FFB000;">{moved_count}</div>
            <div class="metric-panel-sub">AVG SHIFT: {avg_distance} PX</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with kpi_col4:
    st.markdown(
        f"""
        <div class="metric-panel" style="border-top: 2px solid #EF4444;">
            <div class="metric-panel-label" style="color: #EF4444;">// DELTA: VACATED_TARGETS</div>
            <div class="metric-panel-value" style="color: #EF4444;">{removed_count}</div>
            <div class="metric-panel-sub">{(removed_count/total_count*100):.0f}% OF STREAM COMPOSITION</div>
        </div>
        """ if total_count > 0 else """<div class="metric-panel"><div class="metric-panel-label">// REMOVED</div><div class="metric-panel-value">0</div></div>""",
        unsafe_allow_html=True,
    )

with kpi_col5:
    unique_objects = len(available_objects)
    st.markdown(
        f"""
        <div class="metric-panel" style="border-top: 2px solid #FFB000;">
            <div class="metric-panel-label" style="color: #FFB000;">// RECON: MONITORED_CLASSES</div>
            <div class="metric-panel-value" style="color: #FFB000;">{unique_objects}</div>
            <div class="metric-panel-sub">{', '.join(available_objects[:2])}{'...' if len(available_objects) > 2 else ''}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.markdown("<div style='height: 14px;'></div>", unsafe_allow_html=True)

# ==========================================
# MAIN TABS NAVIGATION (RETRO-FUTURISTIC)
# ==========================================
tab_feed, tab_analytics, tab_spatial, tab_explorer = st.tabs([
    "[01] // LIVE_EVENT_FEED",
    "[02] // ANALYTICS_AND_DYNAMICS",
    "[03] // SPATIAL_MOTION_RADAR",
    "[04] // DATA_EXPLORER_AND_EXPORT",
])

# ------------------------------------------
# TAB 1: LIVE EVENT FEED
# ------------------------------------------
with tab_feed:
    st.markdown("#### // TELEMETRY_STREAM // REAL_TIME_DIFFERENTIALS")
    
    if filtered_df.empty:
        st.info("[NOTICE] NO SCENE EVENTS MATCH CURRENT FILTER CONFIGURATION.")
    else:
        # Display Controls
        feed_col1, feed_col2 = st.columns([4, 1.2])
        with feed_col1:
            st.caption(f"TELEMETRY BUFFER: {len(filtered_df)} DETECTED EVENT{'S' if len(filtered_df) != 1 else ''} // REVERSE CHRONO")
        with feed_col2:
            sort_order = st.selectbox("SORT", ["Newest First", "Oldest First", "Highest Confidence"], label_visibility="collapsed")
        
        display_df = filtered_df.copy()
        if sort_order == "Newest First" and "datetime" in display_df.columns:
            display_df = display_df.sort_values(by="datetime", ascending=False)
        elif sort_order == "Oldest First" and "datetime" in display_df.columns:
            display_df = display_df.sort_values(by="datetime", ascending=True)
        elif sort_order == "Highest Confidence" and "confidence" in display_df.columns:
            display_df = display_df.sort_values(by="confidence", ascending=False)

        # Iterate through events
        for _, row in display_df.iterrows():
            etype = row.get("event_type", "UNKNOWN")
            obj_name = row.get("object_name", "Unknown Target")
            tr_id = row.get("track_id", "N/A")
            conf = row.get("confidence", 0.0)
            dist = row.get("distance", None)
            prev_pos = row.get("previous_position")
            curr_pos = row.get("current_position")
            created_at_str = str(row.get("created_at", ""))
            
            # Icon and status formatting
            if etype == "ADDED":
                icon = "🟢"
                type_badge = ":green[[ ADDED ]]"
                action_desc = "VISUAL APPEARANCE // CONFIRMED ENTRY"
            elif etype == "MOVED":
                icon = "🟡"
                type_badge = ":orange[[ DISPLACED ]]"
                action_desc = f"SPATIAL DISPLACEMENT // {dist} PX DELTA" if dist else "COORDINATE DELTA REGISTERED"
            elif etype == "REMOVED":
                icon = "🔴"
                type_badge = ":red[[ VACATED ]]"
                action_desc = "TARGET LOST // CONFIRMED VACATED"
            else:
                icon = "⚪"
                type_badge = ":grey[[ UPDATE ]]"
                action_desc = "STATE UPDATE"

            # Parse timestamp
            time_display = created_at_str
            try:
                dt_obj = pd.to_datetime(created_at_str)
                time_display = dt_obj.strftime("%Y-%m-%d %H:%M:%S UTC")
            except Exception:
                pass

            # Coordinate format
            pos_info = ""
            if prev_pos and curr_pos:
                pos_info = f"COORDS: `{prev_pos}` ➔ `{curr_pos}`"
            elif curr_pos:
                pos_info = f"CENTER: `{curr_pos}`"
            elif prev_pos:
                pos_info = f"LAST_POS: `{prev_pos}`"

            with st.container(border=True):
                col_icon, col_info, col_meta = st.columns([0.6, 5.2, 2.8])
                with col_icon:
                    st.markdown(f"<div style='font-size: 1.7rem; padding-top: 4px;'>{icon}</div>", unsafe_allow_html=True)
                with col_info:
                    st.markdown(f"#### **{obj_name.upper()}** &nbsp; {type_badge} &nbsp; :blue[[ TRACK #{tr_id} ]]")
                    desc_text = f"`{action_desc}`"
                    if pos_info:
                        desc_text += f" &nbsp;•&nbsp; `{pos_info}`"
                    st.caption(desc_text)
                with col_meta:
                    st.caption(f"TIMESTAMP // {time_display}")
                    if conf and conf > 0:
                        conf_val = float(conf) if conf <= 1.0 else float(conf) / 100.0
                        st.progress(min(max(conf_val, 0.0), 1.0), text=f"CONFIDENCE // {int(conf_val * 100)}%")

# ------------------------------------------
# TAB 2: ANALYTICS & TRENDS (RETRO SURVEILLANCE PALETTE)
# ------------------------------------------
with tab_analytics:
    st.markdown("#### // ANALYTICS_ENGINE // DIFFERENTIAL_DYNAMICS")
    
    if df.empty:
        st.info("[NOTICE] NO TELEMETRY DATA AVAILABLE FOR HISTORICAL ANALYSIS.")
    else:
        chart_col1, chart_col2 = st.columns(2)
        
        # Tactical surveillance palette: Cyan, Amber, Crimson (Zero Purple)
        color_map = {
            "ADDED": "#00D8F6",
            "MOVED": "#FFB000",
            "REMOVED": "#EF4444",
        }
        
        # Chart 1: Event Type Breakdown (Donut)
        with chart_col1:
            type_counts = df["event_type"].value_counts().reset_index()
            type_counts.columns = ["Event Type", "Count"]
            
            fig_donut = px.pie(
                type_counts,
                names="Event Type",
                values="Count",
                hole=0.6,
                title="// EVENT_CLASSIFICATION_RATIO",
                color="Event Type",
                color_discrete_map=color_map,
            )
            fig_donut.update_traces(
                textposition='inside',
                textinfo='percent+label',
                marker=dict(line=dict(color='#08090B', width=2))
            )
            fig_donut.update_layout(
                template="plotly_dark",
                paper_bgcolor="#0C0E12",
                plot_bgcolor="#0F1217",
                font=dict(family="JetBrains Mono, monospace", color="#8A94A6"),
                title_font=dict(size=14, color="#FFB000"),
                margin=dict(t=45, b=25, l=20, r=20),
                legend=dict(orientation="h", yanchor="bottom", y=-0.2, xanchor="center", x=0.5),
            )
            st.plotly_chart(fig_donut, width="stretch")

        # Chart 2: Most Frequently Changing Objects
        with chart_col2:
            obj_counts = df.groupby(["object_name", "event_type"]).size().reset_index(name="Count")
            fig_obj = px.bar(
                obj_counts,
                x="object_name",
                y="Count",
                color="event_type",
                title="// VOLATILITY_BY_TARGET_CLASS",
                color_discrete_map=color_map,
                barmode="stack",
            )
            fig_obj.update_layout(
                template="plotly_dark",
                paper_bgcolor="#0C0E12",
                plot_bgcolor="#0F1217",
                font=dict(family="JetBrains Mono, monospace", color="#8A94A6"),
                title_font=dict(size=14, color="#FFB000"),
                xaxis=dict(title="TARGET_CLASS", gridcolor="#1B212B"),
                yaxis=dict(title="EVENT_COUNT", gridcolor="#1B212B"),
                margin=dict(t=45, b=25, l=20, r=20),
                legend=dict(orientation="h", yanchor="bottom", y=-0.25, xanchor="center", x=0.5),
            )
            st.plotly_chart(fig_obj, width="stretch")

        # Chart 3: Chronological Event Activity (Time Series)
        if "datetime" in df.columns and len(df) > 1:
            st.markdown("<div style='height: 8px;'></div>", unsafe_allow_html=True)
            time_df = df.copy()
            time_df["time_bucket"] = time_df["datetime"].dt.floor("min")
            timeline_counts = time_df.groupby(["time_bucket", "event_type"]).size().reset_index(name="Count")
            
            fig_timeline = px.bar(
                timeline_counts,
                x="time_bucket",
                y="Count",
                color="event_type",
                color_discrete_map=color_map,
                title="// CHRONO_FREQUENCY_DISTRIBUTION",
            )
            fig_timeline.update_layout(
                template="plotly_dark",
                paper_bgcolor="#0C0E12",
                plot_bgcolor="#0F1217",
                font=dict(family="JetBrains Mono, monospace", color="#8A94A6"),
                title_font=dict(size=14, color="#FFB000"),
                xaxis=dict(title="TIMESTAMP_BUCKET", gridcolor="#1B212B"),
                yaxis=dict(title="EVENT_FREQUENCY", gridcolor="#1B212B"),
                margin=dict(t=45, b=25, l=20, r=20),
                legend=dict(orientation="h", yanchor="bottom", y=-0.25, xanchor="center", x=0.5),
            )
            st.plotly_chart(fig_timeline, width="stretch")

# ------------------------------------------
# TAB 3: SPATIAL MOTION RADAR
# ------------------------------------------
with tab_spatial:
    st.markdown("#### // SPATIAL_RADAR // 2D_FRAME_AND_MOTION_VECTORS")
    st.caption("TACTICAL FIELD-OF-VIEW CARTESIAN PROJECTION // PHYSICAL MOVEMENT VECTORS")

    spatial_data = []
    vector_data = []

    for _, r in filtered_df.iterrows():
        etype = r.get("event_type")
        obj_name = r.get("object_name")
        tr_id = r.get("track_id")
        prev_p = r.get("previous_position")
        curr_p = r.get("current_position")

        # Capture current/active position
        pos = curr_p or prev_p
        if pos and isinstance(pos, (list, tuple)) and len(pos) >= 2:
            spatial_data.append({
                "x": pos[0],
                "y": pos[1],
                "object": obj_name,
                "track_id": tr_id,
                "event_type": etype,
                "confidence": r.get("confidence", 1.0),
            })

        # Capture movement vectors
        if etype == "MOVED" and prev_p and curr_p:
            if isinstance(prev_p, (list, tuple)) and isinstance(curr_p, (list, tuple)):
                vector_data.append({
                    "x0": prev_p[0],
                    "y0": prev_p[1],
                    "x1": curr_p[0],
                    "y1": curr_p[1],
                    "object": obj_name,
                    "track_id": tr_id,
                    "distance": r.get("distance", 0),
                })

    if not spatial_data and not vector_data:
        st.info("[NOTICE] NO SPATIAL CARTESIAN COORDINATES RECORDED IN CURRENT BUFFER.")
    else:
        sp_df = pd.DataFrame(spatial_data) if spatial_data else pd.DataFrame(columns=["x", "y", "object", "event_type"])
        
        fig_radar = go.Figure()

        # Add Movement Vector Arrows (Amber Phosphor Trail)
        for vec in vector_data:
            fig_radar.add_trace(go.Scatter(
                x=[vec["x0"], vec["x1"]],
                y=[vec["y0"], vec["y1"]],
                mode="lines+markers",
                line=dict(color="#FFB000", width=2.5, dash="dot"),
                marker=dict(size=[5, 9], color=["#576275", "#FFB000"], symbol=["circle", "arrow-right"]),
                name=f"VECTOR: {vec['object']} #{vec['track_id']} ({vec['distance']}px)",
                hoverinfo="text",
                text=f"DISPLACEMENT: {vec['object'].upper()} (ID #{vec['track_id']}) SHIFTED {vec['distance']}px<br>ORIGIN: ({vec['x0']}, {vec['y0']})<br>TARGET: ({vec['x1']}, {vec['y1']})",
            ))

        # Add Object Position Points
        if not sp_df.empty:
            for et in sp_df["event_type"].unique():
                sub = sp_df[sp_df["event_type"] == et]
                color = "#00D8F6" if et == "ADDED" else ("#FFB000" if et == "MOVED" else "#EF4444")
                fig_radar.add_trace(go.Scatter(
                    x=sub["x"],
                    y=sub["y"],
                    mode="markers+text",
                    marker=dict(size=13, color=color, line=dict(width=2, color="#08090B")),
                    text=sub["object"].str.upper(),
                    textposition="top center",
                    name=f"TARGET: {et}",
                    customdata=sub[["track_id", "confidence"]],
                    hovertemplate="<b>%{text}</b> (TRACK #%{customdata[0]})<br>EVENT: " + et + "<br>COORDS: (%{x}, %{y})<br>CONFIDENCE: %{customdata[1]}<extra></extra>",
                ))

        fig_radar.update_layout(
            title="// FIELD_OF_VIEW_CARTESIAN_RADAR",
            template="plotly_dark",
            paper_bgcolor="#0C0E12",
            plot_bgcolor="#0A0C0F",
            font=dict(family="JetBrains Mono, monospace", color="#8A94A6"),
            title_font=dict(size=14, color="#FFB000"),
            xaxis=dict(title="X_AXIS // FRAME_WIDTH", gridcolor="#171D26", zerolinecolor="#283241"),
            yaxis=dict(title="Y_AXIS // FRAME_HEIGHT", gridcolor="#171D26", zerolinecolor="#283241", autorange="reversed"),
            height=540,
            margin=dict(t=50, b=40, l=40, r=40),
            legend=dict(orientation="h", yanchor="bottom", y=-0.22, xanchor="center", x=0.5),
        )

        st.plotly_chart(fig_radar, width="stretch")

# ------------------------------------------
# TAB 4: DATA EXPLORER & EXPORT
# ------------------------------------------
with tab_explorer:
    st.markdown("#### // DATA_REGISTRY // ARCHIVAL_EXPORT")
    
    if filtered_df.empty:
        st.info("[NOTICE] REGISTRY EMPTY UNDER CURRENT FILTER CRITERIA.")
    else:
        # Export Actions
        csv_data = filtered_df.to_csv(index=False).encode("utf-8")
        json_data = filtered_df.to_json(orient="records", indent=2)
        
        btn_col1, btn_col2, btn_col3 = st.columns([1.8, 1.8, 4.4])
        with btn_col1:
            st.download_button(
                label="📥 EXPORT_TELEMETRY_CSV",
                data=csv_data,
                file_name=f"realitydiff_telemetry_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv",
                width="stretch",
            )
        with btn_col2:
            st.download_button(
                label="📦 EXPORT_TELEMETRY_JSON",
                data=json_data,
                file_name=f"realitydiff_telemetry_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                mime="application/json",
                width="stretch",
            )
            
        st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)
        
        # Clean columns for display table
        display_cols = [c for c in ["id", "event_type", "object_name", "track_id", "confidence", "distance", "previous_position", "current_position", "created_at"] if c in filtered_df.columns]
        st.dataframe(
            filtered_df[display_cols],
            width="stretch",
            hide_index=True,
        )

# ==========================================
# AUTO-REFRESH RERUN ENGINE
# ==========================================
if auto_refresh != "Off":
    interval_map = {
        "3 seconds": 3,
        "5 seconds": 5,
        "10 seconds": 10,
        "30 seconds": 30,
    }
    sleep_sec = interval_map.get(auto_refresh, 5)
    time.sleep(sleep_sec)
    st.rerun()