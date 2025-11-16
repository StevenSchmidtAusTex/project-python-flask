from flask import Blueprint, jsonify, request
from ..models import User
from ..extensions import db
from ..services.user_service import create_user, check_password, toggle_user_active

user_bp = Blueprint("user_bp", __name__)


@user_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    username = data.get("username")
    email = data.get("email")
    password = data.get("password")

    user = create_user(username, email, password)
    return jsonify({"message": "User registered successfully"}), 201


@user_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")

    if check_password(email, password) is True:
        user = User.query.filter_by(email=email).first()
        if user.inactive_since is not None:
            return jsonify({"message": "Account is inactive"}), 403
        return jsonify({"message": "Login successful", "email": email}), 200
    else:
        return jsonify({"message": "Invalid credentials"}), 401


@user_bp.route("/users/<int:user_id>/toggle-active", methods=["PATCH"])
def toggle_active(user_id):
    try:
        result = toggle_user_active(user_id)
        return jsonify(result), 200
    except ValueError as e:
        return jsonify({"message": str(e)}), 404


@user_bp.route("/profile", methods=["GET"])
def profile():
    # Dummy profile route for the user
    # In a real system, you would have authentication and user session handling
    return jsonify({"message": "User profile information"}), 200
