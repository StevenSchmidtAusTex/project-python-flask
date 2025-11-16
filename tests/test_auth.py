from datetime import datetime
from app.models import User


def test_register_user(client):
    # Prepare the test data
    data = {
        "username": "testuser",
        "email": "testuser@example.com",
        "password": "testpassword",
    }

    # Send a POST request to register a new user
    response = client.post("/register", json=data)

    # Assert that the response status code is 201 (Created)
    assert response.status_code == 201

    # Assert that the response JSON contains the expected message
    json_data = response.get_json()
    assert json_data["message"] == "User registered successfully"


def test_login_user(client, app):
    # First, register a new user
    register_data = {
        "username": "testuser",
        "email": "testuser@example.com",
        "password": "testpassword",
    }
    client.post("/register", json=register_data)

    with app.app_context():
        user = User.query.filter_by(email="testuser@example.com").first()
        user.inactive_since = None
        from app.extensions import db

        db.session.commit()

    # Prepare login data
    login_data = {"email": "testuser@example.com", "password": "testpassword"}

    # Send a POST request to login
    response = client.post("/login", json=login_data)

    # Assert that the response status code is 200 (OK)
    assert response.status_code == 200

    # Assert that the response JSON contains the expected message
    json_data = response.get_json()
    assert json_data["message"] == "Login successful"
    assert json_data["email"] == "testuser@example.com"


def test_login_invalid_user(client):
    # Prepare invalid login data
    login_data = {
        "username": "notauser",
        "email": "notauser@example.com",
        "password": "validpassword",
    }
    client.post("/register", json=login_data)

    # Send a POST request to login
    # use the wrong password to test the invalid login
    response = client.post(
        "/login", json={"email": "notauser@example.com", "password": "INvalidpassword"}
    )

    # Assert that the response status code is 401 (Unauthorized)
    assert response.status_code == 401


def test_new_users_created_as_inactive(client, app):
    data = {
        "username": "inactiveuser",
        "email": "inactive@example.com",
        "password": "testpassword",
    }
    client.post("/register", json=data)

    with app.app_context():
        user = User.query.filter_by(email="inactive@example.com").first()
        assert user.inactive_since is not None


def test_inactive_users_cannot_login(client):
    register_data = {
        "username": "inactiveuser",
        "email": "inactive@example.com",
        "password": "testpassword",
    }
    client.post("/register", json=register_data)

    login_data = {"email": "inactive@example.com", "password": "testpassword"}
    response = client.post("/login", json=login_data)

    assert response.status_code == 403

    json_data = response.get_json()
    assert json_data["message"] == "Account is inactive"


def test_toggle_route_sets_user_to_active(client, app):
    register_data = {
        "username": "toggleuser",
        "email": "toggle@example.com",
        "password": "testpassword",
    }
    client.post("/register", json=register_data)

    with app.app_context():
        user = User.query.filter_by(email="toggle@example.com").first()
        user_id = user.id

    response = client.patch(f"/users/{user_id}/toggle-active")

    assert response.status_code == 200

    with app.app_context():
        user = User.query.get(user_id)
        assert user.inactive_since is None

    json_data = response.get_json()
    assert json_data["is_active"] is True
    assert json_data["inactive_since"] is None


def test_toggling_user_to_inactive_sets_timestamp(client, app):
    register_data = {
        "username": "toggleuser2",
        "email": "toggle2@example.com",
        "password": "testpassword",
    }
    client.post("/register", json=register_data)

    with app.app_context():
        user = User.query.filter_by(email="toggle2@example.com").first()
        user_id = user.id

    client.patch(f"/users/{user_id}/toggle-active")

    with app.app_context():
        user = User.query.get(user_id)
        assert user.inactive_since is None

    before_toggle = datetime.utcnow()

    response = client.patch(f"/users/{user_id}/toggle-active")

    with app.app_context():
        user = User.query.get(user_id)
        assert user.inactive_since is not None
        assert user.inactive_since >= before_toggle

    json_data = response.get_json()
    assert json_data["is_active"] is False
    assert json_data["inactive_since"] is not None
