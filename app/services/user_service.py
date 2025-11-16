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


## ISSUE III add get_user_report
