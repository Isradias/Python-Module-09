from enum import Enum
from pydantic import BaseModel, Field, model_validator
from datetime import datetime

class Rank(Enum):
    CADET="cadet",
    OFFICER="officer",
    LIEUTENANT="lieutenant",
    CAPTAIN="captain",
    COMMANDER="commander"


class CrewMember(BaseModel):
    member_id: str = Field(min_length=3, max_length=10)
    name: str = Field(min_length=2, max_length=50)
    rank: Rank
    age: int = Field(ge=18, le=80)
    specialization: str = Field(min_length=3, max_length=30)
    years_experience: int = Field(ge=0, le=50)
    is_active: bool = Field(default=True)


class SpaceMission(BaseModel):
    mission_id: str = Field(min_length=5, max_length=15)
    mission_name: str = Field(min_length=3, max_length=100)
    destination: str = Field(min_length=3, max_length=50)
    launch_date: datetime
    duration_days: int = Field(ge=1, le=3650)
    crew: list[CrewMember] = Field(min_length=1, max_length=12)
    mission_status: str = Field(default="planned")
    budget_millions: float = Field(ge=1, le=10000, description="dollars")

    @model_validator(mode='after')
    def id_validator(self) -> None:
        if not self.mission_id.startswith("M"):
            raise ValueError("Mission ID must start with 'M'")

    @model_validator
    def crew_validator(self) -> None:
        if  in (member.rank for member in self.crew):


if __name__ == "__main__":
    