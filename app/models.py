from app.extensions import db, bcrypt


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    inactive_since = db.Column(db.DateTime, nullable=True)

    def __repr__(self):
        return f"<User {self.username}>"
