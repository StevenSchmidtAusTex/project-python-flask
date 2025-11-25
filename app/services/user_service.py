from datetime import datetime
from ..models import User
from ..extensions import db, bcrypt


def create_user(username, email, password):
    hashed_password = bcrypt.generate_password_hash(password).decode("utf-8")
    new_user = User(
        username=username,
        email=email,
        password=hashed_password,
        inactive_since=datetime.utcnow(),
    )
    db.session.add(new_user)
    db.session.commit()
    return {"message": "User registered", "username": new_user.username}


def check_password(email, password):
    user = User.query.filter_by(email=email).first()

    if not user:
        bcrypt.check_password_hash(
            bcrypt.generate_password_hash("dummy").decode("utf-8"), password
        )
        return False

    return bcrypt.check_password_hash(user.password, password)


def toggle_user_active(user_id):
    user = db.session.get(User, user_id)
    if not user:
        raise ValueError(f"User with id {user_id} not found")

    if user.inactive_since is None:
        user.inactive_since = datetime.utcnow()
    else:
        user.inactive_since = None

    db.session.commit()

    return {
        "user_id": user.id,
        "username": user.username,
        "is_active": user.inactive_since is None,
        "inactive_since": user.inactive_since.isoformat()
        if user.inactive_since
        else None,
    }


# New function to generate user access report.
# Simplest approach, maintain a single DB query and readability
# Prefer over Dictionary Dispatch, may provide more scalability
def get_user_report(status="all"):
    query = User.query

    if status == "active":
        query = query.filter(User.inactive_since.is_(None))
    elif status == "inactive":
        query = query.filter(User.inactive_since.isnot(None))

    users = query.all()

    user_list = []
    for user in users:
        roles = [
            {
                "role_id": role.role_id,
                "role_name": role.role_name,
                "department_name": role.department_name,
            }
            for role in user.roles
        ]

        # Append this user to the report
        user_list.append(
            {
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "roles": roles,
                "is_active": user.inactive_since is None,
                "inactive_since": user.inactive_since.isoformat()
                if user.inactive_since
                else None,
            }
        )

    return {"total_users": len(user_list), "status_filter": status, "users": user_list}
