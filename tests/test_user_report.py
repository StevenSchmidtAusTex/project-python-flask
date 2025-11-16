from datetime import datetime
from app.models import User
from app.extensions import db


# Maintained structure from test_auth.py
# Each test handles a single filter/behavior
def test_user_report_all_users(client, app):
    with app.app_context():
        active_user = User(
            username="active_user",
            email="active@test.com",
            password="pass123",
            inactive_since=None,
            role="user",
        )
        inactive_user = User(
            username="inactive_user",
            email="inactive@test.com",
            password="pass123",
            inactive_since=datetime.utcnow(),
            role="admin",
        )
        db.session.add_all([active_user, inactive_user])
        db.session.commit()

    response = client.get("/users/report")

    assert response.status_code == 200

    data = response.get_json()
    assert data["total_users"] == 2
    assert data["status_filter"] == "all"
    assert len(data["users"]) == 2


def test_user_report_active_only(client, app):
    with app.app_context():
        active_user = User(
            username="active_user2",
            email="active2@test.com",
            password="pass123",
            inactive_since=None,
            role="user",
        )
        inactive_user = User(
            username="inactive_user2",
            email="inactive2@test.com",
            password="pass123",
            inactive_since=datetime.utcnow(),
            role="user",
        )
        db.session.add_all([active_user, inactive_user])
        db.session.commit()

    response = client.get("/users/report?status=active")

    assert response.status_code == 200

    data = response.get_json()
    assert data["status_filter"] == "active"
    for user in data["users"]:
        assert user["is_active"] is True
        assert user["inactive_since"] is None


def test_user_report_inactive_only(client, app):
    with app.app_context():
        active_user = User(
            username="active_user3",
            email="active3@test.com",
            password="pass123",
            inactive_since=None,
            role="user",
        )
        inactive_user = User(
            username="inactive_user3",
            email="inactive3@test.com",
            password="pass123",
            inactive_since=datetime.utcnow(),
            role="user",
        )
        db.session.add_all([active_user, inactive_user])
        db.session.commit()

    response = client.get("/users/report?status=inactive")

    assert response.status_code == 200

    data = response.get_json()
    assert data["status_filter"] == "inactive"
    for user in data["users"]:
        assert user["is_active"] is False
        assert user["inactive_since"] is not None


def test_user_report_contains_required_fields(client, app):
    with app.app_context():
        user = User(
            username="compliance_user",
            email="compliance@test.com",
            password="pass123",
            inactive_since=None,
            role="admin",
        )
        db.session.add(user)
        db.session.commit()

    response = client.get("/users/report")

    assert response.status_code == 200

    data = response.get_json()
    assert "total_users" in data
    assert "status_filter" in data
    assert "users" in data

    user_data = data["users"][0]
    assert "id" in user_data
    assert "username" in user_data
    assert "email" in user_data
    assert "role" in user_data
    assert "is_active" in user_data
    assert "inactive_since" in user_data

    assert user_data["email"] == "compliance@test.com"
    assert user_data["role"] == "admin"
    assert user_data["is_active"] is True


def test_user_report_invalid(client):
    response = client.get("/users/report?status=invalid_status")

    assert response.status_code == 400

    data = response.get_json()
    assert "error" in data
    assert "Invalid status parameter" in data["error"]
