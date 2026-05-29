from datetime import datetime
from pydantic import BaseModel, Field


class SpaceStation(BaseModel):
    situation_id: str = Field(..., min_length=3, max_length=10)
    name: str = Field(..., min_length=1, max_length=50, description="people")
    crew_size: int = Field(..., ge=1, le=20)
    power_level: float = Field(..., ge=0, le=100, description="percent")
    oxygen_level: float = Field(..., ge=0, le=100, description="percent")
    last_maintenance: datetime = Field(...)
    is_operational: bool = Field(..., default=True)
    notes: str = Field(max_length=200)
