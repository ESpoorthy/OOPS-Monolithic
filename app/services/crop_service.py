"""Crop suitability and regenerative action business logic."""


def regenerative_actions(soil_type: str, water: str) -> list[dict]:
    actions = [
        {"action": "Keep living roots", "why": "Use a legume cover crop after harvest to protect soil carbon and fix nitrogen.", "impact": "Builds soil organic matter"},
        {"action": "Minimise disturbance", "why": "Use strip or reduced tillage where practical to retain moisture and soil structure.", "impact": "Improves water infiltration"},
    ]
    if water == "low":
        actions.insert(0, {"action": "Mulch crop residues", "why": "A 5–7 cm residue cover reduces evaporation and suppresses weeds.", "impact": "Saves irrigation water"})
    if soil_type == "clay":
        actions.append({"action": "Avoid field traffic after rain", "why": "Reducing compaction protects root channels and drainage in heavy soils.", "impact": "Protects soil structure"})
    return actions


def crop_catalogue(season: str, water: str, soil: str) -> list[dict]:
    options = {
        "kharif": {
            "low": [("Pearl Millet", 9.2, "Drought-tolerant cereal with a low water footprint"), ("Pigeon Pea", 8.7, "Nitrogen-fixing pulse suited to intercropping")],
            "medium": [("Maize + Cowpea", 9.0, "Diverse intercrop that supports soil cover"), ("Sorghum", 8.5, "Climate-resilient cereal for rainfed fields")],
            "high": [("Rice (SRI)", 8.8, "System of Rice Intensification can reduce water and seed use"), ("Maize + Cowpea", 8.6, "Diversified alternative to monocropping")],
        },
        "rabi": {
            "low": [("Chickpea", 9.1, "Nitrogen-fixing pulse with modest irrigation needs"), ("Mustard", 8.6, "Oilseed adapted to limited water")],
            "medium": [("Wheat + Chickpea", 8.9, "Rotation diversity improves nutrient cycling"), ("Barley", 8.4, "Hardy cereal with lower input needs")],
            "high": [("Wheat", 8.7, "Suitable where irrigation is reliable"), ("Barley", 8.2, "Hardy cereal with lower input needs")],
        },
        "zaid": {
            "low": [("Mung Bean", 9.0, "Short-duration nitrogen-fixing crop"), ("Sesame", 8.5, "Heat-tolerant oilseed")],
            "medium": [("Mung Bean", 9.1, "Quick pulse crop that improves rotations"), ("Fodder Cowpea", 8.6, "Adds biomass and livestock feed")],
            "high": [("Summer Mung Bean", 9.0, "Low-input pulse before the monsoon"), ("Vegetable Cowpea", 8.4, "Marketable crop that supports soil health")],
        },
    }
    soil_bonus = 0.3 if soil == "loamy" else 0.1
    return [
        {"crop": crop, "score": min(round(score + soil_bonus, 1), 10), "rationale": rationale,
         "regenerative_fit": "High" if score >= 8.8 else "Good"}
        for crop, score, rationale in options[season][water]
    ]
