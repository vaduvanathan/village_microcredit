import random

def fetch_village_data(district: str, block: str, panchayat: str) -> dict:
    """
    Mocks fetching data for a given village panchayat.
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

    return {
        'panchayat': panchayat,
        'active_job_cards': active_cards,
        'avg_wage': avg_wage,
        'welfare_coverage': {
            'pension': pension_coverage,
            'magalir_urimai': magalir_coverage
        },
        'crop_risk': {
            'yield_anomaly': yield_anomaly,
            'price_trend': price_trend
        }
    }
