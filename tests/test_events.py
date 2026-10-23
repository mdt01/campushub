def test_create_event_reports_seats(client, event):
    assert event["seats_left"] == 2


def test_event_requires_existing_club(client):
    body = {"title": "X", "venue": "Y", "starts_at": "2030-01-01T09:00:00", "club_id": 42}
    assert client.post("/events", json=body).status_code == 404


def test_list_events_sorted_by_start(client, club):
    for title, when in [("Later", "2030-03-01T10:00:00"), ("Sooner", "2030-02-01T10:00:00")]:
        client.post("/events", json={"title": title, "venue": "Hall", "starts_at": when, "club_id": club["id"]})
    titles = [e["title"] for e in client.get("/events").json()]
    assert titles == ["Sooner", "Later"]


def test_search_events_by_keyword(client, event):
    results = client.get("/events/search", params={"q": "Open"}).json()
    assert [e["title"] for e in results] == ["Intro to Open Source"]
