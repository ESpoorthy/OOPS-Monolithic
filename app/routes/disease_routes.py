from fastapi import APIRouter, File, Form, HTTPException, UploadFile

from app.config import ALLOWED_IMAGE_TYPES, MAX_IMAGE_BYTES
from app.schemas.disease_schema import SupportedCrop
from app.services.disease_service import classify_leaf

router = APIRouter()


@router.post("/upload_image")
async def upload_image(
    file: UploadFile | None = File(default=None),
    crop: SupportedCrop = Form(...),
):
    if file is None:
        raise HTTPException(status_code=400, detail="Select a plant image before analysis.")
    if file.content_type not in ALLOWED_IMAGE_TYPES:
        raise HTTPException(status_code=415, detail="Only JPG, PNG, and WEBP images are supported.")
    image_bytes = await file.read(MAX_IMAGE_BYTES + 1)
    if not image_bytes:
        raise HTTPException(status_code=400, detail="The uploaded image is empty.")
    if len(image_bytes) > MAX_IMAGE_BYTES:
        raise HTTPException(status_code=413, detail="Image must be 10 MB or smaller.")
    try:
        return classify_leaf(image_bytes, crop)
    except RuntimeError as exc:
        raise HTTPException(status_code=503, detail="Disease model is temporarily unavailable.") from exc
