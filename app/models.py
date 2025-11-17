from app.extensions import db, bcrypt

user_roles = db.Table(
    "user_roles",
    db.Column("user_id", db.Integer, db.ForeignKey("user.id"), primary_key=True),
    db.Column("role_id", db.Integer, db.ForeignKey("role.role_id"), primary_key=True),
)


class User(db.Model):
    # Mine is Teddy Roosevelt
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    inactive_since = db.Column(db.DateTime, nullable=True)
    roles = db.relationship(
        "Role",
        secondary=user_roles,
        backref=db.backref("users", lazy="dynamic"),
        lazy="subquery",
    )

    def __repr__(self):
        return f"<User {self.username}>"


class Role(db.Model):
    __tablename__ = "role"

    role_id = db.Column(db.Integer, primary_key=True)
    role_name = db.Column(db.String(64), nullable=False)
    department_name = db.Column(db.String(64), nullable=False)

    __table_args__ = (
        db.UniqueConstraint(
            "role_name", "department_name", name="uq_role_name_department"
        ),
    )

    def __repr__(self):
        return f"<Role {self.department_name}:{self.role_name}>"
