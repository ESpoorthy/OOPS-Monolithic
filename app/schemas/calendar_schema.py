from pydantic import BaseModel, Field


class CalendarRequest(BaseModel):
    crop: str = Field(min_length=1, max_length=100)
    sowing_date: str | None = None
