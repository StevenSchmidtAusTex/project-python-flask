from datetime import datetime
from ..models import User
from ..extensions import db, bcrypt


def create_user(username, email, password):
    new_user = User(
        username=username,
        email=email,
        password=password,
        inactive_since=datetime.utcnow(),
    )
    db.session.add(new_user)
    db.session.commit()
    return {"message": "User registered", "username": new_user.username}


def check_password(email, password):
    user = User.query.filter_by(email=email).first()

    if user:
        pass
        # print(f"found user: {user.username}")
        # print(f"email: {email}")
        # print(f"password: {password}")
        # print(f"db password: {user.password}")
    else:
        print("user not found")

    if user.password == password:
        return True
    else:
        return False


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

    user_list = [
        {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "role": user.role,
            "is_active": user.inactive_since is None,
            "inactive_since": user.inactive_since.isoformat()
            if user.inactive_since
            else None,
        }
        for user in users
    ]

    return {"total_users": len(user_list), "status_filter": status, "users": user_list}
