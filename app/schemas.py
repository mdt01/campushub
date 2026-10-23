from datetime import datetime

from pydantic import BaseModel, ConfigDict


class ClubIn(BaseModel):
    name: str
    description: str = ""


class ClubOut(ClubIn):
    model_config = ConfigDict(from_attributes=True)
    id: int


class EventIn(BaseModel):
    title: str
    venue: str
    starts_at: datetime
    capacity: int = 50
    club_id: int


class EventOut(EventIn):
    model_config = ConfigDict(from_attributes=True)
    id: int
    seats_left: int | None = None


class StudentIn(BaseModel):
    roll_no: str
    name: str
    email: str


class StudentOut(StudentIn):
    model_config = ConfigDict(from_attributes=True)
    id: int


class RegistrationIn(BaseModel):
    student_id: int


class RegistrationOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    event_id: int
    student_id: int
    registered_at: datetime
