"""Ask a model for JSON and validate it with Pydantic before trusting it.

Usage:  python -m labs.ch02.structured_output "Robotics club demo, Lab 3, 14 Nov 4pm, 40 seats"
"""
import json
import sys
from datetime import datetime

from pydantic import BaseModel, ValidationError

from labs.ch02.llm_client import default_model, make_client


class EventDraft(BaseModel):
    title: str
    venue: str
    starts_at: datetime
    capacity: int


SYSTEM = (
    "Extract a campus event from the user's text. Reply with JSON only, using the keys "
    "title, venue, starts_at (ISO 8601, assume year 2026) and capacity (integer)."
)


def extract(text: str) -> EventDraft:
    client = make_client()
    response = client.chat.completions.create(
        model=default_model(),
        messages=[{"role": "system", "content": SYSTEM}, {"role": "user", "content": text}],
        temperature=0,
        response_format={"type": "json_object"},
    )
    raw = response.choices[0].message.content
    return EventDraft.model_validate(json.loads(raw))


if __name__ == "__main__":
    try:
        print(extract(" ".join(sys.argv[1:]) or "Coding club meetup, Seminar Hall B, 20 Nov 2026 5pm, 80 seats"))
    except (ValidationError, json.JSONDecodeError) as exc:
        print("The model's output did not match the schema:", exc)
