"""Field intelligence payload generation."""
from datetime import date

from app.services.advisory_service import regenerative_actions


def build_field_intelligence(location: str, soil_type: str, water_availability: str) -> dict:
    moisture = {"low": 28, "medium": 51, "high": 72}[water_availability]
    organic_carbon = {"alluvial": 0.62, "loamy": 0.74, "clay": 0.58}[soil_type]
    risk = "Elevated" if water_availability == "low" else "Watch" if moisture < 55 else "Low"
    return {
        "field": {"location": location, "data_mode": "demo / offline-ready"},
        "satellite": {
            "source": "Sentinel-compatible contract",
            "ndvi": 0.68,
            "trend": "+0.04 over 14 days",
            "observation_date": str(date.today()),
        },
        "soil": {
            "texture": soil_type.title(),
            "ph": 6.7,
            "organic_carbon_percent": organic_carbon,
            "moisture_percent": moisture,
        },
        "weather": {
            "source": "Forecast-provider compatible contract",
            "rainfall_next_7_days_mm": 18,
            "max_temperature_c": 32,
            "risk": risk,
        },
        "advisory": {
            "headline": "Scout moisture and retain ground cover before the next dry window.",
            "confidence": 0.81,
            "actions": regenerative_actions(soil_type, water_availability),
        },
        "provenance": {
            "standard": "AgriN Connect Advisory v1",
            "shareable_fields": ["soil", "satellite", "weather", "advisory"],
            "privacy": "Farm location is kept local; only consented, aggregated indicators are shareable.",
        },
    }
