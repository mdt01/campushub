from tests.conftest import make_student


def test_register_student(client, event):
    s = make_student(client, "21CE001")
    r = client.post(f"/events/{event['id']}/register", json={"student_id": s["id"]})
    assert r.status_code == 201
    assert client.get(f"/events/{event['id']}").json()["seats_left"] == 1


def test_cannot_register_twice(client, event):
    s = make_student(client, "21CE002")
    client.post(f"/events/{event['id']}/register", json={"student_id": s["id"]})
    r = client.post(f"/events/{event['id']}/register", json={"student_id": s["id"]})
    assert r.status_code == 400
    assert "already registered" in r.json()["detail"]


def test_event_capacity_enforced(client, event):
    ids = [make_student(client, f"21IT0{i}")["id"] for i in range(3)]
    codes = [client.post(f"/events/{event['id']}/register", json={"student_id": i}).status_code for i in ids]
    assert codes == [201, 201, 400]


def test_cancel_registration(client, event):
    s = make_student(client, "21CE003")
    client.post(f"/events/{event['id']}/register", json={"student_id": s["id"]})
    assert client.delete(f"/events/{event['id']}/register/{s['id']}").status_code == 204
    assert client.get(f"/events/{event['id']}/attendees").json() == []
