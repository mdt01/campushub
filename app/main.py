from fastapi import FastAPI

from app.database import Base, engine
from app.routers import clubs, events, registrations

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="CampusHub API",
    description="Campus events and clubs platform — companion project for *The Modern Software Developer*.",
    version="0.1.0",
)

app.include_router(clubs.router)
app.include_router(events.router)
app.include_router(registrations.router)


@app.get("/health", tags=["meta"])
def health() -> dict[str, str]:
    return {"status": "ok"}
