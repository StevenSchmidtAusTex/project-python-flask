from app.extensions import db, bcrypt

# ISSUE IV add hook and role model


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    inactive_since = db.Column(db.DateTime, nullable=True)
    role = db.Column(db.String(50), nullable=False, default="user")

    # Add hook into association table

    def __repr__(self):
        return f"<User {self.username}>"


# Add a Role model (Mine is Teddy Roosevelt)
