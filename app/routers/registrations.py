from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import models, schemas
from app.database import get_db
from app.services.registration_service import (
    RegistrationError,
    cancel_registration,
    register_student,
)

router = APIRouter(tags=["registrations"])


@router.post("/students", response_model=schemas.StudentOut, status_code=201)
def create_student(student: schemas.StudentIn, db: Session = Depends(get_db)):
    if db.query(models.Student).filter_by(roll_no=student.roll_no).first():
        raise HTTPException(status_code=409, detail="Roll number already exists")
    obj = models.Student(**student.model_dump())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


@router.post("/events/{event_id}/register", response_model=schemas.RegistrationOut, status_code=201)
def register(event_id: int, body: schemas.RegistrationIn, db: Session = Depends(get_db)):
    try:
        return register_student(db, event_id, body.student_id)
    except RegistrationError as exc:
        raise HTTPException(status_code=400, detail=str(exc))


@router.delete("/events/{event_id}/register/{student_id}", status_code=204)
def cancel(event_id: int, student_id: int, db: Session = Depends(get_db)):
    try:
        cancel_registration(db, event_id, student_id)
    except RegistrationError as exc:
        raise HTTPException(status_code=404, detail=str(exc))


@router.get("/events/{event_id}/attendees", response_model=list[schemas.StudentOut])
def attendees(event_id: int, db: Session = Depends(get_db)):
    event = db.get(models.Event, event_id)
    if event is None:
        raise HTTPException(status_code=404, detail="Event not found")
    return [r.student for r in event.registrations]
