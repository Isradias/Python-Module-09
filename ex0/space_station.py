from datetime import datetime
from pydantic import BaseModel, Field, ValidationError
from json import load


class SpaceStation(BaseModel):
    station_id: str = Field(min_length=3, max_length=10)
    name: str = Field(min_length=1, max_length=50)
    crew_size: int = Field(ge=1, le=20, description="people")
    power_level: float = Field(ge=0, le=100, description="percent")
    oxygen_level: float = Field(ge=0, le=100, description="percent")
    last_maintenance: datetime
    is_operational: bool = True
    notes: str | None = Field(default=None, max_length=200)

    def display(self) -> None:
        print(f"ID: {self.station_id}")
        print(f"Name: {self.name}")
        print(f"Crew: {self.crew_size} people")
        print(f"Power: {self.power_level}%")
        print(f"Oxygen: {self.oxygen_level}%")
        status = "Operational" if self.is_operational else "Inoperational"
        print(f"Status: {status}")
        print("")


def hardcoded_main() -> None:
    print("========================================")
    print("Space Station Data Validation")
    print("========================================\n")

    try:
        sirius_system: SpaceStation = SpaceStation(
            station_id="ISS001",
            name="International Space Station",
            crew_size=6,
            power_level=85.5,
            oxygen_level=92.3,
            last_maintenance=datetime.now()
        )
        sirius_system.display()
    except ValidationError as e:
        for x in e.errors():
            print(f"{x["loc"][0]}: {x["msg"]}")

    print("========================================")
    print("Expected validation error:")
    print("========================================\n")
    try:
        orion: SpaceStation = SpaceStation(
            station_id="USR12002",
            name="Space Division",
            crew_size=-3,
            power_level=102.2,
            oxygen_level=80.3,
            last_maintenance=datetime.now()
        )
        orion.display()
    except ValidationError as e:
        for x in e.errors():
            print(f"{x["loc"][0]}: {x["msg"]}")
        print("")


def main() -> None:
    print("========================================")
    print("Testing space_stations.json")
    print("========================================\n")
    try:
        with open("../generated_data/space_stations.json", "r") as archive:
            valid_stations = load(archive)
        for x in valid_stations:
            try:
                station: SpaceStation = SpaceStation(**x)
                station.display()
                print("")
            except ValidationError as e:
                print(f"Error on {x['station_id']}")
                for error in e.errors():
                    print(f"{error["loc"][0]}: {error["msg"]}")
                print("")
    except Exception as e:
        print(e)

    print("========================================")
    print("Testing invalid_stations.json:")
    print("========================================\n")
    try:
        with open("../generated_data/invalid_stations.json", "r") as archive:
            invalid_stations = load(archive)
        for x in invalid_stations:
            try:
                station = SpaceStation(**x)
                station.display()
            except ValidationError as e:
                print(f"Error on {x['station_id']}")
                for error in e.errors():
                    print(f"{error['loc'][0]}: {error['msg']}")
                print("")
    except Exception as e:
        print(e)


if __name__ == "__main__":
    hardcoded_main()
    main()
