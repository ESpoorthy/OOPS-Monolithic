from fastapi import APIRouter
from app.schemas.crop_schema import CropRecommendPayload
from app.services.crop_service import crop_catalogue

router = APIRouter()


@router.post("/recommend_crop")
def recommend_crop(payload: CropRecommendPayload):
    return {"recommendations": crop_catalogue(payload.season, payload.water_availability, payload.soil_type), "explainability": [f"Season: {payload.season.title()}", f"Water: {payload.water_availability.title()}", f"Soil: {payload.soil_type.title()}"]}
