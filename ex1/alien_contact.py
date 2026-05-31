from pydantic import BaseModel, Field, model_validator, ValidationError
from datetime import datetime
from enum import Enum
from json import load


class ContactType(Enum):
    RADIO = "radio"
    VISUAL = "visual"
    PHYSICAL = "physical"
    TELEPATHIC = "telepathic"


class AlienContact(BaseModel):
    contact_id: str = Field(min_length=5, max_length=15)
    timestamp: datetime = Field(description="DateTime of contact")
    location: str = Field(min_length=3, max_length=100)
    contact_type: ContactType
    signal_strength: float = Field(ge=0, le=10, description="Scale")
    duration_minutes: int = Field(gt=0, le=1440)
    witness_count: int = Field(gt=0, le=100)
    message_received: str | None = Field(max_length=500)
    is_verified: bool = Field(default=False)

    @model_validator(mode='after')
    def id_validator(self):
        if not self.contact_id.startswith("AC"):
            raise ValueError("Contact ID must start with 'AC' (Alien Contact)")
        return self

    @model_validator(mode='after')
    def type_validator(self):
        if self.contact_type is ContactType.PHYSICAL:
            if not self.is_verified:
                raise ValueError("Physical contact reports must be verified")
        if self.contact_type is ContactType.TELEPATHIC:
            if self.witness_count < 3:
                raise ValueError("Telepathic contact requires " +
                                 "at least 3 witnesses")
        return self

    @model_validator(mode='after')
    def signal_validator(self):
        if self.signal_strength > 7.0 and not self.message_received:
            raise ValueError("Strong signals (> 7.0) should " +
                             "include received messages")
        return self

    def display(self) -> None:
        print(f"ID: {self.contact_id}")
        print(f"Type: {self.contact_type}")
        print(f"Location: {self.location}")
        print(f"Signal: {self.signal_strength}/10")
        print(f"Duration: {self.timestamp} minutes")
        print(f"Witnesses: {self.witness_count}")
        if self.message_received:
            print(f"Message: '{self.message_received}'")
        print("")


def test_valid() -> None:
    with open("../generated_data/alien_contacts.json", "r") as archive:
        valid_contact = load(archive)
    for x in valid_contact:
        contact = AlienContact(**x)
        contact.display()


def test_invalid() -> None:
    with open("../generated_data/invalid_contacts.json", "r") as archive:
        invalid_contact = load(archive)
    for x in invalid_contact:
        try:
            contact = AlienContact(**x)
            contact.display()
        except ValidationError as e:
            print(f"Error on {x['contact_id']}")
            for error in e.errors():
                if error['loc']:
                    print(f"{error['loc'][0]}: {error['msg']}")
                else:
                    print(error['msg'])
            print("")


def main() -> None:
    try:
        print("========================================")
        print("Testing alien_contacts.json:")
        print("========================================\n")
        test_valid()

        print("========================================")
        print("Testing invalid_contacts.json")
        print("========================================\n")
        test_invalid()
    except Exception as e:
        print(e)


if __name__ == "__main__":
    main()
