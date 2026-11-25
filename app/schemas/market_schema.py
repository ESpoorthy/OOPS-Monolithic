from pydantic import BaseModel, Field


class PricePredictPayload(BaseModel):
    crop: str = Field(min_length=1, max_length=100)
