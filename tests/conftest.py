import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.database import Base, get_db
from app.main import app


@pytest.fixture()
def client():
    engine = create_engine(
        "sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool
    )
    TestingSession = sessionmaker(bind=engine, autoflush=False, autocommit=False)
    Base.metadata.create_all(bind=engine)

    def override_get_db():
        db = TestingSession()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()


@pytest.fixture()
def club(client):
    return client.post("/clubs", json={"name": "Coding Club", "description": "Code"}).json()


@pytest.fixture()
def event(client, club):
    body = {
        "title": "Intro to Open Source",
        "venue": "Seminar Hall A",
        "starts_at": "2030-01-15T10:00:00",
        "capacity": 2,
        "club_id": club["id"],
    }
    return client.post("/events", json=body).json()


def make_student(client, roll_no, name="Test Student"):
    return client.post(
        "/students", json={"roll_no": roll_no, "name": name, "email": f"{roll_no}@example.edu"}
    ).json()
