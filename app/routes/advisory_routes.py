from fastapi import APIRouter
from app.services.advisory_service import get_model_card

router = APIRouter()


@router.get("/cooperation/model-card")
def model_card():
    return get_model_card()
