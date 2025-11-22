import streamlit as st
import pandas as pd
import pydeck as pdk
import random
from src.data_fetcher import fetch_village_data

# --- Page Configuration ---
st.set_page_config(
    page_title="TN Risk Atlas",
    page_icon="🗺️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Mock Data for UI ---
DISTRICTS = {
    "Madurai": ["Madurai East", "Madurai West", "Thiruparankundram"],
    "Thanjavur": ["Thanjavur", "Papanasam", "Orathanadu"]
}
PANCHAYATS = [f"Village_{i}" for i in range(1, 11)]

# --- Helper Functions ---
def calculate_risk_score(data):
    """Calculates a simplified risk score."""
    # These weights are for demonstration; real model would be complex.
    yield_risk = -data['crop_risk']['yield_anomaly']  # Higher anomaly = higher risk
    welfare_shield = (data['welfare_coverage']['pension'] + data['welfare_coverage']['magalir_urimai']) / 100
    
    # Normalize and calculate score (simplified formula)
    risk_score = (yield_risk * 0.6) - (welfare_shield * 0.4)
    return max(0, min(100, int(risk_score))) # Clamp between 0-100

def get_ai_reason(score, data):
    """Simulates a Gemini response explaining the score."""
    if score > 65:
        reason = f"**High Risk Alert for {data['panchayat']}:** The Resilience Score is critically high at **{score}**. This is primarily driven by a significant **Yield Anomaly of {data['crop_risk']['yield_anomaly']}%** and a '{data['crop_risk']['price_trend']}' price trend for the main crop. While the welfare coverage ({data['welfare_coverage']['pension']} pension, {data['welfare_coverage']['magalir_urimai']} Magalir Urimai) provides some buffer, it is not enough to offset the severe agricultural risk. Immediate risk mitigation strategies are advised before extending further credit."
    elif 40 <= score <= 65:
        reason = f"**Moderate Risk Warning for {data['panchayat']}:** The Resilience Score is {score}. The risk is elevated due to a yield anomaly of {data['crop_risk']['yield_anomaly']}% and concerning price trends. The existing welfare shield is substantial but may be strained if agricultural conditions worsen. Recommend cautious lending and monitoring of crop health."
    else:
        reason = f"**Low Risk Profile for {data['panchayat']}:** The Resilience Score is a healthy **{score}**. This is due to stable crop yields (anomaly at {data['crop_risk']['yield_anomaly']}%) and strong social security coverage. The panchayat shows good resilience to economic shocks. Favorable conditions for micro-lending."
    return reason

# --- Sidebar for User Input ---
with st.sidebar:
    st.title("📍 TN Risk Atlas")
    st.markdown("Micro-Lending Risk Scoring Platform")
    
    selected_district = st.selectbox("Select District", list(DISTRICTS.keys()))
    selected_block = st.selectbox("Select Block", DISTRICTS[selected_district])
    selected_panchayat = st.selectbox("Select Panchayat", PANCHAYATS)
    
    st.markdown("---")
    analyze_button = st.button("Analyze Risk", type="primary")
    st.markdown("---")
    st.info("Built by a Senior Google Cloud Architect and Python Developer.")


# --- Main Dashboard Area ---
st.header(f"Resilience Dashboard: {selected_panchayat}")

if 'data' not in st.session_state:
    st.session_state.data = None

if analyze_button:
    with st.spinner("Fetching data and calculating risk..."):
        st.session_state.data = fetch_village_data(selected_district, selected_block, selected_panchayat)

if st.session_state.data:
    data = st.session_state.data
    risk_score = calculate_risk_score(data)
    welfare_index = data['welfare_coverage']['pension'] + data['welfare_coverage']['magalir_urimai']
    yield_forecast = data['crop_risk']['yield_anomaly']

    # --- Top Metric Cards ---
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric(label="**Resilience Score**", value=risk_score, delta=f"{risk_score-55}",
                  help="Lower is better. Score > 65 is high risk.", delta_color="inverse")
    with col2:
        st.metric(label="**Welfare Index**", value=f"{welfare_index:,}", 
                  help="Total beneficiaries under key schemes.")
    with col3:
        st.metric(label="**Yield Forecast Anomaly**", value=f"{yield_forecast}%", 
                  delta=f"{yield_forecast}% vs normal", delta_color="normal")

    # --- Middle: Map and Data ---
    st.markdown("---")
    
    # Create a sample dataframe for the map
    map_df = pd.DataFrame({
        'lat': [11.0 + random.uniform(-0.5, 0.5) for _ in range(100)],
        'lon': [78.0 + random.uniform(-0.5, 0.5) for _ in range(100)],
        'risk': [random.randint(20, 100) for _ in range(100)]
    })

    # PyDeck HexagonLayer Map
    st.pydeck_chart(pdk.Deck(
        map_style='mapbox://styles/mapbox/light-v9',
        initial_view_state=pdk.ViewState(
            latitude=11.0,
            longitude=78.0,
            zoom=6,
            pitch=50,
        ),
        layers=[
            pdk.Layer(
               'HexagonLayer',
               data=map_df,
               get_position='[lon, lat]',
               radius=10000,
               elevation_scale=100,
               elevation_range=[0, 1000],
               pickable=True,
               extruded=True,
            ),
        ],
        tooltip={"text": "Risk Concentration: {elevationValue}"}
    ))
    
    # --- Bottom: AI Explanation ---
    st.markdown("---")
    st.subheader("🤖 AI-Powered Risk Explanation")
    ai_reason = get_ai_reason(risk_score, data)
    st.text_area("Gemini Analysis", value=ai_reason, height=200, disabled=True)

else:
    st.info("Please select a location and click 'Analyze Risk' to begin.")
