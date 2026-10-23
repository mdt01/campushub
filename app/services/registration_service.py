from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app import models
from app.utils import seats_left


class RegistrationError(Exception):
    """Raised when a student cannot be registered for an event."""


def register_student(db: Session, event_id: int, student_id: int) -> models.Registration:
    """Register a student for an event, enforcing capacity and duplicates."""
    event = db.get(models.Event, event_id)
    if event is None:
        raise RegistrationError("Event not found")
    student = db.get(models.Student, student_id)
    if student is None:
        raise RegistrationError("Student not found")
    if seats_left(event) <= 0:
        raise RegistrationError("Event is full")

    registration = models.Registration(event_id=event_id, student_id=student_id)
    db.add(registration)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise RegistrationError("Student already registered for this event")
    db.refresh(registration)
    return registration


def cancel_registration(db: Session, event_id: int, student_id: int) -> None:
    registration = (
        db.query(models.Registration)
        .filter_by(event_id=event_id, student_id=student_id)
        .first()
    )
    if registration is None:
        raise RegistrationError("Registration not found")
    db.delete(registration)
    db.commit()
