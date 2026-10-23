from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import models, schemas
from app.database import get_db

router = APIRouter(prefix="/clubs", tags=["clubs"])


@router.get("", response_model=list[schemas.ClubOut])
def list_clubs(db: Session = Depends(get_db)):
    return db.query(models.Club).order_by(models.Club.name).all()


@router.post("", response_model=schemas.ClubOut, status_code=201)
def create_club(club: schemas.ClubIn, db: Session = Depends(get_db)):
    if db.query(models.Club).filter_by(name=club.name).first():
        raise HTTPException(status_code=409, detail="Club already exists")
    obj = models.Club(**club.model_dump())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


@router.get("/{club_id}", response_model=schemas.ClubOut)
def get_club(club_id: int, db: Session = Depends(get_db)):
    club = db.get(models.Club, club_id)
    if club is None:
        raise HTTPException(status_code=404, detail="Club not found")
    return club
