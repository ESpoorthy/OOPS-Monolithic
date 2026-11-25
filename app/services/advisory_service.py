"""AgriN Connect cooperation and advisory metadata."""


def get_model_card() -> dict:
    return {"name": "AgriN Connect Advisory v1", "purpose": "Interoperable, localised regenerative agriculture guidance", "inputs": ["soil health", "satellite vegetation index", "weather forecast", "farmer-provided context"], "outputs": ["crop suitability", "risk flags", "regenerative actions", "provenance"], "governance": ["farmer consent", "local data sovereignty", "aggregated cross-border model exchange"]}
