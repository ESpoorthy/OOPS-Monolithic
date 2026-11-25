from typing import Literal
from pydantic import BaseModel, Field


class CropRecommendPayload(BaseModel):
    soil_type: Literal["alluvial", "loamy", "clay"]
    water_availability: Literal["low", "medium", "high"]
    season: Literal["kharif", "rabi", "zaid"]
    location: str | None = Field(default=None, max_length=120)
