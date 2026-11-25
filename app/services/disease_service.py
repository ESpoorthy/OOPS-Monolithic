"""Disease-image workflow and optional model integration.

The original project uses a PyTorch/timm checkpoint. This module keeps the
inference boundary explicit and fails safely when that optional asset or its
dependencies are unavailable; it does not fabricate a diagnosis.
"""
from io import BytesIO
from pathlib import Path
from typing import Any
from PIL import Image, UnidentifiedImageError
from fastapi import HTTPException
from app.config import MODEL_PATH, DIAGNOSIS_CONFIDENCE_THRESHOLD, SUPPORTED_CROPS

_model_session: tuple[Any, Any, list[str]] | None = None


def validate_image(image_bytes: bytes) -> None:
    try:
        Image.open(BytesIO(image_bytes)).verify()
    except (UnidentifiedImageError, OSError) as exc:
        raise HTTPException(status_code=400, detail="Upload a valid JPG, PNG, or WEBP plant image.") from exc


def load_disease_model():
    """Lazily load the checkpoint once per process; optional ML deps are imported here."""
    global _model_session
    if _model_session is not None:
        return _model_session
    if not Path(MODEL_PATH).exists():
        raise RuntimeError("Disease model asset is missing")
    try:
        import torch
        import timm
    except ImportError as exc:
        raise RuntimeError("Disease model dependencies are unavailable") from exc
    package = torch.load(MODEL_PATH, map_location="cpu", weights_only=True)
    model = timm.create_model(package["backbone"], pretrained=False, num_classes=len(package["labels"]), img_size=package["img_size"])
    model.load_state_dict(package["state_dict"])
    model.eval()
    transform = timm.data.create_transform(input_size=package["img_size"], interpolation="bicubic", mean=package["mean"], std=package["std"], crop_pct=0.9)
    _model_session = (model, transform, package["labels"])
    return _model_session


def classify_leaf(image_bytes: bytes, crop: str) -> dict:
    if crop not in SUPPORTED_CROPS:
        raise HTTPException(status_code=422, detail="Unsupported crop. Supported crops: pepper, potato, tomato.")
    validate_image(image_bytes)
    try:
        import torch
        import numpy as np
        image = Image.open(BytesIO(image_bytes)).convert("RGB")
        model, transform, labels = load_disease_model()
        tensor = transform(image).unsqueeze(0)
        with torch.no_grad():
            probabilities = ((model(tensor).softmax(1) + model(torch.flip(tensor, dims=[3])).softmax(1)) / 2)[0].cpu().numpy()
    except RuntimeError:
        raise
    crop_prefix = {"pepper": "Pepper", "potato": "Potato", "tomato": "Tomato"}[crop]
    crop_indices = [i for i, label in enumerate(labels) if label.startswith(crop_prefix)]
    if not crop_indices:
        raise RuntimeError("Model does not contain classes for the selected crop")
    best_index = max(crop_indices, key=lambda i: float(probabilities[i]))
    confidence = float(probabilities[best_index])
    diagnosis = labels[best_index]
    healthy = diagnosis.endswith("healthy")
    top = [{"label": labels[i], "confidence": round(float(probabilities[i]), 3)} for i in sorted(crop_indices, key=lambda i: float(probabilities[i]), reverse=True)[:3]]
    if confidence < DIAGNOSIS_CONFIDENCE_THRESHOLD:
        return {"diagnosis": "Uncertain — no reliable diagnosis", "confidence": round(confidence, 3), "next_step": "Retake a close, well-lit photo of one leaf, or consult a local agricultural extension officer.", "model_mode": f"real-model / low-confidence / {crop}", "crop": crop, "supported_crops": list(SUPPORTED_CROPS), "top_predictions": top}
    return {"diagnosis": "Healthy leaf" if healthy else diagnosis.replace("___", " ").replace("_", " ").title(), "confidence": round(confidence, 3), "next_step": "No disease signal detected; continue routine monitoring." if healthy else "Isolate affected foliage and consult a local extension officer before treatment.", "model_mode": f"real-model / AgriSmart field model / {crop}", "crop": crop, "supported_crops": list(SUPPORTED_CROPS), "top_predictions": top}
