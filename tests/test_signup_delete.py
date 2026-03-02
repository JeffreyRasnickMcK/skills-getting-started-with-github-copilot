def test_unregister_removes_existing_participant(client):
    email = "michael@mergington.edu"

    response = client.delete("/activities/Chess%20Club/signup", params={"email": email})

    assert response.status_code == 200
    assert "message" in response.json()

    activities_response = client.get("/activities")
    participants = activities_response.json()["Chess Club"]["participants"]
    assert email not in participants


def test_unregister_rejects_unknown_activity(client):
    response = client.delete("/activities/Unknown%20Club/signup", params={"email": "test@mergington.edu"})

    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_unregister_rejects_non_member(client):
    response = client.delete("/activities/Chess%20Club/signup", params={"email": "missing@mergington.edu"})

    assert response.status_code == 404
    assert response.json()["detail"] == "Student is not signed up for this activity"


def test_unregister_requires_email_query_param(client):
    response = client.delete("/activities/Chess%20Club/signup")

    assert response.status_code == 422
