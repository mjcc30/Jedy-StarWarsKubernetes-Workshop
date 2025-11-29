from fastapi.testclient import TestClient
from app.main import app
from app.routes import users
from tests.database import get_session as get_test_session, engine
from app.models import User
from sqlmodel import Session
from app.main import app

# Ensure we are overriding the correct dependency
app.dependency_overrides[users.get_session] = get_test_session

client = TestClient(app)


def setup_module(module):
    # Ensure override is present
    app.dependency_overrides[users.get_session] = get_test_session

    # Create a clean database for each test module
    User.metadata.drop_all(engine)
    User.metadata.create_all(engine)


def teardown_module(module):
    # Drop the database tables after each test module
    User.metadata.drop_all(engine)


def test_create_user():
    response = client.post(
        "/users/signup",
        json={"username": "testuser", "password": "testpassword"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == "testuser"
    assert "id" in data
    assert "hashed_password" in data


def test_create_user_duplicate_username():
    response = client.post(
        "/users/signup",
        json={"username": "testuser", "password": "testpassword"},
    )
    assert response.status_code == 400
    assert response.json() == {"detail": "Username already registered"}


def test_login_for_access_token():
    response = client.post(
        "/users/signin",
        data={"username": "testuser", "password": "testpassword"},
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_login_for_access_token_invalid_credentials():
    response = client.post(
        "/users/signin",
        data={"username": "wronguser", "password": "wrongpassword"},
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    assert response.status_code == 401
    assert response.json() == {"detail": "Incorrect username or password"}
