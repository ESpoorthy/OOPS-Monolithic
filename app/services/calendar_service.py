"""Farmer calendar generation."""
from datetime import date, timedelta


def generate_farmer_calendar(crop: str) -> dict:
    start = date.today()
    return {"crop": crop.title(), "calendar": [
        {"date": str(start + timedelta(days=3)), "task": "Inspect soil moisture and mulch cover"},
        {"date": str(start + timedelta(days=10)), "task": "Scout field edges for pests and beneficial insects"},
        {"date": str(start + timedelta(days=18)), "task": "Record crop condition and irrigation decision"},
    ]}
