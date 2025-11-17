from app.models import User, Role, db
from sqlalchemy.exc import IntegrityError
from datetime import datetime


def create_role(role_name, department_name):
    role = Role(role_name=role_name, department_name=department_name)
    db.session.add(role)

    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        raise ValueError("Role with this name and department already exists")

    return {
        "role_id": role.role_id,
        "role_name": role.role_name,
        "department_name": role.department_name,
    }


def assign_role_to_user(user_id, role_id):
    user = db.session.get(User, user_id)
    if not user:
        raise ValueError(f"User with id {user_id} not found")

    role = db.session.get(Role, role_id)
    if not role:
        raise ValueError(f"Role with id {role_id} not found")

    if role not in user.roles:
        user.roles.append(role)
        db.session.commit()

    return {
        "user_id": user.id,
        "username": user.username,
        "roles": [
            {
                "role_id": r.role_id,
                "role_name": r.role_name,
                "department_name": r.department_name,
            }
            for r in user.roles
        ],
    }


def remove_role_from_user(user_id, role_id):
    """Remove a role from a user"""
    user = db.session.get(User, user_id)
    if not user:
        raise ValueError(f"User with id {user_id} not found")

    role = db.session.get(Role, role_id)
    if not role:
        raise ValueError(f"Role with id {role_id} not found")

    if role in user.roles:
        user.roles.remove(role)
        db.session.commit()
    else:
        raise ValueError(
            f"User {user.username} does not have role '{role.role_name}' "
            f"in department '{role.department_name}'"
        )

    return {
        "user_id": user.id,
        "username": user.username,
        "roles": [
            {
                "role_id": r.role_id,
                "role_name": r.role_name,
                "department_name": r.department_name,
            }
            for r in user.roles
        ],
    }


def list_roles():
    roles = Role.query.order_by(Role.department_name, Role.role_name).all()

    return [
        {
            "role_id": role.role_id,
            "role_name": role.role_name,
            "department_name": role.department_name,
        }
        for role in roles
    ]


def get_roles_for_user(user_id):
    user = db.session.get(User, user_id)
    if not user:
        raise ValueError(f"User with id {user_id} not found")

    return [
        {
            "role_id": r.role_id,
            "role_name": r.role_name,
            "department_name": r.department_name,
        }
        for r in user.roles
    ]
