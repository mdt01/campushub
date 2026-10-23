"""Let a model call the CampusHub API through a tool.

Start CampusHub first (uvicorn app.main:app) and load sample data
(python -m scripts.seed), then run:

    python -m labs.ch02.tool_call_demo
"""
import json

import httpx

from labs.ch02.llm_client import default_model, make_client

CAMPUSHUB = "http://127.0.0.1:8000"

TOOLS = [{
    "type": "function",
    "function": {
        "name": "get_upcoming_events",
        "description": "List upcoming CampusHub events with venue, start time and seats left.",
        "parameters": {"type": "object", "properties": {}, "required": []},
    },
}]


def get_upcoming_events() -> list[dict]:
    """The real tool: an ordinary HTTP call that runs in OUR program, not in the model."""
    return httpx.get(f"{CAMPUSHUB}/events", params={"upcoming_only": True}).json()


def main() -> None:
    client = make_client()
    model = default_model()
    messages = [{"role": "user", "content": "Which campus events are coming up, and which has the most free seats?"}]

    first = client.chat.completions.create(model=model, messages=messages, tools=TOOLS)
    reply = first.choices[0].message
    if not reply.tool_calls:
        print("Model answered without the tool:", reply.content)
        return

    messages.append(reply.model_dump(exclude_none=True))
    for call in reply.tool_calls:
        print(f"Model asked to run tool: {call.function.name}")
        result = get_upcoming_events()
        messages.append({"role": "tool", "tool_call_id": call.id, "content": json.dumps(result)})

    final = client.chat.completions.create(model=model, messages=messages, tools=TOOLS)
    print("\nAnswer:", final.choices[0].message.content)


if __name__ == "__main__":
    main()
