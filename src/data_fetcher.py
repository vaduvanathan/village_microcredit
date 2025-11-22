import random
import pandas as pd
import os

# --- Data Loading ---
def load_scheme_rankings():
    """Loads the district scheme ranking data from the CSV file."""
    # Correctly construct the path relative to this file's location
    script_dir = os.path.dirname(__file__) 
    file_path = os.path.join(script_dir, 'district_scheme_ranking.csv')
    try:
        df = pd.read_csv(file_path)
        df.set_index('district', inplace=True)
        return df.to_dict('index')
    except FileNotFoundError:
        # Return a default ranking if the file is missing
        return {}

SCHEME_RANKINGS = load_scheme_rankings()

def fetch_village_data(district: str, block: str, panchayat: str, scheme_inputs: dict) -> dict:
    """
    Mocks fetching data for a given village panchayat and calculates risk based on scheme inputs.
    In a real scenario, this would involve web scraping, database queries,
    and API calls.
    """
    # Mock data based on district to show some variation
    if district == "Madurai":
        active_cards = random.randint(350, 550)
        avg_wage = round(random.uniform(250.0, 280.0), 2)
        pension_coverage = random.randint(150, 250)
        magalir_coverage = random.randint(800, 1200)
        yield_anomaly = random.randint(-15, -5)
        price_trend = "down" if random.random() > 0.4 else "stable"
    elif district == "Thanjavur":
        active_cards = random.randint(450, 700)
        avg_wage = round(random.uniform(270.0, 310.0), 2)
        pension_coverage = random.randint(200, 350)
        magalir_coverage = random.randint(1000, 1500)
        yield_anomaly = random.randint(-10, 5)
        price_trend = "stable" if random.random() > 0.6 else "up"
    else: # Default mock
        active_cards = random.randint(300, 600)
        avg_wage = round(random.uniform(260.0, 290.0), 2)
        pension_coverage = random.randint(100, 300)
        magalir_coverage = random.randint(700, 1300)
        yield_anomaly = -10
        price_trend = "down"

    # Get the district's specific rankings
    district_ranks = SCHEME_RANKINGS.get(district, {
        'kalaignar_magalir_urimai_rank': 19, # Use average rank as default
        'old_age_pension_rank': 19,
        'mgnrega_rank': 19,
        'pongal_gift_rank': 19
    })

    return {
        'panchayat': panchayat,
        'district': district,
        'scheme_inputs': scheme_inputs,
        'district_ranks': district_ranks
    }

def get_district_ranks(district: str) -> dict:
    """
    Returns the scheme rankings for a specific district.
    """
    return SCHEME_RANKINGS.get(district, {
        'kalaignar_magalir_urimai_rank': 19,
        'old_age_pension_rank': 19,
        'mgnrega_rank': 19,
        'pongal_gift_rank': 19
    })

def get_all_district_ranks() -> dict:
    """
    Returns the rankings for all districts.
    """
    return SCHEME_RANKINGS
