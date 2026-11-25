"""Demo crop price and yield context."""
CROP_DATA = {
    "Pearl Millet": {"price": 31, "yield": 1800}, "Pigeon Pea": {"price": 72, "yield": 1200},
    "Maize + Cowpea": {"price": 29, "yield": 2600}, "Sorghum": {"price": 28, "yield": 2200},
    "Rice (SRI)": {"price": 26, "yield": 3500}, "Chickpea": {"price": 62, "yield": 1600},
    "Mustard": {"price": 60, "yield": 1500}, "Wheat + Chickpea": {"price": 34, "yield": 2500},
    "Barley": {"price": 26, "yield": 2300}, "Wheat": {"price": 32, "yield": 2800},
    "Mung Bean": {"price": 80, "yield": 1100}, "Summer Mung Bean": {"price": 79, "yield": 1100},
}


def predict_crop_price(crop: str) -> dict:
    data = CROP_DATA.get(crop, {"price": 30, "yield": 2000})
    return {"crop": crop, "predicted_next_price": data["price"], "predicted_yield_per_hectare": data["yield"], "mode": "demo"}
