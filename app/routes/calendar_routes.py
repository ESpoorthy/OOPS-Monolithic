from fastapi import APIRouter
from app.schemas.calendar_schema import CalendarRequest
from app.services.calendar_service import generate_farmer_calendar

router = APIRouter()


@router.post("/farmer_calendar")
def farmer_calendar(payload: CalendarRequest):
    return generate_farmer_calendar(payload.crop)
