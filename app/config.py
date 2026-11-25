"""Application configuration and shared constants."""
from pathlib import Path

APP_TITLE = "AgriN Connect API"
APP_DESCRIPTION = "Interoperable regenerative agriculture intelligence for smallholder farmers."
APP_VERSION = "1.0.0"

BASE_DIR = Path(__file__).resolve().parent
MODEL_PATH = BASE_DIR / "models" / "agrismart-field-model.pt"
MAX_IMAGE_BYTES = 10 * 1024 * 1024
ALLOWED_IMAGE_TYPES = {"image/jpeg", "image/png", "image/webp"}
ALLOWED_ORIGINS = ["http://localhost:3000"]

DIAGNOSIS_CONFIDENCE_THRESHOLD = 0.65
SUPPORTED_CROPS = ("pepper", "potato", "tomato")
