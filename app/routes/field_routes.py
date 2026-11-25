from fastapi import APIRouter
from app.schemas.field_schema import FieldIntelligenceRequest
from app.services.field_service import build_field_intelligence

router = APIRouter()


@router.post("/field-intelligence")
def field_intelligence(payload: FieldIntelligenceRequest):
    return build_field_intelligence(payload.location, payload.soil_type, payload.water_availability)
