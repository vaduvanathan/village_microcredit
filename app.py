import streamlit as st
import pandas as pd
import pydeck as pdk
import altair as alt
import plotly.express as px
import requests
import random
from src.data_fetcher import fetch_village_data, get_district_ranks, get_all_district_ranks

# --- Page Configuration ---
st.set_page_config(
    page_title="TN Risk Atlas",
    page_icon="🗺️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- UI Data ---
TAMIL_NADU_DATA = {
    "Ariyalur": {
        "Ariyalur Block": ["Ariyalur Panchayat 1", "Ariyalur Panchayat 2"],
        "T.Palur Block": ["T.Palur Panchayat 1", "T.Palur Panchayat 2"]
    },
    "Chengalpattu": {
        "Chengalpattu Block": ["Chengalpattu Panchayat 1", "Chengalpattu Panchayat 2"],
        "St.Thomas Mount Block": ["St.Thomas Mount Panchayat 1", "St.Thomas Mount Panchayat 2"]
    },
    "Chennai": {
        "Chennai Block": ["Chennai Panchayat 1", "Chennai Panchayat 2"]
    },
    "Coimbatore": {
        "Coimbatore North Block": ["Coimbatore North Panchayat 1", "Coimbatore North Panchayat 2"],
        "Coimbatore South Block": ["Coimbatore South Panchayat 1", "Coimbatore South Panchayat 2"]
    },
    "Cuddalore": {
        "Cuddalore Block": ["Cuddalore Panchayat 1", "Cuddalore Panchayat 2"],
        "Panruti Block": ["Panruti Panchayat 1", "Panruti Panchayat 2"]
    },
    "Dharmapuri": {
        "Dharmapuri Block": ["Dharmapuri Panchayat 1", "Dharmapuri Panchayat 2"],
        "Palacode Block": ["Palacode Panchayat 1", "Palacode Panchayat 2"]
    },
    "Dindigul": {
        "Dindigul Block": ["Dindigul Panchayat 1", "Dindigul Panchayat 2"],
        "Palani Block": ["Palani Panchayat 1", "Palani Panchayat 2"]
    },
    "Erode": {
        "Erode Block": ["Erode Panchayat 1", "Erode Panchayat 2"],
        "Bhavani Block": ["Bhavani Panchayat 1", "Bhavani Panchayat 2"]
    },
    "Kallakurichi": {
        "Kallakurichi Block": ["Kallakurichi Panchayat 1", "Kallakurichi Panchayat 2"],
        "Sankarapuram Block": ["Sankarapuram Panchayat 1", "Sankarapuram Panchayat 2"]
    },
    "Kanchipuram": {
        "Kanchipuram Block": ["Kanchipuram Panchayat 1", "Kanchipuram Panchayat 2"],
        "Walajabad Block": ["Walajabad Panchayat 1", "Walajabad Panchayat 2"]
    },
    "Kanyakumari": {
        "Agastheeswaram Block": ["Agastheeswaram Panchayat 1", "Agastheeswaram Panchayat 2"],
        "Thovalai Block": ["Thovalai Panchayat 1", "Thovalai Panchayat 2"]
    },
    "Karur": {
        "Karur Block": ["Karur Panchayat 1", "Karur Panchayat 2"],
        "Aravakurichi Block": ["Aravakurichi Panchayat 1", "Aravakurichi Panchayat 2"]
    },
    "Krishnagiri": {
        "Krishnagiri Block": ["Krishnagiri Panchayat 1", "Krishnagiri Panchayat 2"],
        "Hosur Block": ["Hosur Panchayat 1", "Hosur Panchayat 2"]
    },
    "Madurai": {
        "Madurai East": ["Madurai East Panchayat 1", "Madurai East Panchayat 2"],
        "Madurai West": ["Madurai West Panchayat 1", "Madurai West Panchayat 2"],
        "Thiruparankundram": ["Thiruparankundram Panchayat 1", "Thiruparankundram Panchayat 2"]
    },
    "Mayiladuthurai": {
        "Mayiladuthurai Block": ["Mayiladuthurai Panchayat 1", "Mayiladuthurai Panchayat 2"],
        "Sirkazhi Block": ["Sirkazhi Panchayat 1", "Sirkazhi Panchayat 2"]
    },
    "Nagapattinam": {
        "Nagapattinam Block": ["Nagapattinam Panchayat 1", "Nagapattinam Panchayat 2"],
        "Kilvelur Block": ["Kilvelur Panchayat 1", "Kilvelur Panchayat 2"]
    },
    "Namakkal": {
        "Namakkal Block": ["Namakkal Panchayat 1", "Namakkal Panchayat 2"],
        "Rasipuram Block": ["Rasipuram Panchayat 1", "Rasipuram Panchayat 2"]
    },
    "Nilgiris": {
        "Udhagamandalam Block": ["Udhagamandalam Panchayat 1", "Udhagamandalam Panchayat 2"],
        "Coonoor Block": ["Coonoor Panchayat 1", "Coonoor Panchayat 2"]
    },
    "Perambalur": {
        "Perambalur Block": ["Perambalur Panchayat 1", "Perambalur Panchayat 2"],
        "Veppanthattai Block": ["Veppanthattai Panchayat 1", "Veppanthattai Panchayat 2"]
    },
    "Pudukkottai": {
        "Pudukkottai Block": ["Pudukkottai Panchayat 1", "Pudukkottai Panchayat 2"],
        "Gandarvakottai Block": ["Gandarvakottai Panchayat 1", "Gandarvakottai Panchayat 2"]
    },
    "Ramanathapuram": {
        "Ramanathapuram Block": ["Ramanathapuram Panchayat 1", "Ramanathapuram Panchayat 2"],
        "Rameswaram Block": ["Rameswaram Panchayat 1", "Rameswaram Panchayat 2"]
    },
    "Ranipet": {
        "Ranipet Block": ["Ranipet Panchayat 1", "Ranipet Panchayat 2"],
        "Arakkonam Block": ["Arakkonam Panchayat 1", "Arakkonam Panchayat 2"]
    },
    "Salem": {
        "Salem Block": ["Salem Panchayat 1", "Salem Panchayat 2"],
        "Attur Block": ["Attur Panchayat 1", "Attur Panchayat 2"]
    },
    "Sivaganga": {
        "Sivaganga Block": ["Sivaganga Panchayat 1", "Sivaganga Panchayat 2"],
        "Karaikudi Block": ["Karaikudi Panchayat 1", "Karaikudi Panchayat 2"]
    },
    "Tenkasi": {
        "Tenkasi Block": ["Tenkasi Panchayat 1", "Tenkasi Panchayat 2"],
        "Shenkottai Block": ["Shenkottai Panchayat 1", "Shenkottai Panchayat 2"]
    },
    "Thanjavur": {
        "Thanjavur": ["Thanjavur Panchayat 1", "Thanjavur Panchayat 2"],
        "Papanasam": ["Papanasam Panchayat 1", "Papanasam Panchayat 2"],
        "Orathanadu": ["Orathanadu Panchayat 1", "Orathanadu Panchayat 2"]
    },
    "Theni": {
        "Theni Block": ["Theni Panchayat 1", "Theni Panchayat 2"],
        "Bodinayakanur Block": ["Bodinayakanur Panchayat 1", "Bodinayakanur Panchayat 2"]
    },
    "Thoothukudi": {
        "Thoothukudi Block": ["Thoothukudi Panchayat 1", "Thoothukudi Panchayat 2"],
        "Tiruchendur Block": ["Tiruchendur Panchayat 1", "Tiruchendur Panchayat 2"]
    },
    "Tiruchirappalli": {
        "Tiruchirappalli East": ["Tiruchirappalli East Panchayat 1", "Tiruchirappalli East Panchayat 2"],
        "Tiruchirappalli West": ["Tiruchirappalli West Panchayat 1", "Tiruchirappalli West Panchayat 2"]
    },
    "Tirunelveli": {
        "Tirunelveli Block": ["Tirunelveli Panchayat 1", "Tirunelveli Panchayat 2"],
        "Palayamkottai Block": ["Palayamkottai Panchayat 1", "Palayamkottai Panchayat 2"]
    },
    "Tirupathur": {
        "Tirupathur Block": ["Tirupathur Panchayat 1", "Tirupathur Panchayat 2"],
        "Vaniyambadi Block": ["Vaniyambadi Panchayat 1", "Vaniyambadi Panchayat 2"]
    },
    "Tiruppur": {
        "Tiruppur North": ["Tiruppur North Panchayat 1", "Tiruppur North Panchayat 2"],
        "Tiruppur South": ["Tiruppur South Panchayat 1", "Tiruppur South Panchayat 2"]
    },
    "Tiruvallur": {
        "Tiruvallur Block": ["Tiruvallur Panchayat 1", "Tiruvallur Panchayat 2"],
        "Poonamallee Block": ["Poonamallee Panchayat 1", "Poonamallee Panchayat 2"]
    },
    "Tiruvannamalai": {
        "Tiruvannamalai Block": ["Tiruvannamalai Panchayat 1", "Tiruvannamalai Panchayat 2"],
        "Chengam Block": ["Chengam Panchayat 1", "Chengam Panchayat 2"]
    },
    "Tiruvarur": {
        "Tiruvarur Block": ["Tiruvarur Panchayat 1", "Tiruvarur Panchayat 2"],
        "Nannilam Block": ["Nannilam Panchayat 1", "Nannilam Panchayat 2"]
    },
    "Vellore": {
        "Vellore Block": ["Vellore Panchayat 1", "Vellore Panchayat 2"],
        "Katpadi Block": ["Katpadi Panchayat 1", "Katpadi Panchayat 2"]
    },
    "Viluppuram": {
        "Viluppuram Block": ["Viluppuram Panchayat 1", "Viluppuram Panchayat 2"],
        "Gingee Block": ["Gingee Panchayat 1", "Gingee Panchayat 2"]
    },
    "Virudhunagar": {
        "Virudhunagar Block": ["Virudhunagar Panchayat 1", "Virudhunagar Panchayat 2"],
        "Srivilliputhur Block": ["Srivilliputhur Panchayat 1", "Srivilliputhur Panchayat 2"]
    }
}

# --- Helper Functions ---
@st.cache_data
def load_geojson():
    """Loads India district GeoJSON and filters for Tamil Nadu."""
    url = "https://raw.githubusercontent.com/geohacker/india/master/district/india_district.geojson"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        # Filter for Tamil Nadu
        # Note: Property names might vary. Common ones are NAME_1 (State), NAME_2 (District)
        tn_features = [f for f in data['features'] if f['properties'].get('NAME_1') == 'Tamil Nadu']
        return {'type': 'FeatureCollection', 'features': tn_features}
    except Exception as e:
        st.error(f"Failed to load map data: {e}")
        return None

def calculate_risk_score(data):
    """
    Calculates a risk score based on scheme beneficiaries and district rankings.
    Score is from 0-100, where higher is riskier.
    """
    scheme_inputs = data['scheme_inputs']
    ranks = data['district_ranks']

    # 1. Calculate Welfare Score (0-100, higher is better)
    # Normalize beneficiary numbers against an assumed max of 10,000 per scheme
    total_beneficiaries = sum(scheme_inputs.values())
    max_possible_beneficiaries = 4 * 10000 # 4 schemes, 10k max each
    welfare_score = min(100, (total_beneficiaries / max_possible_beneficiaries) * 100 * 5) # Multiply by 5 to make it more sensitive
    
    # 2. Calculate District Rank Score (0-100, higher is worse)
    # Average the ranks (1-38) and normalize to a 0-100 scale
    avg_rank = sum(ranks.values()) / len(ranks)
    # (avg_rank - 1) / 37 maps it to 0-1. Then scale to 100.
    district_rank_score = ((avg_rank - 1) / 37) * 100

    # 3. Combine scores
    # 60% weight to district performance, 40% to local beneficiary numbers.
    # We subtract welfare_score because higher welfare LOWERS risk.
    final_risk_score = (district_rank_score * 0.6) + ( (100 - welfare_score) * 0.4)
    
    return max(0, min(100, int(final_risk_score))), int(welfare_score), int(avg_rank)

def get_ai_reason(score, data):
    """Simulates a Gemini response explaining the score."""
    panchayat = data['panchayat']
    schemes = data['scheme_inputs']
    ranks = data['district_ranks']
    
    # Find the scheme with the highest beneficiaries
    top_scheme = max(schemes, key=schemes.get)
    top_count = schemes[top_scheme]
    
    # Find the best performing rank (lowest number)
    best_rank_scheme = min(ranks, key=ranks.get)
    best_rank = ranks[best_rank_scheme]

    if score > 65:
        reason = f"**High Risk Alert for {panchayat}:** The Resilience Score is critically high at **{score}**. This indicates a potential vulnerability despite the coverage in schemes like {top_scheme.replace('_', ' ').title()} ({top_count} beneficiaries). The district's ranking in key schemes needs improvement to bolster resilience. Immediate review of coverage gaps is advised."
    elif 40 <= score <= 65:
        reason = f"**Moderate Risk Warning for {panchayat}:** The Resilience Score is {score}. While there is substantial coverage, particularly in {top_scheme.replace('_', ' ').title()}, the overall district performance (best rank: {best_rank} in {best_rank_scheme.replace('_', ' ').title()}) suggests room for improvement. Recommend monitoring beneficiary uptake."
    else:
        reason = f"**Low Risk Profile for {panchayat}:** The Resilience Score is a healthy **{score}**. This reflects strong social security coverage, led by {top_scheme.replace('_', ' ').title()} with {top_count} beneficiaries. The district also performs well in {best_rank_scheme.replace('_', ' ').title()} (Rank {best_rank}). The panchayat shows good resilience to economic shocks."
    return reason

# --- Sidebar for User Input ---
with st.sidebar:
    st.title("📍 TN Risk Atlas")
    st.markdown("Micro-Lending Risk Scoring Platform")
    
    selected_district = st.selectbox("Select District", list(TAMIL_NADU_DATA.keys()))
    
    blocks = list(TAMIL_NADU_DATA[selected_district].keys())
    selected_block = st.selectbox("Select Block", blocks)
    
    panchayats = TAMIL_NADU_DATA[selected_district][selected_block]
    selected_panchayat = st.selectbox("Select Panchayat", panchayats)
    
    st.markdown("---")
    st.subheader("Scheme Beneficiaries")
    
    # Get ranks for the selected district to calculate dynamic defaults
    # Lower rank (e.g., 1) means better performance, so we assign higher beneficiary counts.
    # Formula: Base + (Inverse Rank * Multiplier)
    current_ranks = get_district_ranks(selected_district)
    
    # Kalaignar Magalir Urimai Thittam (Rank 1 -> ~6000, Rank 38 -> ~500)
    def_magalir = 500 + (39 - current_ranks.get('kalaignar_magalir_urimai_rank', 19)) * 150
    magalir_urimai = st.number_input("Kalaignar Magalir Urimai Thittam", min_value=0, value=int(def_magalir), key=f"magalir_{selected_district}")
    
    # Old Age Pension (Rank 1 -> ~2500, Rank 38 -> ~500)
    def_pension = 500 + (39 - current_ranks.get('old_age_pension_rank', 19)) * 50
    old_age_pension = st.number_input("Indira Gandhi National Old Age Pension Scheme", min_value=0, value=int(def_pension), key=f"pension_{selected_district}")
    
    # MGNREGA (Rank 1 -> ~8000, Rank 38 -> ~500)
    def_mgnrega = 500 + (39 - current_ranks.get('mgnrega_rank', 19)) * 200
    mgnrega = st.number_input("Mahatma Gandhi National Rural Employment Guarantee Act", min_value=0, value=int(def_mgnrega), key=f"mgnrega_{selected_district}")
    
    # Pongal Gift (Rank 1 -> ~12000, Rank 38 -> ~500)
    def_pongal = 500 + (39 - current_ranks.get('pongal_gift_rank', 19)) * 300
    pongal_gift = st.number_input("Tamil Nadu Pongal Gift Scheme", min_value=0, value=int(def_pongal), key=f"pongal_{selected_district}")
    
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
        scheme_inputs = {
            "magalir_urimai": magalir_urimai,
            "old_age_pension": old_age_pension,
            "mgnrega": mgnrega,
            "pongal_gift": pongal_gift
        }
        st.session_state.data = fetch_village_data(selected_district, selected_block, selected_panchayat, scheme_inputs)

if st.session_state.data:
    data = st.session_state.data
    risk_score, welfare_score, district_avg_rank = calculate_risk_score(data)

    # --- Top Metric Cards ---
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric(label="**Resilience Score**", value=risk_score, delta=f"{risk_score-50}",
                  help="Lower is better. Score > 65 is high risk.", delta_color="inverse")
    with col2:
        st.metric(label="**Welfare Score**", value=f"{welfare_score}/100", 
                  help="Score based on local beneficiary numbers. Higher is better.")
    with col3:
        st.metric(label="**District Rank**", value=f"{district_avg_rank}/38", 
                  help="Average scheme penetration rank for the district. Lower is better.", delta_color="inverse")

    # --- Middle: Charts ---
    st.markdown("---")
    col_charts_1, col_charts_2 = st.columns([1, 1])
    
    with col_charts_1:
        st.subheader("Scheme Beneficiary Distribution")
        
        # Prepare data for the chart
        total_beneficiaries = sum(data['scheme_inputs'].values())
        chart_data = pd.DataFrame({
            'Scheme': [k.replace('_', ' ').title() for k in data['scheme_inputs'].keys()],
            'Beneficiaries': list(data['scheme_inputs'].values())
        })
        chart_data['Percentage'] = chart_data['Beneficiaries'] / total_beneficiaries
        
        # Create Pie Chart using Altair
        base = alt.Chart(chart_data).encode(
            theta=alt.Theta("Beneficiaries", stack=True)
        )
        
        pie = base.mark_arc(outerRadius=120).encode(
            color=alt.Color("Scheme"),
            order=alt.Order("Beneficiaries", sort="descending"),
            tooltip=["Scheme", "Beneficiaries", alt.Tooltip("Percentage", format=".1%")]
        )
        
        text = base.mark_text(radius=140).encode(
            text=alt.Text("Percentage", format=".1%"),
            order=alt.Order("Beneficiaries", sort="descending"),
            color=alt.value("black") 
        )
        
        st.altair_chart(pie + text, use_container_width=True)

    with col_charts_2:
        st.subheader("District Performance Map")
        geojson_data = load_geojson()
        
        if geojson_data:
            all_ranks = get_all_district_ranks()
            map_data = []
            for dist, ranks in all_ranks.items():
                avg_rank = sum(ranks.values()) / len(ranks)
                # Simple name matching adjustments
                map_name = dist
                if dist == "Kanchipuram": map_name = "Kancheepuram"
                if dist == "Tiruvallur": map_name = "Thiruvallur"
                if dist == "Thoothukudi": map_name = "Thoothukkudi"
                
                map_data.append({'District': map_name, 'Average Rank': avg_rank})
            
            df_map = pd.DataFrame(map_data)
            
            # Create Choropleth
            fig = px.choropleth(
                df_map,
                geojson=geojson_data,
                locations='District',
                featureidkey="properties.NAME_2",
                color='Average Rank',
                color_continuous_scale="RdYlGn_r", # Green (Low Rank) to Red (High Rank)
                range_color=(1, 38),
                fitbounds="locations",
                title="Avg Rank (Green=Good, Red=Bad)"
            )
            fig.update_geos(visible=False)
            fig.update_layout(margin={"r":0,"t":30,"l":0,"b":0})
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning("Could not load map data.")
    
    # --- Bottom: AI Explanation ---
    st.markdown("---")
    st.subheader("🤖 AI-Powered Risk Explanation")
    ai_reason = get_ai_reason(risk_score, data)
    st.text_area("Gemini Analysis", value=ai_reason, height=200, disabled=True)

else:
    st.info("Please select a location and click 'Analyze Risk' to begin.")
