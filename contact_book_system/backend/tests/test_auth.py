from app.models.accounts_model import Account
from app.services.auth import get_password_hash

def test_login_success(client, db_session):
    # Create a test user
    hashed_password = get_password_hash("testpass")
    user = Account(
        name="Test User",
        password=hashed_password,
        role="teacher",
        status="enrolled",
        grade=1,
        class_name="A",
        enrollment_year=2024
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)

    # Test login
    response = client.post(
        "/auth/login",
        json={"id": user.id, "name": "Test User", "password": "testpass"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert "access_token" in data["data"]
    assert data["data"]["name"] == "Test User"

def test_login_failure(client):
    response = client.post(
        "/auth/login",
        json={"id": 999, "name": "NonExistent", "password": "wrongpass"}
    )
    assert response.status_code == 200 # The API returns 200 with success=False
    data = response.json()
    assert data["success"] is False
