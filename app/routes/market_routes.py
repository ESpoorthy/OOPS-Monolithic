from fastapi import APIRouter
from app.schemas.market_schema import PricePredictPayload
from app.services.market_service import predict_crop_price

router = APIRouter()


@router.post("/predict_price")
def predict_price(payload: PricePredictPayload):
    return predict_crop_price(payload.crop)
