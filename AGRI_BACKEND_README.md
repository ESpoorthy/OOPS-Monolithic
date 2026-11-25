# AgriN Connect — Modular Monolithic Backend

A backend-only implementation demonstrating an organized monolithic architecture with FastAPI. It separates HTTP routes, business services, and Pydantic schemas while running as one application and one process.

## Architecture

- **One FastAPI application:** `app/main.py` creates the application and registers feature routers.
- **Routes:** handle HTTP methods, paths, request parsing and response/error handling.
- **Services:** contain agricultural business logic and response construction.
- **Schemas:** validate request payloads with Pydantic.
- **Configuration:** centralizes application metadata, CORS, upload limits and model location.

This is a **modular monolith**, not a microservices system. Modules communicate through regular Python imports and function calls. They are not separately deployed and do not communicate over internal HTTP.

See [ARCHITECTURE.md](ARCHITECTURE.md) for the component diagram, request lifecycle, responsibilities and trade-offs.

## Repository structure

```text
app/
├── main.py
├── config.py
├── routes/
├── services/
├── schemas/
└── models/
tests/
requirements.txt
requirements-dev.txt
ARCHITECTURE.md
```

## Run locally

Python 3.10 or newer is recommended.

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\\Scripts\\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Open:

- API documentation: http://127.0.0.1:8000/docs
- Health check: http://127.0.0.1:8000/health

## API endpoints

| Method | Endpoint | Responsibility |
|---|---|---|
| GET | `/` | Backend status |
| GET | `/health` | Health check |
| POST | `/recommend_crop` | Crop suitability recommendations |
| POST | `/field-intelligence` | Field, soil, satellite-compatible and weather demo brief |
| POST | `/upload_image` | Plant leaf image classification workflow |
| POST | `/predict_price` | Demo price and yield context |
| POST | `/farmer_calendar` | Farmer task calendar |
| GET | `/cooperation/model-card` | Advisory model card |

## Example requests

### Crop recommendation

```json
{
  "soil_type": "loamy",
  "water_availability": "low",
  "season": "kharif",
  "location": "Demo farm"
}
```

### Field intelligence

```json
{
  "location": "Demo farm",
  "soil_type": "clay",
  "water_availability": "medium"
}
```

### Market prediction

```json
{
  "crop": "Chickpea"
}
```

## Disease model integration

The disease endpoint validates the uploaded file and delegates inference to the disease service. The trained checkpoint is intentionally not committed as a placeholder or fabricated asset.

To enable real inference, place the approved checkpoint at:

`app/models/agrismart-field-model.pt`

Then install the optional ML dependencies from `requirements-ml.txt`. The model loads lazily and is cached once per process. When the checkpoint or ML dependencies are unavailable, the endpoint returns HTTP 503 rather than inventing a diagnosis.

See [app/models/README.md](app/models/README.md).

## Testing

Install development dependencies and run the test suite:

```bash
pip install -r requirements-dev.txt
pytest -q
```

The tests exercise health, crop, field, market, calendar, model-card and upload-validation endpoints. Model inference itself requires the optional checkpoint and ML dependencies.

## Data and prototype disclaimer

Crop suitability, field indicators, market estimates and calendar entries are deterministic demonstration logic based on the existing AgriN Connect prototype. They are not live agronomic, market, satellite or weather feeds. Production use requires locally validated data and models.

## Scope

This repository contains only the organized FastAPI backend. It does not contain or rebuild the React frontend, and it does not modify the original [AgriN Connect repository](https://github.com/ESpoorthy/farmer-app).
