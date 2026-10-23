"""Fill the local database with sample clubs, events and students.

Usage:  python -m scripts.seed
"""
from datetime import datetime, timedelta

from app import models
from app.database import Base, SessionLocal, engine


def seed() -> None:
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    if db.query(models.Club).count():
        print("Database already has data; skipping.")
        return
    now = datetime.now().replace(minute=0, second=0, microsecond=0)
    coding = models.Club(name="Coding Club", description="Hackathons, contests and open source.")
    music = models.Club(name="Music Society", description="Bands, choir and open-mic nights.")
    robotics = models.Club(name="Robotics Lab", description="Build and race robots.")
    db.add_all([coding, music, robotics])
    db.flush()
    db.add_all([
        models.Event(title="Intro to Open Source", venue="Seminar Hall A", starts_at=now + timedelta(days=2), capacity=60, club_id=coding.id),
        models.Event(title="24-hour Hackathon", venue="Main Auditorium", starts_at=now + timedelta(days=10), capacity=120, club_id=coding.id),
        models.Event(title="Open-Mic Night", venue="Amphitheatre", starts_at=now + timedelta(days=5), capacity=200, club_id=music.id),
        models.Event(title="Line-Follower Race", venue="Robotics Lab", starts_at=now - timedelta(days=3), capacity=30, club_id=robotics.id),
    ])
    db.add_all([
        models.Student(roll_no="21CE001", name="Ananya Shah", email="ananya@example.edu"),
        models.Student(roll_no="21CE002", name="Rahul Patel", email="rahul@example.edu"),
        models.Student(roll_no="21IT014", name="Meera Joshi", email="meera@example.edu"),
    ])
    db.commit()
    db.close()
    print("Seeded sample data.")


if __name__ == "__main__":
    seed()
