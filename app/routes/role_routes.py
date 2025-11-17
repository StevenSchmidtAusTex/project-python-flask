from flask import Blueprint, request, jsonify
from app.services.role_service import (
    create_role,
    assign_role_to_user,
    list_roles,
    get_roles_for_user,
    remove_role_from_user,
)

role_bp = Blueprint("role", __name__)


@role_bp.route("/roles", methods=["POST"])
def create_role_route():
    data = request.get_json() or {}
    role_name = data.get("role_name")
    department_name = data.get("department_name")

    if not role_name or not department_name:
        return jsonify({"error": "role_name and department_name are required"}), 400

    try:
        role = create_role(role_name=role_name, department_name=department_name)
    except ValueError as ex:
        return jsonify({"error": str(ex)}), 409  # 409 Conflict for duplicate

    return jsonify(role), 201


@role_bp.route("/roles", methods=["GET"])
def list_roles_route():
    roles = list_roles()
    return jsonify({"total_roles": len(roles), "roles": roles}), 200


@role_bp.route("/users/<int:user_id>/roles", methods=["POST"])
def assign_role_route(user_id):
    data = request.get_json() or {}
    role_id = data.get("role_id")

    if role_id is None:
        return jsonify({"error": "role_id is required"}), 400

    try:
        result = assign_role_to_user(user_id=user_id, role_id=role_id)
    except ValueError as ex:
        return jsonify({"error": str(ex)}), 404

    return jsonify(result), 200


@role_bp.route("/users/<int:user_id>/roles", methods=["GET"])
def get_user_roles_route(user_id):
    try:
        roles = get_roles_for_user(user_id)
        return jsonify({"user_id": user_id, "roles": roles}), 200
    except ValueError as ex:
        return jsonify({"error": str(ex)}), 404


# Added a remove role route for completing endpoint coverage
@role_bp.route("/users/<int:user_id>/roles/<int:role_id>", methods=["DELETE"])
def remove_role_route(user_id, role_id):
    try:
        result = remove_role_from_user(user_id=user_id, role_id=role_id)
        return jsonify(result), 200
    except ValueError as ex:
        return jsonify({"error": str(ex)}), 404
