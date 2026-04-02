"""
Tests for Mergington High School API (src/app.py)
Using AAA pattern (Arrange, Act, Assert) with FastAPI TestClient
"""

import uuid
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)


def unique_email():
    return f"student-{uuid.uuid4()}@mergington.edu"


def test_get_activities_returns_200_and_data():
    # Arrange
    # Act
    response = client.get("/activities")

    # Assert
    assert response.status_code == 200
    activities_data = response.json()
    assert "Chess Club" in activities_data
    assert isinstance(activities_data["Chess Club"]["participants"], list)


def test_signup_for_activity_successful():
    # Arrange
    email = unique_email()
    activity_name = "Chess Club"

    # Act
    response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": email},
    )

    # Assert
    assert response.status_code == 200
    assert response.json()["message"] == f"Signed up {email} for {activity_name}"

    activities_data = client.get("/activities").json()
    assert email in activities_data[activity_name]["participants"]


def test_signup_duplicate_returns_400():
    # Arrange
    email = unique_email()
    activity_name = "Programming Class"
    client.post(
        f"/activities/{activity_name}/signup",
        params={"email": email},
    )

    # Act
    response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": email},
    )

    # Assert
    assert response.status_code == 400
    assert response.json()["detail"] == "Student already signed up for this activity"


def test_unregister_participant_successful():
    # Arrange
    email = unique_email()
    activity_name = "Art Club"
    client.post(
        f"/activities/{activity_name}/signup",
        params={"email": email},
    )

    # Act
    response = client.delete(
        f"/activities/{activity_name}/unregister",
        params={"email": email},
    )

    # Assert
    assert response.status_code == 200
    assert response.json()["message"] == f"Unregistered {email} from {activity_name}"

    activities_data = client.get("/activities").json()
    assert email not in activities_data[activity_name]["participants"]


def test_unregister_nonexistent_participant_returns_400():
    # Arrange
    email = unique_email()
    activity_name = "Drama Club"

    # Act
    response = client.delete(
        f"/activities/{activity_name}/unregister",
        params={"email": email},
    )

    # Assert
    assert response.status_code == 400
    assert response.json()["detail"] == "Student not signed up for this activity"
