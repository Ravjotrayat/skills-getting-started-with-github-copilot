import pytest
from fastapi.testclient import TestClient
from src.app import app, activities

client = TestClient(app)

# Utility to reset activities state for test isolation
def reset_activities():
    for activity in activities.values():
        activity["participants"] = []
    # Add some default participants for specific activities if needed
    activities["Chess Club"]["participants"] = ["michael@mergington.edu", "daniel@mergington.edu"]
    activities["Programming Class"]["participants"] = ["emma@mergington.edu", "sophia@mergington.edu"]
    activities["Gym Class"]["participants"] = ["john@mergington.edu", "olivia@mergington.edu"]
    activities["Basketball Team"]["participants"] = ["james@mergington.edu"]
    activities["Tennis Club"]["participants"] = ["lucas@mergington.edu", "ava@mergington.edu"]
    activities["Art Studio"]["participants"] = ["isabella@mergington.edu"]
    activities["Music Band"]["participants"] = ["noah@mergington.edu", "mia@mergington.edu"]
    activities["Debate Team"]["participants"] = ["alexander@mergington.edu"]
    activities["Science Club"]["participants"] = ["charlotte@mergington.edu", "liam@mergington.edu"]

@pytest.fixture(autouse=True)
def run_before_and_after_tests():
    reset_activities()
    yield
    reset_activities()

def test_list_activities():
    # Arrange: nothing to set up, state is reset
    # Act
    response = client.get("/activities")
    # Assert
    assert response.status_code == 200
    data = response.json()
    assert "Chess Club" in data
    assert isinstance(data["Chess Club"], dict)
    assert "participants" in data["Chess Club"]

def test_signup_success():
    # Arrange
    email = "newstudent@mergington.edu"
    activity = "Chess Club"
    # Act
    response = client.post(f"/activities/{activity}/signup?email={email}")
    # Assert
    assert response.status_code == 200
    assert email in activities[activity]["participants"]
    assert response.json()["message"].startswith("Signed up")

def test_signup_duplicate():
    # Arrange
    email = "michael@mergington.edu"
    activity = "Chess Club"
    # Act
    response = client.post(f"/activities/{activity}/signup?email={email}")
    # Assert
    assert response.status_code == 400
    assert response.json()["detail"] == "Student already signed up"

def test_signup_activity_not_found():
    # Arrange
    email = "someone@mergington.edu"
    activity = "Nonexistent Club"
    # Act
    response = client.post(f"/activities/{activity}/signup?email={email}")
    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"

def test_remove_participant_success():
    # Arrange
    email = "michael@mergington.edu"
    activity = "Chess Club"
    # Act
    response = client.delete(f"/activities/{activity}/participant?email={email}")
    # Assert
    assert response.status_code == 200
    assert email not in activities[activity]["participants"]
    assert response.json()["message"].startswith("Removed")

def test_remove_participant_not_found():
    # Arrange
    email = "notfound@mergington.edu"
    activity = "Chess Club"
    # Act
    response = client.delete(f"/activities/{activity}/participant?email={email}")
    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Student not found in this activity"

def test_remove_participant_activity_not_found():
    # Arrange
    email = "someone@mergington.edu"
    activity = "Nonexistent Club"
    # Act
    response = client.delete(f"/activities/{activity}/participant?email={email}")
    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"
