# Disease model asset

The original AgriN Connect repository contains the trained checkpoint at:

`farmer-backend/models/agrismart-field-model.pt`

The new modular backend expects the same checkpoint at:

`app/models/agrismart-field-model.pt`

To reuse the existing asset without changing the original repository, copy it from your local original project checkout:

```bash
mkdir -p app/models
cp /path/to/farmer-app/farmer-backend/models/agrismart-field-model.pt app/models/
```

The checkpoint is approximately 86.6 MB, so it is not duplicated automatically in this backend-only architecture repository.

Install the optional inference dependencies from the repository root:

```bash
pip install -r requirements-ml.txt
```

The disease service lazily loads the checkpoint once per process and applies crop-scoped inference. It returns an HTTP 503 response when the checkpoint or optional ML dependencies are unavailable. It never substitutes a fabricated diagnosis.
