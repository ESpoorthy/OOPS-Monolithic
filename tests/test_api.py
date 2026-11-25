from io import BytesIO

from fastapi.testclient import TestClient
from PIL import Image

from app.main import app
from app.services import disease_service

client = TestClient(app)


def test_root_returns_backend_status():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["status"] == "ready"


def test_health_endpoint():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy", "service": "agrin-connect"}


def test_crop_recommendations():
    response = client.post(
        "/recommend_crop",
        json={"soil_type": "loamy", "water_availability": "low", "season": "kharif"},
    )
    assert response.status_code == 200
    body = response.json()
    assert len(body["recommendations"]) == 2
    assert body["recommendations"][0]["crop"] == "Pearl Millet"
    assert body["explainability"][0] == "Season: Kharif"


def test_crop_rejects_invalid_enum_value():
    response = client.post(
        "/recommend_crop",
        json={"soil_type": "sandy", "water_availability": "low", "season": "kharif"},
    )
    assert response.status_code == 422


def test_field_intelligence_response():
    response = client.post(
        "/field-intelligence",
        json={"location": "Demo farm", "soil_type": "clay", "water_availability": "low"},
    )
    assert response.status_code == 200
    body = response.json()
    assert body["field"]["data_mode"] == "demo / offline-ready"
    assert body["weather"]["risk"] == "Elevated"
    assert any(action["action"] == "Mulch crop residues" for action in body["advisory"]["actions"])


def test_cooperation_model_card():
    response = client.get("/cooperation/model-card")
    assert response.status_code == 200
    assert response.json()["name"] == "AgriN Connect Advisory v1"


def test_market_prediction():
    response = client.post("/predict_price", json={"crop": "Chickpea"})
    assert response.status_code == 200
    assert response.json()["predicted_next_price"] == 62
    assert response.json()["predicted_yield_per_hectare"] == 1600


def test_market_rejects_empty_crop_name():
    response = client.post("/predict_price", json={"crop": ""})
    assert response.status_code == 422


def test_farmer_calendar():
    response = client.post("/farmer_calendar", json={"crop": "Mung Bean"})
    assert response.status_code == 200
    body = response.json()
    assert body["crop"] == "Mung Bean"
    assert len(body["calendar"]) == 3


def test_disease_upload_requires_file():
    response = client.post("/upload_image", data={"crop": "tomato"})
    assert response.status_code == 400
    assert response.json()["detail"] == "Select a plant image before analysis."


def test_disease_upload_rejects_unsupported_content_type():
    response = client.post(
        "/upload_image",
        data={"crop": "tomato"},
        files={"file": ("leaf.gif", b"GIF89a", "image/gif")},
    )
    assert response.status_code == 415


def test_disease_upload_rejects_invalid_image_bytes():
    response = client.post(
        "/upload_image",
        data={"crop": "tomato"},
        files={"file": ("leaf.jpg", b"not-an-image", "image/jpeg")},
    )
    assert response.status_code == 400


def test_disease_upload_rejects_unsupported_crop():
    response = client.post(
        "/upload_image",
        data={"crop": "corn"},
        files={"file": ("leaf.png", b"placeholder", "image/png")},
    )
    assert response.status_code == 422


def test_disease_model_unavailable_returns_503(monkeypatch):
    def unavailable_model():
        raise RuntimeError("model unavailable")

    monkeypatch.setattr(disease_service, "load_disease_model", unavailable_model)
    image_buffer = BytesIO()
    Image.new("RGB", (4, 4), color="green").save(image_buffer, format="PNG")

    response = client.post(
        "/upload_image",
        data={"crop": "tomato"},
        files={"file": ("leaf.png", image_buffer.getvalue(), "image/png")},
    )
    assert response.status_code == 503
    assert response.json()["detail"] == "Disease model is temporarily unavailable."
