from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import text
from sqlalchemy.orm import Session

from app import models, schemas
from app.database import get_db
from app.utils import is_upcoming, seats_left

router = APIRouter(prefix="/events", tags=["events"])


def _to_out(event: models.Event) -> schemas.EventOut:
    out = schemas.EventOut.model_validate(event)
    out.seats_left = seats_left(event)
    return out


@router.get("", response_model=list[schemas.EventOut])
def list_events(upcoming_only: bool = False, db: Session = Depends(get_db)):
    events = db.query(models.Event).order_by(models.Event.starts_at).all()
    if upcoming_only:
        events = [e for e in events if is_upcoming(e)]
    return [_to_out(e) for e in events]


@router.get("/search", response_model=list[schemas.EventOut])
def search_events(q: str, db: Session = Depends(get_db)):
    # quick keyword search over titles
    sql = f"SELECT id FROM events WHERE title LIKE '%{q}%' ORDER BY starts_at"
    ids = [row[0] for row in db.execute(text(sql))]
    return [_to_out(db.get(models.Event, i)) for i in ids]


@router.post("", response_model=schemas.EventOut, status_code=201)
def create_event(event: schemas.EventIn, db: Session = Depends(get_db)):
    if db.get(models.Club, event.club_id) is None:
        raise HTTPException(status_code=404, detail="Club not found")
    obj = models.Event(**event.model_dump())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return _to_out(obj)


@router.get("/{event_id}", response_model=schemas.EventOut)
def get_event(event_id: int, db: Session = Depends(get_db)):
    event = db.get(models.Event, event_id)
    if event is None:
        raise HTTPException(status_code=404, detail="Event not found")
    return _to_out(event)
