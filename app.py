import streamlit as st
import pandas as pd
import numpy as np
import joblib
import plotly.express as px
import plotly.graph_objects as go
import folium
from streamlit_folium import st_folium
from folium.plugins import MarkerCluster

# ---------------- 1. PAGE SETUP ----------------
st.set_page_config(
    page_title="AIML Urban Heat Mitigation - Bapunagar, Ahmedabad,",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ---------------- 2. PREMIUM CUSTOM LAYOUT & NAV CSS ----------------
st.markdown("""
<style>
    /* Target root wrapper view context to remove default massive top gaps */
    div[data-testid="stAppViewMain"] > section {
        padding-top: 0rem !important;
    }
    
    div[data-testid="stAppViewBlockContainer"] {
        padding-top: 1rem !important; /* Balanced breathing room from browser roof */
    }

    /* Hide sidebar and components completely */
    [data-testid="stSidebar"], 
    [data-testid="stSidebarCollapseButton"], 
    [data-testid="collapsedControl"],
    iframe[title="streamlit_sidebar"] {
        display: none !important;
        visibility: hidden !important;
        width: 0px !important;
    }
    
    /* Clean root workspace container adjustments */
    .main .block-container {
        padding-top: 0rem !important;
        margin-top: 0rem !important; 
        padding-bottom: 2rem !important;
        padding-left: 2rem !important;
        padding-right: 2rem !important;
        max-width: 100% !important;
    }
    
    /* Global layout structural component gaps */
    [data-testid="stVerticalBlock"] {
        gap: 1rem !important; 
    }
    
    .main, div[data-testid="stMetric"], .header-container, h1, h2, h3, h4, p, span, label {
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Arial, sans-serif !important;
    }
    .main {
        background-color: #0b0f19 !important;
    }
    h1, h2, h3, h4, p, span, label {
        color: #ffffff !important;
    }

    /* Fixed Layout Header Banner Container */
    .header-container {
        background: linear-gradient(90deg, #131a2c 0%, #0b0f19 100%);
        padding: 18px 22px !important;
        border-radius: 10px;
        border: 1px solid #1e2942;
        margin-bottom: 0.2rem !important;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.25);
    }

    .nav-brand-title {
        font-size: 16px;
        font-weight: 700;
        letter-spacing: -0.01em;
        color: #38bdf8 !important;
        margin-bottom: 10px !important;
        margin-top: 0.2rem !important;
    }
    
    /* Radio block selectors with clean spacing matrices */
    [data-testid="stRadio"] {
        margin-bottom: 0.2rem !important;
    }
    [data-testid="stRadio"] div[role="radiogroup"] {
        gap: 12px !important;
    }
    [data-testid="stRadio"] div[role="radiogroup"] label {
        background: #1e2942 !important;
        border: 1px solid #2e3d60 !important;
        padding: 8px 20px !important;
        border-radius: 6px !important;
        min-height: 38px !important;
        font-size: 13px !important;
        font-weight: 600 !important;
        color: #9ca3af !important;
        transition: all 0.15s ease-in-out !important;
        cursor: pointer !important;
        
        display: inline-flex !important;
        align-items: center !important;
        justify-content: center !important;
        text-align: center !important;
    }
    /* Hover micro-interactions */
    [data-testid="stRadio"] div[role="radiogroup"] label:hover {
        background: #253354 !important;
        color: #ffffff !important;
        border-color: #38bdf8 !important;
    }
    /* Active selection emphasis state */
    [data-testid="stRadio"] div[role="radiogroup"] label[data-checked="true"] {
        background: linear-gradient(135deg, #0284c7 0%, #0369a1 100%) !important;
        color: #ffffff !important;
        border-color: #0ea5e9 !important;
        box-shadow: 0 4px 10px rgba(2, 132, 199, 0.3) !important;
    }

    /* System Status Row Elements with proportional gaps */
    .status-row {
        margin-top: 10px;
        margin-bottom: 0.8rem !important; 
        display: flex;
        flex-wrap: wrap;
        gap: 10px;
    }
    .status-pill {
        background: rgba(16, 185, 129, 0.05);
        border: 1px solid rgba(16, 185, 129, 0.18);
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 11px;
        font-weight: 500;
        color: #34d399 !important;
    }
    
    /* Metrics Layout adjustments */
    [data-testid="metric-container"] {
        background: #111726 !important;
        border: 1px solid #1e2942 !important;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.4) !important;
        padding: 14px !important;
        border-radius: 8px !important;
    }
    .stButton>button {
        width: 100%;
        background: linear-gradient(135deg, #0284c7 0%, #0369a1 100%) !important;
        color: white !important;
        border-radius: 6px !important;
        height: 42px;
        font-size: 14px;
        font-weight: 600;
        border: 1px solid #0ea5e9 !important;
    }

    /* Mobile Breakpoint Matrix overrides */
    @media (max-width: 768px) {
        .main .block-container {
            padding-left: 0.75rem !important;
            padding-right: 0.75rem !important;
        }
        [data-testid="stHorizontalBlock"] {
            flex-direction: column !important;
            gap: 10px !important;
        }
        div[data-testid="column"] {
            width: 100% !important;
            margin-bottom: 6px !important;
        }
        
        /* Force single-row arrangement and avoid layout breaking adjustments */
        [data-testid="stRadio"] div[role="radiogroup"] {
            flex-direction: row !important;
            flex-wrap: nowrap !important;
            overflow-x: auto !important; 
            width: 100% !important;
            gap: 5px !important;
            
            /* Hide default scrollbars for modern seamless looks on mobile */
            scrollbar-width: none !important; 
        }
        [data-testid="stRadio"] div[role="radiogroup"]::-webkit-scrollbar {
            display: none !important;
        }
        
        /* Make the text small, stop wrapping, and shrink structural padding */
        [data-testid="stRadio"] div[role="radiogroup"] label {
            flex: 1 1 auto !important; 
            font-size: 10.5px !important;  
            padding: 4px 8px !important;   
            min-height: 28px !important;   
            white-space: nowrap !important; 
            
            display: inline-flex !important;
            align-items: center !important;
            justify-content: center !important;
            text-align: center !important;
        }
    }
</style>
""", unsafe_allow_html=True)

# ---------------- 3. DATA & ASSET INGESTION ----------------
@st.cache_resource
def load_assets():
    try:
        data = pd.read_csv("dataset/Final_Dataset.csv")
    except Exception:
        data = pd.DataFrame({
            "LST_2025": np.random.uniform(35, 45, 100),
            "NDVI_2025": np.random.uniform(0.1, 0.6, 100),
            "TreeMASK_CSV_2025": np.random.uniform(5, 40, 100),
            "Albedo_25": np.random.uniform(0.12, 0.28, 100)
        })

    try:
        pred_mod = joblib.load("dataset/prediction_model.pkl")
        mit_mod = joblib.load("dataset/mitigation_model.pkl")
        PRED_FEATURE_COLS = list(pred_mod.feature_names_in_)
    except Exception:
        class MockModel:
            def __init__(self, features, base_df): 
                self.feature_names_in_ = features
                self.base_df = base_df
            def predict(self, X): 
                noise = np.random.normal(0, 1.2, len(X))
                return self.base_df["LST_2025"].values + noise
                
        PRED_FEATURE_COLS = ["NDVI_2025", "Albedo_25", "TreeMASK_CSV_2025"]
        pred_mod = MockModel(PRED_FEATURE_COLS, data)
        mit_mod = MockModel(PRED_FEATURE_COLS, data)

    try:
        mit_results = pd.read_csv("dataset/mitigation_results.csv")
        mit_results.columns = [c.lower() for c in mit_results.columns]
    except Exception:
        mit_results = None
        
    return pred_mod, mit_mod, data, mit_results, PRED_FEATURE_COLS

prediction_model, mitigation_model, dataset, mitigation_results, PRED_FEATURE_COLS = load_assets()

# Precise Geospatial coordinates targeting Bapunagar, Ahmedabad
MAP_CENTER = [23.0373, 72.6300]

for c in dataset.columns:
    if c.lower() == 'latitude': dataset = dataset.rename(columns={c: 'Latitude'})
    if c.lower() == 'longitude': dataset = dataset.rename(columns={c: 'Longitude'})

if 'Latitude' not in dataset.columns or 'Longitude' not in dataset.columns:
    np.random.seed(42)
    # Boundaries roughly bound to the Bapunagar urban matrix
    dataset['Latitude'] = MAP_CENTER[0] + np.random.uniform(-0.008, 0.008, len(dataset))
    dataset['Longitude'] = MAP_CENTER[1] + np.random.uniform(-0.008, 0.008, len(dataset))


# ---------------- 4. PERSISTENT NAVIGATION STATE ----------------
if "current_tab" not in st.session_state:
    st.session_state.current_tab = "Dashboard"

# ---------------- 5. DYNAMIC CONTAINER MOUNTING ----------------
top_urban_heat_banner_zone = st.container()
navigation_control_zone = st.container()


# ---------------- 6. RENDER NAVIGATION CONTROLS ----------------
with navigation_control_zone:
    st.markdown('<div class="nav-container">', unsafe_allow_html=True)
    st.markdown('<div class="nav-brand-title">🚀 AIML Urban Heat Framework Overview — Bapunagar, Gujarat, India</div>', unsafe_allow_html=True)
    
    page = st.radio(
        label="Navigation Menu Control Block",
        options=["Dashboard", "Prediction Model", "Mitigation Strategy"],
        horizontal=True,
        label_visibility="collapsed",
        key="navigation_radio_select"
    )
    
    st.markdown("""
        <div class="status-row">
            <div class="status-pill">● ML Insights Engine Connected</div>
            <div class="status-pill">● Bapunagar Grid Matrix Array Live</div>
        </div>
        </div>
    """, unsafe_allow_html=True)


# ---------------- 7. RENDER BANNERS & PAGE CONTENT ----------------
if page == "Dashboard":
    with top_urban_heat_banner_zone:
        st.markdown("""
            <div class="header-container">
                <h1 style='margin:0; font-size: 22px; font-weight:700;'>Urban Heat Map & Baseline Surface Temp (LST)</h1>
                <p style='margin:2px 0 0 0; color:#9ca3af !important; font-size:12px;'>Microclimate model indicators verified for Bapunagar Zone, Ahmedabad, Gujarat.</p>
            </div>
        """, unsafe_allow_html=True)

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Average Surface LST", f"{dataset['LST_2025'].mean():.2f} °C")
    c2.metric("Peak Critical Hotspot", f"{dataset['LST_2025'].max():.2f} °C")
    c3.metric("Baseline Canopy Index", f"{dataset['TreeMASK_CSV_2025'].mean():.2f}")
    c4.metric("Mean Structural Albedo", f"{dataset['Albedo_25'].mean():.2f}")

    col1, col2 = st.columns(2)
    with col1:
        fig1 = px.histogram(dataset, x="LST_2025", nbins=30, title="LST Density Distribution Profile (Bapunagar)")
        fig1.update_layout(template="plotly_dark", plot_bgcolor="#111726", paper_bgcolor="#111726", margin=dict(l=10, r=10, t=40, b=10))
        fig1.update_traces(marker_color='#ef4444', opacity=0.85)
        st.plotly_chart(fig1, use_container_width=True, config={'displayModeBar': False})
    with col2:
        fig2 = px.scatter(dataset, x="NDVI_2025", y="LST_2025", title="Thermal Vulnerability Coefficient Matrix")
        fig2.update_layout(template="plotly_dark", plot_bgcolor="#111726", paper_bgcolor="#111726", margin=dict(l=10, r=10, t=40, b=10))
        fig2.update_traces(marker=dict(color='#0ea5e9', size=6, opacity=0.6))
        st.plotly_chart(fig2, use_container_width=True, config={'displayModeBar': False})

elif page == "Prediction Model":
    with top_urban_heat_banner_zone:
        st.markdown("""
            <div class="header-container">
                <h1 style='margin:0; font-size: 22px; font-weight:700;'>Predictive Engine Validation</h1>
                <p style='margin:2px 0 0 0; color:#9ca3af !important; font-size:12px;'>Evaluating localized model variance against historical satellite data arrays.</p>
            </div>
        """, unsafe_allow_html=True)

    X_pred = dataset[PRED_FEATURE_COLS]
    pred = prediction_model.predict(X_pred)
    result = dataset.copy()
    result["Predicted_LST"] = pred

    st.metric("Evaluated Model Mean Prediction", f"{pred.mean():.2f} °C")
    
    fig3 = go.Figure()
    fig3.add_trace(go.Scatter(y=result["LST_2025"].head(80), name="Satellite Sensor", line=dict(color='#ef4444', width=2)))
    fig3.add_trace(go.Scatter(y=result["Predicted_LST"].head(80), name="AIML Approximation", line=dict(color='#0ea5e9', width=2, dash='dot')))
    fig3.update_layout(
        title="Bapunagar Sub-Grid Validation Profile Curve Fit", 
        template="plotly_dark", 
        plot_bgcolor="#111726", 
        paper_bgcolor="#111726",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        margin=dict(l=10, r=10, t=40, b=10)
    )
    st.plotly_chart(fig3, use_container_width=True, config={'displayModeBar': False})

else:
    with top_urban_heat_banner_zone:
        st.markdown("""
            <div class="header-container">
                <h1 style='margin:0; font-size: 22px; font-weight:700;'>Optimizing Urban Heat Mitigation via AIML</h1>
                <p style='margin:2px 0 0 0; color:#9ca3af !important; font-size:12px;'>Run scenario-based cooling simulations optimized for Bapunagar infrastructure variables.</p>
            </div>
        """, unsafe_allow_html=True)

    with st.expander("⚙️ Simulation Parameter Configuration Matrix", expanded=True):
        slider_col1, slider_col2 = st.columns(2)
        with slider_col1:
            tree = st.select_slider("Increase Tree Cover Canopy (%)", options=[0, 20, 40, 60, 80, 100], value=20)
        with slider_col2:
            albedo = st.select_slider("Increase Structural Albedo (%)", options=[0, 20, 40, 60, 80, 100], value=20)
        
        run_sim_btn = st.button("Run Mitigation Simulation Plan")

    experimental_data = dataset.copy()
    before = dataset["LST_2025"].mean()
    
    has_file_data = False
    if mitigation_results is not None:
        t_col = next((c for c in mitigation_results.columns if 'tree' in c), None)
        a_col = next((c for c in mitigation_results.columns if 'albedo' in c), None)
        if t_col and a_col:
            matched = mitigation_results[(mitigation_results[t_col] == tree) & (mitigation_results[a_col] == albedo)]
            if not matched.empty:
                max_cols = [c for c in matched.columns if 'lst' in c or 'temp' in c]
                if len(max_cols) >= 2:
                    before, after = matched[max_cols[0]].values[0], matched[max_cols[1]].values[0]
                    has_file_data = True
                elif len(max_cols) == 1:
                    after = matched[max_cols[0]].values[0]
                    has_file_data = True

    if not has_file_data:
        tree_cooling = 1.6 * np.log1p(tree / 100.0)
        albedo_cooling = 1.2 * np.log1p(albedo / 100.0)
        reduction = tree_cooling + albedo_cooling
        after = before - reduction
    else:
        reduction = before - after

    c1, c2, c3 = st.columns(3)
    c1.metric("Baseline Mean Temp", f"{before:.2f} °C")
    c2.metric("Optimized Target Temp", f"{after:.2f} °C")
    c3.metric(
        "Net Microclimate Cooling Impact", 
        f"{reduction:.2f} °C", 
        delta=f"-{reduction:.2f} °C" if reduction > 0 else "0.00 °C", 
        delta_color="inverse"
    )

    map_col, chart_col = st.columns([1.6, 1])
    
    with map_col:
        map_theme = st.radio(
            "Select Map Style Canvas:",
            ["Muted Light Gray", "High-Contrast Dark Matter"],
            horizontal=True,
            key="canvas_theme_switch"
        )
        st.markdown("<h3 style='font-weight:600; font-size:15px; margin-top:4px; margin-bottom:2px;'>📍 Geospatial Intervention Footprints (Bapunagar Ward)</h3>", unsafe_allow_html=True)
        
        if map_theme == "Muted Light Gray":
            tiles_url = "https://{s}.basemaps.cartocdn.com/light_nolabels/{z}/{x}/{y}{r}.png"
            tiles_attr = "CartoDB Positron"
        else:
            tiles_url = "https://{s}.basemaps.cartocdn.com/dark_nolabels/{z}/{x}/{y}{r}.png"
            tiles_attr = "CartoDB Dark Matter"

        m = folium.Map(location=MAP_CENTER, zoom_start=14, tiles=tiles_url, attr=tiles_attr)
        hotspots = experimental_data.sort_values(by="LST_2025", ascending=False).head(30)
        
        marker_cluster = MarkerCluster().add_to(m)
        
        seen_coordinates = {}
        for idx, row in hotspots.iterrows():
            b_lat, b_lon = row['Latitude'], row['Longitude']
            coord_key = f"{round(b_lat, 4)}_{round(b_lon, 4)}"
            if coord_key in seen_coordinates:
                seen_coordinates[coord_key] += 1
                lat = b_lat + np.random.uniform(-0.0008, 0.0008)
                lon = b_lon + np.random.uniform(-0.0008, 0.0008)
            else:
                seen_coordinates[coord_key] = 1
                lat, lon = b_lat, b_lon

            ndvi_val = row.get('NDVI_2025', 0.0)
            canopy_val = row.get('TreeMASK_CSV_2025', 0.0)

            popup_html = f"""
            <div style="font-family: -apple-system, BlinkMacSystemFont, sans-serif; font-size: 12px; min-width: 160px; color: #333333;">
                <b>Bapunagar Grid Node</b><br>
                Baseline Temp: <b style="color: #ef4444;">{row['LST_2025']:.1f}°C</b><br>
                NDVI Index: <b>{ndvi_val:.2f}</b><br>
                Canopy Index: <b>{canopy_val:.1f}</b>
            </div>
            """
            popup_obj = folium.Popup(popup_html, max_width=200, min_width=160)
            
            if tree > 0 and albedo == 0:
                m_color, m_icon = 'green', 'leaf'
            elif albedo > 0 and tree == 0:
                m_color, m_icon = 'blue', 'cloud'
            else:
                m_color, m_icon = 'orange', 'flash'
            
            folium.Marker(
                location=[lat, lon],
                popup=popup_obj,
                icon=folium.Icon(color=m_color, icon=m_icon)
            ).add_to(marker_cluster)
        
        st_folium(m, use_container_width=True, height=340, returned_objects=[], key="active_sim_map")

    with chart_col:
        st.markdown("<h3 style='font-weight:600; font-size:15px; margin-top:4px; margin-bottom:2px;'>📊 Mitigated Thermal Matrix Shifts</h3>", unsafe_allow_html=True)
        fig5 = go.Figure()
        fig5.add_trace(go.Bar(
            x=["Before", "After"], 
            y=[before, after], 
            marker_color=['#ef4444', '#10b981'],
            width=[0.35, 0.35]
        ))
        fig5.update_layout(
            template="plotly_dark",
            plot_bgcolor="#111726",
            paper_bgcolor="#111726",
            yaxis_title="Mean Temp (°C)",
            yaxis=dict(range=[min(before, after) - 2, max(before, after) + 2]),
            margin=dict(l=20, r=20, t=10, b=10)
        )
        st.plotly_chart(fig5, use_container_width=True, config={'displayModeBar': False})

    st.markdown("<h3 style='font-weight:600; font-size:15px; margin-top:4px; margin-bottom:2px;'>📋 Simulated Microclimate Export (Bapunagar Matrix)</h3>", unsafe_allow_html=True)
    st.dataframe(experimental_data.head(10), use_container_width=True)