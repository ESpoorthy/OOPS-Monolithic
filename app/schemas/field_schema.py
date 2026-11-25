from typing import Literal
from pydantic import BaseModel, Field


class FieldIntelligenceRequest(BaseModel):
    location: str = Field(default="Demo farm", max_length=120)
    soil_type: Literal["alluvial", "loamy", "clay"] = "loamy"
    water_availability: Literal["low", "medium", "high"] = "medium"
