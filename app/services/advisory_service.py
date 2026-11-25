"""Regenerative recommendations and cooperation metadata."""


def regenerative_actions(soil_type: str, water: str) -> list[dict]:
    actions = [
        {
            "action": "Keep living roots",
            "why": "Use a legume cover crop after harvest to protect soil carbon and fix nitrogen.",
            "impact": "Builds soil organic matter",
        },
        {
            "action": "Minimise disturbance",
            "why": "Use strip or reduced tillage where practical to retain moisture and soil structure.",
            "impact": "Improves water infiltration",
        },
    ]
    if water == "low":
        actions.insert(
            0,
            {
                "action": "Mulch crop residues",
                "why": "A 5–7 cm residue cover reduces evaporation and suppresses weeds.",
                "impact": "Saves irrigation water",
            },
        )
    if soil_type == "clay":
        actions.append(
            {
                "action": "Avoid field traffic after rain",
                "why": "Reducing compaction protects root channels and drainage in heavy soils.",
                "impact": "Protects soil structure",
            }
        )
    return actions


def get_model_card() -> dict:
    return {
        "name": "AgriN Connect Advisory v1",
        "purpose": "Interoperable, localised regenerative agriculture guidance",
        "inputs": ["soil health", "satellite vegetation index", "weather forecast", "farmer-provided context"],
        "outputs": ["crop suitability", "risk flags", "regenerative actions", "provenance"],
        "governance": ["farmer consent", "local data sovereignty", "aggregated cross-border model exchange"],
    }
