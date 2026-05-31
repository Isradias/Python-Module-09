from enum import Enum
from pydantic import BaseModel, Field, model_validator, ValidationError
from datetime import datetime
from json import load


class Rank(Enum):
    CADET = "cadet"
    OFFICER = "officer"
    LIEUTENANT = "lieutenant"
    CAPTAIN = "captain"
    COMMANDER = "commander"


class CrewMember(BaseModel):
    member_id: str = Field(min_length=3, max_length=10)
    name: str = Field(min_length=2, max_length=50)
    rank: Rank
    age: int = Field(ge=18, le=80)
    specialization: str = Field(min_length=3, max_length=30)
    years_experience: int = Field(ge=0, le=50)
    is_active: bool = Field(default=True)

    def display(self) -> None:
        print(f"- {self.name} ({self.rank.value}) - {self.specialization}")


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
    def id_validator(self):
        if not self.mission_id.startswith("M"):
            raise ValueError("Mission ID must start with 'M'")
        return self

    @model_validator(mode='after')
    def crew_validator(self):
        has_leader = any(
            member.rank in (Rank.COMMANDER, Rank.CAPTAIN)
            for member in self.crew
        )

        if not has_leader:
            raise ValueError("Must have at least one Commander or Captain")

        if self.duration_days > 365:
            experienced_member = sum(
                member.years_experience > 5
                for member in self.crew
            )

            total_members = len(self.crew)

            if experienced_member / total_members < 0.5:
                raise ValueError("Long missions (> 365 days) need 50% "
                                 "experienced crew (5+ years)")

        has_all_active = all(member.is_active for member in self.crew)

        if not has_all_active:
            raise ValueError("All crew members must be active")

        return self

    def display(self) -> None:
        print(f"Mission: {self.mission_name}")
        print(f"ID: {self.mission_id}")
        print(f"Destination: {self.destination}")
        print(f"Duration: {self.duration_days} days")
        print(f"Budget: ${self.budget_millions}M")
        print(f"Crew size: {len(self.crew)}")
        print("Crew members:")
        for member in self.crew:
            member.display()
        print()


def main() -> None:
    try:
        with open("../generated_data/space_missions.json", "r") as archive:
            space_missions = load(archive)
    except Exception as e:
        print(e)
        exit(1)

    print("Space Mission Crew Validation")
    print("=========================================\n")
    for x in space_missions:
        try:
            mission: SpaceMission = SpaceMission(**x)
            mission.display()
        except ValidationError as e:
            print(f"Error on {x['mission_name']}")
            for error in e.errors():
                if error['loc']:
                    print(f"{error['loc'][0]}: {error['msg']}")
                else:
                    print(error['msg'])
            print("")


if __name__ == "__main__":
    main()
