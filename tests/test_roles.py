from app.models import User, Role


# Helper functions (consolidating tests)
def create_user(client, username="testuser", email=None, password="testpassword"):
    if email is None:
        email = f"{username}@example.com"

    user_data = {
        "username": username,
        "email": email,
        "password": password,
    }
    return client.post("/register", json=user_data)


def get_user_id(app, email):
    with app.app_context():
        user = User.query.filter_by(email=email).first()
        return user.id if user else None


def create_role(client, role_name, department_name):
    role_data = {"role_name": role_name, "department_name": department_name}
    response = client.post("/roles", json=role_data)
    return response.get_json().get("role_id") if response.status_code == 201 else None


def test_role_creation_and_constraints(client, app):
    # Test role creation
    data = {
        "role_name": "Wizard",
        "department_name": "Arcane",
    }
    response = client.post("/roles", json=data)
    assert response.status_code == 201
    json_data = response.get_json()
    assert json_data["role_name"] == "Wizard"
    assert json_data["department_name"] == "Arcane"
    assert "role_id" in json_data

    # Test missing fields
    response = client.post("/roles", json={"department_name": "Divine"})
    assert response.status_code == 400
    assert "role_name and department_name are required" in response.get_json()["error"]

    # Test duplicate role
    response = client.post("/roles", json=data)
    assert response.status_code == 409
    assert "already exists" in response.get_json()["error"]

    # Test same role name in different departments
    response = client.post(
        "/roles", json={"role_name": "Paladin", "department_name": "Divine"}
    )
    assert response.status_code == 201

    response = client.post(
        "/roles", json={"role_name": "Paladin", "department_name": "Martial"}
    )
    assert response.status_code == 201

    # Verify both Paladin roles exist with different IDs
    with app.app_context():
        divine_paladin = Role.query.filter_by(
            role_name="Paladin", department_name="Divine"
        ).first()
        martial_paladin = Role.query.filter_by(
            role_name="Paladin", department_name="Martial"
        ).first()
        assert divine_paladin is not None
        assert martial_paladin is not None
        assert divine_paladin.role_id != martial_paladin.role_id


def test_list_roles(client):
    roles_data = [
        {"role_name": "Rogue", "department_name": "Stealth"},
        {"role_name": "Bard", "department_name": "Arcane"},
        {"role_name": "Barbarian", "department_name": "Martial"},
    ]

    for role_data in roles_data:
        client.post("/roles", json=role_data)

    response = client.get("/roles")

    assert response.status_code == 200

    json_data = response.get_json()
    assert "total_roles" in json_data
    assert "roles" in json_data
    assert json_data["total_roles"] == 3
    assert len(json_data["roles"]) == 3


def test_assign_role_to_user(client, app):
    # Create user and role using helpers
    create_user(client, "testuser", "testuser@example.com")
    user_id = get_user_id(app, "testuser@example.com")
    role_id = create_role(client, "Ranger", "Martial")

    response = client.post(f"/users/{user_id}/roles", json={"role_id": role_id})
    assert response.status_code == 200

    json_data = response.get_json()
    assert json_data["user_id"] == user_id
    assert json_data["username"] == "testuser"
    assert len(json_data["roles"]) == 1
    assert json_data["roles"][0]["role_name"] == "Ranger"
    assert json_data["roles"][0]["department_name"] == "Martial"

    # Test error cases
    # Non-existent user
    response = client.post("/users/99999/roles", json={"role_id": role_id})
    assert response.status_code == 404
    assert "not found" in response.get_json()["error"].lower()

    # Non-existent role
    response = client.post(f"/users/{user_id}/roles", json={"role_id": 99999})
    assert response.status_code == 404
    assert "not found" in response.get_json()["error"].lower()

    # Missing role_id
    response = client.post(f"/users/{user_id}/roles", json={})
    assert response.status_code == 400
    assert "role_id is required" in response.get_json()["error"]


def test_assign_multiple_roles_to_user(client, app):
    create_user(client, "multiuser", "multiuser@example.com")
    user_id = get_user_id(app, "multiuser@example.com")

    role_ids = [
        create_role(client, "Fighter", "Martial"),
        create_role(client, "Cleric", "Divine"),
        create_role(client, "Warlock", "Arcane"),
    ]

    for role_id in role_ids:
        client.post(f"/users/{user_id}/roles", json={"role_id": role_id})

    response = client.get(f"/users/{user_id}/roles")
    assert response.status_code == 200
    assert len(response.get_json()["roles"]) == 3

    # Test assigning same role twice
    response = client.post(f"/users/{user_id}/roles", json={"role_id": role_ids[0]})
    assert response.status_code == 200
    assert len(response.get_json()["roles"]) == 3


def test_get_and_remove_roles_for_user(client, app):
    # Test getting roles for non-existent user
    response = client.get("/users/99999/roles")
    assert response.status_code == 404
    assert "not found" in response.get_json()["error"].lower()

    create_user(client, "roleuser", "roleuser@example.com")
    user_id = get_user_id(app, "roleuser@example.com")

    role_ids = [
        create_role(client, "Druid", "Nature"),
        create_role(client, "Monk", "Martial"),
    ]

    for role_id in role_ids:
        client.post(f"/users/{user_id}/roles", json={"role_id": role_id})

    response = client.get(f"/users/{user_id}/roles")
    assert response.status_code == 200
    json_data = response.get_json()
    assert json_data["user_id"] == user_id
    assert len(json_data["roles"]) == 2

    # Remove one role
    response = client.delete(f"/users/{user_id}/roles/{role_ids[0]}")
    assert response.status_code == 200
    assert len(response.get_json()["roles"]) == 1

    # Try to remove the same role again
    response = client.delete(f"/users/{user_id}/roles/{role_ids[0]}")
    assert response.status_code == 404
    assert "does not have role" in response.get_json()["error"]


def test_role_assignment_to_multiple_users(client, app):
    users = [
        ("user1", "user1@example.com"),
        ("user2", "user2@example.com"),
        ("user3", "user3@example.com"),
    ]

    user_ids = []
    for username, email in users:
        create_user(client, username, email)
        user_ids.append(get_user_id(app, email))

    # Create and assign one role to all users
    role_id = create_role(client, "Sorcerer", "Arcane")

    for user_id in user_ids:
        response = client.post(f"/users/{user_id}/roles", json={"role_id": role_id})
        assert response.status_code == 200

    # Verify each user has the role
    for user_id in user_ids:
        response = client.get(f"/users/{user_id}/roles")
        json_data = response.get_json()
        assert len(json_data["roles"]) == 1
        assert json_data["roles"][0]["role_name"] == "Sorcerer"
