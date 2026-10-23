def test_create_and_list_clubs(client):
    r = client.post("/clubs", json={"name": "Music Society"})
    assert r.status_code == 201
    names = [c["name"] for c in client.get("/clubs").json()]
    assert names == ["Music Society"]


def test_duplicate_club_rejected(client, club):
    r = client.post("/clubs", json={"name": "Coding Club"})
    assert r.status_code == 409


def test_unknown_club_404(client):
    assert client.get("/clubs/999").status_code == 404
