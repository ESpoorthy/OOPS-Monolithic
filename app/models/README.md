# Disease model asset

The original AgriN Connect backend expects the trained checkpoint at:

`app/models/agrismart-field-model.pt`

This binary checkpoint is intentionally not duplicated in the repository automatically. Add the approved model asset locally when available. The disease service lazily loads it once per process and returns an HTTP 503 response when the asset or the PyTorch/timm dependencies are unavailable. It never substitutes a fabricated diagnosis.
